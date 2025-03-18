from os import getenv
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fake_db import db


load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10)


def get_user(username: str):
    for user in db:
        if user.get("username") == username:
            return user
    return None


def data_verification(user):
    if any(user_data["username"] == user.username for user_data in db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this name already exists"
        )
    hashed_password = pwd_context.hash(user.password)
    return hashed_password


def create_jwt_token(data: dict):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    data["exp"] = expiration_time
    return encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )