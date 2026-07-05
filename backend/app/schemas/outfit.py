from __future__ import annotations

from pydantic import BaseModel, Field

from app.core.enums import OutfitStatus
from app.schemas.common import TimestampedSchema
from app.schemas.product import ProductRead


class OutfitGenerationRequest(BaseModel):
    aesthetics: list[str] = Field(
        default_factory=lambda: [
            "Old Money",
            "Clean Girl",
            "Date Night",
            "Office Chic",
            "Summer Vacation",
            "Fall Capsule Wardrobe",
        ]
    )
    max_outfits: int = 6


class OutfitItemRead(BaseModel):
    id: int
    slot: str
    product: ProductRead

    model_config = {"from_attributes": True}


class OutfitRead(TimestampedSchema):
    user_id: int
    title: str
    description: str
    keywords: list[str]
    pinterest_seo_title: str
    pinterest_description: str
    suggested_board_name: str
    aesthetic: str
    season: str
    occasion: str
    status: OutfitStatus
    items: list[OutfitItemRead]

    model_config = {"from_attributes": True}

