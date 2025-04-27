from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any
from ..database import Base


class BaseRepository:
    model: Base

    def __init__(self, db: Session):
        self._db: Session = db

    @property
    def db(self):
        return self._db

    def get(self, id: int | str) -> Base:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multiple(self) -> list[Base]:
        return self.db.query(self.model).all()

    def create(self, model_data: dict[str, Any]) -> Base:
        new_instance = self.model(**model_data)
        self.db.add(new_instance)
        self.db.commit()
        self.db.refresh(new_instance)

        return new_instance

    def update(self, db_model: Base, model_data: dict[str, Any]) -> Base:
        update_data = dict()

        if isinstance(model_data, dict):
            update_data = model_data
        elif isinstance(model_data, BaseModel):
            update_data = model_data.model_dump(exclude_unset=True)

        for column in db_model.__table__.columns:
            if column.key in update_data:
                setattr(db_model, column.key, update_data[column.key])

        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
        return db_model

    def delete(self, id) -> Base:
        obj = self.db.query(self.model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj

    def delete_instance(self, instance: Base) -> Base:
        self.db.delete(instance)
        self.db.commit()
        return instance
