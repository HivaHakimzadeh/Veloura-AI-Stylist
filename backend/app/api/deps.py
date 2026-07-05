from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import get_db as db_dependency


def get_db() -> Generator[Session, None, None]:
    yield from db_dependency()


def get_current_user_id() -> int:
    return 1

