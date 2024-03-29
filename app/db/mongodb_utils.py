import logging
from urllib.parse import quote_plus

from pymongo import MongoClient
from ..config import settings
from .mongodb import db

logger = logging.getLogger("uvicorn.error")


async def connect_to_mongo():
    try:
        if settings.MONGO_USERNAME is None:
            mongodb_url: str = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}/{settings.DATABASE}"

        else:
            mongodb_url: str = (f"mongodb://{quote_plus(settings.MONGO_USERNAME)}:{quote_plus(settings.MONGO_PASSWORD)}"
                                f"@{settings.MONGO_HOST}:{settings.MONGO_PORT}")
        logger.info("Connecting to the database...")
        db.client = MongoClient(mongodb_url)
        db.client.server_info()
        logger.info("Successfully connected to the database!")
    except ConnectionRefusedError:
        logger.error("Database connecting failed!")


async def close_mongo_connection():
    logger.info("Closing database connection...")
    db.client.close()
    logger.info("Database connection closed！")
