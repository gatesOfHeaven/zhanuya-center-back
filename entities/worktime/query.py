from fastapi import HTTPException, status
from sqlalchemy import select
from datetime import date

from utils.bases import BaseQuery
from utils.facades import week
from .entity import Worktime


class Query(BaseQuery):
    async def actual(self) -> Worktime | None:
        query = (select(Worktime)
            .where(Worktime.end_date == None)
            .order_by(Worktime.start_date.desc())
        )
        return (await self.db.execute(query)).scalar_one_or_none()


    async def get_actual(self) -> Worktime:
        worktime = await self.actual()
        if worktime is None:
            raise HTTPException(
                status.HTTP_501_NOT_IMPLEMENTED,
                'Application has No Configuration'
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
        