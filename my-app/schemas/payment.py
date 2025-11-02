from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PaymentBase(BaseModel):
    amount: float
    payment_date: datetime
    payment_type: str
    is_paid: bool
    transaction_number: Optional[str] = None

class PaymentCreate(PaymentBase):
    order_id: int

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    payment_type: Optional[str] = None
    is_paid: Optional[bool] = None
    transaction_number: Optional[str] = None
    order_id: Optional[int] = None

class PaymentResponse(PaymentBase):
    payment_id: int
    order_id: int

    class Config:
        from_attributes = True
