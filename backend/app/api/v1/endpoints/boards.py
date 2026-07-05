from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.board import board_repository
from app.repositories.outfit import outfit_repository
from app.schemas.board import BoardGenerationRequest, GeneratedBoardRead
from app.services.board_generation import BoardGenerationService

router = APIRouter()


@router.get("/", response_model=list[GeneratedBoardRead])
def list_boards(db: Session = Depends(get_db)) -> list[object]:
    return board_repository.list(db)


@router.post("/generate", response_model=GeneratedBoardRead, status_code=status.HTTP_201_CREATED)
def generate_board(payload: BoardGenerationRequest, db: Session = Depends(get_db)) -> object:
    outfit = outfit_repository.get_with_items(db, payload.outfit_id)
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    return BoardGenerationService().generate_board(db, outfit)
