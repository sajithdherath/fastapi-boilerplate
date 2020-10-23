import logging

from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db
from ..config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT


async def connect_to_mongo():
    logging.info("Mongodb connecting...")
    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logging.info("Mongodb connected！")


async def close_mongo_connection():
    logging.info("Mongodb connection closing...")
    db.client.close()
    logging.info("Mongodb connection closed！")
