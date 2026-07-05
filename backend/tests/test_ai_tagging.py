from app.services.ai_tagging import AIProductTaggingService
from app.schemas.product import ProductCreate


def test_rule_based_tagging_assigns_category_and_aesthetic() -> None:
    payload = ProductCreate(
        title="Linen Blazer",
        price=89.99,
        image_url="https://example.com/blazer.jpg",
        affiliate_link="https://example.com/affiliate/blazer",
        color="Beige",
        style_tags=["tailored", "classic", "minimal"],
        brand="Veloura House",
        occasion_tags=["office"],
    )

    result = AIProductTaggingService().tag_product(payload)

    assert result.category.value == "tops"
    assert result.aesthetic in {"Old Money", "Clean Girl", "Minimalist", "Office Chic"}
    assert result.season
    assert result.ai_summary


def test_rule_based_tagging_prefers_shoes_over_dress_phrase() -> None:
    payload = ProductCreate(
        title="AprCoco Womens Heeled Mules Pointed Open Toe High Heels Dress Shoes",
        price=35.99,
        image_url="https://example.com/heels.jpg",
        affiliate_link="https://example.com/affiliate/heels",
        color="Black",
        style_tags=["elevated"],
        brand="Veloura House",
        occasion_tags=["date night"],
    )

    result = AIProductTaggingService().tag_product(payload)

    assert result.category.value == "shoes"


def test_rule_based_tagging_recognizes_cardigan_as_top() -> None:
    payload = ProductCreate(
        title="Women's Short Sleeve Cardigan Sweater Button Down Knit Top",
        price=37.99,
        image_url="https://example.com/cardigan.jpg",
        affiliate_link="https://example.com/affiliate/cardigan",
        color="Neutral",
        style_tags=["polished"],
        brand="Veloura House",
        occasion_tags=["office"],
    )

    result = AIProductTaggingService().tag_product(payload)

    assert result.category.value == "tops"
