from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.user import User
    from entities.doctor import Doctor


class ExperienceRecord(BaseEntity):
    __tablename__ = 'experience_records'

    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key = True)
    record_id = Column(Integer, primary_key = True)
    organization = Column(String(50), nullable = False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    position = Column(String(50), nullable = False)
    hours_at_day = Column(Integer, default = 8, nullable=False)
    approved_by = Column(Integer, ForeignKey('users.id'), nullable = True)

    doctor: Mapped['Doctor'] = relationship(back_populates = 'experience')
    approved_manager: Mapped['User'] = relationship()