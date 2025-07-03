from enum import Enum

class ExceptionTypes(Enum):
    """ExceptionTypes is an enumeration of the different types of exceptions that can occur in the application.
    
    Args:
        NOT_FOUND (str): Indicates that a requested resource was not found.
        ALREADY_EXISTS (str): Indicates that a resource already exists.
        VALIDATION_ERROR (str): Indicates that a validation error occurred.
        OPERATION_ERROR (str): Indicates that a database operation error occurred.
        UNKNOWN_ERROR (str): Indicates that an unknown error occurred.
        INTEGRITY_ERROR (str): Indicates that a database integrity error occurred.
        UNAUTHORIZED (str): Indicates that the user is not authorized to perform the operation.
        FORBIDDEN (str): Indicates that the user is forbidden from performing the operation.
        BAD_REQUEST (str): Indicates that the request was malformed or invalid.
        INTERNAL_SERVER_ERROR (str): Indicates that an internal server error occurred.
    """
    NOT_FOUND = "Not Found"
    ALREADY_EXISTS = "Already Exists"
    VALIDATION_ERROR = "Validation Error"
    OPERATION_ERROR = "Database Operation Error"
    UNKNOWN_ERROR = "Unknown Error"
    INTEGRITY_ERROR = "Integrity Error"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    BAD_REQUEST = "Bad Request"
    INTERNAL_SERVER_ERROR = "Internal Server Error"