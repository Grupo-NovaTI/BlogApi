from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserRequest(BaseModel):
    id : Optional[int] = Field(None, description="User ID, optional for new users")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., examples=["user@example.com"])
    full_name: str = Field(..., min_length=5, max_length=50, examples=["John Doe", "Jane Smith"])
    hashed_password: str = Field(..., min_length=8, max_length=12)
    created_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), description="Update timestamp, optional for new users")

    class Config:
        from_attributes = True
    