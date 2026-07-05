from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import parse_qs, quote, unquote, urlparse

import httpx
from bs4 import BeautifulSoup

from app.core.enums import ProductCategory
from app.schemas.product import ProductImportPreview


@dataclass
class ProductExtraction:
    title: str
    brand: str
    price: float
    image_url: str
    color: str
    style_tags: list[str]
    occasion_tags: list[str]
    category: Optional[ProductCategory]


class ProductImportService:
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    )

    def import_preview(self, url: str, affiliate_link: Optional[str] = None) -> ProductImportPreview:
        normalized_url = self._normalize_product_url(url)
        try:
            html = self._fetch_page(normalized_url)
            extracted = self._extract(normalized_url, html)
        except Exception:
            extracted = self._fallback_extract(normalized_url)
        return ProductImportPreview(
            title=extracted.title,
            brand=extracted.brand,
            price=extracted.price,
            image_url=extracted.image_url,
            affiliate_link=affiliate_link or normalized_url,
            color=extracted.color,
            style_tags=extracted.style_tags,
            occasion_tags=extracted.occasion_tags,
            category=extracted.category,
        )

    def _fetch_page(self, url: str) -> str:
        response = httpx.get(
            url,
            headers={
                "User-Agent": self.USER_AGENT,
                "Accept-Language": "en-US,en;q=0.9",
            },
            follow_redirects=True,
            timeout=15.0,
        )
        response.raise_for_status()
        return response.text

    def _extract(self, url: str, html: str) -> ProductExtraction:
        soup = BeautifulSoup(html, "html.parser")
        graph = self._json_ld_product(soup)

        title = self._clean_title(
            self._graph_value(graph, "name")
            or self._title_from_soup(soup)
            or self._meta_content(soup, property_name="og:title")
            or self._meta_content(soup, name="twitter:title")
            or (soup.title.string.strip() if soup.title and soup.title.string else "")
        )
        if self._is_unusable_title(title):
            title = self._amazon_slug_title(url) or title
        brand = self._extract_brand(graph, soup, url)
        image_url = (
            self._extract_image(graph)
            or self._extract_image_from_soup(soup)
            or self._meta_content(soup, property_name="og:image")
            or self._meta_content(soup, name="twitter:image")
            or ""
        )
        price = self._extract_price(graph, soup)
        color = self._extract_color(graph, soup, title)
        style_tags = self._extract_style_tags(title, brand, color)
        occasion_tags = self._extract_occasion_tags(title)
        category = self._infer_category(title)

        if not title or self._is_unusable_title(title) or not image_url or price <= 0:
            raise ValueError("Could not reliably extract product details from that URL.")

        return ProductExtraction(
            title=self._clean_title(title),
            brand=brand,
            price=price,
            image_url=image_url,
            color=color,
            style_tags=style_tags,
            occasion_tags=occasion_tags,
            category=category,
        )

    def _fallback_extract(self, url: str) -> ProductExtraction:
        parsed = urlparse(url)
        slug = self._amazon_slug_title(url) or unquote(parsed.path.split("/")[-1]).strip()
        slug = re.sub(r"\.[a-z0-9]+$", "", slug, flags=re.IGNORECASE)
        slug = re.sub(r"[-_]+", " ", slug)
        title = self._clean_title(slug).title() if slug else "Imported Fashion Product"
        brand_root = parsed.netloc.replace("www.", "").split(".")[0].replace("-", " ")
        brand = brand_root.title() if brand_root else "Imported Brand"
        category = self._infer_category(title)
        color = self._extract_color({}, BeautifulSoup("", "html.parser"), title)
        return ProductExtraction(
            title=title,
            brand=brand,
            price=0.0,
            image_url=self._placeholder_image(title),
            color=color,
            style_tags=self._extract_style_tags(title, brand, color),
            occasion_tags=self._extract_occasion_tags(title),
            category=category,
        )

    def _normalize_product_url(self, url: str) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        wrapped = query.get("url") or query.get("u")
        if wrapped:
            candidate = unquote(wrapped[0])
            if candidate.startswith("/"):
                candidate = f"{parsed.scheme or 'https'}://{parsed.netloc}{candidate}"
            if candidate.startswith(("http://", "https://")) and candidate != url:
                return self._normalize_product_url(candidate)

        amazon_match = re.search(r"/dp/([A-Z0-9]{10})", parsed.path, re.IGNORECASE)
        if amazon_match and "amazon." in parsed.netloc:
            prefix = self._amazon_slug_title(url)
            if prefix:
                safe_prefix = re.sub(r"\s+", "-", prefix.strip().lower())
                return f"https://www.amazon.com/{safe_prefix}/dp/{amazon_match.group(1).upper()}"
            return f"https://www.amazon.com/dp/{amazon_match.group(1).upper()}"
        return url

    def _amazon_slug_title(self, url: str) -> str:
        parsed = urlparse(url)
        if "amazon." not in parsed.netloc:
            return ""
        path = unquote(parsed.path)
        slug_match = re.search(r"/([^/]+)/dp/[A-Z0-9]{10}", path, re.IGNORECASE)
        if slug_match:
            return slug_match.group(1).replace("-", " ").replace("_", " ").strip()
        return ""

    def _is_unusable_title(self, title: str) -> bool:
        normalized = self._clean_title(title).lower()
        if not normalized:
            return True
        blocked_patterns = (
            "amazon.com",
            "ref=",
            "sspa",
            "sr ",
            "click here",
        )
        return any(pattern in normalized for pattern in blocked_patterns)

    def _json_ld_product(self, soup: BeautifulSoup) -> dict[str, Any]:
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            text = script.string or script.get_text(strip=True)
            if not text:
                continue
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                continue

            product = self._find_product_node(payload)
            if product:
                return product
        return {}

    def _find_product_node(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, list):
            for item in payload:
                product = self._find_product_node(item)
                if product:
                    return product
            return {}
        if not isinstance(payload, dict):
            return {}

        node_type = payload.get("@type")
        if node_type == "Product" or (isinstance(node_type, list) and "Product" in node_type):
            return payload

        for key in ("@graph", "itemListElement", "mainEntity"):
            nested = payload.get(key)
            product = self._find_product_node(nested)
            if product:
                return product
        return {}

    def _graph_value(self, graph: dict[str, Any], key: str) -> str:
        value = graph.get(key)
        if isinstance(value, str):
            return value.strip()
        return ""

    def _extract_brand(self, graph: dict[str, Any], soup: BeautifulSoup, url: str) -> str:
        brand = graph.get("brand")
        if isinstance(brand, dict):
            name = brand.get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()
        if isinstance(brand, str) and brand.strip():
            return brand.strip()
        meta_brand = self._meta_content(soup, property_name="product:brand") or self._meta_content(
            soup, name="brand"
        )
        if meta_brand:
            return meta_brand
        hostname = urlparse(url).netloc.replace("www.", "")
        root = hostname.split(".")[0].replace("-", " ").replace("_", " ")
        return root.title() if root else "Unknown Brand"

    def _extract_image(self, graph: dict[str, Any]) -> str:
        image = graph.get("image")
        if isinstance(image, str):
            return image
        if isinstance(image, list):
            for candidate in image:
                if isinstance(candidate, str):
                    return candidate
        if isinstance(image, dict):
            url = image.get("url")
            if isinstance(url, str):
                return url

        # Amazon product pages often keep the usable product image on the landing image tag.
        # Prefer the highest-confidence direct source before falling back to regex parsing.
        return ""

    def _extract_image_from_soup(self, soup: BeautifulSoup) -> str:
        landing_image = soup.select_one("#landingImage")
        if landing_image:
            for attr in ("data-old-hires", "src"):
                value = landing_image.get(attr)
                if isinstance(value, str) and value.strip():
                    return value.strip()
            dynamic = landing_image.get("data-a-dynamic-image")
            if isinstance(dynamic, str):
                try:
                    payload = json.loads(dynamic)
                    if isinstance(payload, dict) and payload:
                        return next(iter(payload.keys()))
                except json.JSONDecodeError:
                    pass

        image_input = soup.select_one("#imgBlkFront, #main-image")
        if image_input and image_input.get("src"):
            return str(image_input.get("src")).strip()

        html = str(soup)
        large_match = re.search(r'"large":"(https://m\.media-amazon\.com/images[^"]+)"', html)
        if large_match:
            return large_match.group(1).replace("\\u0026", "&").replace("\\/", "/")

        dynamic_match = re.search(
            r'data-a-dynamic-image="({&quot;https://m\.media-amazon\.com/images[^"]+})"', html
        )
        if dynamic_match:
            try:
                payload = json.loads(dynamic_match.group(1).replace("&quot;", '"'))
                if isinstance(payload, dict) and payload:
                    return next(iter(payload.keys()))
            except json.JSONDecodeError:
                pass
        return ""

    def _extract_price(self, graph: dict[str, Any], soup: BeautifulSoup) -> float:
        offers = graph.get("offers")
        if isinstance(offers, list):
            for offer in offers:
                price = self._price_from_offer(offer)
                if price:
                    return price
        if isinstance(offers, dict):
            price = self._price_from_offer(offers)
            if price:
                return price

        for property_name, name in (
            ("product:price:amount", None),
            (None, "price"),
            (None, "twitter:data1"),
        ):
            value = self._meta_content(soup, property_name=property_name, name=name)
            price = self._parse_price(value)
            if price:
                return price

        for selector in (
            ".priceToPay .a-offscreen",
            ".apexPriceToPay .a-offscreen",
            "#corePriceDisplay_desktop_feature_div .a-price .a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            "#price_inside_buybox",
        ):
            node = soup.select_one(selector)
            if node:
                price = self._parse_price(node.get_text(" ", strip=True))
                if price:
                    return price

        html = str(soup)
        price_to_pay_match = re.search(
            r'priceToPay[^<]{0,500}?\$([0-9]+(?:\.[0-9]{2})?)', html, flags=re.IGNORECASE
        )
        if price_to_pay_match:
            return float(price_to_pay_match.group(1))

        html_text = soup.get_text(" ", strip=True)
        match = re.search(r"\$\s?([0-9]+(?:\.[0-9]{2})?)", html_text)
        return float(match.group(1)) if match else 0.0

    def _price_from_offer(self, offer: Any) -> float:
        if not isinstance(offer, dict):
            return 0.0
        for key in ("price", "lowPrice"):
            value = offer.get(key)
            price = self._parse_price(value)
            if price:
                return price
        return 0.0

    def _parse_price(self, value: Any) -> float:
        if isinstance(value, (float, int)):
            return float(value)
        if isinstance(value, str):
            cleaned = value.replace(",", "").strip()
            cleaned = cleaned.replace("$", "")
            match = re.search(r"([0-9]+(?:\.[0-9]{1,2})?)", cleaned)
            if match:
                return float(match.group(1))
        return 0.0

    def _extract_color(self, graph: dict[str, Any], soup: BeautifulSoup, title: str) -> str:
        value = graph.get("color")
        if isinstance(value, str) and value.strip():
            return value.strip().title()

        text = " ".join(
            [
                title,
                self._meta_content(soup, name="keywords"),
                self._meta_content(soup, property_name="og:description"),
                soup.get_text(" ", strip=True)[:1500],
            ]
        ).lower()
        for color in (
            "black",
            "white",
            "beige",
            "brown",
            "blue",
            "red",
            "green",
            "pink",
            "cream",
            "camel",
            "gold",
            "silver",
            "ivory",
            "navy",
            "gray",
        ):
            if re.search(rf"\b{re.escape(color)}\b", text):
                return color.title()
        return "Neutral"

    def _extract_style_tags(self, title: str, brand: str, color: str) -> list[str]:
        text = f"{title} {brand} {color}".lower()
        tags: list[str] = []
        keyword_map = {
            "tailored": ["blazer", "trouser", "structured", "tailored"],
            "minimal": ["minimal", "clean", "sleek"],
            "classic": ["classic", "loafer", "linen"],
            "elevated": ["heel", "silk", "statement"],
            "resort": ["vacation", "resort", "beach", "breezy"],
            "polished": ["office", "structured", "refined"],
        }
        for tag, markers in keyword_map.items():
            if any(marker in text for marker in markers):
                tags.append(tag)
        return tags or ["versatile"]

    def _extract_occasion_tags(self, title: str) -> list[str]:
        text = title.lower()
        tags: list[str] = []
        if any(token in text for token in ("office", "blazer", "trouser")):
            tags.append("office")
        if any(token in text for token in ("vacation", "beach", "resort", "sandal")):
            tags.append("vacation")
        if any(token in text for token in ("heel", "dress", "silk", "evening")):
            tags.append("date night")
        return tags or ["everyday"]

    def _infer_category(self, title: str) -> Optional[ProductCategory]:
        text = title.lower()
        if re.search(r"\b(dress|gown)\b", text):
            return ProductCategory.DRESSES
        if re.search(r"\b(heel|loafer|boot|shoe|sneaker|sandal)\b", text):
            return ProductCategory.SHOES
        if re.search(r"\b(bag|tote|clutch|purse|crossbody)\b", text):
            return ProductCategory.BAGS
        if re.search(r"\b(earring|ring|bracelet|necklace|hoop)\b", text):
            return ProductCategory.JEWELRY
        if re.search(r"\b(scarf|belt|hat|sunglasses|watch)\b", text):
            return ProductCategory.ACCESSORIES
        if re.search(r"\b(pant|pants|trouser|jean|skirt|short)\b", text):
            return ProductCategory.BOTTOMS
        if re.search(r"\b(blazer|shirt|top|blouse|tee|tank|sweater|jacket|cardigan)\b", text):
            return ProductCategory.TOPS
        return None

    def _meta_content(
        self, soup: BeautifulSoup, property_name: Optional[str] = None, name: Optional[str] = None
    ) -> str:
        attrs = {}
        if property_name:
            attrs["property"] = property_name
        if name:
            attrs["name"] = name
        if not attrs:
            return ""
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return str(tag["content"]).strip()
        return ""

    def _title_from_soup(self, soup: BeautifulSoup) -> str:
        product_title = soup.select_one("#productTitle")
        if product_title:
            value = product_title.get_text(" ", strip=True)
            if value:
                return value

        html = str(soup)
        json_title = re.search(r'productTitle\\?&quot;:\\?&quot;([^"&]+)', html)
        if json_title:
            return (
                json_title.group(1)
                .replace("&#39;", "'")
                .replace("\\u0026", "&")
                .replace("\\/", "/")
            )
        return ""

    def _clean_title(self, title: str) -> str:
        cleaned = title.replace("|", " ").replace(" - Amazon.com", "")
        cleaned = re.sub(r":\s*Amazon\.com\s*$", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r":\s*Handbags\s*:\s*Amazon\.com\s*$", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    def _placeholder_image(self, title: str) -> str:
        safe_title = title[:30]
        svg = (
            "<svg xmlns='http://www.w3.org/2000/svg' width='1000' height='1500' viewBox='0 0 1000 1500'>"
            "<rect width='1000' height='1500' rx='48' fill='#f6eee4'/>"
            "<rect x='52' y='52' width='896' height='1396' rx='40' fill='#fffaf5' stroke='#9c5f50' stroke-width='4'/>"
            "<text x='86' y='120' font-family='Georgia, serif' font-size='36' fill='#9c5f50'>Veloura</text>"
            f"<text x='86' y='190' font-family='Georgia, serif' font-size='42' fill='#2e2018'>{safe_title}</text>"
            "<text x='86' y='238' font-family='Arial, sans-serif' font-size='24' fill='#7a6758'>Imported preview</text>"
            "<rect x='86' y='320' width='828' height='960' rx='32' fill='#eadbcf'/>"
            "</svg>"
        )
        return f"data:image/svg+xml;charset=UTF-8,{quote(svg)}"
