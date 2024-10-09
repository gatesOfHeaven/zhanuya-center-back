from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.db import BaseEntity

if TYPE_CHECKING:
    from entities.user import User
    from entities.category import Category
    from entities.room import Room


class Doctor(BaseEntity):
    __tablename__ = 'doctors'

    id = Column(Integer, ForeignKey('users.id'), primary_key = True, index = False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable = False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable = False)
    avatar_url = Column(String, nullable = False)   # unique
    career_started_on = Column(Date, nullable = False)

    profile: Mapped['User'] = relationship()
    category: Mapped['Category'] = relationship(back_populates = 'doctors')
    office: Mapped['Room'] = relationship(back_populates = 'doctors')