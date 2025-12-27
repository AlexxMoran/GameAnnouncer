from fastapi import APIRouter
from .games import router as games_router
from .announcements import router as announcements_router
from .users import router as users_router
from .registration_requests import router as registration_requests_router

router = APIRouter(prefix="/v1")
router.include_router(games_router)
router.include_router(announcements_router)
router.include_router(users_router)
router.include_router(registration_requests_router)
