from typing import List
from users.repositories.user_repository import UserRepository
from users.excepctions.user_exceptions import UserNotFoundException, UserAlreadyExistsException
from users.models.user_model import UserModel


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

        check_user_exists: UserModel | None = self._user_repository.get_user_by_username(
            username=str(user_data.username))
        if check_user_exists:
            raise UserAlreadyExistsException(
                "User with this username already exists.")
        check_user_exists = self._user_repository.get_user_by_email(
            email=str(user_data.email))
        if check_user_exists:
            raise UserAlreadyExistsException(
                "User with this email already exists.")
        return self._user_repository.create_user(user=user_data)

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The unique identifier of the user to retrieve.

        Returns:
            UserModel: The user object if found.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        user: UserModel | None = self._user_repository.get_user_by_id(
            user_id=user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")
        return user

    def get_user_by_username(self, username: str) -> UserModel:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            UserModel: The user object if found.

        Raises:
            UserNotFoundException: If the user with the given username does not exist.
        """
        user: UserModel | None = self._user_repository.get_user_by_username(
            username=username)
        if not user:
            raise UserNotFoundException(
                f"User with username {username} not found.")
        return user

    def update_user(self, user_id: int, user_data: UserModel) -> UserModel:
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
        user: UserModel | None = self._user_repository.get_user_by_id(
            user_id=user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        return self._user_repository.update_user(user=user_data)
