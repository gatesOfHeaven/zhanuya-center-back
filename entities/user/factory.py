from random import randint, choice
from datetime import date, timedelta

from utils.bases import BaseFactory
from utils.facades import hash, calc
from entities.role import RoleID
from .entity import User


def iin_from(date: str, num: int) -> str:
    first_part = calc.time_to_str(date, '%y%m%d')
    second_part = str(num)
    while len(second_part) < 6:
        second_part = '0' + second_part
    return first_part + second_part


class Factory(BaseFactory):
    async def seed(self, count: int):
        fakes: list[User] = []

        for _ in range(count):
            role = self.get_role(87, 10)
            birth_date = self.get_birth_date(role)
            password = self.fake.password()
            [name, surname, *_] = self.fake.name().split(' ')

            fakes.append(User(
                email = self.fake.email(),
                role_id = role.value,
                iin = iin_from(birth_date, randint(1, 10**6 - 1)),
                name = name,
                surname = surname,
                gender = choice(['male', 'female']),
                birth_date = birth_date,
                password = password, # test only
                password_hash = hash.it(password)
            ))
            
        await self.flush(fakes)
        return fakes


    def get_role(self, patient_probability: int, doctor_probability: int) -> RoleID:
        return (
            RoleID.PATIENT if self.fake.boolean(patient_probability) else
            RoleID.DOCTOR if self.fake.boolean(100 * doctor_probability/(100 - patient_probability)) else
            RoleID.MANAGER
        )


    def get_birth_date(self, role: RoleID) -> date:
        today = date.today()
        return (
            self.fake.date_between(
                today - timedelta(days = 60 * 365),
                today - timedelta(days = 20 * 365)
            ) if role == RoleID.DOCTOR else self.fake.date_between(
                today - timedelta(days = 60 * 365),
                today - timedelta(days = 20 * 365)
            ) if role == RoleID.MANAGER else self.fake.date_between(
                today - timedelta(days = 100 * 365),
                today
            )
        )