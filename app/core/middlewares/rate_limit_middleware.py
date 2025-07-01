from typing import List, Optional
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config.application_config import ApplicationConfig
from app.core.dependencies import provide_application_config

_application_config: ApplicationConfig = provide_application_config()

def get_ip_for_rate_limit(request: Request) -> str:
    """Custom key function to print the client IP for debugging."""
    client_ip = get_remote_address(request)
    print(f"DEBUG: Rate limit key (IP): {client_ip}") # <-- ADD THIS
    return client_ip

rate_limiter: Limiter = Limiter(
    key_func=get_ip_for_rate_limit,
    default_limits=["5/minute"],
    storage_uri=_application_config.redis_url,  # Use the Redis URL from the application config

)

