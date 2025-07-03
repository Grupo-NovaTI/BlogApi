from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.enums import operations
from app.utils.errors.exceptions import IntegrityException, OperationException, UnknownException


def handle_repository_exception(
    model: str,
    operation: operations.Operations,
    db_session: Session,
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except IntegrityError as e:
                db_session.rollback()
                raise IntegrityException(
                    model=model,
                    operation=operation,
                    details=str(e)
                )
            except SQLAlchemyError as e:
                db_session.rollback()
                raise OperationException(
                    model=model,
                    operation=operation,
                    details=str(e)
                )
            except Exception as e:
                db_session.rollback()
                raise UnknownException(
                    model=model,
                    operation=operation,
                    details=str(e)
                )
        return wrapper
    return decorator
