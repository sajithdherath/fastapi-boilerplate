from typing import Optional, List

from pydantic import AnyUrl, BaseModel

from .dbmodel import DBModelMixin
from .rwmodel import RWModel
from ..services.security import generate_salt, get_password_hash, verify_password


class UserBase(RWModel, DBModelMixin):
    username: str
    email: str
    profile_picture: Optional[AnyUrl] = None


class UserInDB(UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class User(UserBase):
    pass


class UserInLogin(RWModel):
    email: str
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(RWModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class Users(RWModel):
    users: List[User]
