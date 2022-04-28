from fastapi import Depends, status, APIRouter
from pydantic.types import UUID4
from .. import models
from sqlalchemy.orm import Session
from ..schemas import vote as vote_schema
from ..schemas import user as user_schema
from ..database import get_db
from ..utils import authentication

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)


@router.get("")
async def get_votes():
    return None


@router.get("/{vote_id}")
async def get_vote():
    return None


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_votes(
        vote: vote_schema.Vote,
        db: Session = Depends(get_db),
        current_user: user_schema.UserCreate = Depends(authentication.get_current_user)
):
    vote_query = db.query(models.Vote).filter(models.Vote.blog_id == vote.blog_id, models.Vote.user_id == current_user.user_id)
    found_vote = vote_query.first()
    if vote.direction == 1:
        if found_vote:
            response = vote_schema.VoteErrorResponse(
                status=status.HTTP_409_CONFLICT,
                error="user has already voted for the blog"
            )
            return response
        new_vote = models.Vote(blog_id=vote.blog_id, user_id=current_user.user_id)
        db.add(new_vote)
        db.commit()
        response = vote_schema.VoteResponse(
            status=status.HTTP_201_CREATED,
            message="successfully added the vote"
        )
        return response
    else:
        if not found_vote:
            response = vote_schema.VoteErrorResponse(
                status=status.HTTP_404_NOT_FOUND,
                error="Vote does not exists"
            )
            return response
        vote_query.delete(synchronize_session=False)
        db.commit()
        response = vote_schema.VoteResponse(
            status=status.HTTP_204_NO_CONTENT,
            message="successfully deleted the vote"
        )
        return response


@router.put("/{vote_id}")
async def create_votes(vote, vote_id: UUID4):
    return None


@router.delete("/{vote_id}")
async def create_votes(vote_id: UUID4):
    return None

