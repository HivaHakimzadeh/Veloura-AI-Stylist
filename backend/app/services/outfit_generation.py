from __future__ import annotations

from collections import defaultdict
from typing import Optional

from sqlalchemy.orm import Session

from app.core.enums import OutfitStatus, ProductCategory
from app.models.outfit import Outfit, OutfitItem
from app.models.product import Product
from app.repositories.outfit import outfit_repository


class OutfitGenerationService:
    REQUIRED_SEQUENCE = [
        ProductCategory.TOPS,
        ProductCategory.BOTTOMS,
        ProductCategory.DRESSES,
        ProductCategory.SHOES,
        ProductCategory.BAGS,
        ProductCategory.JEWELRY,
        ProductCategory.ACCESSORIES,
    ]

    def generate_outfits(
        self, db: Session, user_id: int, products: list[Product], aesthetics: list[str], max_outfits: int
    ) -> list[Outfit]:
        catalog = defaultdict(list)
        for product in products:
            catalog[product.category].append(product)

        outfits: list[Outfit] = []
        for aesthetic in aesthetics[:max_outfits]:
            selected = self._select_items_for_aesthetic(catalog, aesthetic)
            if not selected:
                continue

            season = self._dominant_value([product.season for _, product in selected], "All Season")
            occasion = self._occasion_for_aesthetic(aesthetic)
            keywords = self._keywords(selected, aesthetic, occasion)
            outfit = outfit_repository.create(
                db,
                user_id=user_id,
                title=f"{aesthetic} Edit",
                description=self._description(selected, aesthetic),
                keywords=keywords,
                pinterest_seo_title=f"{aesthetic} Outfit Ideas with Amazon Fashion Finds",
                pinterest_description=(
                    f"Shop this {aesthetic.lower()} outfit featuring curated Amazon fashion "
                    f"pieces for {occasion.lower()} styling."
                ),
                suggested_board_name=f"{aesthetic} Mood",
                aesthetic=aesthetic,
                season=season,
                occasion=occasion,
                status=OutfitStatus.GENERATED,
            )
            for slot, product in selected:
                db.add(OutfitItem(outfit_id=outfit.id, product_id=product.id, slot=slot))
            db.flush()
            outfits.append(outfit)

        db.commit()
        return [outfit_repository.get_with_items(db, outfit.id) for outfit in outfits if outfit.id]

    def _select_items_for_aesthetic(
        self, catalog: dict[ProductCategory, list[Product]], aesthetic: str
    ) -> list[tuple[str, Product]]:
        selected: list[tuple[str, Product]] = []
        used_ids: set[int] = set()

        dress_option = self._best_match(catalog[ProductCategory.DRESSES], aesthetic, used_ids)
        if dress_option:
            selected.append(("dress", dress_option))
            used_ids.add(dress_option.id)
        else:
            top = self._best_match(catalog[ProductCategory.TOPS], aesthetic, used_ids)
            bottom = self._best_match(catalog[ProductCategory.BOTTOMS], aesthetic, used_ids)
            if not top or not bottom:
                return []
            selected.extend([("top", top), ("bottom", bottom)])
            used_ids.update({top.id, bottom.id})

        for slot, category in (
            ("shoes", ProductCategory.SHOES),
            ("bag", ProductCategory.BAGS),
            ("jewelry", ProductCategory.JEWELRY),
            ("accessory", ProductCategory.ACCESSORIES),
        ):
            option = self._best_match(catalog[category], aesthetic, used_ids)
            if option:
                selected.append((slot, option))
                used_ids.add(option.id)

        return selected

    def _best_match(
        self, products: list[Product], aesthetic: str, used_ids: set[int]
    ) -> Optional[Product]:
        ranked = sorted(
            [product for product in products if product.id not in used_ids],
            key=lambda item: (
                item.aesthetic.lower() != aesthetic.lower(),
                item.season == "All Season",
                item.price,
            ),
        )
        return ranked[0] if ranked else None

    def _description(self, selected: list[tuple[str, Product]], aesthetic: str) -> str:
        item_names = ", ".join(product.title for _, product in selected[:4])
        return (
            f"A polished {aesthetic.lower()} outfit built around {item_names}. "
            f"The mix balances affiliate-friendly staples with Pinterest-ready styling."
        )

    def _keywords(self, selected: list[tuple[str, Product]], aesthetic: str, occasion: str) -> list[str]:
        base = [aesthetic.lower(), occasion.lower(), "amazon fashion", "outfit ideas", "veloura"]
        base.extend(product.brand.lower() for _, product in selected[:2])
        return list(dict.fromkeys(base))

    def _occasion_for_aesthetic(self, aesthetic: str) -> str:
        mapping = {
            "Old Money": "Brunch",
            "Clean Girl": "Everyday",
            "Date Night": "Date Night",
            "Office Chic": "Office",
            "Summer Vacation": "Vacation",
            "Fall Capsule Wardrobe": "Transitional Season",
        }
        return mapping.get(aesthetic, "Everyday")

    def _dominant_value(self, values: list[str], default: str) -> str:
        frequency: dict[str, int] = {}
        for value in values:
            frequency[value] = frequency.get(value, 0) + 1
        return max(frequency, key=frequency.get) if frequency else default
