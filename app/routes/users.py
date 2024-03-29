from typing import Annotated

from fastapi import APIRouter, Body, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from starlette.status import HTTP_201_CREATED
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pymongo import MongoClient

from ..services.auth import get_current_user
from ..db.mongodb import get_database
from ..models.user import User, UserInUpdate, UserInCreate
from ..services.users import UserService

router = APIRouter()


def get_service(db: Annotated[MongoClient, Depends(get_database)]):
    return UserService(db)


@router.get("/me", tags=["users"], response_model=User)
async def get_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/verify", tags=["users"])
async def verify_user(email: EmailStr, code: str, service: Annotated[UserService, Depends(get_service)]):
    _ = await service.verify(email, code)
    return {"status": "success"}


@router.post("", tags=["users"], status_code=HTTP_201_CREATED, response_model=User)
async def register(user: UserInCreate, service: Annotated[UserService, Depends(get_service)]):
    user_db = await service.create(user)
    return User(**user_db.model_dump(exclude={"verification_code"}))


@router.put("", tags=["users"], response_model=User)
async def update_current_user(user: UserInUpdate,
                              current_user: Annotated[User, Depends(get_current_user)],
                              service: Annotated[UserService, Depends(get_service)]):
    user_updated = await service.update(current_user, user)
    return user_updated
