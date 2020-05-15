from starlette.config import Config

API_PREFIX = "/api"
VERSION = "0.0.0"
API_NAME = "API"

config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
