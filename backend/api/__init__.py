from fastapi import APIRouter
from core.config import settings

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "GameAnnouncer API is running! 🎮"}

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database_url": str(settings.db.url)[:50] + "...",
        "service": "GameAnnouncer"
    }
