from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from config.seed import SEED


baseFaker = Faker()
Faker.seed(SEED)


class BaseFactory:
    fake: Faker
    db: AsyncSession
    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %H:%M:%S'
    
    def __init__(self, db: AsyncSession):
        self.fake = baseFaker
        self.db = db

    async def flush(self, fakes: list):
        self.db.add_all(fakes)
        await self.db.flush()