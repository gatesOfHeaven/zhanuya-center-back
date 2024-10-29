from sqlalchemy import Column, Integer, ForeignKey, Date, Time, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.user import User
    from entities.appointment_type import AppointmentType
    from entities.workday import Workday


class Slot(BaseEntity):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key = True)
    doctor_id = Column(Integer, nullable = False)
    date = Column(Date, nullable = False)
    index = Column(Integer, nullable = False)
    patient_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    type_id = Column(Integer, ForeignKey('appointment_types.id'), nullable = False)
    starts_at = Column(Time, nullable = False)
    ends_at = Column(Time, nullable = False)

    __table_args__: tuple[ForeignKeyConstraint] = tuple([
        ForeignKeyConstraint(
            ['doctor_id', 'date'],
            ['workdays.doctor_id', 'workdays.date']
        )
    ])

    patient: Mapped['User'] = relationship()
    type: Mapped['AppointmentType'] = relationship()
    workday: Mapped['Workday'] = relationship(back_populates = 'slots')