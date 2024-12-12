from fastapi import HTTPException, status
from datetime import datetime, timedelta

from entities.user import User
from entities.manager import Manager
from entities.terminal import Terminal
from entities.appointment_type import AppointmentType
from .entity import Slot
from .values import TIMEDELTA_BEFORE_START_TO_CONFIRM, TIMEDELTA_AFTER_START_TO_CONFIRM


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


    @staticmethod
    def validate_access(slot: Slot, me: User):
        doctor = slot.workday.doctor
        building = doctor.office.building
        am_i_patient = isinstance(me, User) and slot.patient == me
        am_i_doctor = isinstance(me, User) and doctor == me.as_doctor
        am_i_manager = isinstance(me, User) and isinstance(me.as_manager, Manager) and building == me.as_manager.building
        is_terminal = isinstance(me, Terminal) and building == me.building
        if not (am_i_patient or am_i_doctor or am_i_manager or is_terminal):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'Appointment Unavailable For You'
            )


    @staticmethod
    def validate_medical_history_access(slot: Slot):
        now = datetime.now()
        if now < slot.start_datetime() - timedelta(hours = 1): raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            'You Cannot See Medical Records of Current Patient Yet'
        )
        if now > slot.end_datetime() + timedelta(hours = 2): raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            'You Need to Request Access'
        )


    @staticmethod
    def validate_pay_ability(slot: Slot):
        starts_at = slot.start_datetime()
        left_bound = starts_at - TIMEDELTA_BEFORE_START_TO_CONFIRM
        right_bound = starts_at + TIMEDELTA_AFTER_START_TO_CONFIRM
        if not left_bound < datetime.now() < right_bound or slot.payment is not None:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'You Cannot Confirm Your Appointment Now'
            )