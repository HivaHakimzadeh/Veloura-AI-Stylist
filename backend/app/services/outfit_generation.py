from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.core.enums import OutfitStatus, ProductCategory
from app.models.outfit import Outfit, OutfitItem
from app.models.product import Product
from app.repositories.outfit import outfit_repository


class OutfitGenerationService:
    AESTHETIC_PROFILES: dict[str, dict[str, set[str]]] = {
        "Old Money": {
            "style_terms": {"tailored", "classic", "linen", "cashmere", "structured", "polished", "refined"},
            "colors": {"beige", "camel", "cream", "ivory", "white", "brown", "gold", "neutral"},
            "occasions": {"office", "brunch", "resort"},
            "seasons": {"All Season", "Fall", "Summer"},
        },
        "Clean Girl": {
            "style_terms": {"minimal", "sleek", "polished", "simple", "clean", "refined"},
            "colors": {"white", "cream", "ivory", "beige", "neutral", "black", "gold"},
            "occasions": {"everyday", "office"},
            "seasons": {"All Season", "Spring", "Summer"},
        },
        "Date Night": {
            "style_terms": {"elevated", "silky", "glam", "statement", "sleek", "fitted"},
            "colors": {"black", "red", "gold", "silver", "burgundy"},
            "occasions": {"date night", "party", "evening"},
            "seasons": {"All Season", "Fall", "Summer"},
        },
        "Office Chic": {
            "style_terms": {"tailored", "polished", "structured", "workwear", "blazer", "classic"},
            "colors": {"black", "white", "ivory", "camel", "brown", "neutral", "navy"},
            "occasions": {"office", "work"},
            "seasons": {"All Season", "Fall", "Spring"},
        },
        "Summer Vacation": {
            "style_terms": {"resort", "beach", "breezy", "woven", "lightweight", "relaxed"},
            "colors": {"white", "ivory", "tan", "beige", "neutral", "gold", "blue"},
            "occasions": {"vacation", "beach", "resort"},
            "seasons": {"Summer", "Spring"},
        },
        "Fall Capsule Wardrobe": {
            "style_terms": {"layered", "knit", "boot", "camel", "transitional", "structured"},
            "colors": {"camel", "brown", "black", "cream", "ivory", "olive", "neutral"},
            "occasions": {"office", "everyday"},
            "seasons": {"Fall", "All Season"},
        },
    }
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
        usage_counts: dict[int, int] = defaultdict(int)
        core_signatures: set[tuple[int, ...]] = set()
        for aesthetic in aesthetics[:max_outfits]:
            selected = self._select_items_for_aesthetic(catalog, aesthetic, usage_counts, core_signatures)
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
                usage_counts[product.id] += 1
            db.flush()
            outfits.append(outfit)
            core_signatures.add(self._core_signature(selected))

        db.commit()
        return [outfit_repository.get_with_items(db, outfit.id) for outfit in outfits if outfit.id]

    def _select_items_for_aesthetic(
        self,
        catalog: dict[ProductCategory, list[Product]],
        aesthetic: str,
        usage_counts: Optional[dict[int, int]] = None,
        core_signatures: Optional[set[tuple[int, ...]]] = None,
    ) -> list[tuple[str, Product]]:
        usage_counts = usage_counts or {}
        core_signatures = core_signatures or set()
        used_ids: set[int] = set()
        core_items = self._select_core_items_for_aesthetic(catalog, aesthetic, usage_counts, core_signatures)
        if not core_items:
            return []

        selected = list(core_items)
        used_ids.update(product.id for _, product in core_items)
        anchor_colors = self._palette_union(product for _, product in core_items)

        for slot, category in (
            ("shoes", ProductCategory.SHOES),
            ("bag", ProductCategory.BAGS),
            ("jewelry", ProductCategory.JEWELRY),
            ("accessory", ProductCategory.ACCESSORIES),
        ):
            option = self._best_match(
                catalog[category],
                aesthetic,
                used_ids,
                usage_counts,
                slot=slot,
                anchor_colors=anchor_colors,
            )
            if option:
                selected.append((slot, option))
                used_ids.add(option.id)

        return selected

    def _select_core_items_for_aesthetic(
        self,
        catalog: dict[ProductCategory, list[Product]],
        aesthetic: str,
        usage_counts: dict[int, int],
        core_signatures: set[tuple[int, ...]],
    ) -> list[tuple[str, Product]]:
        candidates: list[tuple[float, list[tuple[str, Product]]]] = []

        for dress in catalog[ProductCategory.DRESSES]:
            score = self._product_score(dress, aesthetic, usage_counts, slot="dress") + 6
            candidates.append((score, [("dress", dress)]))

        tops = catalog[ProductCategory.TOPS]
        bottoms = catalog[ProductCategory.BOTTOMS]
        for top in tops:
            for bottom in bottoms:
                if top.id == bottom.id:
                    continue
                score = (
                    self._product_score(top, aesthetic, usage_counts, slot="top")
                    + self._product_score(bottom, aesthetic, usage_counts, slot="bottom")
                    + self._color_harmony(top, bottom)
                )
                candidates.append((score, [("top", top), ("bottom", bottom)]))

        if not candidates:
            return []

        ranked = sorted(
            candidates,
            key=lambda item: (
                -item[0],
                sum(usage_counts.get(product.id, 0) for _, product in item[1]),
                tuple(product.id for _, product in item[1]),
            ),
        )
        for _score, items in ranked:
            if self._core_signature(items) not in core_signatures:
                return items
        return ranked[0][1]

    def _best_match(
        self,
        products: list[Product],
        aesthetic: str,
        used_ids: set[int],
        usage_counts: dict[int, int],
        slot: str,
        anchor_colors: Optional[set[str]] = None,
    ) -> Optional[Product]:
        ranked = sorted(
            [product for product in products if product.id not in used_ids],
            key=lambda item: (
                -self._product_score(item, aesthetic, usage_counts, anchor_colors=anchor_colors, slot=slot),
                usage_counts.get(item.id, 0),
                item.price,
                item.id,
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

    def _product_score(
        self,
        product: Product,
        aesthetic: str,
        usage_counts: dict[int, int],
        anchor_colors: Optional[set[str]] = None,
        slot: str = "",
    ) -> float:
        profile = self.AESTHETIC_PROFILES.get(aesthetic, {})
        style_terms = profile.get("style_terms", set())
        preferred_colors = profile.get("colors", set())
        preferred_occasions = profile.get("occasions", set())
        preferred_seasons = profile.get("seasons", set())

        tokens = self._product_tokens(product)
        palette = self._palette_union([product])

        score = 0.0
        if product.aesthetic.lower() == aesthetic.lower():
            score += 28
        score += len(tokens & style_terms) * 6
        score += len(palette & preferred_colors) * 4
        score += len({tag.lower() for tag in product.occasion_tags} & preferred_occasions) * 5
        if product.season in preferred_seasons:
            score += 4
        elif product.season == "All Season":
            score += 2
        if anchor_colors:
            score += len(anchor_colors & palette) * 5
        if slot in {"dress", "top", "bottom"}:
            score += 2
        score -= usage_counts.get(product.id, 0) * 14
        return score

    def _color_harmony(self, left: Product, right: Product) -> float:
        left_palette = self._palette_union([left])
        right_palette = self._palette_union([right])
        overlap = left_palette & right_palette
        if overlap:
            return 10 + len(overlap)
        neutral_family = {"black", "white", "ivory", "cream", "beige", "camel", "brown", "neutral", "gold"}
        if left_palette & neutral_family and right_palette & neutral_family:
            return 6
        return 0

    def _palette_union(self, products: Iterable[Product]) -> set[str]:
        palette: set[str] = set()
        for product in products:
            palette.add(product.color.lower())
            palette.update(color.lower() for color in product.color_palette)
        return palette

    def _product_tokens(self, product: Product) -> set[str]:
        return {
            token
            for token in (
                product.title.lower().split()
                + [product.aesthetic.lower()]
                + [product.season.lower()]
                + [product.color.lower()]
                + [tag.lower() for tag in product.style_tags]
                + [tag.lower() for tag in product.occasion_tags]
            )
        }

    def _core_signature(self, selected: list[tuple[str, Product]]) -> tuple[int, ...]:
        core_slots = {"dress", "top", "bottom"}
        return tuple(product.id for slot, product in selected if slot in core_slots)
