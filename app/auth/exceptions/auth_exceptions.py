class InvalidUserCredentialsException(Exception):
    """Exception raised when user credentials are invalid."""
    def __init__(self, message: str = "Invalid user credentials") -> None:
        super().__init__(message)
        self.message = message


class UserPermissionDeniedException(Exception):
    """Exception raised when a user does not have permission to perform an action."""
    def __init__(self, message: str = "User permission denied") -> None:
        super().__init__(message)
        self.message = message

class OperationNotAllowedException(Exception):
    """Exception raised when an operation is not allowed."""
    def __init__(self, message: str = "Operation not allowed") -> None:
        super().__init__(message)
        self.message = message

class OperationFailedException(Exception):
    """Exception raised when an operation fails."""
    def __init__(self, message: str = "Operation failed") -> None:
        super().__init__(message)
        self.message = message