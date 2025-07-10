from typing import Any, List, Optional
from sqlalchemy.orm import Session
from app.users.repositories.user_repository import UserRepository
from app.utils.errors.exceptions import NotFoundException as UserNotFoundException, AlreadyExistsException as UserAlreadyExistsException
from app.users.models.user_model import UserModel
from app.utils.errors.exception_handlers import handle_read_exceptions, handle_service_transaction
from app.utils.enums.operations import Operations
_MODEL_NAME = "Users"


class UserService:
    def __init__(self, user_repository: UserRepository, db_session: Session) -> None:
        self._user_repository: UserRepository = user_repository
        self._db_session: Session = db_session

    def get_all_users(self) -> List[UserModel]:
        """
        Retrieve all users from the repository.

        Returns:
            List of users.
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
            user_data: Data for the new user.

        Returns:
            The created user.
        """
        user_model = UserModel(**user_data)
        check_user_exists: Optional[UserModel] = self._user_repository.get_user_by_email_or_username(
            email=str(user_model.email), username=str(user_model.username))
        if check_user_exists:
            raise UserAlreadyExistsException(
                identifier="email or username",
                model=_MODEL_NAME
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
            UserModel: The user object if found.

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
            UserModel: The user object if found.

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
            user_data: Data for updating the user.

        Returns:
            The updated user.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        user_updated_result:  Optional[UserModel] = self._user_repository.update_user(
            user_id=user_id, user_data=user_data)
        if not user_updated_result:
            raise UserNotFoundException(
                identifier=user_id,
                model=_MODEL_NAME
            )

        return user_updated_result

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by their ID from the repository.

        Args:
            user_id (int): The unique identifier of the user to delete.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        deletion_result: bool = self._user_repository.delete_user(
            user_id=user_id)
        if not deletion_result:
            raise UserNotFoundException(
                identifier=user_id,
                model=_MODEL_NAME
            )

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
        updated_user: Optional[UserModel] = self._user_repository.update_user_active_status(
            user_id=user_id, is_active=is_active)
        if not updated_user:
            raise UserNotFoundException(
                identifier=user_id,
                model=_MODEL_NAME
            )
        return updated_user
