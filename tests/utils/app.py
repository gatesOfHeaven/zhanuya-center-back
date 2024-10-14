from pytest import fixture
from logging import Logger, getLogger


@fixture(scope = 'session')
def anyio_backend():
    return 'asyncio'


@fixture(scope = 'session')
def logger() -> Logger:
    return getLogger('test_log')