"""
Pydantic schema for tag response data.

This module defines the TagResponse schema for serializing tag data returned by the API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TagResponse(BaseModel):
    """
    Schema for tag response data.

    Attributes:
        id (int): Unique identifier of the tag.
        name (str): Name of the tag.
        description (Optional[str]): Optional description of the tag.
        updated_at (datetime): Timestamp of last update.
        created_at (datetime): Timestamp of creation.
    """
    id: int
    name: str
    description: Optional[str]
    updated_at: datetime
    created_at: datetime

    class Config:
        """
        Pydantic configuration for TagResponse schema.
        """
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "example_tag",
                "description": "This is an example tag.",
            }
        }
