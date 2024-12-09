from datetime import timedelta

from core.secondary_db import redis
from entities.slot import Slot


async def save(key: str, content: str | int | bool, minutes: int):
    if not isinstance(content, str): content = str(content)
    await redis.set(key, content, timedelta(minutes = minutes))
    print(key, content)


async def verify(key: str, content: str | int | bool) -> bool:
    if not isinstance(content, str): content = str(content)
    record = await redis.get(key)
    print(key, content)
    if record is None: return False
    assert isinstance(record, bytes)
    if record.decode() != content: return False
    await redis.delete(key)
    return True