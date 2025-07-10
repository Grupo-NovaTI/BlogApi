from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.users.schemas.user_response import UserResponse
from app.tags.schemas.tag_response import TagResponse
class BlogResponse(BaseModel):
    """
    Schema for blog response.
    """
    id: int
    title: str
    content: str
    user_id: int
    updated_at: datetime
    created_at: datetime
    is_published: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "user_id": 1,
                "is_published": True
            }
        }
        
class BlogResponseFull(BlogResponse):
    """
    Full blog response schema including user and tags.
    """
    user: UserResponse
    tags: List[TagResponse]