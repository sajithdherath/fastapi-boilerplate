from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .config import API_NAME
from .db.mongodb import get_database
from .models import HealthResponse, Item
from .services.items import ItemService
from .utils import create_aliased_response

router = APIRouter()


@router.get('/health', response_model=HealthResponse)
def health():
    return create_aliased_response(HealthResponse(status=f'{API_NAME} service is available.'))


@router.post("/items")
async def save_item(item: Item,
              db: AsyncIOMotorClient = Depends(get_database)):
    service = ItemService()
    return await service.save(db, item)


@router.get("/items/{item_id}")
async def fetch_item(item_id: str,
               db: AsyncIOMotorClient = Depends(get_database)):
    service = ItemService()
    return await service.fetch(db, item_id)

@router.get("/items")
async def fetch_item(db: AsyncIOMotorClient = Depends(get_database)):
    service = ItemService()
    return await service.fetch_all(db)
