"""
Pydantic schema for comment response data.

This module defines the CommentResponse schema for serializing comment data returned by the API.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from app.users.schemas.user_response import UserResponse


class CommentResponse(BaseModel):
    """
    Schema for comment response data.

    Attributes:
        id (int): Unique identifier of the comment.
        blog_id (int): ID of the blog post the comment belongs to.
        user_id (int): ID of the user who made the comment.
        content (str): Content of the comment.
        user (Optional[UserResponse]): User details for the comment author.
        created_at (datetime): Timestamp of comment creation.
        updated_at (datetime): Timestamp of last update.
    """

    id: int
    blog_id: int
    user_id: int
    content: str
    user: Optional[UserResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Pydantic configuration for CommentResponse schema.
        """

        json_schema_extra: dict[str, Any] = {
            "example": {
                "id": 1,
                "blog_id": 1,
                "user_id": 1,
                "user": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john_doe@example.com",
                },
                "content": "This is a sample comment.",
                "created_at": "2023-10-01T12:00:00Z",
                "updated_at": "2023-10-01T12:00:00Z",
            }
        }