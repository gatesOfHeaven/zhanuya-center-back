from random import randint, choice

from utils.bases import BaseFactory
from utils.facades import hash, calc
from entities.role import Role
from .entity import User


def iin_from(date: str, num: int) -> str:
    first_part = calc.time_to_str(date, '%y%m%d')
    second_part = str(num)
    while len(second_part) < 6:
        second_part = '0' + second_part
    return first_part + second_part


class Factory(BaseFactory):
    async def seed(self, count: int, roles: list[Role]):
        fakes: list[User] = []

        for _ in range(count):
            birth_date = calc.str_to_time(self.fake.date(), self.date_format).date()
            password = self.fake.password()
            [name, surname, *_] = self.fake.name().split(' ')
            fakes.append(User(
                email = self.fake.email(),
                role = choice(roles),
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