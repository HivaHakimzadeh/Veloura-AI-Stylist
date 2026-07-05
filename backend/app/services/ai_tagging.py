from __future__ import annotations

import json
from collections import Counter
from typing import Optional

from openai import OpenAI

from app.core.enums import ProductCategory
from app.schemas.product import ProductCreate, ProductTaggingResult


class AIProductTaggingService:
    CATEGORY_KEYWORDS: dict[ProductCategory, tuple[str, ...]] = {
        ProductCategory.TOPS: (
            "shirt",
            "top",
            "blouse",
            "tee",
            "sweater",
            "cardigan",
            "tank",
            "blazer",
            "jacket",
        ),
        ProductCategory.BOTTOMS: ("jean", "pant", "trouser", "short", "skirt", "legging"),
        ProductCategory.DRESSES: ("dress", "gown", "slip dress"),
        ProductCategory.SHOES: ("shoe", "heel", "boot", "loafer", "sneaker", "sandal"),
        ProductCategory.BAGS: ("bag", "tote", "clutch", "crossbody", "purse"),
        ProductCategory.JEWELRY: ("necklace", "ring", "bracelet", "earring", "jewelry"),
        ProductCategory.ACCESSORIES: ("belt", "scarf", "hat", "sunglasses", "watch"),
    }
    AESTHETICS = {
        "Old Money": {"neutral", "tailored", "linen", "cashmere", "classic"},
        "Clean Girl": {"minimal", "sleek", "neutral", "polished", "simple"},
        "Streetwear": {"oversized", "edgy", "cargo", "sneaker", "graphic"},
        "Minimalist": {"simple", "timeless", "capsule", "monochrome", "structured"},
        "Date Night": {"silky", "elevated", "heels", "glam", "statement"},
        "Office Chic": {"blazer", "tailored", "structured", "workwear", "polished"},
        "Summer Vacation": {"resort", "beach", "breezy", "woven", "lightweight"},
        "Fall Capsule Wardrobe": {"layered", "knit", "boot", "camel", "transitional"},
    }

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or ""
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def tag_product(self, product: ProductCreate) -> ProductTaggingResult:
        if self.client:
            try:
                return self._tag_with_openai(product)
            except Exception:
                pass
        return self._tag_with_rules(product)

    def _tag_with_openai(self, product: ProductCreate) -> ProductTaggingResult:
        prompt = {
            "title": product.title,
            "color": product.color,
            "brand": product.brand,
            "style_tags": product.style_tags,
            "occasion_tags": product.occasion_tags,
        }
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Classify fashion products and return JSON with category, color_palette, "
                        "aesthetic, season, occasion, ai_summary."
                    ),
                },
                {"role": "user", "content": json.dumps(prompt)},
            ],
        )
        payload = json.loads(response.choices[0].message.content or "{}")
        return ProductTaggingResult(
            category=ProductCategory(payload.get("category", self._infer_category(product))),
            color_palette=payload.get("color_palette", self._palette_from_color(product.color)),
            aesthetic=payload.get("aesthetic", self._infer_aesthetic(product.style_tags, product.title)),
            season=payload.get("season", self._infer_season(product)),
            occasion=payload.get("occasion", self._infer_occasion(product)),
            ai_summary=payload.get("ai_summary", self._summary(product)),
        )

    def _tag_with_rules(self, product: ProductCreate) -> ProductTaggingResult:
        return ProductTaggingResult(
            category=product.category or self._infer_category(product),
            color_palette=self._palette_from_color(product.color),
            aesthetic=self._infer_aesthetic(product.style_tags, product.title),
            season=self._infer_season(product),
            occasion=self._infer_occasion(product),
            ai_summary=self._summary(product),
        )

    def _infer_category(self, product: ProductCreate) -> ProductCategory:
        haystack = f"{product.title} {' '.join(product.style_tags)}".lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in haystack for keyword in keywords):
                return category
        return ProductCategory.ACCESSORIES

    def _palette_from_color(self, color: str) -> list[str]:
        base = color.lower().strip()
        palette_map = {
            "black": ["black", "charcoal", "silver"],
            "white": ["white", "ivory", "beige"],
            "beige": ["beige", "camel", "cream"],
            "brown": ["brown", "camel", "gold"],
            "blue": ["navy", "powder blue", "white"],
            "red": ["crimson", "blush", "gold"],
            "green": ["sage", "olive", "cream"],
            "pink": ["rose", "blush", "white"],
        }
        for key, palette in palette_map.items():
            if key in base:
                return palette
        return [base or "neutral", "ivory", "gold"]

    def _infer_aesthetic(self, style_tags: list[str], title: str) -> str:
        tokens = {tag.lower() for tag in style_tags}
        tokens.update(title.lower().split())
        scores = {
            aesthetic: sum(1 for token in tokens if token in markers)
            for aesthetic, markers in self.AESTHETICS.items()
        }
        best_match = Counter(scores).most_common(1)[0]
        return best_match[0] if best_match[1] > 0 else "Minimalist"

    def _infer_season(self, product: ProductCreate) -> str:
        text = f"{product.title} {' '.join(product.style_tags)}".lower()
        if any(token in text for token in ("linen", "breezy", "sandals", "swim", "resort")):
            return "Summer"
        if any(token in text for token in ("knit", "coat", "boot", "wool")):
            return "Fall"
        if any(token in text for token in ("floral", "pastel", "lightweight")):
            return "Spring"
        return "All Season"

    def _infer_occasion(self, product: ProductCreate) -> str:
        text = " ".join(product.occasion_tags + product.style_tags + [product.title]).lower()
        if "office" in text or "work" in text:
            return "Office"
        if "date" in text or "party" in text or "evening" in text:
            return "Date Night"
        if "vacation" in text or "beach" in text or "resort" in text:
            return "Vacation"
        return "Everyday"

    def _summary(self, product: ProductCreate) -> str:
        tags = ", ".join(product.style_tags[:3]) if product.style_tags else "versatile styling"
        return (
            f"{product.title} from {product.brand} is a {product.color.lower()} fashion piece "
            f"suited for {tags} looks."
        )
