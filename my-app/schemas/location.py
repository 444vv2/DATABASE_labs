from typing import Optional
from pydantic import BaseModel

class LocationBase(BaseModel):
    city: str
    country: str

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class LocationResponse(LocationBase):
    location_id: int

    class Config:
        from_attributes = True
