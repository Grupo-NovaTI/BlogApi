from core.security.jwt_handler import JwtHandler
from users.models.user_model import UserModel as User
from core.security.password_hasher import PasswordHasher
from users.excepctions.user_exception import InvalidUserCredentialsException
from utils.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class AuthRepository(BaseRepository):
    def __init__(self, db_session, jwt_handler: JwtHandler):
        super().__init__(db_session=db_session)
        self._db_session = db_session
        self._jwt_handler = jwt_handler

    def login(self, username: str, password: str) -> str:
        """Authenticate user with username and password."""
        user = self._db_session.query(User).filter(User.username == username).first()
        if user and PasswordHasher().verify_password(plain_password=password, hashed_password=user.hashed_password):
            return self._jwt_handler.create_access_token(data={"sub": str(user.id), "role": user.role})
        raise InvalidUserCredentialsException("Invalid username or password")
