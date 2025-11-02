from typing import Optional
from pydantic import BaseModel

class InsuranceBase(BaseModel):
    country_travel: str
    starting_time: str
    finish_time: str
    number_tourists: int
    price: int

class InsuranceCreate(InsuranceBase):
    order_id: int

class InsuranceUpdate(BaseModel):
    country_travel: Optional[str] = None
    starting_time: Optional[str] = None
    finish_time: Optional[str] = None
    number_tourists: Optional[int] = None
    price: Optional[int] = None
    order_id: Optional[int] = None

class InsuranceResponse(InsuranceBase):
    insurance_id: int
    order_id: int

    class Config:
        from_attributes = True
