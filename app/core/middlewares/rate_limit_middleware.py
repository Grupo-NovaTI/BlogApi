"""
Rate limiting middleware configuration for FastAPI.

This module sets up the SlowAPI Limiter for request rate limiting using the client's remote address.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

rate_limiter: Limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5/minute"],
)

