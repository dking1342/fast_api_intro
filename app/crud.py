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
            status=status.HTTP_200_OK,
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
