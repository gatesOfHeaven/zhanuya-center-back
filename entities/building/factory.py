from utils.bases import BaseFactory
from .entity import Building


class Factory(BaseFactory):
    fakes: list[Building]

    async def seed(self, count: int):
        self.fakes = []
        
        for _ in range(count):
            building = Building(address = self.fake.address())
            self.fakes.append(building)
            self.db.add(building)
        await self.flush()
        return self.fakes