from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username : str
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
