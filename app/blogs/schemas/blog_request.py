from pydantic import BaseModel, Field
from typing import Optional, List

class BlogRequest(BaseModel):
    title: str = Field(..., description="Title of the blog post")
    content: str = Field(..., description="Content of the blog post")
    author_id: int = Field(..., description="ID of the author")
    is_published: bool = Field(False, description="Publication status of the blog post")
     
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "author_id": 1,
                "tags": ["introduction", "first post"],
                "is_published": True
            }
        }