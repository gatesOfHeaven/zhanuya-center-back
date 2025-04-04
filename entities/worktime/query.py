from fastapi import HTTPException, status
from sqlalchemy import select, or_
from datetime import date

from core.bases import BaseQuery
from core.facades import week
from .entity import Worktime


class Query(BaseQuery):
    async def actual(self) -> Worktime:
        query = (select(Worktime)
            .where(Worktime.end_date == None)
            .order_by(Worktime.start_date.desc())
        )
        worktime = await self.first(query)
        if worktime is None:
            raise HTTPException(
                status.HTTP_501_NOT_IMPLEMENTED,
                'Application has No Configuration'
            )
        return worktime
    

    async def get(self, day: date, raise_: bool = True) -> Worktime | None:
        query = select(Worktime).where(
            Worktime.start_date <= day,
            or_(Worktime.end_date == None, day <= Worktime.end_date)
        )
        worktime = await self.first(query)
        if raise_ and worktime is None:
            raise HTTPException(
                status.HTTP_501_NOT_IMPLEMENTED,
                'Application has No Configuration for Given Day'
            )
        return worktime
    

    async def configure_worktime(
        self,
        start_date: date,
        starts_at: int,
        ends_at: int
    ) -> Worktime:
        prev_worktime = await self.actual()
        if prev_worktime is not None:
            prev_worktime.end_date = week.get_week(start_date, -1)[-1]

        new_worktime = Worktime(
            start_date = week.get_week(start_date)[0],
            starts_at = starts_at,
            ends_at = ends_at
        )
        self.db.add(new_worktime)
        await self.commit()
        return new_worktime
        