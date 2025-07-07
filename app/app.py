from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from starlette import status
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
from app.utils.logger.application_logger import ApplicationLogger
from app.core.middlewares import rate_limiter, clear_redis_cache, init_redis_cache
from app.status.status_routes import app as status_router
from app.admin.routes.admin_routes import admin_router
from app.utils.errors.exceptions import BaseApplicationException, BaseAuthenticationException, BaseIdentifierException
from app.core.config.application_config import APP_NAME, APP_VERSION, DEBUG

_logger: ApplicationLogger = ApplicationLogger(
    name=__name__, log_to_console=False)
# Gets the application global configuration


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to initialize Redis and FastAPI Cache."""

    _logger.log_info(
        message=f"Starting application: {app.title} v{app.version} in {'debug' if app.debug else 'production'} mode.")
    init_db()
    # Initialize Redis connection
    redis_initialized: bool = await init_redis_cache()
    if not redis_initialized:
        _logger.log_error(
            message="Failed to connect to Redis. Please check your Redis configuration.")
        raise RuntimeError(
            "Redis connection failed. Check your configuration.")
    _logger.log_info(
        message="Redis connection established and FastAPI Cache initialized.")
    yield
    await clear_redis_cache()  # Clear cache on shutdown
    _logger.log_info(message="Application shutdown initiated.")


# Initialize the database at application startup

app = FastAPI(
    lifespan=lifespan,
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG,
)

# Rate Limiting Configuration
app.state.limiter = rate_limiter  # Set the rate limiter from the config


# Handle rate limit exceeded exceptions
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded exceptions."""
    return _rate_limit_exceeded_handler(request, exc)


# Handle BaseApplicationException
@app.exception_handler(BaseApplicationException)
async def base_application_exception_handler(request: Request, exc: BaseApplicationException) -> JSONResponse:
    """Custom handler for BaseApplicationException."""
    _logger.log_error(
        message=f"[{exc.id}]: {exc.message}. Details: {exc.details}.")
    # Log the error with the logger
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_id": exc.id,
            "message": exc.message,
        },
    )

# Handle BaseAuthenticationException
@app.exception_handler(BaseAuthenticationException)
async def base_authentication_exception_handler(request: Request, exc: BaseAuthenticationException) -> JSONResponse:
    """Custom handler for BaseAuthenticationException."""
    _logger.log_error(message=f"Authentication error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error_id": exc.id,
            "message": exc.message,
        },
    )

# Handle BaseIdentifierException
@app.exception_handler(BaseIdentifierException)
async def base_identifier_exception_handler(request: Request, exc: BaseIdentifierException) -> JSONResponse:
    """Custom handler for BaseIdentifierException."""
    _logger.log_error(message=f"[{exc.id}]: {exc.message}. Details:{exc.details}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_id": exc.id,
            "message": exc.message,
        },
    )

# Handle ResponseValidationError
@app.exception_handler(ResponseValidationError)
async def response_validation_error_handler(request: Request, exc: ResponseValidationError) -> JSONResponse:
    """Custom handler for ResponseValidationError."""
    _logger.log_error(message=f"Response validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Invalid response data."},
    )


@app.exception_handler(RequestValidationError)  # Handle RequestValidationError
async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Custom handler for RequestValidationError."""
    _logger.log_error(message=f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Invalid request data: " + str(exc.errors()[0]["msg"])},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Custom handler for generic exceptions."""
    _logger.log_error(message=f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"Internal server error. {exc}"},
    )



# Add SlowAPI middleware for rate limiting
app.add_middleware(middleware_class=SlowAPIMiddleware)

# Register routers for different modules
app.include_router(user_router, prefix="/api/v1", tags=["authors"])
app.include_router(comment_router, prefix="/api/v1", tags=["comments"])
app.include_router(blog_router, prefix="/api/v1", tags=["blogs"])
app.include_router(tag_router, prefix="/api/v1", tags=["tags"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(status_router, prefix="", tags=["status"])
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])
