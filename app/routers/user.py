import uuid
from typing import Union
from uuid import UUID
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..schemas import user as user_schema
from ..database import get_db
from ..utils import authorization

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("", status_code=status.HTTP_200_OK, response_model=user_schema.UserResponse)
async def get_users(db: Session = Depends(get_db)):
    payload = db.query(models.User).all()
    if payload is None:
        response = user_schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to find any users"
        )
        return response
    else:
        response = user_schema.UserResponse(
            status=status.HTTP_200_OK,
            message="All users retrieved"
        )
        response.data = payload
        response.count = len(response.data)
        return response


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=user_schema.UserResponse)
async def get_user(
        user_id: Union[int, str, UUID],
        db: Session = Depends(get_db)
):
    payload = db.query(models.User).filter(models.User.user_id == user_id).first()
    if payload is None:
        response = user_schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to find the user"
        )
        return response
    else:
        response = user_schema.UserResponse(
            status=status.HTTP_200_OK,
            message=f"user with id: {user_id} retrieved"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserResponse)
async def create_user(
        user: user_schema.UserBase,
        db: Session = Depends(get_db)
):
    hashed_pw = authorization.hash_the_password(user.password)
    user.password = hashed_pw
    payload = models.User(**user.dict())
    if payload is None:
        response = user_schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to create the user"
        )
        return response
    else:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        response = user_schema.UserResponse(
            status=status.HTTP_201_CREATED,
            message=f"user with id of {payload.user_id} created successfully"
        )
        response.data.append(payload)
        response.count = len(response.data)
        return response


# @router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=user_schema.UserResponse)
# async def update_user(
#         user: user_schema.UserBase,
#         user_id: Union[int, str, UUID],
#         db: Session = Depends(get_db)
# ):
#     payload = db.query(models.User).filter(models.User.user_id == user_id)
#     if payload.first() is None:
#         response = user_schema.UserResponse(
#             status=status.HTTP_404_NOT_FOUND,
#             message="Unable to update the user"
#         )
#         return response
#     else:
#         payload.update(user.dict(), synchronize_session=False)
#         db.commit()
#         response = user_schema.UserResponse(
#             status=status.HTTP_200_OK,
#             message=f"user with id of {user_id} updated successfully"
#         )
#         response.data.append(payload.first())
#         response.count = len(response.data)
#         return response


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=user_schema.UserResponse)
async def delete_user(
        user_id: Union[int, str, UUID],
        db: Session = Depends(get_db)
):
    payload = db.query(models.User).filter(models.User.user_id == user_id)
    if payload.first() is None:
        response = user_schema.UserResponse(
            status=status.HTTP_404_NOT_FOUND,
            message="Unable to delete the user"
        )
        return response
    else:
        payload.delete(synchronize_session=False)
        db.commit()
        response = user_schema.UserResponse(
            status=status.HTTP_200_OK,
            message=f"user with id of {user_id} was deleted successfully"
        )
        return response
