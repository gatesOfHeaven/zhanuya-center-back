from sqlalchemy import Column, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.db import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor
    from entities.slot import Slot


class Workday(BaseEntity):
    __tablename__ = 'workdays'

    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key = True, index = False)
    date = Column(Date, primary_key = True)
    day_at_week = Column(Integer, nullable = False)
    starts_at = Column(Time, nullable = False)
    ends_at = Column(Time, nullable = False)
    lunch_starts_at = Column(Time, nullable = False)
    lunch_ends_at = Column(Time, nullable = False)

    doctor: Mapped['Doctor'] = relationship()
    slots: Mapped[list['Slot']] = relationship(back_populates = 'workday')