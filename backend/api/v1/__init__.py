from fastapi import APIRouter
from core.config import get_settings
from .games import router as games_router
from .announcements import router as announcements_router
from .users import router as users_router
from .registration_requests import router as registration_requests_router

settings = get_settings()

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(games_router)
router.include_router(announcements_router)
router.include_router(users_router)
router.include_router(registration_requests_router)
