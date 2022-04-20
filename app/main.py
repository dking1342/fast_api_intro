from typing import List
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status

from app.Post import Post

app = FastAPI()

# short term db
my_posts: List[Post] = [
    Post(
        id="b66d5ca0-7a03-41cf-8eb6-fff6d5cc0fca",
        title="title of post 1",
        content="content of post 1"
    ),
    Post(
        id="b9bfd9ce-d38f-4c7a-bc3e-df0a31aac065",
        title="second post",
        content="beaches are nice"
    )
]


@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"detail": my_posts}


@app.get("/posts/{post_id}")
async def get_post(post_id: UUID):
    payload = find_post(post_id)
    if payload["data"] is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    else:
        return {"detail": payload["data"]}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = uuid4()
    my_posts.append(post_dict)
    return {"detail": post_dict}


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post: Post, post_id: UUID):
    payload = find_post(post_id)
    if payload["data"] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    elif payload["data"] is not None and payload["index"] is not None:
        post.id = post_id
        my_posts[payload["index"]] = post
        return {"detail": f"post with id: {post_id} has been updated"}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: UUID):
    payload = find_post(post_id)
    if payload["data"] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    else:
        my_posts.remove(payload["data"])
        return {"detail": f"item with id {post_id} has been removed"}


def find_post(post_id):
    payload = None
    index = None
    for index, item in enumerate(my_posts):
        if post_id in item.dict().values():
            payload = item
            index = index
            break
    return dict(data=payload, index=index)
