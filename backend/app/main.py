from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.db.session import SessionLocal, engine
from app.utils.seed import ensure_demo_user, init_database

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_v1_str)
app.mount("/static", StaticFiles(directory="uploads"), name="static")


@app.on_event("startup")
def startup() -> None:
    init_database(engine)
    with SessionLocal() as db:
        ensure_demo_user(db)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
