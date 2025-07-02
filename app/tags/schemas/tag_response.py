from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TagResponse(BaseModel):
    """
    Schema for tag response.
    """
    id: int
    name: str
    description: Optional[str]
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "example_tag",
                "description": "This is an example tag.",
            }
        }
