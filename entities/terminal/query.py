from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.bases import BaseQuery
from entities.manager import Manager
from .entity import Terminal


class Query(BaseQuery):
    async def get(self, id: int, manager: Manager):
        query = (
            select(Terminal)
            .where(Terminal.id == id)
            .options(joinedload(Terminal.building))
        )
        terminal = await self.first(query)
        if terminal is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'Terminal[id={id}] Not Found'
            )
        if terminal.building_id != manager.building_id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f'Terminal[id={id}] Unavailable For You'
            )
        return terminal