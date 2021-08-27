import logging

from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.db.mongodb_utils import connect_to_mongo

logger = logging.getLogger("uvicorn.error")


async def build_response(data, status_code=200):
    try:
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'payload': data
            },
        )
    except Exception as e:
        # logger.error(str(e))
        raise HTTPException(500, detail="json error")


async def startup():
    await connect_to_mongo()
    logger = logging.getLogger("uvicorn.error")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
