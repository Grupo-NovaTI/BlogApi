class BlogOperationException(Exception):
    """Custom exception for blog operations."""
    pass

class BlogNotFoundException(BlogOperationException):
    """Exception raised when a blog is not found."""
    pass

class BlogAlreadyExistsException(BlogOperationException):
    """Exception raised when a blog already exists."""
    pass