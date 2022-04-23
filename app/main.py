from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import models, schema, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/blogs")
async def get_blogs(db: Session = Depends(get_db)):
    payload = await crud.get_blogs(db)
    return payload


@app.get("/blogs/{blog_id}")
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    payload = await crud.get_blog(blog_id, db)
    return payload


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: schema.BlogCreate, db: Session = Depends(get_db)):
    payload = await crud.create_blog(blog, db)
    return payload


@app.put("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
async def update_blog(blog_id: int, blog: schema.BlogCreate, db: Session = Depends(get_db)):
    payload = await crud.update_blog(blog_id, blog, db)
    return payload


@app.delete("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
async def remove_blog(blog_id: int, db: Session = Depends(get_db)):
    payload = await crud.delete_blog(blog_id, db)
    return payload
