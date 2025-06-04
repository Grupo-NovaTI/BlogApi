from users.models.user_model import UserModel
from core.security.jwt_handler import JwtHandler
from users.repositories.user_repository import UserRepository
from auth.exceptions.auth_exceptions import InvalidUserCredentialsException
from core.security.password_hasher import PasswordHasher

class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_handler: JwtHandler, password_service : PasswordHasher) -> None:
        self._user_repository: UserRepository = user_repository
        self._jwt_handler: JwtHandler = jwt_handler
        self._password_hasher_service: PasswordHasher = password_service

    def login(self, username, password) -> str:
        """
        Authenticate user with username and password.
        Returns a JWT token if authentication is successful.
        """
        user: UserModel | None = self._user_repository.get_user_by_username(username=username)
        if not user or not self._password_hasher_service.verify_password(
                plain_password=password, hashed_password=str(user.hashed_password)):
            raise InvalidUserCredentialsException(
                "Invalid username or password")
        return self._jwt_handler.create_access_token(data={"sub": str(user.id), "role": user.role})

    def register(self, user: UserModel) -> str:
        registered_user: UserModel = self._user_repository.create_user(user=user)
        return self._jwt_handler.create_access_token(data={"sub": str(registered_user.id), "role": str(registered_user.role)})
