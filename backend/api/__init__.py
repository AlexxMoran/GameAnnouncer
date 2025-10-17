from fastapi import APIRouter
from core.config import settings
from .v1 import router as v1_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(v1_router, prefix=settings.api.v1.prefix)


@router.get("/")
async def root():
    return {"message": "GameAnnouncer API is running! 🎮"}


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database_url": str(settings.db.url)[:50] + "...",
        "service": "GameAnnouncer",
    }
