from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from typing import AsyncGenerator
from dotenv import load_dotenv
from os import getenv

from .bases import BaseEntity


load_dotenv()

engine = create_async_engine('sqlite+aiosqlite:///./test.db')


asyncSession = sessionmaker(
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