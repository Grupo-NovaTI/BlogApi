from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

# Rate Limiting
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

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
from app.core.middlewares.cache_middleware import clear_redis_cache, init_redis_cache

_logger: ApplicationLogger = ApplicationLogger(name=__name__, log_to_console=False)
# Gets the application global configuration
application_config: ApplicationConfig = provide_application_config()



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    """Lifespan event handler to initialize Redis and FastAPI Cache."""
    
    _logger.log_info(message=f"Starting application: {app.title} v{app.version} in {'debug' if app.debug else 'production'} mode.")
    init_db()
    # Initialize Redis connection
    redis_initialized = await init_redis_cache()
    if not redis_initialized:
        _logger.log_error(message="Failed to connect to Redis. Please check your Redis configuration.")
        raise RuntimeError("Redis connection failed. Check your configuration.")
    _logger.log_info(message="Redis connection established and FastAPI Cache initialized.")
    yield
    await clear_redis_cache()  # Clear cache on shutdown
    _logger.log_info(message="Application shutdown initiated.")


# Initialize the database at application startup

app = FastAPI(
    lifespan=lifespan,
    title=application_config.app_name,
    version=application_config.app_version,
    debug=application_config.debug,
)

# Rate Limiting Configuration
app.state.limiter = rate_limiter  # Set the rate limiter from the config

@app.exception_handler(RateLimitExceeded)  # Handle rate limit exceeded exceptions
async def rate_limit_exceeded_handler(request : Request, exc : RateLimitExceeded):
    """Custom handler for rate limit exceeded exceptions."""
    return _rate_limit_exceeded_handler(request, exc)


app.add_middleware(middleware_class=SlowAPIMiddleware)  # Add SlowAPI middleware for rate limiting

# Register routers for different modules
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(comment_router, prefix="/api/v1", tags=["comments"])
app.include_router(blog_router, prefix="/api/v1", tags=["blogs"])
app.include_router(tag_router, prefix="/api/v1", tags=["tags"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(status_router, prefix="", tags=["status"])
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])

