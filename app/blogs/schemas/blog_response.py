from pydantic import BaseModel
from users.schemas.user_response import UserResponse
from typing import List, Optional
from tags.schemas.tag_response import TagResponse
class BlogResponse(BaseModel):
    """
    Schema for blog response.
    """
    id: int
    title: str
    content: str
    author_id: int

    is_published: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "author_id": 1,
                "is_published": True
            }
        }
        
class BlogResponseFull(BlogResponse):
    """
    Full blog response schema including author and tags.
    """
    author: UserResponse
    tags: List[TagResponse]