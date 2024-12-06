from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, time
from typing import Callable

from core.bases import BaseQuery
from core.facades import week
from entities.doctor import Doctor
from entities.slot import Slot
from .entity import Workday


class Query(BaseQuery):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.slot_comparator: Callable[[Slot], time] = lambda slot: slot.starts_at

    
    async def get(self, doctor: Doctor, day: date) -> Workday:
        query = select(Workday).where(
            Workday.doctor == doctor,
            Workday.date == day
        ).options(
            joinedload(Workday.doctor),
            joinedload(Workday.lunch),
            joinedload(Workday.slots)
        )
        workday = (await self.db.execute(query)).unique().scalar_one_or_none()
        if not workday:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'This Doctor Does Not Work This Day'
            )
        workday.slots.sort(key = self.slot_comparator)
        return workday


    async def get_schedule(self, doctor: Doctor, week_num: int) -> list[Workday]:
        query = select(Workday).where(
            Workday.doctor == doctor,
            Workday.date.in_(week.get_week(week_num = week_num))
        ).options(
            joinedload(Workday.lunch),
            joinedload(Workday.slots).joinedload(Slot.patient)
        )
        workdays:list[Workday] = (await self.db.execute(query)).unique().scalars().all()

        day_comparator: Callable[[Workday], date] = lambda day: day.date
        workdays.sort(key = day_comparator)
        for workday in workdays:
            workday.slots.sort(key = self.slot_comparator)
        return workdays