from typing import Optional
from app.utils.errors.exceptions import (
    NotFoundException,
    OperationException,
    AlreadyExistsException,
    ValidationException
)

_MODEL = "Comment"
class CommentOperationException(OperationException):
    """Exception raised when a Comment cannot be created or updated due to validation errors."""
    def __init__(self, message: str, operation: str) -> None:
        super().__init__(model=_MODEL, message=message, operation=operation)
        self.operation: str = operation
        self.message: str = message
        self.model: str = _MODEL
class CommentNotFoundException(NotFoundException):
    """Exception raised when a Comment is not found in the system."""
    def __init__(self, identifier: str | int, message: str = "Comment not found") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)

class CommentAlreadyExistsException(AlreadyExistsException):
    """Exception raised when trying to create a Comment that already exists."""
    def __init__(self, identifier: str, message: str = "Comment already exists") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)

class CommentInvalidException(ValidationException):
    """Exception raised when a Comment is invalid or does not meet the required criteria."""
    def __init__(self, message: str) -> None:
        super().__init__(model=_MODEL, message=message)
