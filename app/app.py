from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError, RequestValidationError, HTTPException
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
from app.core.config.application_config import ApplicationConfig
from app.utils.logger.application_logger import ApplicationLogger
from app.core.dependencies.dependencies import provide_application_config
from app.core.middlewares import rate_limiter, clear_redis_cache, init_redis_cache
from app.status.status_routes import app as status_router
from app.admin.routes.admin_routes import admin_router
from app.auth.exceptions.auth_exceptions import (
    InvalidUserCredentialsException,
    OperationFailedException,
    OperationNotAllowedException,
    UserPermissionDeniedException

)
from app.utils.errors.exceptions import (
    NotFoundException,
    OperationException,
    AlreadyExistsException,
    ValidationException
)

_logger: ApplicationLogger = ApplicationLogger(
    name=__name__, log_to_console=False)
# Gets the application global configuration
application_config: ApplicationConfig = provide_application_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to initialize Redis and FastAPI Cache."""

    _logger.log_info(
        message=f"Starting application: {app.title} v{app.version} in {'debug' if app.debug else 'production'} mode.")
    init_db()
    # Initialize Redis connection
    redis_initialized = await init_redis_cache()
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
    title=application_config.app_name,
    version=application_config.app_version,
    debug=application_config.debug,
)

# Rate Limiting Configuration
app.state.limiter = rate_limiter  # Set the rate limiter from the config


# Handle rate limit exceeded exceptions

@app.exception_handler(InvalidUserCredentialsException)
async def invalid_user_credentials_exception_handler(request: Request, exc: InvalidUserCredentialsException):
    """Custom handler for invalid user credentials exceptions."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message},
    )


@app.exception_handler(OperationFailedException)
async def operation_failed_exception_handler(request: Request, exc: OperationFailedException):
    """Custom handler for operation failed exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": exc.message},
    )


@app.exception_handler(OperationNotAllowedException)
async def operation_not_allowed_exception_handler(request: Request, exc: OperationNotAllowedException):
    """Custom handler for operation not allowed exceptions."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": exc.message},
    )


@app.exception_handler(UserPermissionDeniedException)
async def user_permission_denied_exception_handler(request: Request, exc: UserPermissionDeniedException):
    """Custom handler for user permission denied exceptions."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": exc.message},
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded exceptions."""
    return _rate_limit_exceeded_handler(request, exc)


@app.exception_handler(NotFoundException)  # Handle NotFoundException
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """Custom handler for NotFoundException."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"{exc.model} with identifier '{exc.identifier}' not found."},
    )


@app.exception_handler(OperationException)  # Handle OperationException
async def operation_exception_handler(request: Request, exc: OperationException):
    """Custom handler for OperationException."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"{exc.model} {exc.operation} failed: {exc.message}"},
    )


@app.exception_handler(AlreadyExistsException)  # Handle AlreadyExistsException
async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
    """Custom handler for AlreadyExistsException."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": f"{exc.model} with identifier '{exc.identifier}' already exists."},
    )


@app.exception_handler(ValidationException)  # Handle ValidationException
async def validation_exception_handler(request: Request, exc: ValidationException) -> JSONResponse:
    """Custom handler for ValidationException."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": f"{exc.model} Validation error: {exc.message}" },
    )

# Handle ResponseValidationError


@app.exception_handler(ResponseValidationError)
async def response_validation_error_handler(request: Request, exc: ResponseValidationError) -> JSONResponse:
    """Custom handler for ResponseValidationError."""
    _logger.log_error(message=f"Response validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Invalid response data. "},
    )


@app.exception_handler(RequestValidationError)  # Handle RequestValidationError
async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Custom handler for RequestValidationError."""
    _logger.log_error(message=f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Invalid request data."},
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
