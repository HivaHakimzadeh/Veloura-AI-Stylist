from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class PinterestBoard(TimestampMixin, Base):
    __tablename__ = "pinterest_boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    remote_id: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)

    user = relationship("User", back_populates="pinterest_boards")
    pins = relationship("PinterestPin", back_populates="pinterest_board")
    scheduled_posts = relationship("ScheduledPost", back_populates="pinterest_board")


class PinterestPin(TimestampMixin, Base):
    __tablename__ = "pinterest_pins"

    id: Mapped[int] = mapped_column(primary_key=True)
    generated_board_id: Mapped[int] = mapped_column(ForeignKey("generated_boards.id"), nullable=False)
    pinterest_board_id: Mapped[int] = mapped_column(ForeignKey("pinterest_boards.id"), nullable=False)
    remote_id: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    saves: Mapped[int] = mapped_column(Integer, default=0)
    outbound_clicks: Mapped[int] = mapped_column(Integer, default=0)

    generated_board = relationship("GeneratedBoard", back_populates="pins")
    pinterest_board = relationship("PinterestBoard", back_populates="pins")
