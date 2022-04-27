from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import database, models
from ..schemas import user as user_schmea
from ..schemas import auth as auth_schema
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os


load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# secret key
# algorithm needed
# expiration


secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("JWT_ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credential_exception
        token_data = auth_schema.TokenData(user_id=user_id)
        return token_data

    except JWTError:
        raise credential_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    verified_token = verify_access_token(token, credential_exception)
    user: user_schmea.UserCreate = db.query(models.User).filter(models.User.user_id == verified_token.user_id).first()
    return user

