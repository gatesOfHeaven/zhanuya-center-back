from sqlalchemy import Column, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor
    from entities.lunch import Lunch
    from entities.slot import Slot


class Workday(BaseEntity):
    __tablename__ = 'workdays'

    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key = True)
    date = Column(Date, primary_key = True)
    day_at_week = Column(Integer, nullable = False)
    starts_at = Column(Time, nullable = False)
    ends_at = Column(Time, nullable = False)

    doctor: Mapped['Doctor'] = relationship()
    lunch: Mapped[Optional['Lunch']] = relationship(back_populates = 'workday')
    slots: Mapped[list['Slot']] = relationship(back_populates = 'workday')


    def start_datetime(self) -> datetime:
        return datetime.combine(self.date, self.starts_at)

    def end_datetime(self) -> datetime:
        return datetime.combine(self.date, self.ends_at)