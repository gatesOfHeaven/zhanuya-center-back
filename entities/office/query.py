from fastapi import HTTPException, status
from sqlalchemy import select

from utils.bases import BaseQuery
from .entity import Office


class Query(BaseQuery):
    async def all(self) -> list[Office]:
        query = select(Office)
        return (await self.db.execute(query)).scalars().all()