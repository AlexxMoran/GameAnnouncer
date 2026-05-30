from fastapi import APIRouter

from .collection import router as collection_router
from .dependencies import get_game_dependency
from .detail import router as detail_router
from .media import router as media_router

router = APIRouter()
router.include_router(collection_router, prefix="/games", tags=["games"])
router.include_router(detail_router, prefix="/games", tags=["games"])
router.include_router(media_router, prefix="/games", tags=["games"])

__all__ = ["get_game_dependency", "router"]
