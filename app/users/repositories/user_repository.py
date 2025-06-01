from utils.repositories.base_repository import BaseRepository
from users.models.user_model import UserModel as User
from users.excepctions.user_exception import UserNotFoundException, UserAlreadyExistsException


class UserRepository(BaseRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their ID.
        Args:
            user_id (int): The ID of the user to retrieve.
        Returns:
            User: The user object if found.
        Raises:
            UserNotFoundException: If no user with the given ID exists.
        """

        user = self.db_session.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found.")
        return user

    def get_user_by_username(self, username: str):
        """
        Retrieve a user by their username.
        Args:
            username (str): The username of the user to retrieve.
        Returns:
            User: The user object if found.
        Raises:
            UserNotFoundException: If no user with the given username exists.
        """

        user = self.db_session.query(User).filter(User.username == username).first()
        if not user:
            raise UserNotFoundException(f"User with username {username} not found.")
        return user

    def create_user(self, user: User) -> User:
        """
        Create a new user in the database.
        Args:
            user (User): The user object to create.
        Returns:
            User: The created user object.
        Raises:
            UserAlreadyExistsException: If a user with the same username or email already exists.
        """
        existing_user = self.db_session.query(
            User).filter(User.username == user.username).first()
         # Check if the user already exists by username or email
        if existing_user:
            raise UserAlreadyExistsException(
                f"User with username {user.username} already exists.")
        existing_email = self.db_session.query(
            User).filter(User.email == user.email).first()
        if existing_email:
            raise UserAlreadyExistsException(
                f"User with email {user.email} already exists.")
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def update_user(self, user: User) -> User:
        """
        Update an existing user in the database.
        Args:
            user (User): The user object with updated information.
        Returns:
            User: The updated user object.
        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
            UserAlreadyExistsException: If a user with the same username or email already exists.
        """
        existing_user = self.db_session.query(
            User).filter(User.id == user.id).first()
        if not existing_user:
            raise UserNotFoundException(f"User with id {user.id} not found.")
        existing_user = self.db_session.query(User).filter(User.email == user.email).first()
        if existing_user and existing_user.id != user.id:
            raise UserAlreadyExistsException(
                f"User with email {user.email} already exists.")
        existing_user = self.db_session.query(User).filter(User.username == user.username).first()
        if existing_user and existing_user.id != user.id:
            raise UserAlreadyExistsException(
                f"User with username {user.username} already exists.")
        self.db_session.commit()
        return user

    def delete_user(self, user: User) -> User:
        """
        Delete a user from the database.
        Args:
            user (User): The user object to delete.
        Returns:
            User: The deleted user object.
        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
         # Check if the user exists before attempting to delete
        existing_user = self.db_session.query(
            User).filter(User.id == user.id).first()
        if not existing_user:
            raise UserNotFoundException(f"User with id {user.id} not found.")
        self.db_session.delete(user)
        self.db_session.commit()
        return user

    def get_all_users(self) -> list[User]:
        """
        Retrieve all users from the database.
        Returns:
            list[User]: A list of all user objects.
        """
         # Return all users from the database
        return self.db_session.query(User).all()
