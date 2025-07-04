# from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.users.models.user_model import UserModel
from app.core.security.password_hasher import PasswordHasher
from app.utils.constants.constants import EMAIL_PATTERN
from app.utils.enums.user_roles import UserRole
from app.utils.errors.exceptions import ValidationException

class UserRequest(BaseModel):
    id: Optional[int] = Field(
        default=None, description="User ID, optional for new users", exclude=True)
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., examples=["user@example.com"], pattern=EMAIL_PATTERN)
    name: str = Field(..., min_length=1, max_length=50, examples=[
        "John", "Jane"])
    last_name: str = Field(..., min_length=1, max_length=50, examples=[
        "Doe", "Smith"])
    password: str = Field(..., min_length=8, max_length=12)
    role: UserRole = Field(
        default=UserRole.USER, description="User role, default is 'user'", examples=["user", "admin", "reader"]
    )

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char in "!@#$%^&*+." for char in value):
            raise ValueError("Password must contain at least one special character")
        return value

    class Config:
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

    def to_orm(self) -> UserModel:
        return UserModel(
            username=self.username,
            email=self.email,
            name=self.name,
            last_name=self.last_name,
            hashed_password=PasswordHasher().hash_password(self.password),
            role=self.role
        )