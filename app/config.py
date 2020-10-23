from databases import DatabaseURL
from starlette.config import Config

API_PREFIX = "/app"
VERSION = "0.0.0"
API_NAME = "API"

config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

"""
Database Configurations
"""
MONGO_HOST: str = config("MONGO_HOST", cast=str)
MONGO_PORT = config("MONGO_PORT", cast=int, default=27017)
MONGO_DB = config("MONGO_DB", cast=str)

MONGODB_URL = DatabaseURL(
    f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

database_name = MONGO_DB
items_collection = "items"
