from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


def http_exception_handler(request: Request, e: HTTPException):
    return JSONResponse(
        status_code=e.status_code,
        content={
            "success": False,
            "error": {
                "code": e.status_code,
                "message": e.detail
            }
        },
    )
