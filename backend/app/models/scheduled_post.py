from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import CampaignType, ScheduleStatus
from app.models.base import Base, TimestampMixin


class ScheduledPost(TimestampMixin, Base):
    __tablename__ = "scheduled_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    generated_board_id: Mapped[int] = mapped_column(ForeignKey("generated_boards.id"), nullable=False)
    pinterest_board_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("pinterest_boards.id"), nullable=True
    )
    campaign_type: Mapped[CampaignType] = mapped_column(SqlEnum(CampaignType), nullable=False)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[ScheduleStatus] = mapped_column(
        SqlEnum(ScheduleStatus), default=ScheduleStatus.DRAFT, nullable=False
    )
    caption: Mapped[str] = mapped_column(Text, nullable=False)
    hashtags: Mapped[list[str]] = mapped_column(JSON, default=list)
    affiliate_earnings: Mapped[float] = mapped_column(Float, default=0.0)

    generated_board = relationship("GeneratedBoard", back_populates="scheduled_posts")
    pinterest_board = relationship("PinterestBoard", back_populates="scheduled_posts")
