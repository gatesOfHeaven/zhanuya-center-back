from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class BaseQuery:
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit(self):
        try: await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)