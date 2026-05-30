from fastapi import APIRouter, Depends

from core.permissions import authorize_action
from core.schemas.base import DataResponse
from core.users import current_user
from modules.registration.models import RegistrationRequest
from modules.registration.schemas.responses import RegistrationRequestResponse
from modules.users.model import User

from .dependencies import get_registration_request_dependency

router = APIRouter()


@router.get(
    "/{registration_request_id}",
    response_model=DataResponse[RegistrationRequestResponse],
)
async def get_registration_request(
    registration_request: RegistrationRequest = Depends(
        get_registration_request_dependency
    ),
    user: User = Depends(current_user),
) -> DataResponse[RegistrationRequestResponse]:
    authorize_action(user, registration_request, "view")
    return DataResponse(data=registration_request)
