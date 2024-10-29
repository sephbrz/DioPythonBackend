from src.database import database
from src.models.user import userTable

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from src.exceptions import AuthorizationError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password, hashed_password)


def get_password_hash(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    return bcrypt.hashpw(password.encode("utf-8"), salt)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def authenticate_user(username: str, password: str):
    query = userTable.select().where(userTable.c.username == username)
    record = await database.fetch_one(query)
    if record:
        if verify_password(password.encode("utf-8"), record.password):
            return {
                "access_token": create_access_token(
                    data={"sub": username},
                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                )
            }
        else:
            return {"message": "user not authorized"}
    else:
        return {"message": "user not authorized"}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthorizationError("Invalid credentials")
    except InvalidTokenError:
        raise AuthorizationError("Invalid credentials")
    query = userTable.select().where(userTable.c.username == username)
    record = await database.fetch_one(query)
    return record.id


def decode_jwt():
    pass


def login_required(current_user_id: Annotated[int, Depends(get_current_user)]):
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return current_user_id
