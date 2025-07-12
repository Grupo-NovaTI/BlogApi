"""
Redis cache middleware utilities for FastAPI.

This module provides functions to initialize and clear the FastAPI cache using Redis as the backend.
"""

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.core.config.application_config import REDIS_URL


async def init_redis_cache() -> bool:
    """
    Initialize Redis and FastAPI Cache.

    Returns:
        bool: True if Redis is reachable and cache is initialized, False otherwise.
    """
    redis: aioredis.Redis = aioredis.from_url(
        REDIS_URL, encoding="utf-8", decode_responses=True)
    FastAPICache.init(backend=RedisBackend(
        redis=redis), prefix="fastapi-cache")
    return await redis.ping()


async def clear_redis_cache():
    """
    Clear the FastAPI Cache.
    """
    await FastAPICache.clear()
