from fastapi import APIRouter

from .bracket import router as bracket_router
from .collection import router as collection_router
from .dependencies import get_announcement_dependency
from .detail import router as detail_router
from .lifecycle import router as lifecycle_router
from .media import router as media_router
from .participants import router as participants_router
from .registration_requests import router as registration_requests_router

router = APIRouter()
router.include_router(
    collection_router, prefix="/announcements", tags=["announcements"]
)
router.include_router(detail_router, prefix="/announcements", tags=["announcements"])
router.include_router(
    participants_router, prefix="/announcements", tags=["announcements"]
)
router.include_router(
    registration_requests_router, prefix="/announcements", tags=["announcements"]
)
router.include_router(lifecycle_router, prefix="/announcements", tags=["announcements"])
router.include_router(bracket_router, prefix="/announcements", tags=["announcements"])
router.include_router(media_router, prefix="/announcements", tags=["announcements"])

__all__ = ["get_announcement_dependency", "router"]
