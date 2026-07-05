from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import CampaignType, ScheduleStatus
from app.schemas.common import TimestampedSchema


class ScheduleCreate(BaseModel):
    generated_board_id: int
    pinterest_board_id: Optional[int] = None
    campaign_type: CampaignType
    scheduled_for: datetime
    caption: str
    hashtags: list[str] = Field(default_factory=list)


class ScheduledPostRead(TimestampedSchema):
    generated_board_id: int
    pinterest_board_id: Optional[int]
    campaign_type: CampaignType
    scheduled_for: datetime
    status: ScheduleStatus
    caption: str
    hashtags: list[str]
    affiliate_earnings: float
