class BlogOperationException(Exception):
    """
    Exception raised for errors that occur during blog operations.

    This custom exception can be used to signal issues specific to blog-related actions,
    such as creation, update, or deletion failures.

    Attributes:
        message (str): Optional error message describing the exception.
    """
    pass

class BlogNotFoundException(BlogOperationException):
    """Exception raised when a blog is not found."""
    pass

class BlogAlreadyExistsException(BlogOperationException):
    """Exception raised when a blog already exists."""
    pass