from random import randint
from datetime import date, time, timedelta

from core.bases import BaseFactory
from entities.doctor import Doctor
from entities.worktime import Worktime
from .entity import Workday


def date_assignable(worktime: Worktime, day: date) -> bool:
    return worktime.end_date is None or (worktime.start_date <= day <= worktime.end_date)


class Factory(BaseFactory):
    async def seed(self, worktimes: list[Worktime], doctors: list[Doctor]):
        fakes: list[Workday] = []
        today = date.today()
        last_day = today + timedelta(weeks = 5)
        curr_day = today - timedelta(weeks = 2)

        while curr_day < last_day:
            worktime = [
                worktime for worktime in worktimes
                if date_assignable(worktime, curr_day)
            ][0]

            for doctor in doctors:
                try: starts_at = randint(worktime.starts_at, worktime.ends_at - 4)
                except ValueError: starts_at = randint(worktime.starts_at, worktime.ends_at)
                ends_at = randint(starts_at, worktime.ends_at)
                fakes.append(Workday(
                    doctor = doctor,
                    date = curr_day,
                    day_at_week = curr_day.weekday(),
                    starts_at = time(starts_at),
                    ends_at = time(ends_at)
                ))
            curr_day += timedelta(days = 1)
            
        await self.flush(fakes)
        return fakes