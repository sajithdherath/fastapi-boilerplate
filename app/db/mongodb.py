from pymongo import MongoClient


class DataBase:
    client: MongoClient = None


db = DataBase()


async def get_database() -> MongoClient:
    return db.client
