from fastapi import HTTPException, status
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import TypeVar

from .BaseEntity import Entity
from core.secondary_db import redis


T = TypeVar('T')


class BaseQuery:
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()


    async def commit(self):
        try: await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def field(self, query: Select[tuple[T]]) -> T | None:
        return (await self.db.execute(query)).scalar()


    async def first(self, query: Select[tuple[Entity]]) -> Entity | None:
        return (await self.db.execute(query)).unique().scalar_one_or_none()


    async def fetch_all(self, query: Select[tuple[Entity]]) -> list[Entity]:
        return (await self.db.execute(query)).unique().scalars().all()
    

class SecondarySchemeQuery:
    def __init__(self):
        self.db = redis