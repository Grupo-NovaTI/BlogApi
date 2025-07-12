"""
JWT handler utility for token creation and validation.

This module defines the JwtHandler class, which provides methods for creating and decoding
JSON Web Tokens (JWT) for authentication and authorization in the application.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException
from jose import JWTError, jwt
from starlette import status

from app.core.config.application_config import (ACCESS_TOKEN_EXPIRE_MINUTES,
                                                JWT_ALGORITHM, JWT_SECRET_KEY)


class JwtHandler:
    """
    Handles the creation and validation of JSON Web Tokens (JWT).
    """
    def __init__(self) -> None:
        """
        Initialize the JwtHandler with secret key, algorithm, and expiration settings.
        """
        self._secret_key: str = JWT_SECRET_KEY
        self._algorithm: str = JWT_ALGORITHM
        self._access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES

    @property
    def secret_key(self) -> str:
        """
        Returns the secret key used for JWT operations.

        Returns:
            str: The secret key.
        """
        return self._secret_key

    @property
    def algorithm(self) -> str:
        """
        Returns the algorithm used for JWT operations.

        Returns:
            str: The algorithm name.
        """
        return self._algorithm

    @property
    def access_token_expire_minutes(self) -> int:
        """
        Returns the expiration time for access tokens in minutes.

        Returns:
            int: Expiration time in minutes.
        """
        return self._access_token_expire_minutes

    def create_access_token(self, data: dict) -> str:
        """
        Creates a new access token.

        Args:
            data (dict): The payload to encode into the token. Must contain 'sub'.

        Returns:
            str: The encoded JWT.
        """
        to_encode: dict[str, Any] = data.copy()
        expire: datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(claims=to_encode, key=self._secret_key, algorithm=self._algorithm)

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
            payload: dict[str, Any] = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

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
            
            return {
                "user_id": payload.get("sub"),
                "role": payload.get("role"),
                "exp": payload.get("exp"),
            }
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )