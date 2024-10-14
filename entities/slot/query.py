from fastapi import status, HTTPException
from sqlalchemy import select, exists, or_, and_
from datetime import date, time, timedelta

from utils.bases import BaseQuery
from entities.user import User
from entities.doctor import Doctor
from entities.workday import Workday
from .entity import Slot


class Query(BaseQuery):
    async def new(
        self,
        patient: User,
        workday: Workday,
        starts_at: time,
        commit: bool = True
    ) -> Slot:
        ends_at = starts_at + timedelta(minutes = 30)
        query = select(exists(Slot).where(
            Slot.date == workday.date,
            Slot.doctor_id == workday.doctor.id,
            or_(
                and_(Slot.starts_at <= starts_at, starts_at <= Slot.ends_at),
                and_(Slot.starts_at <= ends_at, ends_at <= Slot.ends_at)
            )
        ))

        slot_is_busy = (await self.db.execute(query)).scalar()
        slot_is_busy = slot_is_busy and (
            (workday.lunch_starts_at <= ends_at and ends_at <= workday.lunch_ends_at) or
            (workday.lunch_starts_at <= starts_at and starts_at <= workday.lunch_ends_at)
        ) and not (
            (workday.starts_at <= ends_at and ends_at <= workday.ends_at) or
            (workday.starts_at <= starts_at and starts_at <= workday.ends_at)
        )

        if slot_is_busy:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'Such Doctor For Such Time Not Available'
            )
        
        slot = Slot(
            patient = patient,
            workday = workday,
            starts_at = starts_at,
            ends_at = ends_at
        )
        self.db.add(slot)
        if commit: await self.commit()
        return slot