# from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from users.models.user_model import UserModel
from core.security.password_hasher import PasswordHasher
from utils.validators.regex_patterns import email_pattern
from utils.enumns.user_roles import UserRole

class UserRequest(BaseModel):
    id: Optional[int] = Field(
        default=None, description="User ID, optional for new users", exclude=True)
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., examples=["user@example.com"], pattern=email_pattern)
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
        
    def to_orm(self) -> UserModel:
        return UserModel(
            id=self.id,
            username=self.username,
            email=self.email,
            name=self.name,
            last_name=self.last_name,
            hashed_password=PasswordHasher().hash_password(self.password),
            role=self.role
        )