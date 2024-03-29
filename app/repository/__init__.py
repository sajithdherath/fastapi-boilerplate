from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from ..config import settings


class BaseRepository:
    database: str = settings.DATABASE
    collection: str

    def __init__(self, client: MongoClient):
        self.client = client

    async def find(self, **q):
        try:
            row = self.client[self.database][self.collection].find_one(q)
            if row:
                return row
        except PyMongoError as e:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Get {self.collection} failed'
            )

    async def create(self, obj: dict):
        try:
            row = self.client[self.database][self.collection].insert_one(obj)
            return row
        except PyMongoError as e:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Create {self.collection} failed'
            )

    async def update(self, _id: str, obj: dict):
        try:
            row = self.client[self.database][self.collection].update_one({"_id": ObjectId(_id)},
                                                                         {"$set": obj})
            return row
        except PyMongoError as e:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Create {self.collection} failed'
            )

    async def delete(self, _id: str):
        try:
            row = self.client[self.database][self.collection].delete_one({"_id": ObjectId(_id)})
            return row
        except PyMongoError as e:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Create {self.collection} failed'
            )
