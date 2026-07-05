from fastapi import APIRouter

from app.api.v1.endpoints.analytics import router as analytics_router
from app.api.v1.endpoints.boards import router as boards_router
from app.api.v1.endpoints.outfits import router as outfits_router
from app.api.v1.endpoints.pinterest import router as pinterest_router
from app.api.v1.endpoints.products import router as products_router
from app.api.v1.endpoints.schedule import router as schedule_router

api_router = APIRouter()
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(outfits_router, prefix="/outfits", tags=["outfits"])
api_router.include_router(boards_router, prefix="/boards", tags=["boards"])
api_router.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(pinterest_router, prefix="/pinterest", tags=["pinterest"])

