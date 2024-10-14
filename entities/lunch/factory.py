from random import randint
from datetime import datetime, date, time, timedelta

from utils.bases import BaseFactory
from entities.workday import Workday
from .entity import Lunch


class Factory(BaseFactory):
    async def seed(self, workdays: list[Workday]):
        fakes: list[Lunch] = []

        for workday in workdays:
            workday_starts_at = datetime.combine(date.today(), workday.starts_at)
            workday_ends_at = datetime.combine(date.today(), workday.ends_at)
            if workday_ends_at - workday_starts_at <= timedelta(hours = 4):
                workday.lunch = None
                continue
            lunch_starts_at = randint(workday_starts_at.hour + 1, workday_ends_at.hour - 2)

            lunch = Lunch(
                workday = workday,
                starts_at = time(lunch_starts_at),
                ends_at = time(lunch_starts_at + 1)
            )
            workday.lunch = lunch
            fakes.append(lunch)

        await self.flush(fakes)
        return fakes