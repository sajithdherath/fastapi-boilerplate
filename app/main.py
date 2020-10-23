import logging

import uvicorn as uvicorn

from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from .db.mongodb_utils import connect_to_mongo, close_mongo_connection
from .routers import router

from .config import API_PREFIX, VERSION, DEBUG, API_NAME
from .exceptions import http_exception_handler

app = FastAPI(version=VERSION,
              debug=DEBUG,
              description=f'This is an auto generated document for the {API_NAME} service',
              openapi_url=f'{API_PREFIX}/openapi.json',
              docs_url=f'{API_PREFIX}/docs'
              )

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger("app")

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(router, prefix=API_PREFIX)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
