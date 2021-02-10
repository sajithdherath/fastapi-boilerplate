from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED

from ...services.jwt import get_current_user_authorizer
from ...services.users import check_free_username_and_email
from ...crud.users import update_user, create_user
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...models.user import User, UserInResponse, UserInUpdate, UserInCreate
from ...utils import build_response

router = APIRouter()


@router.get("", tags=["users"])
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer)):
    return await build_response(jsonable_encoder(user))


@router.post("", tags=["users"], status_code=HTTP_201_CREATED)
async def register(user: UserInCreate,
                   db: AsyncIOMotorClient = Depends(get_database)):
    await check_free_username_and_email(db, user.username, user.email)

    async with await db.start_session() as s:
        async with s.start_transaction():
            await create_user(db, user)
            return await build_response("User created successfully", 201)


@router.put("", response_model=UserInResponse, tags=["users"])
async def update_current_user(
        user: UserInUpdate = Body(..., embed=True),
        current_user: User = Depends(get_current_user_authorizer),
        db: AsyncIOMotorClient = Depends(get_database),
):
    if user.username == current_user.username:
        user.username = None
    if user.email == current_user.email:
        user.email = None

    await check_free_username_and_email(db, user.username, user.email)

    dbuser = await update_user(db, current_user.username, user)
    return UserInResponse(user=User(**dbuser.dict(), token=current_user.token))
