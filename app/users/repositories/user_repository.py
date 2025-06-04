from typing import List
from users.models.user_model import UserModel as User
from users.excepctions.user_exception import UserOperationException
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db_session : Session) -> None:
        self._db_session:Session = db_session

    def get_user_by_id(self, user_id: int) -> User | None:
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
        except Exception as e:
            raise UserOperationException(
                f"Error on retrieving user by ID: {str(e)}"
            )

    def get_user_by_username(self, username: str) -> User | None:
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
        except Exception as e:
            raise UserOperationException(
                f"Error on retrieving user by username: {str(e)}"
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
        except Exception as e:
            self._db_session.rollback()
            raise UserOperationException(
                f"User cannot be created due to: {str(e)}")

    def update_user(self, user: User) -> User:
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
            self._db_session.add(user)
            self._db_session.commit()
            return user
        except Exception as e:
            self._db_session.rollback()
            raise UserOperationException(
                f"User cannot be updated due to: {str(e)}")

    def delete_user(self, user: User) -> User:
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
            self._db_session.delete(user)
            self._db_session.commit()
            return user
        except Exception as e:
            self._db_session.rollback()
            raise UserOperationException(
                f"User cannot be deleted due to: {str(e)}"
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
        except Exception as e:
            raise UserOperationException(
                f"Error on retrieving all users: {str(e)}"
            )

    def get_user_by_email(self, email: str) -> User | None:
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
        except Exception as e:
            raise UserOperationException(
                f"Error on retrieving user by email: {str(e)}"
            )
