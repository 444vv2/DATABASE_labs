from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PlaneBase(BaseModel):
    plane_class: Optional[str] = None
    departure_time: datetime
    arrival_time: Optional[datetime] = None
    seat_amount: int

class PlaneCreate(PlaneBase):
    from_id: int
    to_id: int

class PlaneUpdate(BaseModel):
    plane_class: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    from_id: Optional[int] = None
    to_id: Optional[int] = None
    seat_amount: Optional[int] = None

class PlaneResponse(PlaneBase):
    plane_id: int
    from_id: int
    to_id: int

    class Config:
        from_attributes = True
