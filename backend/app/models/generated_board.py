from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import BoardStatus
from app.models.base import Base, TimestampMixin


class GeneratedBoard(TimestampMixin, Base):
    __tablename__ = "generated_boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[BoardStatus] = mapped_column(SqlEnum(BoardStatus), default=BoardStatus.QUEUED)
    width: Mapped[int] = mapped_column(Integer, default=1000)
    height: Mapped[int] = mapped_column(Integer, default=1500)

    outfit = relationship("Outfit", back_populates="boards")
    pins = relationship("PinterestPin", back_populates="generated_board")
    scheduled_posts = relationship("ScheduledPost", back_populates="generated_board")

