from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.user import User


class Role(BaseEntity):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key = True)
    name = Column(String(15), unique = True, nullable = False)

    users: Mapped[list['User']] = relationship(back_populates = 'role')