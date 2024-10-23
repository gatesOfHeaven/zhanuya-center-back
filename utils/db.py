from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from typing import AsyncGenerator

from config.app import DB_URL
from .bases import BaseEntity


engine = create_async_engine(DB_URL)
asyncSession: sessionmaker[AsyncSession] = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autoflush = False
)


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        metadata: MetaData = BaseEntity.metadata
        await conn.run_sync(metadata.create_all)
    yield


async def connect_db() -> AsyncGenerator[AsyncSession, None]:
    async with asyncSession() as session:
        yield session