from asyncio import run
from redis.asyncio import from_url
from datetime import timedelta


async def main():
    redis = from_url('redis://localhost')
    # await redis.set('my-val', 'value of it', timedelta(seconds = 15))
    val: bytes = await redis.get('email:meteorite.medik@gmail.com')
    print(val.decode())


run(main())