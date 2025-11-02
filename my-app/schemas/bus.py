from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BusBase(BaseModel):
    departure_date: datetime
    arrival_time: Optional[datetime] = None
    seat_amount: int

class BusCreate(BusBase):
    from_id: int
    to_id: int

class BusUpdate(BaseModel):
    departure_date: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    from_id: Optional[int] = None
    to_id: Optional[int] = None
    seat_amount: Optional[int] = None

class BusResponse(BusBase):
    bus_id: int
    from_id: int
    to_id: int

    class Config:
        from_attributes = True
