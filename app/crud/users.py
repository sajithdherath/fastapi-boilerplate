from datetime import datetime

from ..db.mongodb import AsyncIOMotorClient
from bson.objectid import ObjectId

from ..config import database_name, users_collection
from ..models.user import UserInCreate, UserInDB, UserInUpdate


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def get_user_by_email(conn: AsyncIOMotorClient, email: str) -> UserInDB:
    row = await conn[database_name][users_collection].find_one({"email": email})
    if row:
        return UserInDB(**row)


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.dict(), created_at=datetime.now(), updated_at=datetime.now())
    dbuser.change_password(user.password)

    row = await conn[database_name][users_collection].insert_one(dbuser.dict())

    dbuser.id = row.inserted_id
    return dbuser


async def update_user(conn: AsyncIOMotorClient, username: str, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, username)

    dbuser.username = user.username or dbuser.username
    dbuser.email = user.email or dbuser.email
    dbuser.image = user.image or dbuser.image
    if user.password:
        dbuser.change_password(user.password)

    updated_at = await conn[database_name][users_collection] \
        .update_one({"username": dbuser.username}, {'$set': dbuser.dict()})
    dbuser.updated_at = updated_at
    return dbuser
