from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id, get_db
from app.repositories.outfit import outfit_repository
from app.repositories.product import product_repository
from app.schemas.outfit import OutfitGenerationRequest, OutfitRead
from app.services.outfit_generation import OutfitGenerationService
from app.services.recommendations import RecommendationService

router = APIRouter()


@router.get("/", response_model=list[OutfitRead])
def list_outfits(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)) -> list[object]:
    return outfit_repository.list_with_items(db, user_id=user_id)


@router.post("/generate", response_model=list[OutfitRead])
def generate_outfits(
    payload: OutfitGenerationRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> list[object]:
    products = product_repository.list(db, user_id=user_id)
    if len(products) < 2:
        raise HTTPException(status_code=400, detail="Add more products before generating outfits.")
    return OutfitGenerationService().generate_outfits(db, user_id, products, payload.aesthetics, payload.max_outfits)


@router.get("/recommendations", response_model=list[str])
def aesthetic_recommendations(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
) -> list[str]:
    products = product_repository.list(db, user_id=user_id)
    return RecommendationService().recommend_aesthetics(products)

