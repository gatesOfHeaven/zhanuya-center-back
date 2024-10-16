from random import choice
from datetime import time, timedelta

from utils.bases import BaseFactory
from utils.facades import calc
from entities.user import User
from entities.workday import Workday
from entities.appointment_type import AppointmentType
from entities.role import RoleID
from .entity import Slot


def is_lunch_time(workday: Workday, some_time: time) -> bool:
    if workday.lunch is None:
        return False
    return workday.lunch.starts_at <= some_time <= workday.lunch.ends_at


class Factory(BaseFactory):
    async def seed(
        self,
        workdays: list[Workday],
        users: list[User],
        types: list[AppointmentType]
    ):
        fakes: list[Slot] = []
        patients = [user for user in users if user.role_id == RoleID.PATIENT.value]

        for workday in workdays:
            curr_time = workday.starts_at
            while curr_time < workday.ends_at:
                next_time = calc.add_times(curr_time, timedelta(minutes = 30))
                if not is_lunch_time(workday, curr_time) and self.fake.boolean(75):
                    fakes.append(Slot(
                        doctor_id = workday.doctor_id,
                        date = workday.date,
                        patient = choice(patients),
                        type = choice(types),
                        starts_at = curr_time,
                        ends_at = next_time
                    ))
                curr_time = next_time
        await self.flush(fakes)
        return fakes