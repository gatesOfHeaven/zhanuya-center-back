from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.user import User
    from entities.category import Category
    from entities.room import Room
    from entities.price import Price
    from entities.experience_record import ExperienceRecord
    from entities.education_record import EducationRecord


class Doctor(BaseEntity):
    __tablename__ = 'doctors'

    id = Column(Integer, ForeignKey('users.id'), primary_key = True, index = True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable = False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable = False)
    avatar_url = Column(String, nullable = False)   # unique
    career_started_on = Column(Date, nullable = False)

    profile: Mapped['User'] = relationship(back_populates = 'as_doctor')
    category: Mapped['Category'] = relationship(back_populates = 'doctors')
    price_list: Mapped[list['Price']] = relationship(back_populates = 'doctor')
    office: Mapped['Room'] = relationship(back_populates = 'doctors')
    experience: Mapped[list['ExperienceRecord']] = relationship(back_populates = 'doctor')
    education: Mapped[list['EducationRecord']] = relationship(back_populates = 'doctor')