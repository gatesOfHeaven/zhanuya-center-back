from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.building import Building


class Terminal(BaseEntity):
    __tablename__ = 'terminals'

    id = Column(Integer, primary_key = True)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable = False)

    building: Mapped['Building'] = relationship(back_populates = 'terminals')