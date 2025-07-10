from typing import Optional
from sqlalchemy.orm import Session
from app.users.models.user_model import UserModel
from app.core.security.jwt_handler import JwtHandler
from app.users.repositories.user_repository import UserRepository
from app.utils.errors.exceptions import InvalidUserCredentialsException, AlreadyExistsException as UserAlreadyExistsException
from app.core.security.password_hasher import PasswordHasher
from app.utils.errors.exception_handlers import handle_service_transaction, handle_read_exceptions
from app.utils.enums.operations import Operations

class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_handler: JwtHandler, password_service : PasswordHasher, db_session : Session) -> None:
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
        Returns a JWT token if authentication is successful.
        """
        user: Optional[UserModel] = self._user_repository.get_user_by_username(username=username)
        if not user or not self._password_hasher_service.verify_password(
                plain_password=password, hashed_password=str(user.hashed_password)):
            raise InvalidUserCredentialsException(
                "Invalid username or password")
        return self._jwt_handler.create_access_token(data={"sub": str(user.id), "role": user.role})

    @handle_service_transaction(
        model="Users",
        operation=Operations.CREATE
    )
    def register(self, user: UserModel) -> str:
        check_user_exists: Optional[UserModel] = self._user_repository.get_user_by_email_or_username(
            email=str(user.email), username=str(user.username))
        if check_user_exists:
            raise UserAlreadyExistsException(
                identifier="email or username",
                model="Users"
            )
        registered_user: UserModel = self._user_repository.create_user(user=user)
        return self._jwt_handler.create_access_token(data={"sub": str(registered_user.id), "role": str(registered_user.role)})
