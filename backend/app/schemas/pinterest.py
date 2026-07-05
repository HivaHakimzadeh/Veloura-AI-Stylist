from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.common import TimestampedSchema


class PinterestBoardCreate(BaseModel):
    name: str
    description: str = ""


class PinterestBoardRead(TimestampedSchema):
    user_id: int
    name: str
    remote_id: str
    description: str


class PinterestPinRead(TimestampedSchema):
    generated_board_id: int
    pinterest_board_id: int
    remote_id: str
    title: str
    description: str
    published_at: Optional[datetime]
    impressions: int
    clicks: int
    saves: int
    outbound_clicks: int
