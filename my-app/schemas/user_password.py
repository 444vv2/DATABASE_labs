from pydantic import BaseModel

class PasswordBase(BaseModel):
    password_hash: str

class PasswordUpdate(BaseModel):
    password_hash: str

class PasswordCreate(BaseModel):
    user_id: int

class PasswordResponse(BaseModel):
    user_id: int

    class Config:
        from_attributes = True
