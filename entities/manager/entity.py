from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.user import User
    from entities.user import User
    from entities.building import Building


class Manager(BaseEntity):
    __tablename__ = 'managers'

    id = Column(Integer, ForeignKey('users.id'), primary_key = True)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable = False)
    avatar_url = Column(String, nullable = False)   # unique

    profile: Mapped['User'] = relationship(back_populates = 'as_manager')
    building: Mapped['Building'] = relationship()