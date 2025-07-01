from contextlib import asynccontextmanager

from fastapi import FastAPI

## Redis
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Rate Limiting
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

# Application Imports
from app.core.db.database import init_db
from app.users.routes.user_routes import user_router
from app.comments.routes.comment_routes import comment_router
from app.blogs.routes.blog_routes import blog_router
from app.auth.routes.auth_routes import auth_router
from app.tags.routes.tag_routes import tag_router
from app.core.config.application_config import ApplicationConfig
from app.utils.logger.application_logger import ApplicationLogger
from app.core.dependencies.dependencies import provide_application_config
from app.core.middlewares.rate_limit_middleware import rate_limiter
from app.status.status_routes import app as status_router
from app.admin.routes.admin_routes import admin_router

_logger: ApplicationLogger = ApplicationLogger(name=__name__, log_to_console=False)
# Gets the application global configuration
application_config: ApplicationConfig = provide_application_config()



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    """Lifespan event handler to initialize Redis and FastAPI Cache."""
    
    _logger.log_info(message=f"Starting application: {app.title} v{app.version} in {'debug' if app.debug else 'production'} mode.")
    init_db()
    # Initialize Redis connection
    redis: aioredis.Redis = aioredis.from_url(application_config.redis_url, encoding="utf-8", decode_responses=True)
    FastAPICache.init(backend=RedisBackend(redis=redis), prefix="fastapi-cache")
    
    _logger.log_info(message="Redis connection established and FastAPI Cache initialized.")
    yield
    _logger.log_info(message="Application shutdown initiated.")
    await FastAPICache.clear()  # Clear cache on shutdown
    

# Initialize the database at application startup

app = FastAPI(
    lifespan=lifespan,
    title=application_config.app_name,
    version=application_config.app_version,
    debug=application_config.debug,
)

# Rate Limiting Configuration
app.state.limiter = rate_limiter  # Set the rate limiter from the config

app.add_exception_handler(exc_class_or_status_code=RateLimitExceeded, handler=_rate_limit_exceeded_handler)  # Handle rate limit exceeded exceptions

app.add_middleware(middleware_class=SlowAPIMiddleware)  # Add SlowAPI middleware for rate limiting

# Register routers for different modules
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(comment_router, prefix="/api/v1", tags=["comments"])
app.include_router(blog_router, prefix="/api/v1", tags=["blogs"])
app.include_router(tag_router, prefix="/api/v1", tags=["tags"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(status_router, prefix="", tags=["status"])
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])

