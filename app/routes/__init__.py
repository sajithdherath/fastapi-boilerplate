from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as user_router
from .files import router as files
from .system import router as system_router

router = APIRouter()
router.include_router(auth_router, prefix="/oauth")
router.include_router(user_router, prefix="/users")
router.include_router(files, prefix="/files")
router.include_router(system_router)