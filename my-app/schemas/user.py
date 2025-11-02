from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    surname: str
    phone: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    user_id: int

    class Config:
        from_attributes = True
