from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor
    from entities.room import Room


class Building(BaseEntity):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key = True)
    address = Column(String, nullable = False)

    rooms: Mapped[list['Room']] = relationship(back_populates = 'building')