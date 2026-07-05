from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id, get_db
from app.repositories.product import product_repository
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.ai_tagging import AIProductTaggingService
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)) -> list[object]:
    return product_repository.list(db, user_id=user_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> object:
    data = payload.model_dump()
    data.pop("run_ai_tagging", None)
    if payload.run_ai_tagging:
        tags = AIProductTaggingService(settings.openai_api_key).tag_product(payload)
        data["category"] = tags.category
        data["color_palette"] = tags.color_palette
        data["aesthetic"] = tags.aesthetic
        data["season"] = tags.season
        data["ai_summary"] = tags.ai_summary
        data["occasion_tags"] = list(dict.fromkeys(data["occasion_tags"] + [tags.occasion]))
    else:
        data.setdefault("color_palette", [payload.color])
        data.setdefault("aesthetic", "Minimalist")
        data.setdefault("season", "All Season")
        data.setdefault("ai_summary", f"{payload.title} added manually.")
        data.setdefault("category", payload.category)

    if data.get("category") is None:
        raise HTTPException(status_code=400, detail="Category is required if AI tagging is disabled.")

    product = product_repository.create(db, user_id=user_id, **data)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> object:
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)) -> object:
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = product_repository.update(db, product, **payload.model_dump(exclude_none=True))
    db.commit()
    db.refresh(updated)
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_repository.delete(db, product)
    db.commit()
