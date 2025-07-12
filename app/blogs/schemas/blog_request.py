"""
Pydantic schemas for blog creation and update requests.

This module defines schemas for validating and serializing blog input data for creation and patch operations.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class BlogRequest(BaseModel):
    """
    Schema for creating a new blog post.

    Attributes:
        title (str): Title of the blog post.
        content (str): Content of the blog post.
        is_published (bool): Publication status of the blog post.
        tags (List[int]): List of tag IDs associated with the blog post.
    """

    title: str = Field(..., description="Title of the blog post")
    content: str = Field(..., description="Content of the blog post")
    is_published: bool = Field(False, description="Publication status of the blog post")
    tags: List[int] = Field(default_factory=list, description="List of tag IDs associated with the blog post")

    class Config:
        """
        Pydantic configuration for BlogRequest schema.
        """
        json_schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "tags": [1, 2, 3],
                "is_published": True
            }
        }


class BlogPatchRequest(BaseModel):
    """
    Schema for updating an existing blog post.

    Attributes:
        title (Optional[str]): Updated title of the blog post.
        content (Optional[str]): Updated content of the blog post.
        is_published (Optional[bool]): Updated publication status.
        tags (Optional[List[int]]): Updated list of tag IDs.
    """

    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    tags: Optional[List[int]] = None

    class Config:
        """
        Pydantic configuration for BlogPatchRequest schema.
        """
        json_schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "content": "Updated content for the blog post.",
                "is_published": False,
                "tags": [2, 3]
            }
        }