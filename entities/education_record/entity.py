from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.bases import BaseEntity

if TYPE_CHECKING:
    from entities.doctor import Doctor
    from entities.manager import Manager


class EducationRecord(BaseEntity):
    __tablename__ = 'education_records'

    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key = True)
    record_id = Column(Integer, primary_key = True)
    organization = Column(String(50), nullable = False)
    speciality = Column (String(75), nullable = False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    gpa = Column(Float, nullable=False)
    gpa_from = Column(Integer, nullable=False)
    approved_by = Column(Integer, ForeignKey('managers.id'), nullable = True)

    doctor: Mapped['Doctor'] = relationship(back_populates = 'education')
    approved_manager: Mapped['Manager'] = relationship()