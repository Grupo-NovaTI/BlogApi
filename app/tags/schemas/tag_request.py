"""
Pydantic schema for tag creation and update requests.

This module defines the TagRequest schema for validating and serializing tag input data.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TagRequest(BaseModel):
    """
    Schema for tag request data.

    Attributes:
        name (str): Name of the tag, must be unique and up to 50 characters long.
        description (Optional[str]): Optional description of the tag, up to 255 characters.
    """

    name: str = Field(
        max_length=50,
        description="Name of the tag, must be unique and up to 50 characters long.",
        min_length=3,
        examples=["example_tag", "tech", "health"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Description of the tag, optional and up to 255 characters long.",
        examples=["This is an example tag.", "Tag for technology-related content."],
    )

    class Config:
        """
        Pydantic configuration for TagRequest schema.
        """

        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "example_tag",
                "description": "This is an example tag.",
            }
        }
