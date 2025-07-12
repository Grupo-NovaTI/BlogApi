"""
Pydantic schema for authentication token response.

This module defines the TokenResponse schema for serializing JWT token data returned by the API.
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Schema for authentication token response.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (default: 'bearer').
    """

    access_token: str
    token_type: str = "bearer"