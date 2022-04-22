from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from . import schema

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/blogs")
async def fetch_blogs(db: Session = Depends(get_db)):
    payload = db.query(models.Blog).all()
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to find any blogs"
        )
    else:
        return {"detail": payload}


@app.get("/blogs/{blog_id}")
async def fetch_blog(blog_id: int, db: Session = Depends(get_db)):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to find the blog"
        )
    else:
        return {"detail": payload}


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: schema.Blog, db: Session = Depends(get_db)):
    # verbose way of saving
    # new_blog = models.Blog(title=blog.title, content=blog.content, published=blog.published)

    # short version of saving
    payload = models.Blog(**blog.dict())
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to create the post"
        )
    else:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        return {"detail": payload}


@app.put("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
async def update_blog(blog_id: int, blog: schema.Blog, db: Session = Depends(get_db)):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id)
    if payload.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to find the post"
        )
    else:
        payload.update(blog.dict(), synchronize_session=False)
        db.commit()
        return {"detail": payload.first()}


@app.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_blog(blog_id: int, db: Session = Depends(get_db)):
    payload = db.query(models.Blog).filter(models.Blog.blog_id == blog_id)
    if payload.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to find the post"
        )
    else:
        payload.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"blog id: {blog_id} has been removed"}

