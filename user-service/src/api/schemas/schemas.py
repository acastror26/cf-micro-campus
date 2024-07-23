from pydantic import BaseModel
from typing import Optional

class UserInfo(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    is_active: Optional[bool] = True
    is_m2m_account: Optional[bool] = False

class UserBase(UserInfo):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserInfo):
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: Optional[int] = None

class TokenRequest(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    user: User
    is_valid: bool
