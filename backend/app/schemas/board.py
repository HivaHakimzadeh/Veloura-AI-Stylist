from __future__ import annotations

from pydantic import BaseModel

from app.core.enums import BoardStatus
from app.schemas.common import TimestampedSchema


class BoardGenerationRequest(BaseModel):
    outfit_id: int


class GeneratedBoardRead(TimestampedSchema):
    outfit_id: int
    title: str
    image_url: str
    storage_key: str
    status: BoardStatus
    width: int
    height: int

