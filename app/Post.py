from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class Post(BaseModel):
    id: Optional[UUID] = uuid4()
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
