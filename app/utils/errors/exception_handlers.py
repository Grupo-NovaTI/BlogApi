# app/utils/errors/exception_handlers.py (Versión Refactorizada)

from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.enums.operations import Operations
from app.utils.errors.exceptions import (
    IntegrityException, OperationException, UnknownException, 
    NotFoundException, AlreadyExistsException, ForbiddenException, ValidationException, InvalidUserCredentialsException
)
# Asumiendo que tienes un logger configurado
# import logging
# logger = logging.getLogger(__name__)

# --- DECORADOR PARA OPERACIONES DE ESCRITURA ---
def handle_service_transaction(model: str, operation: Operations):
    """
    Decorator for WRITE operations (CUD). Manages the full transaction lifecycle
    (commit/rollback) and handles exceptions.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self._db_session.commit()
                return result
            except (NotFoundException, AlreadyExistsException, ForbiddenException, ValidationException) as e:
                self._db_session.rollback()
                raise e
            except IntegrityError as e:
                self._db_session.rollback()
                # logger.error(f"Integrity Error on {model} {operation}: {e.orig}")
                raise IntegrityException(
                    model=model,
                    operation=operation,
                    details=str(e)
                )
            except SQLAlchemyError as e:
                self._db_session.rollback()
                # logger.error(f"Database Error on {model} {operation}: {e}")
                raise OperationException(model=model, operation=operation, details=str(e))
            except Exception as e:
                self._db_session.rollback()
                # logger.error(f"Unknown Error on {model} {operation}: {e}", exc_info=True)
                raise UnknownException(model=model, operation=operation, details=str(e))
        return wrapper
    return decorator

# --- DECORADOR PARA OPERACIONES DE LECTURA ---
def handle_read_exceptions(model: str, operation: Operations):
    """
    Decorator for READ operations. Does NOT manage transactions.
    It catches unexpected errors during data fetching.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            # No se necesita rollback, no hay cambios pendientes
            except SQLAlchemyError as e:
                # logger.error(f"Database Read Error on {model} {operation}: {e}")
                raise OperationException(model=model, operation=operation, details=str(e))
            except InvalidUserCredentialsException as e:
                raise e
            except Exception as e:
                # logger.error(f"Unknown Read Error on {model} {operation}: {e}", exc_info=True)
                raise UnknownException(model=model, operation=operation, details=str(e))
            
        return wrapper
    return decorator