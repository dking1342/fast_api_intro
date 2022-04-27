import uuid
from uuid import UUID
from datetime import datetime
from typing import List, Union, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    blog_id: Optional[Union[int, str, UUID]]
    title: str
    content: str
    published: bool = True
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class BlogCreate(BlogBase):
    pass


class BlogResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    status: str
    message: str
    data: List[BlogBase] = []
    count: int = 0

    class Config:
        orm_mode = True


class BlogErrorResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    status: str
    error: str

    class Config:
        orm_mode = True
