from contextlib import asynccontextmanager

from datetime import datetime
from typing import Optional
from uuid import uuid4
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
from app.utils.errors.exceptions import BaseAPIException
from app.core.config.application_config import APP_NAME, APP_VERSION, DEBUG

_logger: ApplicationLogger = ApplicationLogger(
    name=__name__, log_to_console=False)
# Gets the application global configuration


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.

    This asynchronous generator function manages the application's startup and shutdown events.
    On startup, it logs the application state, initializes the database, and attempts to establish
    a Redis cache connection. If the Redis connection fails, it logs an error and raises a RuntimeError.
    On shutdown, it clears the Redis cache and logs the shutdown event.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None

    Raises:
        RuntimeError: If the Redis cache connection cannot be established.
    """

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
    """
    This asynchronous handler is triggered when a client exceeds the allowed number of requests
    within a specified time window. It returns a JSON response with a 429 status code, a user-friendly
    error message, a unique error identifier, and a timestamp indicating when the error occurred.

        request (Request): The incoming HTTP request that triggered the rate limit.
        exc (RateLimitExceeded): The exception instance indicating the rate limit was exceeded.

        JSONResponse: A response object with HTTP 429 status and error details in JSON format.
    """
    return _rate_limit_exceeded_handler(request, exc)


# Handle BaseApplicationException
@app.exception_handler(BaseAPIException)
async def base_application_exception_handler(request: Request, exc: BaseAPIException) -> JSONResponse:
    """
    Handles exceptions of type BaseAPIException by logging the error details and returning a JSON response.

    Args:
        request (Request): The incoming HTTP request that triggered the exception.
        exc (BaseAPIException): The exception instance containing error details.

    Returns:
        JSONResponse: A response with the error ID, timestamp, and message, along with the appropriate HTTP status code.
    """
    _logger.log_error(
        message=f"[{exc.exception_id}] At [{exc.timestamp}]: {exc.details}")
    # Log the error with the logger
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_id": exc.exception_id,
            "timestamp": exc.timestamp.isoformat(),
            "message": exc.message,
        },
    )


# Handle ResponseValidationError
@app.exception_handler(ResponseValidationError)
async def response_validation_error_handler(request: Request, exc: ResponseValidationError) -> JSONResponse:
    """
    Handles response validation errors by logging the error details and returning a standardized JSON response.

    Args:
        request (Request): The incoming HTTP request that triggered the error.
        exc (ResponseValidationError): The exception instance containing validation error details.

    Returns:
        JSONResponse: A JSON response with HTTP 500 status, an error message, a unique error ID, and a timestamp.
    """
    exception_id = str(uuid4())
    _logger.log_error(
        message=f"[{exception_id}]: Response validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Invalid response data.",
                 "error_id": exception_id, "timestamp": datetime.now().isoformat()},
    )


@app.exception_handler(RequestValidationError)  # Handle RequestValidationError
async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles FastAPI RequestValidationError exceptions by logging the error with a unique ID and returning a structured JSON response.

    Args:
        request (Request): The incoming HTTP request that caused the validation error.
        exc (RequestValidationError): The exception instance containing validation error details.

    Returns:
        JSONResponse: A response with HTTP 422 status code, including an error message, error ID, and timestamp.

    The response content includes:
        - message: A description of the validation error and the field involved.
        - error_id: A unique identifier for the error instance.
        - timestamp: The time the error was handled.
    """
    exception_id = str(uuid4())
    _logger.log_error(
        message=f"[{exception_id}]: Request validation error: {exc.errors()}")
    exc_message: Optional[str] = exc.errors(
    )[0]["msg"] if exc.errors() else "Invalid request data"
    exc_field: Optional[str] = exc.errors()[0]["loc"][1] if exc.errors() and len(
        exc.errors()[0]["loc"]) > 1 else "Unknown field"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": f"Invalid request data: {exc_message} (field: {exc_field})",
                 "error_id": exception_id, "timestamp": datetime.now().isoformat()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles unexpected exceptions raised during request processing.

    This asynchronous exception handler logs the error with a unique identifier and returns a standardized JSON response containing:
        - A generic error message
        - A unique error ID for tracking
        - The timestamp of the error occurrence

    Args:
        request (Request): The incoming HTTP request that caused the exception.
        exc (Exception): The exception instance that was raised.

    Returns:
        JSONResponse: A response with HTTP 500 status code and error details in JSON format.
    """
    """Custom handler for generic exceptions."""
    exception_id = str(uuid4())
    _logger.log_error(message=f"[{exception_id}]: Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"Internal server error.",
                 "error_id": exception_id, "timestamp": datetime.now().isoformat()},
    )


# Add SlowAPI middleware for rate limiting
app.add_middleware(middleware_class=SlowAPIMiddleware)

# Register routers for different modules
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(comment_router, prefix="/api/v1", tags=["comments"])
app.include_router(blog_router, prefix="/api/v1", tags=["blogs"])
app.include_router(tag_router, prefix="/api/v1", tags=["tags"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(status_router, prefix="", tags=["status"])
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])
