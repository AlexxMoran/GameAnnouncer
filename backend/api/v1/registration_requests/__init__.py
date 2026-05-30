from fastapi import APIRouter

from .collection import router as collection_router
from .dependencies import get_registration_request_dependency
from .detail import router as detail_router
from .status import RegistrationAction
from .status import router as status_router

router = APIRouter()
router.include_router(
    detail_router, prefix="/registration_requests", tags=["registration_requests"]
)
router.include_router(
    collection_router, prefix="/registration_requests", tags=["registration_requests"]
)
router.include_router(
    status_router, prefix="/registration_requests", tags=["registration_requests"]
)

__all__ = ["RegistrationAction", "get_registration_request_dependency", "router"]
