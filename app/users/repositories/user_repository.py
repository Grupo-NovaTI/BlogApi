from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.users.models.user_model import UserModel as User
from app.users.excepctions.user_exceptions import UserOperationException
from app.utils.errors.error_messages import database_error_message, unknown_error_message, integrity_error_message
from app.utils.logger.application_logger import ApplicationLogger

_logger = ApplicationLogger(__name__)


class UserRepository:
    def __init__(self, db_session : Session) -> None:
        self._db_session:Session = db_session

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID from the database.

        Args:
            user_id (int): The unique identifier of the user to retrieve.

        Returns:
            User: The user object if found.

        Raises:
            UserOperationException: If there is a database error during retrieval.
        """
        try:
            return self._db_session.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            _logger.log_error(database_error_message(
                operation="retrieving", instance="user", exception=e))
            raise UserOperationException(
                database_error_message(operation="retrieving", instance="user", exception=e)
            )
        except Exception as e:
            _logger.log_error(unknown_error_message(
                operation="retrieving", instance="user", exception=e))
            raise UserOperationException(
                unknown_error_message(operation="retrieving", instance="user", exception=e)
            )

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username from the database.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object if found.

        Raises:
            UserOperationException: If there is a database error during retrieval.
        """
        try:
            return self._db_session.query(User).filter(User.username == username).first()
        except SQLAlchemyError as e:
            _logger.log_error(database_error_message(
                operation="retrieving", instance="user by username", exception=e))
            raise UserOperationException(database_error_message(
                operation="retrieving", instance="user by username", exception=e))
        except Exception as e:
            _logger.log_error(unknown_error_message(
                operation="retrieving", instance="user by username", exception=e))
            raise UserOperationException(
                unknown_error_message(operation="retrieving", instance="user by username", exception=e)
            )

    def create_user(self, user: User) -> User:
        """
        Create a new user in the database.

        Args:
            user (User): The user object containing the user details to be created.

        Returns:
            User: The created user object with updated database information.

        Raises:
            UserOperationException: If there is a database error during creation,
                                  such as duplicate username or email.
        """
        try:
            self._db_session.add(user)
            self._db_session.commit()
            self._db_session.refresh(user)
            return user
        except IntegrityError as e:
            self._db_session.rollback()
            _logger.log_error(integrity_error_message(
                operation="creating", instance="user", exception=e))
            raise UserOperationException(
                integrity_error_message(
                    operation="creating", instance="user", exception=e
                )
            )
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(database_error_message(
                operation="creating", instance="user", exception=e))
            raise UserOperationException(
                database_error_message(operation="creating", instance="user", exception=e))    
        except Exception as e:
            _logger.log_error(unknown_error_message(
                operation="creating", instance="user", exception=e))
            self._db_session.rollback()
            raise UserOperationException(
                unknown_error_message(
                    operation="creating", instance="user", exception=e))

    def update_user(self, user_data: dict, user_id : int) -> Optional[User]:
        """
        Update an existing user's information in the database.

        Args:
            user (User): The user object containing the updated information.

        Returns:
            User: The updated user object.

        Raises:
            UserOperationException: If there is a database error during update,
                                  such as user not found or duplicate unique fields.
        """
        try:
            rows_affected :int = self._db_session.query(User).filter(User.id == user_id).update(user_data)
            if rows_affected == 0:
                return None
            self._db_session.commit()
            return self.get_user_by_id(user_id=user_id)
        except IntegrityError as e:
            self._db_session.rollback()
            _logger.log_error(integrity_error_message(
                operation="updating", instance="user", exception=e))
            raise UserOperationException(
                integrity_error_message(
                    operation="updating", instance="user", exception=e)
            )
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(database_error_message(
                operation="updating", instance="user", exception=e))
            raise UserOperationException(
                database_error_message(operation="updating", instance="user", exception=e)
            )
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(unknown_error_message(
                operation="updating", instance="user", exception=e))
            raise UserOperationException(
                unknown_error_message(
                    operation="updating", instance="user", exception=e))

    def delete_user(self, user_id : int) -> bool:
        """
        Delete a user from the database.

        Args:
            user (User): The user object to be deleted.

        Returns:
            User: The deleted user object.

        Raises:
            UserOperationException: If there is a database error during deletion,
                                  such as user not found or constraint violations.
        """
        try:
            user : Optional[User] = self.get_user_by_id(user_id=user_id)
            if not user:
                return False
            self._db_session.delete(user)
            self._db_session.commit()
            return True
        except IntegrityError as e:
            self._db_session.rollback()
            _logger.log_error(integrity_error_message(
                operation="deleting", instance="user", exception=e))
            raise UserOperationException(
                integrity_error_message(
                    operation="deleting", instance="user", exception=e
                )
            )
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(database_error_message(
                operation="deleting", instance="user", exception=e))
            raise UserOperationException(
                database_error_message(operation="deleting", instance="user", exception=e)
            )
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(unknown_error_message(
                operation="deleting", instance="user", exception=e))
            raise UserOperationException(
                unknown_error_message(
                    operation="deleting", instance="user", exception=e
                )
            )

    def get_all_users(self, offset: int=0 , limit: int=10) -> List[User]:
        """
        Retrieve all users from the database.
        Args:
            offset (int): The number of records to skip before starting to return results. [DEFAULT: 0]
            limit (int): The maximum number of records to return. [DEFAULT: 10]

        Returns:
            list[User]: A list containing all user objects in the database.

        Raises:
            UserOperationException: If there is a database error while retrieving users.
        """
        try:
            return self._db_session.query(User).offset(offset=offset).limit(limit=limit).all()
        except SQLAlchemyError as e:
            _logger.log_error(database_error_message(
                operation="retrieving", instance="all users", exception=e))
            raise UserOperationException(database_error_message(
                operation="retrieving", instance="all users", exception=e))
        except Exception as e:
            raise UserOperationException(
                unknown_error_message(
                    operation="retrieving", instance="all users", exception=e
                )
            )

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email from the database.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User: The user object if found.

        Raises:
            UserOperationException: If there is a database error during retrieval.
        """
        try:
            return self._db_session.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            _logger.log_error(database_error_message(
                operation="retrieving", instance="user by email", exception=e))
            raise UserOperationException(database_error_message(
                operation="retrieving", instance="user by email", exception=e))
        except Exception as e:
            _logger.log_error(unknown_error_message(
                operation="retrieving", instance="user by email", exception=e))
            raise UserOperationException(
                unknown_error_message(operation="retrieving", instance="user by email", exception=e)
            )

    def update_user_active_status(self, user_id: int, is_active: bool) -> Optional[User]:
        """
        Update the active status of a user in the database.

        Args:
            user_id (int): The unique identifier of the user to update.
            is_active (bool): The new active status of the user.

        Returns:
            User: The updated user object.

        Raises:
            UserOperationException: If there is a database error during update.
        """
        try:
            rows_affected :int = self._db_session.query(User).filter(User.id == user_id).update({"is_active": is_active})
            if rows_affected == 0:
                return None
            self._db_session.commit()
            return self.get_user_by_id(user_id=user_id)
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(database_error_message(
                operation="updating active status", instance="user", exception=e))
            raise UserOperationException(
                database_error_message(operation="updating active status", instance="user", exception=e)
            )
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(unknown_error_message(
                operation="updating active status", instance="user", exception=e))
            raise UserOperationException(
                unknown_error_message(operation="updating active status", instance="user", exception=e)
            )