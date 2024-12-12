from pytest import fixture
from httpx import AsyncClient, ASGITransport
from logging import Logger, getLogger

from main import app
from config.app import HOST


@fixture(scope = 'session')
def anyio_backend():
    return 'asyncio'


@fixture(scope = 'session')
async def client():
    async with AsyncClient(
        transport = ASGITransport(app),
        base_url = HOST
    ) as client:
        yield client


@fixture(scope = 'session')
def logger() -> Logger:
    return getLogger('test_log')