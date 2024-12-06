from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from config.seed import SEED
from .BaseEntity import Entity
from .BaseQuery import BaseQuery


baseFaker = Faker()
Faker.seed(SEED)


class BaseFactory(BaseQuery):
    fake: Faker
    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %H:%M:%S'
    
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.fake = baseFaker

    async def flush(self, fakes: list[Entity]):
        self.db.add_all(fakes)
        await self.db.flush()

    async def refresh(self, object: Entity):
        await self.db.refresh(object)