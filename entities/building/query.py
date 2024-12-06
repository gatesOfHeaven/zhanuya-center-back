from fastapi import HTTPException, status
from sqlalchemy import select

from core.bases import BaseQuery
from .entity import Building


class Query(BaseQuery):
    async def all(self) -> list[Building]:
        query = select(Building)
        return await self.fetch_all(query)