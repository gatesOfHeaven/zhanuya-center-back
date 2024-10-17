from sqlalchemy import select

from utils.bases import BaseQuery
from .entity import AppointmentType


class Query(BaseQuery):
    async def all(self) -> list[AppointmentType]:
        query = select(AppointmentType)
        return (await self.db.execute(query)).scalars().all()
    
    async def get(self, id: int) -> AppointmentType:
        query = select(AppointmentType).where(AppointmentType.id == id)
        return (await self.db.execute(query)).scalar_one_or_none()