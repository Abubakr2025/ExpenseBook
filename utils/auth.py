import jwt
import datetime

from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel

from configs.config import settings


class TokenPayload(BaseModel):
    id: int
    role: str
    exp: datetime.datetime


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.auth.access_token_expire_minutes)

    to_encode.update({'exp': expire})

    if "role" not in to_encode:
        raise ValueError("Missing role in token payload")

    encoded_jwt = jwt.encode(
        to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])

        if "role" not in payload or payload["role"] is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token: Missing role")

        return TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
