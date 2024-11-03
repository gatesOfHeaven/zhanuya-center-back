from fastapi import HTTPException, status
from datetime import datetime, timedelta

from entities.user import User
from entities.appointment_type import AppointmentType
from .entity import Slot


class Validator:
    @staticmethod
    def validate_patient(slot: Slot, me: User, action: str):
        if slot.patient != me:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f'You Can {action} Only YOUR Appointments'
            )


    @staticmethod
    def validate_duration(slot: Slot, appointment_type: AppointmentType):
        min_duration = timedelta(minutes = appointment_type.min_duration_mins)
        max_duration = timedelta(minutes = appointment_type.max_duration_mins)
        if not min_duration <= slot.duration() <= max_duration:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Invalid Appointment Duration'
            )


    @staticmethod
    def validate_workday_time(slot: Slot):
        start = slot.workday.starts_at
        end = slot.workday.ends_at
        if not (start <= slot.starts_at < end and start < slot.ends_at <= end):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Slot time is outside workday hours'
            )
        
        if slot.workday.lunch:
            start = slot.workday.lunch.starts_at
            end = slot.workday.lunch.ends_at
            if start < slot.ends_at <= end or start <= slot.starts_at < end:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    'Slot overlaps with lunch break'
                )
        

    @staticmethod
    def validate_isnt_past(slot: Slot):
        if slot.end_datetime() < datetime.now():
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'You Cannot Make Appointment for Past'
            )
        

    @staticmethod
    def validate_doesnt_start(slot: Slot, action: str):
        if slot.start_datetime() < datetime.now():
            raise HTTPException(
                status.HTTP_408_REQUEST_TIMEOUT,
                f'You Cannot {action} Your Appointment More'
            )