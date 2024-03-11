from databases import DatabaseURL
from starlette.config import Config
from urllib.parse import quote_plus

VERSION = "v0.1"
API_PREFIX = f"/api/{VERSION}"
API_NAME = "API"

config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=True)

"""
Security
"""
# openssl rand -hex 32
SECRET_KEY = "83cd07fdf2c8311cd4ff3d8b4b9aa6d1c3895bfd6fec1a707dba551b1e021bf4"
ALGORITHM = "HS256"
JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

"""
Database
"""
MONGO_HOST: str = config("MONGO_HOST", cast=str, default="localhost")
MONGO_PORT = config("MONGO_PORT", cast=int, default=27017)
MONGO_DB = config("MONGO_DB", cast=str, default="fastapi_boilerplate")
MONGO_USERNAME = config('MONGO_USERNAME', cast=str, default=None)
MONGO_PASSWORD = config('MONGO_PASSWORD', cast=str, default=None)
if MONGO_USERNAME is None:
    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )
else:
    MONGODB_URL = DatabaseURL(
        f"mongodb://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_HOST}:{MONGO_PORT}"
    )
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

database_name = MONGO_DB
users_collection = "users"
