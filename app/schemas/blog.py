from datetime import datetime
from typing import List
from pydantic import BaseModel, UUID4
from ..schemas import user as user_schema


class BlogBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime = datetime.utcnow()


class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    pass

    class Config:
        orm_mode = True


class BlogOutput(BlogBase):
    blog_id: UUID4
    user_id: UUID4
    owner: user_schema.UserBase

    class Config:
        orm_mode = True


class BlogResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    status: str
    message: str
    count: int = 0
    data: List[BlogOutput] = []

    class Config:
        orm_mode = True


class BlogErrorResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    status: str
    error: str

    class Config:
        orm_mode = True
