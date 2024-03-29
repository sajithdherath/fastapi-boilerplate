from pymongo import MongoClient

from . import BaseRepository
from ..config import settings


class UserRepository(BaseRepository):
    collection = settings.users_collection

    def __init__(self, client: MongoClient):
        super().__init__(client)
