from random import randint
from datetime import date, time, timedelta

from utils.bases import BaseFactory
from entities.doctor import Doctor
from entities.worktime import Worktime
from .entity import Workday


def date_assignable(worktime: Worktime, day: date) -> bool:
    return worktime.end_date is None or (
        worktime.start_date <= day and day <= worktime.end_date
    )


class Factory(BaseFactory):
    async def seed(
        self,
        start_date: date,
        worktimes: list[Worktime],
        doctors: list[Doctor]
    ):
        fakes: list[Workday] = []

        last_day = date.today() + timedelta(weeks = 3)
        curr_day = start_date

        while curr_day < last_day:
            worktime = [
                worktime for worktime in worktimes
                if date_assignable(worktime, curr_day)
            ][0]

            for doctor in doctors:
                starts_at = randint(worktime.starts_at, worktime.ends_at)
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