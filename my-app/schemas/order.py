from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class OrderBase(BaseModel):
    order_date: Optional[datetime] = None  # В моделі може бути None
    payment_status: str
    ticket_type: str
    delivery_type: str

class OrderCreate(OrderBase):
    user_id: int

class OrderUpdate(BaseModel):
    order_date: Optional[datetime] = None
    payment_status: Optional[str] = None
    ticket_type: Optional[str] = None
    delivery_type: Optional[str] = None
    user_id: Optional[int] = None

class OrderResponse(OrderBase):
    order_id: int
    user_id: int

    class Config:
        from_attributes = True
