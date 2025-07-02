from typing import List, Optional
from app.users.repositories.user_repository import UserRepository
from app.users.excepctions.user_exceptions import UserNotFoundException, UserAlreadyExistsException
from app.utils.errors.error_messages import not_found_message, already_exists_message
from app.users.models.user_model import UserModel


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository: UserRepository = user_repository

    def get_all_users(self) -> List[UserModel]:
        """
        Retrieve all users from the repository.

        Returns:
            List of users.
        """
        return self._user_repository.get_all_users()

    def create_user(self, user_data: UserModel) -> UserModel:
        """
        Create a new user in the repository.

        Args:
            user_data: Data for the new user.

        Returns:
            The created user.
        """

        check_user_exists: Optional[UserModel] = self._user_repository.get_user_by_username(
            username=str(user_data.username))
        if check_user_exists:
            raise UserAlreadyExistsException(
                identifier=str(user_data.username),
                message=already_exists_message(
                    instance="user",
                    identifier=str(user_data.username)))
        check_user_exists = self._user_repository.get_user_by_email(
            email=str(user_data.email))
        if check_user_exists:
            raise UserAlreadyExistsException(
                identifier=str(user_data.email),
                message=already_exists_message(
                    instance="user",
                    identifier=str(user_data.email)))
        return self._user_repository.create_user(user=user_data)

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
        user_updated_result :  Optional[UserModel]= self._user_repository.update_user(user_id=user_id, user_data=user_data)
        if not user_updated_result:
            raise UserNotFoundException(
                identifier=user_id,
                message=not_found_message(
                    instance="user",
                    identifier=user_id
                )
            )
        return user_updated_result
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by their ID from the repository.

        Args:
            user_id (int): The unique identifier of the user to delete.

        Returns:
            bool: True if the user was deleted, False otherwise.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        deletion_result: bool = self._user_repository.delete_user(user_id=user_id)
        if not deletion_result:
            raise UserNotFoundException(
                identifier=user_id,
                message=not_found_message(
                    instance="user",
                    identifier=user_id
                )
            )
        return deletion_result
    
    
    def reactivate_user_account(self, user_id: int) -> UserModel:
        """
        Activate a user by their ID.

        Args:
            user_id (int): The unique identifier of the user to activate.

        Returns:
            UserModel: The activated user.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        activated_user: Optional[UserModel] = self._user_repository.update_user_active_status(user_id=user_id, is_active=True)
        if not activated_user:
            raise UserNotFoundException(
                identifier=user_id,
                message=not_found_message(
                    instance="user",
                    identifier=user_id
                )
            )
        return activated_user
    
    def set_user_inactive(self, user_id: int) -> UserModel:
        """
        Deactivate a user by their ID.

        Args:
            user_id (int): The unique identifier of the user to deactivate.

        Returns:
            UserModel: The deactivated user.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        deactivated_user: Optional[UserModel] = self._user_repository.update_user_active_status(user_id=user_id, is_active=False)
        if not deactivated_user:
            raise UserNotFoundException(
                identifier=user_id,
                message=not_found_message(
                    instance="user",
                    identifier=user_id
                )
            )
        return deactivated_user