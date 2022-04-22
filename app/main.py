from uuid import UUID
from fastapi import FastAPI, HTTPException, status
from app.Post import Post
from database.delete_post import delete_post
from database.get_post import get_post
from database.get_posts import get_posts
from database.insert_post import insert_post
from database.update_post import update_post

app = FastAPI()


@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/posts", status_code=status.HTTP_200_OK)
async def fetch_posts():
    payload = await get_posts()
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts retrieved"
        )
    else:
        return {"detail": payload}


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def fetch_post(post_id: UUID):
    payload = await get_post(post_id)
    if payload is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    else:
        return {"detail": payload}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    payload = await insert_post(post_dict)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to create the post"
        )
    else:
        return {"detail": payload}


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def set_post(post: Post, post_id: UUID):
    post_dict = post.dict()
    payload = await update_post(post_id, post_dict)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to update"
        )
    else:
        return {"detail": payload}


@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def remove_post(post_id: UUID):
    payload = await delete_post(post_id)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to delete post"
        )
    else:
        return {"detail": payload}
