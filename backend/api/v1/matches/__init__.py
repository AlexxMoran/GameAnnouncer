from fastapi import APIRouter

from .dependencies import get_announcement_for_match_dependency, get_match_dependency
from .detail import router as detail_router
from .results import router as results_router

router = APIRouter()
router.include_router(detail_router, prefix="/matches", tags=["matches"])
router.include_router(results_router, prefix="/matches", tags=["matches"])

__all__ = [
    "get_announcement_for_match_dependency",
    "get_match_dependency",
    "router",
]
