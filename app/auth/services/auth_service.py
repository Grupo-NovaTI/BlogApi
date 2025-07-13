"""
Service layer for user authentication and registration.

This module defines the AuthService class, which provides business logic for user authentication
(login) and registration, using the UserRepository, JwtHandler, and PasswordHasher.
"""

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.core.security.jwt_handler import JwtHandler
from app.core.security.password_hasher import PasswordHasher
from app.users.models.user_model import UserModel
from app.users.repositories.user_repository import UserRepository
from app.utils.enums.operations import Operations
from app.utils.errors.exception_handlers import (handle_read_exceptions,
                                                 handle_service_transaction)
from app.utils.errors.exceptions import \
    ConflictException as UserAlreadyExistsException
from app.utils.errors.exceptions import UnauthorizedException

_MODEL_NAME: str = "User"


class AuthService:
    """
    Service for user authentication and registration.
    """

    def __init__(self, user_repository: UserRepository, jwt_handler: JwtHandler, password_service: PasswordHasher, db_session: Session) -> None:
        """
        Initialize the AuthService with required dependencies.

        Args:
            user_repository (UserRepository): The user repository instance.
            jwt_handler (JwtHandler): The JWT handler instance.
            password_service (PasswordHasher): The password hasher instance.
            db_session (Session): SQLAlchemy session for database operations.
        """
        self._user_repository: UserRepository = user_repository
        self._jwt_handler: JwtHandler = jwt_handler
        self._password_hasher_service: PasswordHasher = password_service
        self._db_session: Session = db_session

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.AUTHENTICATE
    )
    def login(self, username, password) -> str:
        """
        Authenticate user with username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: JWT token if authentication is successful.
        """
        user: Optional[UserModel] = self._user_repository.get_user_by_username(
            username=username)
        if not user or not self._verify_password(
                current_user_password=str(user.hashed_password), password_to_verify=password):
            raise UnauthorizedException()
        return self._create_access_token(user=user)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.CREATE
    )
    def register(self, user_data: dict[str, Any]) -> str:
        """
        Register a new user and return a JWT token.

        Args:
            user_data (dict[str, Any]): The user data.

        Returns:
            str: JWT token for the newly registered user.
        """
        existing_user: Optional[UserModel] = self._user_repository.get_user_by_email_or_username(
            email=str(user_data.get("email")), username=str(user_data.get("username"))
        )
        if existing_user != None:
            raise UserAlreadyExistsException(
                resource_type="Users", identifier="username or email")
        password: str = user_data.pop("password")
        user_data["hashed_password"] = self._password_hasher_service.hash_password(
            password=password)
        user_to_create: UserModel = UserModel(**user_data)
        registered_user: UserModel = self._user_repository.create_user(
            user=user_to_create)
        return self._create_access_token(user=registered_user)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_password(self, user_id: int, current_password: str, new_password: str) -> None:
        """
        Update the user's password.

        Args:
            user_id (int): The ID of the user whose password is being updated.
            current_password (str): The user's current password.
            new_password (str): The new password to set for the user.

        Raises:
            UnauthorizedException: If the user is not found or the current password is incorrect.
        """
        user_to_update: Optional[UserModel] = self._user_repository.get_user_by_id(
            user_id=user_id)
        if not user_to_update:
            raise UnauthorizedException(details="User not found.")
        if not self._verify_password(
                current_user_password=str(user_to_update.hashed_password), password_to_verify=current_password):
            raise UnauthorizedException(
                details="Current password is incorrect.")
        new_hashed_password: str = self._password_hasher_service.hash_password(
            password=new_password)
        self._user_repository.update_user(user=user_to_update, user_data={
            "hashed_password": new_hashed_password})

    def _create_access_token(self, user: UserModel) -> str:
        """
        Create an access token for the authenticated user.

        Args:
            user (UserModel): The authenticated user.

        Returns:
            str: JWT token for the user.
        """
        return self._jwt_handler.create_access_token(data={"sub": str(user.id), "role": str(user.role)})

    def _verify_password(self, current_user_password: str, password_to_verify: str) -> bool:
        """
        Verify the user's password against the stored hashed password.

        Args:
            current_user_password (str): The stored hashed password.
            password_to_verify (str): The password to verify.

        Returns:
            bool: True if the password matches, otherwise False.
        """
        return self._password_hasher_service.verify_password(
            plain_password=password_to_verify, hashed_password=current_user_password
        )
