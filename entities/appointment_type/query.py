from sqlalchemy import select

from utils.bases import BaseQuery
from .entity import AppointmentType


class Query(BaseQuery):
    async def all(self) -> AppointmentType:
        query = select(AppointmentType)
        return (await self.db.execute(query)).scalars().all()