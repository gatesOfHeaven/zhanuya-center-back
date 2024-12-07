from redis.asyncio import from_url

from config.app import REDIS_URL


redis = from_url(REDIS_URL)