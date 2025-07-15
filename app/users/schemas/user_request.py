"""
Pydantic schema for user creation and update requests.

This module defines the UserRequest class, which is used to validate and serialize user input
data for user creation and update operations. It includes field constraints, password validation,
and a method to convert the request to a UserModel ORM object.
"""

import re
from typing import Any

from git import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.constants.constants import EMAIL_PATTERN, PASSWORD_PATTERN
from app.utils.enums.user_roles import UserRole


class UserRequest(BaseModel):
    """
    Schema for user creation and update requests.

    Validates user input data, enforces field constraints, and provides a method to convert
    the request to a UserModel ORM object.
    """
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., examples=[
                            "user@example.com"], pattern=EMAIL_PATTERN)
    name: str = Field(..., min_length=1, max_length=50,
                      examples=["John", "Jane"])
    last_name: str = Field(..., min_length=1,
                           max_length=50, examples=["Doe", "Smith"])
    password: str = Field(..., min_length=8, max_length=12)
    role: UserRole = Field(
        default=UserRole.USER, description="User role, default is 'user'", examples=["user", "admin", "reader"]
    )

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Validates the password to ensure it meets security requirements using a single regex.
        - At least one uppercase letter.
        - At least one digit.
        - At least one special character (!@#$%^&*+.).
        - At least 8 characters long.
        """
        if not re.fullmatch(pattern=PASSWORD_PATTERN, string=value):
            raise ValueError(
                "Password must be at least 8 characters long and include at least one uppercase letter, "
                "one lowercase letter, one number, and one special character (!@#$%^&*+.)."
            )
        return value

    class Config:
        """
        Pydantic configuration for ORM compatibility and schema examples.
        """
        from_attributes = True
        json_schema_extra: dict[str, Any] = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "name": "John",
                "last_name": "Doe",
                "password": "Password123!",
                "role": "user"
            }
        }


class UserUpdateRequest(BaseModel):
    """
    Schema for user update requests.

    Validates user input data for updating user information, excluding the password field.
    """
    name : Optional[str] = Field(
        None, min_length=1, max_length=50, examples=["John", "Jane"])
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=50, examples=["Doe", "Smith"])
    email: Optional[EmailStr] = Field(
        None, examples=["johndoe@example.com"], pattern=EMAIL_PATTERN)