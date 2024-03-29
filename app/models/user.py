from typing import Optional, List

from pydantic import BaseModel

from .dbmodel import DBModelMixin


class UserBase(DBModelMixin):
    email: str
    is_active: bool
    is_deleted: bool
    verification_code: str | None = None


class UserInDB(UserBase):
    hashed_password: str = ""


class User(UserBase):
    pass


class UserInCreate(BaseModel):
    email: str
    password: str


class UserInLogin(UserInCreate):
    pass


class UserInUpdate(DBModelMixin):
    password: Optional[str] = None


class Users(BaseModel):
    users: List[User]
