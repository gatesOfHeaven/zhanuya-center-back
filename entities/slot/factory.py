from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import joinedload
from random import choice
from datetime import time, datetime, timedelta

from core.bases import BaseFactory
from core.facades import calc
from entities.user import User, Role
from entities.doctor import Doctor
from entities.manager import Manager
from entities.payment import Payment
from entities.room import Room
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
    

    async def random(
        self,
        count: int,
        finished_only: bool = False,
        paid_only: bool = False
    ) -> list[Slot]:
        now = datetime.now()
        conditions = []
        if finished_only: conditions.append(or_(
            Slot.date <= now.date(),
            and_(
                Slot.date == now.date(),
                Slot.starts_at <= now.time()
            )
        ))
        if paid_only: conditions.append(Slot.payment != None)

        query = select(Slot).where(*conditions).options(
            joinedload(Slot.workday).joinedload(Workday.doctor).options(
                joinedload(Doctor.profile),
                joinedload(Doctor.category),
                joinedload(Doctor.office).joinedload(Room.building),
                joinedload(Doctor.price_list).joinedload(Price.appointment_type)
            ),
            (joinedload(Slot.payment).options(
                joinedload(Payment.manager)
                .joinedload(Manager.profile)
            )),
            joinedload(Slot.payment).joinedload(Payment.terminal),
            joinedload(Slot.patient),
            joinedload(Slot.type),
            joinedload(Slot.records)
        ).order_by(func.random()).limit(count)
        return await self.fetch_all(query)


    async def by_doctor(self, doctor: Doctor, count: int) -> list[Slot]:
        query = select(Slot).where(Slot.doctor_id == doctor.id).options(
            joinedload(Slot.workday).joinedload(Workday.doctor).options(
                joinedload(Doctor.profile),
                joinedload(Doctor.category),
                joinedload(Doctor.office).joinedload(Room.building),
                joinedload(Doctor.price_list).joinedload(Price.appointment_type)
            ),
            (joinedload(Slot.payment).options(
                joinedload(Payment.manager)
                .joinedload(Manager.profile)
            )),
            joinedload(Slot.payment).joinedload(Payment.terminal),
            joinedload(Slot.patient),
            joinedload(Slot.type),
            joinedload(Slot.records)
        ).order_by(func.random()).limit(count)
        return await self.fetch_all(query)