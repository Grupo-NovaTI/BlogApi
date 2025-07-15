"""
Pydantic schema for user response objects returned by the API.

This module defines the UserResponse class, which is used to serialize user data
when sending responses to clients. It ensures type safety and proper formatting
of user-related fields.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    """
    Schema for representing user data in API responses.

    Attributes:
        id (int): Unique identifier of the user.
        username (str): Username of the user.
        email (EmailStr): Email address of the user.
        name (str): First name of the user.
        last_name (str): Last name of the user.
        is_active (bool): Indicates if the user account is active.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
        role (str): Role assigned to the user.
        profile_picture (Optional[str]): URL of the user's profile picture.
    """
    id: int
    username : str
    email: EmailStr
    name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    role: str
    profile_picture: Optional[str] = None   

    class Config:
        """
        Pydantic configuration for ORM compatibility.
        """
        from_attributes = True
