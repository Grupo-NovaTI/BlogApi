from fastapi_cache import FastAPICache

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.core.dependencies import provide_application_config
from app.core.config.application_config import ApplicationConfig

_application_config: ApplicationConfig = provide_application_config()


async def init_redis_cache() -> bool:
    """Initialize Redis and FastAPI Cache."""
    redis: aioredis.Redis = aioredis.from_url(
        _application_config.redis_url, encoding="utf-8", decode_responses=True)
    FastAPICache.init(backend=RedisBackend(
        redis=redis), prefix="fastapi-cache")
    return await redis.ping()


async def clear_redis_cache():
    """Clear the FastAPI Cache."""
    await FastAPICache.clear()
