from sqlalchemy import select

from core.bases import BaseQuery
from .entity import AppointmentType


class Query(BaseQuery):
    async def all(self) -> list[AppointmentType]:
        query = select(AppointmentType)
        return await self.fetch_all(query)
    
    async def get(self, id: int) -> AppointmentType:
        query = select(AppointmentType).where(AppointmentType.id == id)
        return await self.first(query)