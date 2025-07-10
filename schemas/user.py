from datetime import date

from pydantic import BaseModel


class UserSchema(BaseModel):
    full_name: str
    username: str
    email: str
    birth_date: str
    password: str


class UserSignInSchema(BaseModel):
    username: str
    password: str
