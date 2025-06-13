class TagOperationException(Exception):
    """Exception raised when a tag cannot be created or updated due to validation errors."""
    pass

class TagNotFoundException(Exception):
    """Exception raised when a tag is not found in the system."""
    pass

class TagAlreadyExistsException(Exception):
    """Exception raised when trying to create a tag that already exists."""
    pass

