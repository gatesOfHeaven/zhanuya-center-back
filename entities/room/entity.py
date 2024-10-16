from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor
    from entities.building import Building


class Room(BaseEntity):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key = True)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable = False)
    title = Column(String(20), nullable = False)

    building: Mapped['Building'] = relationship(back_populates = 'rooms')
    doctors: Mapped[list['Doctor']] = relationship(back_populates = 'office')