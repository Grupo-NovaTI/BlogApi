# app/core/security/jwt_handler.py

from datetime import datetime, timedelta, timezone
from starlette import status
from fastapi import HTTPException
from jose import jwt, JWTError

from app.core.config.application_config import JWT_ALGORITHM, JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

class JwtHandler:
    """
    Handles the creation and validation of JSON Web Tokens (JWT).
    """
    def __init__(self):
        self._secret_key: str = JWT_SECRET_KEY
        self._algorithm: str = JWT_ALGORITHM
        self._access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES

    @property
    def secret_key(self) -> str:
        """Returns the secret key used for JWT operations."""
        return self._secret_key

    @property
    def algorithm(self) -> str:
        """Returns the algorithm used for JWT operations."""
        return self._algorithm

    @property
    def access_token_expire_minutes(self) -> int:
        """Returns the expiration time for access tokens in minutes."""
        return self._access_token_expire_minutes

    def create_access_token(self, data: dict) -> str:
        """
        Creates a new access token.

        Args:
            data (dict): The payload to encode into the token. Must contain 'sub'.

        Returns:
            str: The encoded JWT.
        """
        to_encode = data.copy()
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict:
        """
        Decodes an access token and validates its claims.

        Args:
            token (str): The JWT to decode.

        Returns:
            dict: The decoded payload containing user_id, role, and expiration.

        Raises:
            HTTPException: If the token is invalid, expired, or has incorrect claims.
        """
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

            if payload.get("sub") is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: Subject (sub) claim is missing.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if payload.get("exp") is None or datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(tz=timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Map 'sub' to 'user_id' for consistency within the application
            return {
                "user_id": payload.get("sub"),
                "role": payload.get("role"),
                "exp": payload.get("exp"),
            }
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )