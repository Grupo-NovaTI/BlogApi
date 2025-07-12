"""
Service layer for user authentication and registration.

This module defines the AuthService class, which provides business logic for user authentication
(login) and registration, using the UserRepository, JwtHandler, and PasswordHasher.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.users.models.user_model import UserModel
from app.core.security.jwt_handler import JwtHandler
from app.users.repositories.user_repository import UserRepository
from app.utils.errors.exceptions import ConflictException as UserAlreadyExistsException, UnauthorizedException
from app.core.security.password_hasher import PasswordHasher
from app.utils.errors.exception_handlers import handle_service_transaction, handle_read_exceptions
from app.utils.enums.operations import Operations

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
        model="Users",
        operation=Operations.FETCH_BY
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
        user: Optional[UserModel] = self._user_repository.get_user_by_username(username=username)
        if not user or not self._password_hasher_service.verify_password(
                plain_password=password, hashed_password=str(user.hashed_password)):
            raise UnauthorizedException()
        return self._jwt_handler.create_access_token(data={"sub": str(user.id), "role": user.role})

    @handle_service_transaction(
        model="Users",
        operation=Operations.CREATE
    )
    def register(self, user: UserModel) -> str:
        """
        Register a new user and return a JWT token.

        Args:
            user (UserModel): The user model instance to register.

        Returns:
            str: JWT token for the newly registered user.
        """
        check_user_exists: Optional[UserModel] = self._user_repository.get_user_by_email_or_username(
            email=str(user.email), username=str(user.username))
        if check_user_exists:
            raise UserAlreadyExistsException(
                identifier="email or username",
                resource_type="Users",
                details="A user with this email or username already exists."
            )
        registered_user: UserModel = self._user_repository.create_user(user=user)
        return self._jwt_handler.create_access_token(data={"sub": str(registered_user.id), "role": str(registered_user.role)})
