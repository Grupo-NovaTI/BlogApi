

from typing import Optional
from pydantic import BaseModel, Field

from app.tags.models.tag_model import TagModel


class TagRequest(BaseModel):
    """
    Schema for tag request.
    """
    id: Optional[int] = Field(
        default=None, description="Unique identifier for the tag, optional for new tags.", exclude=True
    )
    name: str = Field(max_length=50, description="Name of the tag, must be unique and up to 50 characters long.",
                      min_length=3, examples=["example_tag", "tech", "health"])

    description: Optional[str] = Field(
        default=None, max_length=255, description="Description of the tag, optional and up to 255 characters long.", examples=["This is an example tag.", "Tag for technology-related content."]
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "example_tag",
                "description": "This is an example tag.",
            }
        }

    def to_model(self) -> TagModel:
        """
        Convert the TagRequest schema to a TagModel instance.
        
        Returns:
            TagModel: An instance of TagModel with the data from the request.
        """
        return TagModel(
            id=self.id,
            name=self.name,
            description=self.description
        )