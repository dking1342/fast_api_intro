from uuid import UUID
from datetime import datetime
from typing import List, Union
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Union[int, str, UUID] = None


class UserLoginCreate(BaseModel):
    user_id: Union[int, str, UUID] = None
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
