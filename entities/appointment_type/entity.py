from sqlalchemy import Column, Integer, String

from utils.bases import BaseEntity


class AppointmentType(BaseEntity):
    __tablename__ = 'appointment_types'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(25), nullable = False)
    min_duration_mins = Column(Integer, nullable = False)
    max_duration_mins = Column(Integer, nullable = False)