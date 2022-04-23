from datetime import datetime
from random import randrange
from typing import List

from pydantic import BaseModel


class BlogBase(BaseModel):
    blog_id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


class BlogCreate(BlogBase):
    pass


class UserBase(BaseModel):
    user_id: int = randrange(1000)
    email: str
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    user_id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class BlogResponse(BaseModel):
    timestamp: datetime = datetime.now()
    status: str
    message: str
    data: List[BlogBase] = []
    count: int = 0

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
