"""
Pydantic schema for user creation and update requests.

This module defines the UserRequest class, which is used to validate and serialize user input
data for user creation and update operations. It includes field constraints, password validation,
and a method to convert the request to a UserModel ORM object.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.users.models.user_model import UserModel
from app.core.security.password_hasher import PasswordHasher
from app.utils.constants.constants import EMAIL_PATTERN
from app.utils.enums.user_roles import UserRole


class UserRequest(BaseModel):
    """
    Schema for user creation and update requests.

    Validates user input data, enforces field constraints, and provides a method to convert
    the request to a UserModel ORM object.
    """
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., examples=["user@example.com"], pattern=EMAIL_PATTERN)
    name: str = Field(..., min_length=1, max_length=50, examples=["John", "Jane"])
    last_name: str = Field(..., min_length=1, max_length=50, examples=["Doe", "Smith"])
    password: str = Field(..., min_length=8, max_length=12)
    role: UserRole = Field(
        default=UserRole.USER, description="User role, default is 'user'", examples=["user", "admin", "reader"]
    )

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Validates the password to ensure it meets security requirements.

        Args:
            value (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password does not meet the required criteria.
        """
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char in "!@#$%^&*+." for char in value):
            raise ValueError("Password must contain at least one special character")
        return value

    class Config:
        """
        Pydantic configuration for ORM compatibility and schema examples.
        """
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "name": "John",
                "last_name": "Doe",
                "password": "Password123!",
                "role": "user"
            }
        }

    def to_orm(self, user_id: Optional[int] = None) -> UserModel:
        """
        Converts the UserRequest instance to a UserModel ORM object.

        Args:
            user_id (Optional[int]): The user ID to assign (for updates).

        Returns:
            UserModel: The corresponding UserModel ORM object.
        """
        return UserModel(
            id=user_id,
            username=self.username,
            email=self.email,
            name=self.name,
            last_name=self.last_name,
            hashed_password=PasswordHasher().hash_password(self.password),
            role=self.role
        )