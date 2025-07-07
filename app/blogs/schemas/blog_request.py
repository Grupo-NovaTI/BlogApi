from pydantic import BaseModel, Field
from typing import Optional, List
from app.blogs.models.blog_model import BlogModel

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
        
    def to_orm(self, blog_id : Optional[int] = None) -> BlogModel:
        """ Convert the BlogRequest schema to a BlogModel instance."""
        return BlogModel(
            id=blog_id,
            title=self.title,
            content=self.content,
            author_id=self.author_id,
            is_published=self.is_published
        )
        
class BlogPatchRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "content": "Updated content for the blog post.",
                "is_published": False
            }
        }