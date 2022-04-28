from uuid import UUID
from typing import Union, Optional
from fastapi import Depends, status, APIRouter
from pydantic.types import UUID4
from sqlalchemy.orm import Session
from .. import models
from ..schemas import blog as blog_schema
from ..schemas import user as user_schema
from ..database import get_db
from ..utils import authentication, protected_responses

router = APIRouter(
    prefix="/blogs",
    tags=['Blogs']
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_blogs(
        db: Session = Depends(get_db),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ""
        # current_user: user_schema.UserCreate = Depends(authentication.get_current_user)
):
    # filters to show only the users blogs
    # payload = db.query(models.Blog).filter(models.Blog.user_id == current_user.user_id).all()

    # shows all posts regardless of user
    payload = db.query(models.Blog)\
        .filter(models.Blog.title.contains(search))\
        .order_by(models.Blog.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    if payload is None:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            error="Unable to find any blog"
        )
        return response
    elif len(payload) == 0:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_200_OK,
            error="No blogs found"
        )
        return response
    else:
        payload = protected_responses.convert_payload(payload)
        response = blog_schema.BlogResponse(
            status=status.HTTP_200_OK,
            message="All blogs retrieved"
        )
        response.data = payload
        response.count = len(response.data)
        return response


@router.get("/{blog_id}", status_code=status.HTTP_200_OK)
async def get_blog(
        blog_id: Union[int, str, UUID],
        db: Session = Depends(get_db),
        current_user: user_schema.UserCreate = Depends(authentication.get_current_user)
):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
    if payload is None:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            error="Unable to find the blog"
        )
        return response
    else:
        payload = protected_responses.convert_payload(payload)
        response = blog_schema.BlogResponse(
            status=status.HTTP_200_OK,
            message=f"blog with id: {blog_id} retrieved"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_blog(
        blog: blog_schema.Blog,
        db: Session = Depends(get_db),
        current_user: user_schema.UserCreate = Depends(authentication.get_current_user)
):
    payload = models.Blog(user_id=current_user.user_id, **blog.dict())
    if payload is None:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            error="Unable to create a blog"
        )
        return response
    else:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        payload = blog_schema.BlogOutput(**payload.__dict__)
        response = blog_schema.BlogResponse(
            status=status.HTTP_201_CREATED,
            message=f"blog was created successfully"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


@router.put("/{blog_id}", status_code=status.HTTP_200_OK)
async def update_blog(
        blog_id: UUID4,
        blog: blog_schema.Blog,
        db: Session = Depends(get_db),
        current_user: user_schema.UserCreate = Depends(authentication.get_current_user)
):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id)
    if payload.first() is None:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            error="Unable to update the blog"
        )
        return response
    elif payload.first().user_id and payload.first().user_id != current_user.user_id:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_403_FORBIDDEN,
            error="You are not the owner of this blog"
        )
        return response
    else:
        updated_blog = blog.dict()
        updated_blog.update(blog_id=blog_id, user_id=current_user.user_id)
        payload.update(updated_blog, synchronize_session=False)
        db.commit()
        payload = blog_schema.BlogOutput(**payload.first().__dict__)
        response = blog_schema.BlogResponse(
            status=status.HTTP_200_OK,
            message=f"blog with id of {blog_id} updated successfully"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
async def delete_blog(
        blog_id: Union[int, str, UUID],
        db: Session = Depends(get_db),
        current_user: user_schema.UserCreate = Depends(authentication.get_current_user)
):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id)
    if payload.first() is None:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to delete the blog"
        )
        return response
    elif payload.first().user_id and payload.first().user_id != current_user.user_id:
        response = blog_schema.BlogErrorResponse(
            status=status.HTTP_403_FORBIDDEN,
            error="You are not the owner of this blog"
        )
        return response
    else:
        payload.delete(synchronize_session=False)
        db.commit()
        response = blog_schema.BlogResponse(
            status=status.HTTP_200_OK,
            message=f"blog with id of {blog_id} was deleted successfully"
        )
        return response
