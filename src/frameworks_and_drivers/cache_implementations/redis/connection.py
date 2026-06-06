from redis import asyncio as aioredis
from redis.asyncio.client import Redis

from src.frameworks_and_drivers.cache_implementations.redis.settings import (
    redis_settings,
)

redis_client: Redis | None = None


async def init_redis_connection() -> Redis:
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            redis_settings.url,
            decode_responses=True,
        )
    return redis_client


async def close_redis_connection() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
    redis_client = None


def get_redis_client() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis connection is not initialized")
    return redis_client
