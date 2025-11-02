from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class InsuranceBase(BaseModel):
    country_travel: str
    starting_time: datetime
    finish_time: datetime
    number_tourist: int
    price: int

class InsuranceCreate(InsuranceBase):
    order_id: int

class InsuranceUpdate(BaseModel):
    country_travel: Optional[str] = None
    starting_time: Optional[datetime] = None
    finish_time: Optional[datetime] = None
    number_tourist: Optional[int] = None
    price: Optional[int] = None
    order_id: Optional[int] = None

class InsuranceResponse(InsuranceBase):
    insurance_id: int
    order_id: int

    class Config:
        from_attributes = True
