from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from core.config.application_config import ApplicationConfig

class JWTAuth:
    def __init__(self):
        self._config = ApplicationConfig()
        self._secret_key = self._config.jwt_secret_key
        self._algorithm = self._config.jwt_algorithm
        self._access_token_expire_minutes = self._config.access_token_expire_minutes

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except JWTError:
            return {}
