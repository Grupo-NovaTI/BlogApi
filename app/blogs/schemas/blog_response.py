"""
Pydantic schemas for blog response data.

This module defines schemas for serializing blog data returned by the API, including full responses with user and tags.
"""

from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app.tags.schemas.tag_response import TagResponse
from app.users.schemas.user_response import UserResponse


class BlogResponse(BaseModel):
    """
    Schema for blog response.

    Attributes:
        id (int): Unique identifier of the blog post.
        title (str): Title of the blog post.
        content (str): Content of the blog post.
        user_id (int): ID of the user who created the blog post.
        updated_at (datetime): Timestamp of last update.
        created_at (datetime): Timestamp of creation.
        is_published (bool): Publication status of the blog post.
    """
    id: int
    title: str
    content: str
    user_id: int
    updated_at: datetime
    created_at: datetime
    is_published: bool

    class Config:
        """
        Pydantic configuration for BlogResponse schema.
        """
        from_attributes = True
        json_schema_extra: dict[str, Any] = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "user_id": 1,
                "is_published": True
            }
        }


class BlogResponseFull(BlogResponse):
    """
    Full blog response schema including user and tags.

    Attributes:
        user (UserResponse): User details for the blog author.
        tags (List[TagResponse]): List of tags associated with the blog post.
    """
    user: UserResponse
    tags: List[TagResponse]
