from fastapi import APIRouter

from .me import router as me_router
from .public import router as public_router

router = APIRouter()
router.include_router(me_router, prefix="/users", tags=["users"])
router.include_router(public_router, prefix="/users", tags=["users"])

__all__ = ["router"]
