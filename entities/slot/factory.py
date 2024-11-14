from random import choice
from datetime import time, timedelta

from utils.bases import BaseFactory
from utils.facades import calc
from entities.user import User, Role
from entities.workday import Workday
from entities.price import Price
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
        prices: list[Price]
    ):
        fakes: list[Slot] = []
        patients = [user for user in users if user.role_type == Role.PATIENT]

        for workday in workdays:
            price = choice([price for price in prices if price.doctor == workday.doctor])
            curr_time = workday.starts_at
            while curr_time < workday.ends_at:
                next_time = calc.add_times(curr_time, timedelta(minutes = 30))
                if not is_lunch_time(workday, curr_time) and self.fake.boolean(75):
                    patient = choice(patients)
                    fakes.append(Slot(
                        doctor_id = workday.doctor.id,
                        date = workday.date,
                        patient = patient,
                        index = len([slot.index for slot in fakes if slot.patient == patient]) + 1,
                        type = price.appointment_type,
                        starts_at = curr_time,
                        ends_at = next_time,
                        price = price.cost
                    ))
                curr_time = next_time
        await self.flush(fakes)
        return fakes