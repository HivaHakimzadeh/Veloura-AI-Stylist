from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.models.outfit import Outfit, OutfitItem
from app.repositories.base import Repository


class OutfitRepository(Repository[Outfit]):
    def __init__(self) -> None:
        super().__init__(Outfit)

    def list_with_items(self, db: Session, user_id: int) -> list[Outfit]:
        return (
            db.query(Outfit)
            .options(joinedload(Outfit.items).joinedload(OutfitItem.product))
            .filter(Outfit.user_id == user_id)
            .order_by(Outfit.id.desc())
            .all()
        )

    def get_with_items(self, db: Session, outfit_id: int) -> Optional[Outfit]:
        return (
            db.query(Outfit)
            .options(joinedload(Outfit.items).joinedload(OutfitItem.product))
            .filter(Outfit.id == outfit_id)
            .first()
        )


outfit_repository = OutfitRepository()
