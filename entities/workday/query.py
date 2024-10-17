from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import date

from utils.bases import BaseQuery
from utils.facades import week
from entities.doctor import Doctor
from .entity import Workday


class Query(BaseQuery):
    async def get(self, doctor: Doctor, day: date) -> Workday:
        query = select(Workday).where(
            Workday.doctor_id == doctor.id,
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
        return workday

    async def get_schedule(self, doctor: Doctor, week_num: int) -> list[Workday]:
        schedule: list[Workday] = []
        for day in week.get_week(week_num = week_num):
            workday = await self.get(doctor, day)
            if workday is not None:
                schedule.append(workday)
        return schedule
        