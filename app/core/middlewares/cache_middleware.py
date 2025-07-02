from fastapi_cache import FastAPICache

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.core.dependencies import provide_application_config
from app.core.config.application_config import ApplicationConfig
## Redis


_application_config: ApplicationConfig = provide_application_config()

async def init_redis_cache():
    """Initialize Redis and FastAPI Cache."""
    redis: aioredis.Redis = aioredis.from_url(_application_config.redis_url, encoding="utf-8", decode_responses=True)
    FastAPICache.init(backend=RedisBackend(redis=redis), prefix="fastapi-cache")
    return await redis.ping()
     # Debugging line to confirm Redis connection
    
async def clear_redis_cache():
    """Clear the FastAPI Cache."""
    value = await FastAPICache.clear()  # Clear cache on shutdown
    print(f"Cache cleared: {value}")  # Debugging line to confirm cache clearing