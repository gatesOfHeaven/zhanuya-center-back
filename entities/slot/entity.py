from sqlalchemy import Column, Integer, ForeignKey, Date, Time, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.user import User
    from entities.appointment_type import AppointmentType
    from entities.workday import Workday
    from entities.payment import Payment
    from entities.medical_record import MedicalRecord


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
    price = Column(Integer, nullable = False)

    __table_args__ = (ForeignKeyConstraint(
        ['doctor_id', 'date'],
        ['workdays.doctor_id', 'workdays.date']
    ),)

    type: Mapped['AppointmentType'] = relationship()
    patient: Mapped['User'] = relationship()
    workday: Mapped['Workday'] = relationship(back_populates = 'slots')
    payment: Mapped[Optional['Payment']] = relationship(back_populates = 'slot')
    records: Mapped[list['MedicalRecord']] = relationship(back_populates = 'slot')


    def start_datetime(self) -> datetime:
        day = self.date if self.date else self.workday.date
        return datetime.combine(day, self.starts_at)

    def end_datetime(self) -> datetime:
        day = self.date if self.date else self.workday.date
        return datetime.combine(day, self.ends_at)
    
    def duration(self) -> timedelta:
        return self.end_datetime() - self.start_datetime()