from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from core.config.application_config import ApplicationConfig
from starlette import status

oauth_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

class JwtHandler:
    def __init__(self, oauth_scheme : str = "api/v1/auth/login"):
        self._config = ApplicationConfig()
        self._secret_key: str = self._config.jwt_secret_key
        self._algorithm: str = self._config.jwt_algorithm
        self._access_token_expire_minutes = self._config.access_token_expire_minutes
        self._oauth_scheme = oauth_scheme

    @property
    def oauth_scheme(self) -> OAuth2PasswordBearer:
        """
        Returns the OAuth2PasswordBearer instance for token authentication.
        """
        return OAuth2PasswordBearer(tokenUrl=self._oauth_scheme)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            
            if "exp" not in payload or "sub" not in payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token claims",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(tz=timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return payload
        except JWTError as e:
            print(f"ERROR: JWTError during decoding: {e}")  # See what JWTError says
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
