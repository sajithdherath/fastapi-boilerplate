from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .utils import startup
from .db.mongodb_utils import close_mongo_connection
from .routes import router
from .config import settings

app = FastAPI(version=settings.VERSION,
              debug=settings.DEBUG,
              description=f'This is an auto generated document for the {settings.API_NAME} service',
              openapi_url=f'{settings.API_PREFIX}/openapi.json',
              docs_url=f'{settings.API_PREFIX}/docs'
              )

# Set all CORS enabled origins
if settings.ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(router, prefix=settings.API_PREFIX)
