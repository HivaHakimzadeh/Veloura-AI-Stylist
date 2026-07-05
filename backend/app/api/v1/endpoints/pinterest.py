from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id, get_db
from app.repositories.board import board_repository
from app.repositories.pinterest import pinterest_board_repository, pinterest_pin_repository
from app.schemas.pinterest import (
    PinterestBoardCreate,
    PinterestBoardRead,
    PinterestPinRead,
)
from app.services.pinterest import PinterestService

router = APIRouter()


@router.get("/boards", response_model=list[PinterestBoardRead])
def list_pinterest_boards(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
) -> list[object]:
    return pinterest_board_repository.list(db, user_id=user_id)


@router.post("/boards", response_model=PinterestBoardRead, status_code=status.HTTP_201_CREATED)
def create_pinterest_board(
    payload: PinterestBoardCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> object:
    remote = PinterestService().create_board(payload)
    board = pinterest_board_repository.create(db, user_id=user_id, **remote)
    db.commit()
    db.refresh(board)
    return board


@router.post("/pins/{generated_board_id}", response_model=PinterestPinRead, status_code=status.HTTP_201_CREATED)
def publish_pin(
    generated_board_id: int,
    pinterest_board_id: int,
    db: Session = Depends(get_db),
) -> object:
    board = board_repository.get(db, generated_board_id)
    pinterest_board = pinterest_board_repository.get(db, pinterest_board_id)
    if not board or not pinterest_board:
        raise HTTPException(status_code=404, detail="Board or Pinterest board not found")

    remote = PinterestService().upload_pin(
        board_name=pinterest_board.name,
        title=board.title,
        description=board.outfit.pinterest_description,
        image_url=board.image_url,
    )
    analytics = PinterestService().analytics_snapshot()
    pin = pinterest_pin_repository.create(
        db,
        generated_board_id=generated_board_id,
        pinterest_board_id=pinterest_board_id,
        remote_id=remote["remote_id"],
        title=board.title,
        description=board.outfit.pinterest_description,
        published_at=datetime.fromisoformat(remote["published_at"]),
        **analytics,
    )
    db.commit()
    db.refresh(pin)
    return pin

