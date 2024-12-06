from random import randint, choice

from core.bases import BaseFactory
from entities.building import Building
from .entity import Room


class Factory(BaseFactory):
    async def seed(self, count: int, buildings: list[Building]):
        fakes: list[Room] = [Room(
            building = choice(buildings),
            title = f'{self.fake.random_uppercase_letter()}{randint(100, 600)}'
        ) for _ in range(count)]
        
        await self.flush(fakes)
        return fakes