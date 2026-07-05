from __future__ import annotations

from app.models.product import Product


class RecommendationService:
    def recommend_aesthetics(self, products: list[Product]) -> list[str]:
        if not products:
            return []
        scores: dict[str, int] = {}
        for product in products:
            scores[product.aesthetic] = scores.get(product.aesthetic, 0) + 2
            for tag in product.style_tags:
                if "tailored" in tag.lower():
                    scores["Old Money"] = scores.get("Old Money", 0) + 1
                if "minimal" in tag.lower():
                    scores["Clean Girl"] = scores.get("Clean Girl", 0) + 1
        return [name for name, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:5]]

