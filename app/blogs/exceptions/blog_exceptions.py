from typing import Optional
from app.utils.errors.exceptions import (
    NotFoundException,
    OperationException,
    AlreadyExistsException,
    ValidationException
)

_MODEL = "Blog"

class BlogOperationException(OperationException):
    """
    Exception raised for errors that occur during blog operations.

    This custom exception can be used to signal issues specific to blog-related actions,
    such as creation, update, or deletion failures.

    Attributes:
        message (str): Optional error message describing the exception.
    """
    def __init__(self, message: str, operation: str) -> None:
        super().__init__(model=_MODEL, message=message, operation=operation)
        self.operation: str = operation
        self.message: str = message
        self.model: str = _MODEL

class BlogNotFoundException(NotFoundException):
    """Exception raised when a blog is not found."""
    def __init__(self, identifier: str | int, message: str = "Blog not found") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)

class BlogAlreadyExistsException(AlreadyExistsException):
    """Exception raised when a blog already exists."""
    def __init__(self, identifier: str , message: str = "Blog already exists") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)

class BlogInvalidException(ValidationException):
    """Exception raised when a blog is invalid or does not meet the required criteria."""
    def __init__(self, message: str) -> None:
        super().__init__(model=_MODEL, message=message)
        self.message: str = message
        self.model: str = _MODEL