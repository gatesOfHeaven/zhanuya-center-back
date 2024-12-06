from core.bases import BaseFactory
from .entity import Building


class Factory(BaseFactory):
    async def seed(self, count: int):
        fakes: list[Building] = [
            Building(address = self.fake.address())
            for _ in range(count)
        ]
        await self.flush(fakes)
        return fakes