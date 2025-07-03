from typing import Optional
import uuid
from datetime import datetime
from app.utils.enums.operations import Operations
from app.utils.enums.exception_types import ExceptionTypes


class BaseApplicationException(Exception):
    """BaseApplicationException is the base class for all application-specific exceptions.

    Args:
        model (str): The name of the model or resource where the error occurred.
        operation (Operations): The operation that failed.
        type (ExceptionType): The type of exception (e.g., "not_found", "already_exists").
        details (Optional[str]): Additional details about the exception.
        message (str): The error message to be displayed.
        id (str): A unique identifier for the exception instance.
        timestamp (datetime): The timestamp when the exception was created.
    """

    def __init__(self, model: str, operation: Operations, type: ExceptionTypes, details: Optional[str] = None) -> None:
        self.model: str = model.capitalize()
        self.id: str = str(object=uuid.uuid4())
        self.timestamp: datetime = datetime.now()
        self.operation: str = operation.value
        self.type: str = type.value
        self.details: str = details or "No additional details provided"
        self.message: str = f"{self.type} exception in {self.model} during {self.operation}"
        super().__init__(self.message)


class OperationException(BaseApplicationException):
    """OperationException is raised when an operation fails."""
    def __init__(self, model: str, operation: Operations, details: Optional[str] = None) -> None:
        super().__init__(model=model, operation=operation, type=ExceptionTypes.OPERATION_ERROR, details=details)


class UnknownException(BaseApplicationException):
    """UnknownException is raised when an unknown error occurs.
    """
    def __init__(self, model: str, operation: Operations, details: Optional[str] = None) -> None:
        super().__init__(model=model, operation=operation, type=ExceptionTypes.UNKNOWN_ERROR, details=details)


class IntegrityException(BaseApplicationException):
    """IntegrityErrorException is raised when a database integrity error occurs."""
    def __init__(self, model: str, operation: Operations, details: Optional[str] = None) -> None:
        super().__init__(model=model, operation=operation, type=ExceptionTypes.INTEGRITY_ERROR, details=details)


class BaseAuthenticationException(Exception):
    """BaseAuthenticationException is the base class for all authentication-specific exceptions.

    Args:
        Exception (str): The error message.
    """

    def __init__(self, message: str) -> None:
        self.id: str = str(object=uuid.uuid4())
        self.type : str = ExceptionTypes.UNAUTHORIZED.value
        self.timestamp: datetime = datetime.now()
        self.message: str = message
        super().__init__(self.message)

class InvalidUserCredentialsException(BaseAuthenticationException):
    """InvalidUserCredentialsException is raised when user credentials are invalid.
    
    Args:
        message (str): The error message.
    """
    
    pass

class UserPermissionDeniedException(BaseAuthenticationException):
    """UserPermissionDeniedException is raised when a user does not have permission to perform an action.
    Args:
        message (str): The error message."""
    pass


class BaseIdentifierException(Exception):
    """BaseIdentifierException is the base class for all identifier-specific exceptions.

    Args:
        Exception (str): The error message.
        model (str): The name of the model or resource where the identifier error occurred.
        operation (str): The name of the operation that failed.
        type (str): The type of exception (e.g., "not_found", "already_exists").
        details (Optional[str]): Additional details about the exception.
        identifier (str | int): The identifier of the resource that caused the exception.


    """

    def __init__(self, model: str, type : ExceptionTypes, identifier: str | int, details: Optional[str] = None) -> None:
        self.model: str = model.capitalize()
        self.id: str = str(object=uuid.uuid4())
        self.timestamp: datetime = datetime.now()
        self.identifier: str | int = identifier
        self.exception_type: str = type.value
        self.details: str = details or "No additional details provided"
        self.message: str = f"{self.model} with identifier {self.identifier} {self.exception_type}"
        super().__init__(self.message)


class NotFoundException(BaseIdentifierException):
    """NotFoundException is raised when a requested resource is not found."""
    def __init__(self, model: str, identifier: str | int, details: Optional[str] = None) -> None:
        super().__init__(model=model, type=ExceptionTypes.NOT_FOUND, identifier=identifier, details=details)


class AlreadyExistsException(BaseIdentifierException):
    """AlreadyExistsException is raised when a resource already exists."""
    def __init__(self, model: str, identifier: str | int, details: Optional[str] = None) -> None:
        super().__init__(model=model, type=ExceptionTypes.ALREADY_EXISTS, identifier=identifier, details=details)


class ValidationException(BaseIdentifierException):
    """ValidationException is raised when a validation error occurs."""
    def __init__(self, model: str, identifier: str | int, details: Optional[str] = None) -> None:
        super().__init__(model=model, type=ExceptionTypes.VALIDATION_ERROR, identifier=identifier, details=details)
