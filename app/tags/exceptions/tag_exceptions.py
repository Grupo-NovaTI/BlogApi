from typing import Optional
from app.utils.errors.exceptions import (
    NotFoundException,
    OperationException,
    AlreadyExistsException,
    ValidationException
)

_MODEL = "Tag"

class TagOperationException(OperationException):
    """Exception raised when a tag cannot be created or updated due to validation errors."""
    def __init__(self, operation: str, message: str = "Tag operation failed") -> None:
        super().__init__(message=message, model=_MODEL, operation=operation)
        self.message: str = message
        self.model: str = _MODEL
        self.operation: str = operation
    
class TagNotFoundException(NotFoundException):
    """Exception raised when a tag is not found in the system."""
    def __init__(self, identifier: str | int, message: str = "Tag not found") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)
        self.message: str = message
        self.model: str = _MODEL
        self.identifier: str | int = identifier

class TagAlreadyExistsException(AlreadyExistsException):
    """Exception raised when trying to create a tag that already exists."""
    def __init__(self, identifier: str, message: str = "Tag already exists") -> None:
        super().__init__(model=_MODEL, identifier=identifier, message=message)
        self.message: str = message
        self.model: str = _MODEL
        self.identifier: str = identifier

class TagInvalidException(ValidationException):
    """Exception raised when a tag is invalid or does not meet the required criteria."""
    def __init__(self, message: str = "Tag is invalid") -> None:
        super().__init__(model=_MODEL, message=message)
        self.message: str = message
        self.model: str = _MODEL
        
        