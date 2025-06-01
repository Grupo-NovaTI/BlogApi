class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the system."""
    pass


class UserAlreadyExistsException(Exception):
    """Exception raised when trying to create a user that already exists."""
    pass


class InvalidUserCredentialsException(Exception):
    """Exception raised when user credentials are invalid."""
    pass


class UserPermissionDeniedException(Exception):
    """Exception raised when a user does not have permission to perform an action."""
    pass
