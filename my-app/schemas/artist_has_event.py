from typing import Optional
from pydantic import BaseModel

class ArtistHasEventCreate(BaseModel):
    artist_name: str
    artist_surname: str
    event_name: str

class ArtistHasEventUpdate(BaseModel):
    artist_id: Optional[int] = None
    event_id: Optional[int] = None

class ArtistHasEventResponse(BaseModel):
    artist_id: int
    event_id: int

    class Config:
        from_attributes = True
