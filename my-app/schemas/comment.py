from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    user_id: int
    descriptions: str
    created_at: datetime

class CommentCreate(BaseModel):
    user_id: int
    descriptions: str

class CommentUpdate(BaseModel):
    user_id: Optional[int] = None
    descriptions: Optional[str] = None
    created_at: Optional[datetime] = None

class CommentResponse(CommentBase):
    comment_id: int

    class Config:
        from_attributes = True
