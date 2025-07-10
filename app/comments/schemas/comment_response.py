from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.users.schemas.user_response import UserResponse

class CommentResponse(BaseModel):
    id: int
    blog_id: int
    user_id: int
    content: str
    user: Optional[UserResponse]
    created_at: datetime
    updated_at: datetime
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "blog_id": 1,
                "user_id": 1,
                "user": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john_doe@example.com"
                },
                "content": "This is a sample comment.",
                "created_at": "2023-10-01T12:00:00Z",
                "updated_at": "2023-10-01T12:00:00Z"
            }
        }