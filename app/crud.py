from . import models, schema
from sqlalchemy.orm import Session
from fastapi import Depends, status
from .database import get_db


async def get_blogs(db: Session = Depends(get_db)):
    payload = db.query(models.Blog).all()
    if payload is None:
        response = schema.BlogResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to find any blog"
        )
        return response
    else:
        response = schema.BlogResponse(
            status=status.HTTP_200_OK,
            message="All blogs retrieved"
        )
        response.data = payload
        response.count = len(response.data)
        return response


async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
    if payload is None:
        response = schema.BlogResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to find the blog"
        )
        return response
    else:
        response = schema.BlogResponse(
            status=status.HTTP_200_OK,
            message=f"blog with id: {blog_id} retrieved"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


async def create_blog(blog: schema.BlogCreate, db: Session = Depends(get_db)):
    # verbose way of saving
    # new_blog = models.Blog(title=blog.title, content=blog.content, published=blog.published)

    # short version of saving
    payload = models.Blog(**blog.dict())
    if payload is None:
        response = schema.BlogResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to create a blog"
        )
        return response
    else:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        response = schema.BlogResponse(
            status=status.HTTP_201_CREATED,
            message=f"blog with id of {payload.blog_id} created successfully"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


async def update_blog(blog_id: int, blog: schema.BlogCreate, db: Session = Depends(get_db)):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id)
    if payload.first() is None:
        response = schema.BlogResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to update the blog"
        )
        return response
    else:
        payload.update(blog.dict(), synchronize_session=False)
        db.commit()
        response = schema.BlogResponse(
            status=status.HTTP_200_OK,
            message=f"blog with id of {blog_id} updated successfully"
        )
        response.data.append(payload.first())
        response.count = len(response.data)
        return response


async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id)
    if payload.first() is None:
        response = schema.BlogResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to delete the blog"
        )
        return response
    else:
        payload.delete(synchronize_session=False)
        db.commit()
        response = schema.BlogResponse(
            status=status.HTTP_200_OK,
            message=f"blog with id of {blog_id} was deleted successfully"
        )
        return response


async def get_users(db: Session = Depends(get_db)):
    payload = db.query(models.User).all()
    if payload is None:
        response = schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to find any users"
        )
        return response
    else:
        response = schema.UserResponse(
            status=status.HTTP_200_OK,
            message="All users retrieved"
        )
        response.data = payload
        response.count = len(response.data)
        return response


async def get_user(user_id: int, db: Session = Depends(get_db)):
    payload = db.query(models.User).filter(models.User.user_id == user_id).first()
    if payload is None:
        response = schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to find the user"
        )
        return response
    else:
        response = schema.UserResponse(
            status=status.HTTP_200_OK,
            message=f"user with id: {user_id} retrieved"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


async def create_user(user: schema.UserBase, db: Session = Depends(get_db)):
    payload = models.User(**user.dict())
    if payload is None:
        response = schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to create the user"
        )
        return response
    else:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        response = schema.UserResponse(
            status=status.HTTP_201_CREATED,
            message=f"blog with id of {payload.user_id} created successfully"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


async def update_user(user: schema.UserBase, user_id: int, db: Session = Depends(get_db)):
    payload = db.query(models.User).filter(models.User.user_id == user_id)
    if payload.first() is None:
        response = schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to update the user"
        )
        return response
    else:
        payload.update(user.dict(), synchronize_session=False)
        db.commit()
        response = schema.UserResponse(
            status=status.HTTP_200_OK,
            message=f"user with id of {user_id} updated successfully"
        )
        response.data.append(payload.first())
        response.count = len(response.data)
        return response


async def delete_user(user_id: int, db: Session = Depends(get_db)):
    payload = db.query(models.User).filter(models.User.user_id == user_id)
    if payload.first() is None:
        response = schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to delete the user"
        )
        return response
    else:
        payload.delete(synchronize_session=False)
        db.commit()
        response = schema.UserResponse(
            status=status.HTTP_200_OK,
            message=f"user with id of {user_id} was deleted successfully"
        )
        return response
