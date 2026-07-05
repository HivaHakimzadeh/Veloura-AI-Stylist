from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.core.enums import ProductCategory
from app.schemas.common import TimestampedSchema


class ProductBase(BaseModel):
    title: str
    category: Optional[ProductCategory] = None
    price: float
    image_url: str
    affiliate_link: str
    color: str
    style_tags: list[str] = Field(default_factory=list)
    brand: str
    occasion_tags: list[str] = Field(default_factory=list)

    @field_validator("image_url", "affiliate_link")
    @classmethod
    def validate_urlish_value(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("URL is required.")
        normalized = cls._normalize_urlish_value(value)
        if normalized.startswith(("http://", "https://", "data:")):
            return normalized
        raise ValueError("URL must start with http://, https://, or data:.")

    @staticmethod
    def _normalize_urlish_value(value: str) -> str:
        normalized = value.strip()
        if normalized.startswith("data:"):
            return normalized
        parsed = urlparse(normalized)
        if not parsed.scheme and parsed.netloc == "" and "." in parsed.path:
            return f"https://{normalized}"
        return normalized


class ProductCreate(ProductBase):
    run_ai_tagging: bool = True


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[ProductCategory] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    affiliate_link: Optional[str] = None
    color: Optional[str] = None
    style_tags: Optional[list[str]] = None
    brand: Optional[str] = None
    occasion_tags: Optional[list[str]] = None
    color_palette: Optional[list[str]] = None
    aesthetic: Optional[str] = None
    season: Optional[str] = None
    ai_summary: Optional[str] = None

    @field_validator("image_url", "affiliate_link")
    @classmethod
    def validate_optional_urlish_value(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = ProductBase._normalize_urlish_value(value)
        if normalized.startswith(("http://", "https://", "data:")):
            return normalized
        raise ValueError("URL must start with http://, https://, or data:.")


class ProductTaggingResult(BaseModel):
    category: ProductCategory
    color_palette: list[str]
    aesthetic: str
    season: str
    occasion: str
    ai_summary: str


class ProductImportRequest(BaseModel):
    url: str
    affiliate_link: Optional[str] = None

    @field_validator("url", "affiliate_link")
    @classmethod
    def validate_import_url(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = ProductBase._normalize_urlish_value(value)
        if normalized.startswith(("http://", "https://")):
            return normalized
        raise ValueError("URL must start with http:// or https://.")


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
