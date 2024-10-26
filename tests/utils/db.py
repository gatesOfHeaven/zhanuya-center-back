from pytest import fixture
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from main import app
from seed import seed
from utils import connect_db, asyncSession
from utils.bases import BaseEntity


engine = create_async_engine('sqlite+aiosqlite:///./temp.db')
tempSessionLocal: sessionmaker[AsyncSession] = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autoflush = False
)


@fixture(scope = 'session', autouse = True)
async def setup_database():
    metadata: MetaData = BaseEntity.metadata
    async with engine.connect() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
        async with tempSessionLocal() as session:
            await seed(session)
            await session.commit()
            yield session
        yield


@fixture(scope = 'function')
async def temp_db():
    async with asyncSession() as session:
        yield session


@fixture(autouse = True)
async def override_db_conn(temp_db: AsyncSession):
    app.dependency_overrides[connect_db] = lambda: temp_db
    yield
    app.dependency_overrides.clear()