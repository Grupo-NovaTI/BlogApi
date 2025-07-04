from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.enums import operations
from app.utils.errors.exceptions import IntegrityException, OperationException, UnknownException


def handle_repository_exception(
    model: str,
    operation: operations.Operations,
):
    """handle_repository_exception Handle Repository exceptions

    Args:
        model (str): _description_
        operation (operations.Operations): _description_
    """
    def decorator(func):
        def wrapper(self,*args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except IntegrityError as e:
                self._db_session.rollback()
                raise IntegrityException(
                    model=model,
                    operation=operation,
                    details=str(e._message())
                )
            except SQLAlchemyError as e:
                self.db_session.rollback()
                raise OperationException(
                    model=model,
                    operation=operation,
                    details=str(e)
                )
            except Exception as e:
                self._db_session.rollback()
                raise UnknownException(
                    model=model,
                    operation=operation,
                    details=str(e)
                )
        return wrapper
    return decorator
