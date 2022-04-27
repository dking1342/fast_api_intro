from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import auth as auth_schema
from .. import models
from ..utils import authentication, authorization
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        response = auth_schema.AuthErrorResponse(
            status=status.HTTP_403_FORBIDDEN,
            error="Invalid credentials"
        )
        return response

    if not authorization.verify(user_credentials.password, user.password):
        response = auth_schema.AuthErrorResponse(
            status=status.HTTP_403_FORBIDDEN,
            error="Invalid credentials"
        )
        return response

    access_token = authentication.create_access_token(data={"user_id": user.user_id})
    response = auth_schema.AuthResponse(
        status=status.HTTP_200_OK,
        message="Successful login"
    )
    response.data.append(auth_schema.UserLoginCreate(user_id=user.user_id, token=access_token))
    response.count = len(response.data)
    return response

