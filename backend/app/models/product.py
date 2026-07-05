from __future__ import annotations

from sqlalchemy import Float, ForeignKey, JSON, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ProductCategory
from app.models.base import Base, TimestampMixin


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[ProductCategory] = mapped_column(SqlEnum(ProductCategory), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    affiliate_link: Mapped[str] = mapped_column(String(1024), nullable=False)
    color: Mapped[str] = mapped_column(String(128), nullable=False)
    style_tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    occasion_tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    color_palette: Mapped[list[str]] = mapped_column(JSON, default=list)
    aesthetic: Mapped[str] = mapped_column(String(128), nullable=False)
    season: Mapped[str] = mapped_column(String(64), nullable=False)
    ai_summary: Mapped[str] = mapped_column(Text, default="", nullable=False)

    user = relationship("User", back_populates="products")
    outfit_items = relationship("OutfitItem", back_populates="product")

