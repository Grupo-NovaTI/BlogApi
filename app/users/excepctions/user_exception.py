class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the system."""
    pass


class UserAlreadyExistsException(Exception):
    """Exception raised when trying to create a user that already exists."""
    pass


class UserOperationException(Exception):
    """Exception raised when a user cannot be created due to validation errors."""
    pass