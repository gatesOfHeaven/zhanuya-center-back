from random import choice

from core.bases import BaseFactory
from entities.building import Building
from .entity import Terminal


class Factory(BaseFactory):
    async def seed(self, count: int, buildings: list[Building]):
        fakes: list[Terminal] = [
           Terminal(building = choice(buildings))
           for _ in range(count)
        ]
        await self.flush(fakes)
        return fakes