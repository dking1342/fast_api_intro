from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, UUID4


class UserBase(BaseModel):
    user_id: Optional[UUID4]
    email: EmailStr
    password: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    user_id: UUID4
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    timestamp: datetime = datetime.now()
    status: str
    message: str
    data: List[UserCreate] = []
    count: int = 0

    class Config:
        orm_mode = True
