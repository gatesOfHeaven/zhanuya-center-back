from fastapi import status, HTTPException
from sqlalchemy import select, exists, or_, and_
from datetime import datetime, date, time, timedelta

from utils.bases import BaseQuery
from entities.user import User
from entities.doctor import Doctor
from entities.workday import Workday
from entities.appointment_type import AppointmentType
from .entity import Slot


class Query(BaseQuery):
    async def new(
        self,
        patient: User,
        workday: Workday,
        type: AppointmentType,
        starts_at: time,
        ends_at: time,
        commit: bool = True
    ) -> Slot:
        start_datetime = datetime.combine(workday.date, starts_at)
        end_datetime = datetime.combine(workday.date, ends_at)
        min_duration = timedelta(minutes = type.min_duration_mins)
        max_duration = timedelta(minutes = type.max_duration_mins)
        if not min_duration <= end_datetime - start_datetime <= max_duration:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Invalid Appointment Duration'
            )
        
        query = select(exists(Slot).where(
            Slot.date == workday.date,
            Slot.doctor_id == workday.doctor.id,
            or_(
                and_(Slot.starts_at <= starts_at < Slot.ends_at),
                and_(Slot.starts_at <= ends_at < Slot.ends_at)
            )
        ))
        slot_is_busy = (await self.db.execute(query)).scalar()
        slot_is_busy = slot_is_busy and (
            (workday.lunch.starts_at <= starts_at < workday.lunch.ends_at) or
            (workday.lunch.starts_at <= ends_at < workday.lunch.ends_at)
        ) and not (
            (workday.starts_at <= ends_at < workday.ends_at) or
            (workday.starts_at <= starts_at < workday.ends_at)
        )
        if slot_is_busy:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'Such Doctor For Such Time Unavailable'
            )
        
        if end_datetime < datetime.now():
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'You Cannot Make Appointment for Past'
            )
        
        slot = Slot(
            patient = patient,
            workday = workday,
            type = type,
            starts_at = starts_at,
            ends_at = ends_at
        )
        self.db.add(slot)
        if commit: await self.commit()
        return slot