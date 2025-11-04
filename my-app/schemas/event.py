from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class EventBase(BaseModel):
    title: str
    date_time: datetime
    seat_amount: int

class EventCreate(EventBase):
    location_id: int

class EventUpdate(BaseModel):
    title: Optional[str] = None
    date_time: Optional[datetime] = None
    location_id: Optional[int] = None
    seat_amount: Optional[int] = None

class EventResponse(EventBase):
    event_id: int
    location_id: int

    class Config:
        from_attributes = True

class ArtistInEvent(BaseModel):
    artist_id: int
    name: str
    surname: str
    nickname: Optional[str] = None
    genre: Optional[str] = None
    is_group: Optional[bool] = False

    class Config:
        from_attributes = True

class EventWithArtistsResponse(EventBase):
    event_id: int
    location_id: int
    artists: List[ArtistInEvent] = []

    class Config:
        from_attributes = True
