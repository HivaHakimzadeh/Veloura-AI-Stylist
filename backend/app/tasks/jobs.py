from __future__ import annotations

from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.jobs.generate_board_task")
def generate_board_task(outfit_id: int) -> dict[str, int]:
    return {"outfit_id": outfit_id}


@celery_app.task(name="app.tasks.jobs.publish_pin_task")
def publish_pin_task(scheduled_post_id: int) -> dict[str, int]:
    return {"scheduled_post_id": scheduled_post_id}

