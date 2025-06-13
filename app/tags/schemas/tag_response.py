from pydantic import BaseModel, Field
from typing import Optional


class TagResponse(BaseModel):
    """
    Schema for tag response.
    """
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "example_tag",
                "description": "This is an example tag.",
            }
        }
