from __future__ import annotations

from app.models.scheduled_post import ScheduledPost
from app.repositories.base import Repository


class ScheduleRepository(Repository[ScheduledPost]):
    def __init__(self) -> None:
        super().__init__(ScheduledPost)


schedule_repository = ScheduleRepository()

