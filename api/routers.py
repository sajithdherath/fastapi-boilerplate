from fastapi import APIRouter
from .cfg import API_NAME
from .models import HealthResponse
from .utils import create_aliased_response

router = APIRouter()


@router.get('/health', response_model=HealthResponse)
def health():
    return create_aliased_response(HealthResponse(status=f'{API_NAME} service is available.'))