from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class Repository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, entity_id: int) -> ModelType:
        return db.get(self.model, entity_id)

    def list(self, db: Session, **filters: Any) -> list[ModelType]:
        query = db.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        return query.order_by(self.model.id.desc()).all()

    def create(self, db: Session, **values: Any) -> ModelType:
        entity = self.model(**values)
        db.add(entity)
        db.flush()
        db.refresh(entity)
        return entity

    def update(self, db: Session, entity: ModelType, **values: Any) -> ModelType:
        for key, value in values.items():
            setattr(entity, key, value)
        db.add(entity)
        db.flush()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity: ModelType) -> None:
        db.delete(entity)
        db.flush()
