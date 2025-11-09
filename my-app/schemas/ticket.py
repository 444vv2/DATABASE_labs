from typing import Optional
from pydantic import BaseModel

class TicketBase(BaseModel):
    ticket_type: str
    seat_number: int
    price: float
    is_available: bool

class TicketCreate(TicketBase):
    bus_id: Optional[int] = None
    plane_id: Optional[int] = None
    train_id: Optional[int] = None
    event_id: Optional[int] = None
    order_id: int

class TicketUpdate(BaseModel):
    ticket_type: Optional[str] = None
    seat_number: Optional[int] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    bus_id: Optional[int] = None
    plane_id: Optional[int] = None
    train_id: Optional[int] = None
    event_id: Optional[int] = None
    order_id: Optional[int] = None

class TicketResponse(TicketBase):
    ticket_id: int
    order_id: int

    class Config:
        from_attributes = True
