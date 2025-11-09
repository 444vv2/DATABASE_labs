from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TrainBase(BaseModel):
    train_class: Optional[str] = None
    departure_date: datetime
    arrival_time: Optional[datetime] = None
    seat_amount: int

class TrainCreate(TrainBase):
    from_id: int
    to_id: int

class TrainUpdate(BaseModel):
    train_class: Optional[str] = None
    departure_date: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    from_id: Optional[int] = None
    to_id: Optional[int] = None
    seat_amount: Optional[int] = None

class TrainResponse(TrainBase):
    train_id: int
    from_id: int
    to_id: int

    class Config:
        from_attributes = True
