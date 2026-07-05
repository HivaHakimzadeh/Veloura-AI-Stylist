from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.base import Base
from app.models.user import User


def init_database(engine) -> None:
    Base.metadata.create_all(bind=engine)


def ensure_demo_user(db: Session) -> None:
    if db.query(User).filter(User.id == 1).first():
        return
    db.add(
        User(
            id=1,
            email="demo@veloura.ai",
            full_name="Veloura Demo",
            hashed_password="not-for-auth",
            is_active=True,
        )
    )
    db.commit()

