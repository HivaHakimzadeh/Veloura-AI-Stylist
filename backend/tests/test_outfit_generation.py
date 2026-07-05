from app.core.enums import ProductCategory
from app.models.product import Product
from app.services.outfit_generation import OutfitGenerationService


class DummyDB:
    def add(self, *_args, **_kwargs) -> None:
        pass

    def flush(self) -> None:
        pass

    def commit(self) -> None:
        pass


def build_product(product_id: int, category: ProductCategory, title: str, aesthetic: str) -> Product:
    return Product(
        id=product_id,
        user_id=1,
        title=title,
        category=category,
        price=79.0,
        image_url="https://example.com/item.jpg",
        affiliate_link="https://example.com/affiliate/item",
        color="black",
        style_tags=["polished"],
        brand="Veloura",
        occasion_tags=["office"],
        color_palette=["black", "ivory"],
        aesthetic=aesthetic,
        season="All Season",
        ai_summary="summary",
    )


def test_select_items_for_outfit() -> None:
    service = OutfitGenerationService()
    catalog = {
        ProductCategory.TOPS: [build_product(1, ProductCategory.TOPS, "Silk Shirt", "Office Chic")],
        ProductCategory.BOTTOMS: [build_product(2, ProductCategory.BOTTOMS, "Wide Leg Pants", "Office Chic")],
        ProductCategory.DRESSES: [],
        ProductCategory.SHOES: [build_product(3, ProductCategory.SHOES, "Leather Loafer", "Office Chic")],
        ProductCategory.BAGS: [build_product(4, ProductCategory.BAGS, "Structured Tote", "Office Chic")],
        ProductCategory.JEWELRY: [],
        ProductCategory.ACCESSORIES: [],
    }

    selected = service._select_items_for_aesthetic(catalog, "Office Chic")

    assert len(selected) >= 4
    assert {slot for slot, _ in selected}.issuperset({"top", "bottom", "shoes", "bag"})

