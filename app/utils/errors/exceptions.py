"""
Custom exception classes for API error handling.

This module defines a hierarchy of exception classes to provide consistent and structured error responses
across the application. Each exception includes a status code, a user-friendly message, and detailed information
for logging and debugging. These exceptions are intended to be raised in service, repository, or route layers
and handled by global exception handlers to return appropriate HTTP responses.
"""
from typing import Optional
from starlette import status
import uuid
from datetime import datetime
from app.utils.enums.operations import Operations


class BaseAPIException(Exception):
    """
    Base class for all custom API exceptions in the application.
    Ensures a consistent error response structure.

    Attributes:
        status_code (int): The HTTP status code to be returned.
        message (str): A user-friendly, static message for the API response.
        details (Any): Specific error details for logging. Not sent to the client.
        exception_id (str): A unique ID for this specific error instance for traceability.
        timestamp (datetime): The time when the exception was created.
    """
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "An internal server error occurred."

    def __init__(self, details: Optional[str] = None):
        """
        Initialize the BaseAPIException.

        Args:
            details (Optional[str]): Specific error details for logging. Defaults to a generic message.
        """
        self.details: str = details or "No specific details provided."
        self.exception_id: str = str(uuid.uuid4())
        self.timestamp: datetime = datetime.now()
        super().__init__(self.message)


class UnauthorizedException(BaseAPIException):
    """
    Raised for authentication failures (401). Invalid, expired, or missing credentials.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication credentials were not provided or are invalid."


class ForbiddenException(BaseAPIException):
    """
    Raised for authorization failures (403). User is authenticated but lacks permissions.
    """
    status_code = status.HTTP_403_FORBIDDEN
    message = "You do not have permission to perform this action."


class NotFoundException(BaseAPIException):
    """
    Raised when a specific resource is not found (404).

    Args:
        resource_type (str): The type of resource that was not found.
        identifier (str | int): The unique identifier of the resource.
    """
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, resource_type: str, identifier: str | int):
        """
        Initialize NotFoundException with resource type and identifier.
        """
        self.message = f"{resource_type.capitalize()} not found."
        details = f"Resource of type '{resource_type}' with identifier '{identifier}' could not be found."
        super().__init__(details=details)


class ConflictException(BaseAPIException):
    """
    Raised when an action cannot be completed due to a conflict with the current state of the resource (409).

    Args:
        resource_type (str): The type of resource that caused the conflict.
        identifier (str | int): The unique identifier of the resource.
        details (Optional[str]): Additional details about the conflict.
    """
    status_code = status.HTTP_409_CONFLICT
    message = "A conflict occurred with an existing resource."

    def __init__(self, resource_type: str, identifier: str | int, details: Optional[str] = None):
        """
        Initialize ConflictException with resource type, identifier, and optional details.
        """
        self.message = f"A conflict occurred with {resource_type.capitalize()}."
        self.details = f"Conflict for resource '{resource_type}' with identifier '{identifier}'. Details: {details}"
        super().__init__(details=self.details)


class UnprocessableContentException(BaseAPIException):
    """
    Raised for validation errors in user input (422). Often used for semantic errors in a payload.
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "The provided data is invalid or cannot be processed."


class DatabaseException(BaseAPIException):
    """
    Raised for generic database errors during an operation.

    Args:
        operation (Operations): The database operation being performed (e.g., CREATE, UPDATE).
        model (str): The name of the model involved in the operation.
        original_exception (Exception): The original exception that occurred.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "A database error occurred. Please try again later."

    def __init__(self, operation: Operations, model: str, original_exception: Exception):
        """
        Initialize DatabaseException with operation, model, and original exception.
        """
        details: str = f"Database operation '{operation.value}' failed on model '{model}'. Original error: {original_exception}"
        super().__init__(details=details)
        
class FileStorageException(BaseAPIException):
    """
    Raised for errors related to file storage operations (e.g., upload, download).

    Args:
        operation (Operations): The file storage operation being performed.
        details (str): Additional details about the error.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "An error occurred while processing the file storage operation."

    def __init__(self, details: str) -> None:
        """
        Initialize FileStorageException with operation and details.
        """
        super().__init__(details=f"File storage error: {details}")


class IntegrityConstraintException(DatabaseException):
    """
    Raised for database integrity violations (e.g., unique constraint).
    """
    message: str = "The resource could not be created due to a data conflict."
    status_code: int = status.HTTP_409_CONFLICT


class UnknownException(BaseAPIException):
    """
    Raised for unexpected errors that do not fit into other categories.

    Args:
        operation (Operations): The operation being performed when the error occurred.
        model (str): The name of the model involved in the operation.
        details (str): Additional details about the error.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "An unknown error occurred. Please try again later."

    def __init__(self, operation: Operations, model: str, details: str):
        """
        Initialize UnknownException with operation, model, and details.
        """
        super().__init__(
            details=f"Unknown error during {operation.value} on {model}: {details}")
