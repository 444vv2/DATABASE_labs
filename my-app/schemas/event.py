from typing import Optional
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
