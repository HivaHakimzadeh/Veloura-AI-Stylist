from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.analytics import AnalyticsSummary
from app.services.analytics import AnalyticsService
from app.services.trending import TrendingFashionService
from app.repositories.product import product_repository

router = APIRouter()


@router.get("/", response_model=AnalyticsSummary)
def get_analytics(db: Session = Depends(get_db)) -> AnalyticsSummary:
    return AnalyticsService().summary(db)


@router.get("/trending", response_model=dict[str, list[str]])
def get_trending(db: Session = Depends(get_db)) -> dict[str, list[str]]:
    return TrendingFashionService().detect(product_repository.list(db))

