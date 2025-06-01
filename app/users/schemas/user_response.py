from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username : str
    email: EmailStr
    name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    role: str

    class Config:
        from_attributes = True
