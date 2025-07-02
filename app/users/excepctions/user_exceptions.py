from typing import Optional
from app.utils.errors.exceptions import (
    NotFoundException,
    OperationException,
    AlreadyExistsException,
    ValidationException
)
_MODEL = "User"

class UserNotFoundException(NotFoundException):
    """Exception raised when a user is not found in the system."""
    def __init__(self, identifier: str | int, message: str = "User not found") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)
        self.message: str = message
        self.model: str = _MODEL
        self.identifier: str | int = identifier


class UserAlreadyExistsException(AlreadyExistsException):
    """Exception raised when trying to create a user that already exists."""
    def __init__(self, identifier: str, message: str = "User already exists") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)
        self.message: str = message
        self.model: str = _MODEL
        self.identifier: str = identifier


class UserOperationException(OperationException):
    """Exception raised when a user cannot be created due to validation errors."""
    def __init__(self, message: str, operation: str) -> None:
        super().__init__(model=_MODEL, message=message, operation=operation)
        self.operation: str = operation
        self.message: str = message
        self.model: str = _MODEL

class UserInvalidException(ValidationException):
    """Exception raised when a user is invalid or does not meet the required criteria."""
    def __init__(self, message: str) -> None:
        super().__init__(model=_MODEL, message=message)
        self.message: str = message
        self.model: str = _MODEL
