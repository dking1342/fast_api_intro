from datetime import datetime
from typing import List

from pydantic import BaseModel, UUID4, conint


class Vote(BaseModel):
    blog_id: UUID4
    direction: conint(le=1)


class VoteErrorResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    status: str
    error: str

    class Config:
        orm_mode = True


class VoteResponse(BaseModel):
    timestamp: datetime = datetime.utcnow()
    status: str
    message: str

    class Config:
        orm_mode = True

