from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from core.bases import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor


class Category(BaseEntity):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    title = Column(String, unique = True, nullable = False)

    doctors: Mapped[list['Doctor']] = relationship(back_populates = 'category')