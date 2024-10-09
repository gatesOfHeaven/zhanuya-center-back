from random import randint, choice

from utils.bases import BaseFactory
from entities.building import Building
from .entity import Room


class Factory(BaseFactory):
    fakes: list[Room]

    async def seed(self, count: int, buildings: list[Building]):
        self.fakes = []

        for _ in range(count):
            room = Room(
                building = choice(buildings),
                title = f'{self.fake.random_uppercase_letter()}{randint(100, 600)}'
            )
            self.fakes.append(room)
            self.db.add(room)
        await self.flush()
        return self.fakes