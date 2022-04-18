import http
from typing import List
from uuid import uuid4, UUID

from fastapi import FastAPI, HTTPException

from models import User, Gender, Role

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("f3ee64c0-3fcd-48f3-8eb2-854414200567"),
        first_name="Jack",
        last_name="Johnson",
        gender=Gender.male,
        roles=[Role.student]
    ),
    User(
        id=UUID("123acb8c-8c9b-414f-abbf-d34907decf60"),
        first_name="Jill",
        last_name="Takao",
        gender=Gender.female,
        roles=[Role.admin, Role.user]
    )
]


@app.get("/")
async def root():
    # await abc();
    return {"Hello": "World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.get("/api/v1/user/{user_id}")
async def fetch_user(user_id: UUID):
    user: List = []
    for item in db:
        if item.id == user_id:
            user.append(item)
            break
    if len(user) > 0:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} cannot be found"
        )

@app.post("/api/v1/users")
async def register_user(user: User):
    user.id = uuid4()
    db.append(user)
    return {
        "id": user.id
    }


@app.put("/api/v1/user/{user_id}")
async def update_user(user_id: UUID, user: User):
    user_response: List = []
    for item in db:
        if item.id == user_id:
            item.first_name = user.first_name
            item.last_name = user.last_name
            item.middle_name = user.middle_name
            item.gender = user.gender
            item.roles = user.roles
            user_response.append(item)
            break
    if len(user_response) > 0:
        return user_response
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to update user {user_id}"
        )


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    user: List = []
    for item in db:
        if item.id == user_id:
            user.append(item)
            db.remove(item)
            break

    if len(user) > 0:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} does not exist"
        )
