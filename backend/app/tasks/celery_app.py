from __future__ import annotations

from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery("veloura", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_routes = {
    "app.tasks.jobs.generate_board_task": {"queue": "boards"},
    "app.tasks.jobs.publish_pin_task": {"queue": "publishing"},
}

