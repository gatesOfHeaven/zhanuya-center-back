from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.db import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor


class Office(BaseEntity):
    __tablename__ = 'offices'

    id = Column(Integer, primary_key = True)
    city = Column(String, nullable=False)
    address = Column(String, unique = True, nullable = False)
    room = Column(String, nullable=False)

    doctors: Mapped[list['Doctor']] = relationship(back_populates = 'office')