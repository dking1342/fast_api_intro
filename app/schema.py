from datetime import datetime
from typing import List

from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    content: str
    published: bool = True


class BlogCreate(BlogBase):
    pass


class BlogResponse(BaseModel):
    timestamp: datetime = datetime.now()
    status: str
    message: str
    data: List[BlogBase] = []
    count: int = 0
