from typing import Optional
from pydantic import BaseModel

class ArtistHasEventCreate(BaseModel):
    artist_id: int
    event_id: int

class ArtistHasEventUpdate(BaseModel):
    artist_id: Optional[int] = None
    event_id: Optional[int] = None

class ArtistHasEventResponse(ArtistHasEventCreate):
    id: int

    class Config:
        from_attributes = True
