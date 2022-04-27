from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, UUID4


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[UUID4] = None


class UserLoginCreate(BaseModel):
    user_id: str
    token: str

    class Config:
        orm_mode = True


class AuthResponse(BaseModel):
    timestamp: datetime = datetime.now()
    status: str
    message: str
    data: List[UserLoginCreate] = []
    count: int = 0

    class Config:
        orm_mode = True


class AuthErrorResponse(BaseModel):
    timestamp: datetime = datetime.now()
    status: str
    error: str

    class Config:
        orm_mode = True
