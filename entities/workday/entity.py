from sqlalchemy import Column, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING, Optional

from utils.db import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor
    from entities.lunch import Lunch
    from entities.slot import Slot


class Workday(BaseEntity):
    __tablename__ = 'workdays'

    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key = True, index = False)
    date = Column(Date, primary_key = True)
    day_at_week = Column(Integer, nullable = False)
    starts_at = Column(Time, nullable = False)
    ends_at = Column(Time, nullable = False)

    doctor: Mapped['Doctor'] = relationship()
    lunch: Mapped[Optional['Lunch']] = relationship(back_populates = 'workday')
    slots: Mapped[list['Slot']] = relationship(back_populates = 'workday')