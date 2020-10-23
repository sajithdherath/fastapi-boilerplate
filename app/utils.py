from fastapi.encoders import jsonable_encoder
from pydantic.main import BaseModel
from starlette.responses import JSONResponse


def create_aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(status_code=200,
                        content=jsonable_encoder(model, by_alias=True))
