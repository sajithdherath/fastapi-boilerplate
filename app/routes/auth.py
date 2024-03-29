from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from pymongo import MongoClient

from ..db.mongodb import get_database
from ..models.token import Token
from ..models.user import UserInLogin, UserInDB
from ..repository.users import UserRepository
from ..config import settings
from ..services.auth import create_access_token
from ..services.security import verify_password

router = APIRouter()


def get_repository(db: Annotated[MongoClient, Depends(get_database)]):
    return UserRepository(db)


@router.post("/token", tags=["authentication"], response_model=Token)
async def login(user: UserInLogin, user_repository: Annotated[UserRepository, Depends(get_repository)]):
    db_user = await user_repository.find(email=user.email)
    if not db_user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    db_user = UserInDB(**db_user)
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"email": db_user.email}, expires_delta=access_token_expires
    )
    token = Token(access_token=token)
    return token
