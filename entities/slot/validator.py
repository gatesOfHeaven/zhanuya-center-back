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
        start_datetime = datetime.combine(slot.workday.date, slot.starts_at)
        end_datetime = datetime.combine(slot.workday.date, slot.ends_at)
        min_duration = timedelta(minutes = appointment_type.min_duration_mins)
        max_duration = timedelta(minutes = appointment_type.max_duration_mins)
        if not min_duration <= end_datetime - start_datetime <= max_duration:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Invalid Appointment Duration'
            )


    @staticmethod
    def validate_workday_time(slot: Slot):
        start_out_of_workday = not slot.workday.starts_at <= slot.starts_at < slot.workday.ends_at
        end_out_of_workday = not slot.workday.starts_at < slot.ends_at <= slot.workday.ends_at

        if start_out_of_workday or end_out_of_workday:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Slot time is outside workday hours'
            )
        
        if slot.workday.lunch and (
            (slot.workday.lunch.starts_at <= slot.ends_at <= slot.workday.lunch.ends_at) or
            (slot.workday.lunch.starts_at <= slot.starts_at <= slot.workday.lunch.ends_at)
        ):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'Slot overlaps with lunch break'
            )
        

    @staticmethod
    def validate_isnt_past(slot: Slot):
        if datetime.combine(slot.workday.date, slot.ends_at) < datetime.now():
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'You Cannot Make Appointment for Past'
            )
        

    @staticmethod
    def validate_doesnt_start(slot: Slot, action: str):
        if datetime.combine(slot.workday.date, slot.starts_at) < datetime.now():
            raise HTTPException(
                status.HTTP_408_REQUEST_TIMEOUT,
                f'You Cannot {action} Your Appointment More'
            )