from __future__ import annotations

from collections import Counter

from app.models.product import Product


class TrendingFashionService:
    def detect(self, products: list[Product]) -> dict[str, list[str]]:
        aesthetic_counts = Counter(product.aesthetic for product in products)
        keyword_counts = Counter(tag for product in products for tag in product.style_tags)
        occasion_counts = Counter(tag for product in products for tag in product.occasion_tags)
        return {
            "aesthetics": [name for name, _ in aesthetic_counts.most_common(5)],
            "keywords": [name for name, _ in keyword_counts.most_common(10)],
            "occasions": [name for name, _ in occasion_counts.most_common(5)],
        }

