from fastapi import APIRouter

from .authenticaion import router as auth_router
from .users import router as user_router
from .system import router as system_router

router = APIRouter()
router.include_router(auth_router, prefix="/oauth")
router.include_router(user_router, prefix="/users")
router.include_router(system_router)
