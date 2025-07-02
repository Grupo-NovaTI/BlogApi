from typing import Optional


class NotFoundException(Exception):
    """NotFoundException is raised when a requested resource is not found.

    Args:
        Exception (str): The error message.
        model (str): The name of the model or resource that was not found.
        identifier (Optional[str | int]): The identifier of the resource that was not found.
    """
    def __init__(self, model: str, identifier: str | int, message: str = "Resource not found") -> None:
        super().__init__(message)
        self.message: str = message
        self.model: str = model.capitalize()
        self.identifier: str | int = identifier

class OperationException(Exception):
    """OperationException is raised when an operation on a resource fails.

    Args:
        Exception (str): The error message.
        model (str): The name of the model or resource on which the operation failed.
        operation (str): The name of the operation that failed.
    """
    def __init__(self, model :str, operation: str, message: str = "Operation failed") -> None:
        super().__init__(message)
        self.model : str = model
        self.operation: str = operation.lower()
        self.message: str = message

class AlreadyExistsException(Exception):
    """AlreadyExistsException is raised when a resource already exists.

    Args:
        Exception (str): The error message.
        model (str): The name of the model or resource that already exists.
        identifier (str): The identifier of the resource that already exists.
    """
    def __init__(self, model: str, identifier: str, message: str = "Resource already exists") -> None:
        super().__init__(message)
        self.model: str = model.capitalize()
        self.identifier: str = identifier
        self.message: str = message
    


class ValidationException(Exception):
    """ValidationException is raised when a validation error occurs.

    Args:
        Exception (str): The error message.
        model (str): The name of the model or resource that failed validation.
    """
    def __init__(self, model: str, identifier: str, message: str = "Validation error") -> None:
        super().__init__(message)
        self.message: str = message
        self.model: str = model.capitalize()
        self.identifier: str = identifier

class UnknownException(Exception):
    """UnknownException is raised when an unknown error occurs.

    Args:
        Exception (str): The error message.
        model (str): The name of the model or resource where the error occurred.
    """
    def __init__(self, model: str, message: str = "An unknown error occurred") -> None:
        super().__init__(message)
        self.message: str = message
        self.model: str = model.capitalize()