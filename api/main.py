import uvicorn as uvicorn

from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from .routers import router

from .cfg import API_PREFIX, VERSION, DEBUG, API_NAME
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

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(router, prefix=API_PREFIX)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
