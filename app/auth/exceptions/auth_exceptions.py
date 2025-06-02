class InvalidUserCredentialsException(Exception):
    """Exception raised when user credentials are invalid."""
    pass


class UserPermissionDeniedException(Exception):
    """Exception raised when a user does not have permission to perform an action."""
    pass

class OperationNotAllowedException(Exception):
    """Exception raised when an operation is not allowed."""
    pass

class OperationFailedException(Exception):
    """Exception raised when an operation fails."""
    pass