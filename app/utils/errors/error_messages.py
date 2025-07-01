from typing import Optional


def database_error_message(operation: str, instance: str, exception: Optional[Exception] = None) -> str:
    """database_error_message 
Generates a standardized error message for database operations.

    Args:
        operation (str): The database operation being performed (e.g., "creating", "retrieving").
        instance (str): The specific instance being operated on (e.g., "tag", "user").
        exception (Optional[Exception], optional): The exception raised during the operation, if any. Defaults to None.

    Returns:
        str: A standardized error message.
    """
    if exception:
        return f"Database error on {operation} {instance}: {str(exception)}"
    return f"Database error on {operation} {instance}"

def not_found_message(instance: str, identifier: str | int) -> str:
    """not_found_message 
Generates a standardized not found error message for database operations.

    Args:
        instance (str): The specific instance being searched for (e.g., "tag", "user").
        identifier (str): The unique identifier of the instance (e.g., ID or name).

    Returns:
        str: A standardized not found error message.
    """
    return f"{instance.capitalize()} with identifier '{identifier}' not found." 

def unknown_error_message(operation: str, instance: str, exception: Optional[Exception] = None) -> str:
    """unknown_error_message 
Generates a standardized unknown error message for database operations.

    Args:
        operation (str): The database operation being performed (e.g., "creating", "retrieving").
        instance (str): The specific instance being operated on (e.g., "tag", "user").
        exception (Optional[Exception], optional): The exception raised during the operation, if any. Defaults to None.

    Returns:
        str: A standardized unknown error message.
    """
    if exception:
        return f"Unknown error on {operation} {instance}: {str(exception)}"
    return f"Unknown error on {operation} {instance}"

def validation_error_message(field: str, message: str) -> str:
    """validation_error_message"""
    """Generates a standardized validation error message.

    Args:
        field (str): The field that failed validation.
        message (str): The validation error message.

    Returns:
        str: A standardized validation error message.
    """
    return f"Validation error on field '{field}': {message}"

def already_exists_message(instance: str, identifier: str | int) -> str:
    """already_exists_message"""
    return f"{instance.capitalize()} with identifier '{identifier}' already exists."