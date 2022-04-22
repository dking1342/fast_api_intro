import random
from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    blog_id: Optional[int] = random.randrange(1000)
    title: str
    content: str
    published: bool = True
    created_at: datetime
