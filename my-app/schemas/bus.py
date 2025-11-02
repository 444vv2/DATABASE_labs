from typing import Optional
from datetime import time
from pydantic import BaseModel

class BusBase(BaseModel):
    departure_date: time
    arrival_time: Optional[time] = None
    seat_amount: int

class BusCreate(BusBase):
    from_id: int
    to_id: int

class BusUpdate(BaseModel):
    departure_date: Optional[time] = None
    arrival_time: Optional[time] = None
    from_id: Optional[int] = None
    to_id: Optional[int] = None
    seat_amount: Optional[int] = None

class BusResponse(BusBase):
    bus_id: int
    from_id: int
    to_id: int

    class Config:
        from_attributes = True
