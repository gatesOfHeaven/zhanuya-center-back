from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from random import randint, choice
from datetime import date, timedelta

from core.bases import BaseFactory
from core.facades import hash, calc
from core.facades import auth
from .entity import User, Role, Gender


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
            role = self.get_role(77, 17)
            birth_date = self.get_birth_date(role)
            password = self.fake.password()
            [name, surname, *_] = self.fake.name().split(' ')

            fakes.append(User(
                email = self.fake.email(),
                role_type = role,
                iin = iin_from(birth_date, randint(1, 10**6 - 1)),
                name = name,
                surname = surname,
                gender = choice(list(Gender)),
                birth_date = birth_date,
                password = password, # test only
                password_hash = hash.it(password)
            ))
            
        await self.flush(fakes)
        return fakes
    

    async def new(self) -> tuple[User, str]:
        email = 'test@test.qa'
        query = select(User).where(User.email == email)
        user = await self.first(query)
        if user is None:
            [name, surname, *_] = self.fake.name().split(' ')
            birth_date = self.get_birth_date(Role.PATIENT)
            password = self.fake.password()
            user = User(
                email = email,
                role_type = Role.PATIENT,
                iin = iin_from(birth_date, randint(1, 10**6 - 1)),
                name = name,
                surname = surname,
                gender = choice(list(Gender)),
                birth_date = birth_date,
                password = password, # test only
                password_hash = hash.it(password)
            )
            self.db.add(user)
            await self.commit()
        return (user, auth.generate_token(user.id))
    

    async def get_random(self, count: int, role: Role | None = None) -> list[User]:
        query = select(User).order_by(func.random()).limit(count)
        if role is not None:
            query = query.where(User.role_type == role.name)
        return await self.fetch_all(query)
    
    
    async def remove(self, user: User):
        await self.db.delete(user)
        await self.commit()


    def get_role(self, patient_probability: int, doctor_probability: int) -> Role:
        return (
            Role.PATIENT if self.fake.boolean(patient_probability) else
            Role.DOCTOR if self.fake.boolean(100 * doctor_probability/(100 - patient_probability)) else
            Role.MANAGER
        )


    def get_birth_date(self, role: Role) -> date:
        today = date.today()
        return (
            self.fake.date_between(
                today - timedelta(days = 60 * 365),
                today - timedelta(days = 20 * 365)
            ) if role == Role.DOCTOR else self.fake.date_between(
                today - timedelta(days = 60 * 365),
                today - timedelta(days = 20 * 365)
            ) if role == Role.MANAGER else self.fake.date_between(
                today - timedelta(days = 100 * 365),
                today
            )
        )