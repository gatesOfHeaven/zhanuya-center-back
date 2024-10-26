from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar


class BaseEntity(DeclarativeBase):
    ...


Entity = TypeVar('Entity', bound = BaseEntity)