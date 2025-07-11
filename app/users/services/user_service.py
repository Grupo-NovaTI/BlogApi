from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.users.models.user_model import UserModel
from app.users.repositories.user_repository import UserRepository
from app.utils.enums.operations import Operations
from app.utils.errors.exception_handlers import (handle_read_exceptions,
                                                 handle_service_transaction)
from app.utils.errors.exceptions import \
    ConflictException as UserAlreadyExistsException
from app.utils.errors.exceptions import \
    ForbiddenException as UserForbiddenException
from app.utils.errors.exceptions import \
    NotFoundException as UserNotFoundException

_MODEL_NAME = "Users"


class UserService:
    """UserService provides business logic for managing user entities in the application.
    This service acts as an intermediary between the user repository and higher-level
    application logic, handling user-related operations such as creation, retrieval,
    updating, and deletion. It also manages exception handling and transactional
    integrity for user operations.
    Attributes:
        _user_repository (UserRepository): The repository instance for user data access.
        _db_session (Session): The SQLAlchemy session for database transactions.
    Methods:
        get_all_users() -> List[UserModel]:
        create_user(user_data: dict[str, Any]) -> UserModel:
            Create a new user with the provided data.
        get_user_by_id(user_id: int) -> Optional[UserModel]:
            Retrieve a user by their unique ID.
        get_user_by_username(username: str) -> Optional[UserModel]:
        update_user(user_id: int, user_data: dict) -> UserModel:
            Update an existing user's information.
        delete_user_by_id(user_id: int) -> None:
            Delete a user by their unique ID.
        update_user_active_status(user_id: int, is_active: bool) -> UserModel:
        UserNotFoundException: If a user with the specified identifier does not exist.
        UserAlreadyExistsException: If attempting to create a user with an existing email or username."""

    def __init__(self, user_repository: UserRepository, db_session: Session) -> None:
        """
        Initialize the UserService.

        Args:
            user_repository (UserRepository): The repository for managing user data.
            db_session (Session): The SQLAlchemy session for database transactions.
        """
        self._user_repository: UserRepository = user_repository
        self._db_session: Session = db_session

    def _get_user_or_raise(self, user_id: int) -> UserModel:
        """
        Retrieve a user by ID or raise an exception if not found.

        Args:
            user_id (int): The unique identifier of the user to retrieve.

        Returns:
            UserModel: The user object if found.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        user: Optional[UserModel] = self._user_repository.get_user_by_id(
            user_id=user_id)
        if not user:
            raise UserNotFoundException(
                identifier=user_id, resource_type=_MODEL_NAME)
        return user

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH
    )
    def get_all_users(self) -> List[UserModel]:
        """
        Retrieve all users from the repository.

        Returns:
            List[UserModel]: A list of all users.
        """
        return self._user_repository.get_all_users()

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.CREATE
    )
    def create_user(self, user_data: dict[str, Any]) -> UserModel:
        """
        Create a new user in the repository.

        Args:
            user_data (dict[str, Any]): The data for the new user.

        Returns:
            UserModel: The created user object.

        Raises:
            UserAlreadyExistsException: If a user with the same email or username already exists.
        """
        user_model = UserModel(**user_data)
        existing_user: Optional[UserModel] = self._user_repository.get_user_by_email_or_username(
            email=str(user_model.email), username=str(user_model.username))
        if existing_user:
            raise UserAlreadyExistsException(
                identifier="email or username",
                resource_type=_MODEL_NAME,
                details="A user with this email or username already exists."
            )
        return self._user_repository.create_user(user=user_model)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The unique identifier of the user to retrieve.

        Returns:
            Optional[UserModel]: The user object if found, otherwise None.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        return self._user_repository.get_user_by_id(
            user_id=user_id)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[UserModel]: The user object if found, otherwise None.

        Raises:
            UserNotFoundException: If the user with the given username does not exist.
        """
        return self._user_repository.get_user_by_username(
            username=username)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_user(self, user_id: int, user_data: dict) -> UserModel:
        """
        Update an existing user in the repository.

        Args:
            user_id (int): The unique identifier of the user to update.
            user_data (dict): The data for updating the user.

        Returns:
            UserModel: The updated user object.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """

        user_to_update: UserModel = self._get_user_or_raise(user_id=user_id)
        updated_user: UserModel = self._user_repository.update_user(
            user=user_to_update, user_data=user_data)
        return updated_user

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_user_by_id(self, user_id: int) -> None:
        """
        Delete a user by their ID from the repository.

        Args:
            user_id (int): The unique identifier of the user to delete.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """

        user_to_delete: UserModel = self._get_user_or_raise(user_id=user_id)
        self._user_repository.delete_user(user=user_to_delete)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_user_active_status(self, user_id: int, is_active: bool) -> UserModel:
        """
        Update the active status of a user.

        Args:
            user_id (int): The unique identifier of the user.
            is_active (bool): The new active status of the user.

        Returns:
            UserModel: The updated user object.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        user_to_update = self._get_user_or_raise(user_id=user_id)
        updated_user: Optional[UserModel] = self._user_repository.update_user(
            user=user_to_update, user_data={"is_active": is_active})
        return updated_user
