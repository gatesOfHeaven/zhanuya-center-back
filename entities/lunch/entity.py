from sqlalchemy import Column, Integer, Date, Time, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.workday import Workday
    from entities.slot import Slot


class Lunch(BaseEntity):
    __tablename__ = 'lunches'

    doctor_id = Column(Integer, primary_key = True)
    date = Column(Date, primary_key = True)
    starts_at = Column(Time, nullable = False)
    ends_at = Column(Time, nullable = False)

    __table_args__: tuple[ForeignKeyConstraint] = tuple([
        ForeignKeyConstraint(
            ['doctor_id', 'date'],
            ['workdays.doctor_id', 'workdays.date']
        )
    ])

    workday: Mapped['Workday'] = relationship(back_populates = 'lunch')