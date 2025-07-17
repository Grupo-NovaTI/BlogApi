"""
Exception handler decorators for service and repository layers.

This module provides decorators for handling exceptions and managing transactions in service methods.
It ensures consistent error handling and rollback/commit logic for both write and read operations.
"""

from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.enums.operations import Operations
from app.utils.errors.exceptions import (
    NotFoundException,
    IntegrityConstraintException,
    ConflictException,
    DatabaseException,
    ForbiddenException,
    UnknownException,
    UnauthorizedException,
)


def handle_service_transaction(model: str, operation: Operations):
    """
    Decorator for service methods that perform WRITE operations (Create, Update, Delete).
    Manages the full transaction lifecycle (commit/rollback) and handles exceptions.

    Args:
        model (str): The name of the model being operated on.
        operation (Operations): The type of operation being performed.

    Returns:
        Callable: The decorated function with transaction and error handling.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self._db_session.commit()
                return result
            except (NotFoundException, ConflictException, ForbiddenException, IntegrityConstraintException) as e:
                self._db_session.rollback()
                raise e
            except IntegrityError as e:
                self._db_session.rollback()
                raise IntegrityConstraintException(
                    model=model,
                    operation=operation,
                    original_exception=e,
                )
            except SQLAlchemyError as e:
                self._db_session.rollback()
                raise DatabaseException(model=model, operation=operation, original_exception=e)
            except Exception as e:
                self._db_session.rollback()
                raise UnknownException(model=model, operation=operation, details=str(e))
        return wrapper
    return decorator


def handle_read_exceptions(model: str, operation: Operations):
    """
    Decorator for service methods that perform READ operations.
    Does NOT manage transactions, but catches and wraps unexpected errors during data fetching.

    Args:
        model (str): The name of the model being operated on.
        operation (Operations): The type of operation being performed.

    Returns:
        Callable: The decorated function with error handling for read operations.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except SQLAlchemyError as e:
                raise DatabaseException(model=model, operation=operation, original_exception=e)
            except (UnauthorizedException, ForbiddenException, NotFoundException) as e:
                raise e
            except Exception as e:
                raise UnknownException(model=model, operation=operation, details=str(e))
        return wrapper
    return decorator