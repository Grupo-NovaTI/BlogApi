from pydantic import BaseModel, Field
from typing import Optional, List
from app.blogs.models.blog_model import BlogModel

class BlogRequest(BaseModel):
    title: str = Field(..., description="Title of the blog post")
    content: str = Field(..., description="Content of the blog post")
    is_published: bool = Field(False, description="Publication status of the blog post")
    tags : List[int] = Field(default_factory=list, description="List of tag IDs associated with the blog post")
     
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "tags": [1, 2, 3],
                "is_published": True
            }
        }
        
        
class BlogPatchRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    tags : Optional[List[int]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "content": "Updated content for the blog post.",
                "is_published": False,
                "tags": [2, 3]
            }
        }