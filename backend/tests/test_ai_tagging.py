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
