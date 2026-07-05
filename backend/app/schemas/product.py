from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.core.enums import ProductCategory
from app.schemas.common import TimestampedSchema


class ProductBase(BaseModel):
    title: str
    category: Optional[ProductCategory] = None
    price: float
    image_url: HttpUrl
    affiliate_link: HttpUrl
    color: str
    style_tags: list[str] = Field(default_factory=list)
    brand: str
    occasion_tags: list[str] = Field(default_factory=list)


class ProductCreate(ProductBase):
    run_ai_tagging: bool = True


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[ProductCategory] = None
    price: Optional[float] = None
    image_url: Optional[HttpUrl] = None
    affiliate_link: Optional[HttpUrl] = None
    color: Optional[str] = None
    style_tags: Optional[list[str]] = None
    brand: Optional[str] = None
    occasion_tags: Optional[list[str]] = None
    color_palette: Optional[list[str]] = None
    aesthetic: Optional[str] = None
    season: Optional[str] = None
    ai_summary: Optional[str] = None


class ProductTaggingResult(BaseModel):
    category: ProductCategory
    color_palette: list[str]
    aesthetic: str
    season: str
    occasion: str
    ai_summary: str


class ProductImportRequest(BaseModel):
    url: HttpUrl
    affiliate_link: Optional[HttpUrl] = None


class ProductImportPreview(BaseModel):
    title: str
    brand: str
    price: float
    image_url: str
    affiliate_link: str
    color: str
    style_tags: list[str] = Field(default_factory=list)
    occasion_tags: list[str] = Field(default_factory=list)
    category: Optional[ProductCategory] = None


class ProductRead(TimestampedSchema):
    user_id: int
    title: str
    category: ProductCategory
    price: float
    image_url: str
    affiliate_link: str
    color: str
    style_tags: list[str]
    brand: str
    occasion_tags: list[str]
    color_palette: list[str]
    aesthetic: str
    season: str
    ai_summary: str
