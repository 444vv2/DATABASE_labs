from typing import Optional
from pydantic import BaseModel

class DeliveryBase(BaseModel):
    delivery_type: str
    delivery_time: Optional[str] = None
    is_delivered: bool

class DeliveryCreate(DeliveryBase):
    order_id: int

class DeliveryUpdate(BaseModel):
    delivery_type: Optional[str] = None
    delivery_time: Optional[str] = None
    is_delivered: Optional[bool] = None
    order_id: Optional[int] = None

class DeliveryResponse(DeliveryBase):
    delivery_id: int
    order_id: int

    class Config:
        from_attributes = True
