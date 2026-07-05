from __future__ import annotations

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import OutfitStatus
from app.models.base import Base, TimestampMixin


class Outfit(TimestampMixin, Base):
    __tablename__ = "outfits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    pinterest_seo_title: Mapped[str] = mapped_column(String(255), nullable=False)
    pinterest_description: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_board_name: Mapped[str] = mapped_column(String(255), nullable=False)
    aesthetic: Mapped[str] = mapped_column(String(128), nullable=False)
    season: Mapped[str] = mapped_column(String(64), nullable=False)
    occasion: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[OutfitStatus] = mapped_column(SqlEnum(OutfitStatus), default=OutfitStatus.DRAFT)

    user = relationship("User", back_populates="outfits")
    items = relationship("OutfitItem", back_populates="outfit", cascade="all, delete-orphan")
    boards = relationship("GeneratedBoard", back_populates="outfit", cascade="all, delete-orphan")


class OutfitItem(Base):
    __tablename__ = "outfit_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    slot: Mapped[str] = mapped_column(String(64), nullable=False)

    outfit = relationship("Outfit", back_populates="items")
    product = relationship("Product", back_populates="outfit_items")

