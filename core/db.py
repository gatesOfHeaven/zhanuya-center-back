from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from config.app import DB_URL


engine = create_async_engine(DB_URL)
asyncSession: sessionmaker[AsyncSession] = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autoflush = False
)


async def connect_db() -> AsyncGenerator[AsyncSession, None]:
    async with asyncSession() as session:
        yield session