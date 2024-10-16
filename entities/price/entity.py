from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity
from entities.appointment_type import AppointmentType

if TYPE_CHECKING:
    from entities.doctor import Doctor


class Price(BaseEntity):
    __tablename__ = 'prices'

    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key = True, index = True)
    type_id = Column(Integer, ForeignKey('appointment_types.id'), primary_key = True)
    half_hour_price = Column(Integer, nullable = False)

    appointment_type: Mapped['AppointmentType'] = relationship()
    doctor: Mapped['Doctor'] = relationship(back_populates = 'price_list')