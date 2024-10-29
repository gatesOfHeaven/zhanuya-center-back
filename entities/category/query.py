from fastapi import HTTPException, status
from sqlalchemy import select

from utils.bases import BaseQuery
from .entity import Category


class Query(BaseQuery):
    async def all(self) -> list[Category]:
        query = select(Category)
        return await self.all(query)