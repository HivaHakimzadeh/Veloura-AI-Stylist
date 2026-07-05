from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.enums import ScheduleStatus
from app.repositories.board import board_repository
from app.repositories.schedule import schedule_repository
from app.schemas.schedule import ScheduleCreate, ScheduledPostRead
from app.services.captioning import CaptionService
from app.services.earnings import AffiliateEarningsService

router = APIRouter()


@router.get("/", response_model=list[ScheduledPostRead])
def list_scheduled_posts(db: Session = Depends(get_db)) -> list[object]:
    return schedule_repository.list(db)


@router.post("/", response_model=ScheduledPostRead, status_code=status.HTTP_201_CREATED)
def create_scheduled_post(payload: ScheduleCreate, db: Session = Depends(get_db)) -> object:
    board = board_repository.get(db, payload.generated_board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Generated board not found")

    if not payload.caption:
        raise HTTPException(status_code=400, detail="Caption is required")

    earnings = AffiliateEarningsService().estimate([item.product.price for item in board.outfit.items], clicks=120)
    scheduled = schedule_repository.create(
        db,
        **payload.model_dump(),
        status=ScheduleStatus.SCHEDULED,
        affiliate_earnings=earnings,
    )
    db.commit()
    db.refresh(scheduled)
    return scheduled


@router.post("/autofill-caption/{generated_board_id}", response_model=dict[str, object])
def autofill_caption(generated_board_id: int, db: Session = Depends(get_db)) -> dict[str, object]:
    board = board_repository.get(db, generated_board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Generated board not found")
    caption, hashtags = CaptionService().build_caption(
        outfit_title=board.outfit.title,
        aesthetic=board.outfit.aesthetic,
        board_name=board.title,
    )
    return {"caption": caption, "hashtags": hashtags}

