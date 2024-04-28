from typing import Type
from abc import ABC

from sqlalchemy.orm import Session, Query

from .models import User, UserMessage
from .database import Base


class BaseCrud(ABC):
    """
    This abstract class implements base CRUD (only those used in the project) and utility methods.
    You should inherit this class and override its __init__ method to create a new CRUD class.
    """

    def __init__(self, model: Type[Base], db: Session) -> None:

        self.model = model
        self.db = db

    def _get_query_filtered(self, **kwargs) -> Query:
        return self.db.query(self.model).filter_by(**kwargs)

    def add_to_db_and_refresh(self, object_to_add: Type[Base]) -> None:

        self.db.add(object_to_add)
        self.db.commit()
        self.db.refresh(object_to_add)

    def create(self, **kwargs) -> Type[Base]:

        db_object = self.model(**kwargs)

        self.add_to_db_and_refresh(db_object)

        return db_object

    def get(self, **kwargs) -> Type[Base]:
        return self._get_query_filtered(**kwargs).first()

    def get_or_create(self, **kwargs) -> Type[Base]:
        return self._get_query_filtered(**kwargs).first() or self.create(**kwargs)

    def get_many(self, **kwargs) -> list[Type[Base]]:
        return self._get_query_filtered(**kwargs).all()


class UserCrud(BaseCrud):
    def __init__(self, db: Session) -> None:
        super().__init__(User, db)


class UserMessageCrud(BaseCrud):
    def __init__(self, db: Session) -> None:
        super().__init__(UserMessage, db)
