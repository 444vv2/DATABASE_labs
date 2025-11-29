from typing import Optional
from pydantic import BaseModel

class ArtistBase(BaseModel):
    name: str
    surname: str
    nickname: Optional[str] = None
    genre: Optional[str] = None
    is_group: Optional[bool] = False

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    nickname: Optional[str] = None
    genre: Optional[str] = None
    is_group: Optional[bool] = None

class ArtistResponse(ArtistBase):
    artist_id: int

    class Config:
        from_attributes = True
