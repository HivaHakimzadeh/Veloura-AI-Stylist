from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlparse

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
        html = self._fetch_page(str(url))
        extracted = self._extract(str(url), html)
        return ProductImportPreview(
            title=extracted.title,
            brand=extracted.brand,
            price=extracted.price,
            image_url=extracted.image_url,
            affiliate_link=affiliate_link or str(url),
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

        title = (
            self._graph_value(graph, "name")
            or self._meta_content(soup, property_name="og:title")
            or self._meta_content(soup, name="twitter:title")
            or (soup.title.string.strip() if soup.title and soup.title.string else "")
        )
        brand = self._extract_brand(graph, soup, url)
        image_url = (
            self._extract_image(graph)
            or self._meta_content(soup, property_name="og:image")
            or self._meta_content(soup, name="twitter:image")
            or ""
        )
        price = self._extract_price(graph, soup)
        color = self._extract_color(graph, soup, title)
        style_tags = self._extract_style_tags(title, brand, color)
        occasion_tags = self._extract_occasion_tags(title)
        category = self._infer_category(title)

        if not title or not image_url or price <= 0:
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

    def _clean_title(self, title: str) -> str:
        return re.sub(r"\s+", " ", title.replace("|", " ").replace(" - Amazon.com", "")).strip()

