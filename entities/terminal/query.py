from fastapi import HTTPException, status
from sqlalchemy import select

from core.bases import BaseQuery
from .entity import Terminal


class Query(BaseQuery):
    async def get(self, id: int):
        query = select(Terminal).where(Terminal.id == id)
        terminal = await self.first(query)
        if terminal is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'Terminal[id={id}] Not Found'
            )
        return terminal