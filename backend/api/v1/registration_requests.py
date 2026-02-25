from enum import Enum

from fastapi import APIRouter, Depends

from exceptions import AppException
from core.schemas.base import DataResponse
from core.deps import SessionDep
from domains.users.model import User
from core.users import current_user

from domains.announcements.repository import AnnouncementRepository
from domains.registration.models import RegistrationRequest
from domains.registration.repository import RegistrationRequestRepository
from domains.registration.schemas import (
    RegistrationRequestCreate,
    RegistrationRequestResponse,
)
from domains.registration.services.create_request import (
    CreateRegistrationRequestService,
)
from domains.registration.services import update_status as registration_status
from core.permissions import authorize_action


router = APIRouter(prefix="/registration_requests", tags=["registration_requests"])


class RegistrationAction(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    CANCEL = "cancel"


async def get_registration_request_dependency(
    session: SessionDep,
    registration_request_id: int,
) -> RegistrationRequest:
    repo = RegistrationRequestRepository(session)
    registration_request = await repo.find_by_id(registration_request_id)
    if not registration_request:
        raise AppException("Registration Request not found", status_code=404)
    return registration_request


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


@router.post("", response_model=DataResponse[RegistrationRequestResponse])
async def create(
    session: SessionDep,
    registration_request_in: RegistrationRequestCreate,
    user: User = Depends(current_user),
) -> DataResponse[RegistrationRequestResponse]:
    announcement_repo = AnnouncementRepository(session)
    announcement = await announcement_repo.find_by_id(
        registration_request_in.announcement_id
    )
    if not announcement:
        raise AppException("Announcement not found", status_code=404)

    registration_request = await CreateRegistrationRequestService(
        session=session,
        announcement=announcement,
        user=user,
        registration_request_in=registration_request_in,
    ).call()

    return DataResponse(data=registration_request)


@router.patch(
    "/{registration_request_id}/{action}",
    response_model=DataResponse[RegistrationRequestResponse],
)
async def update_registration_request_status(
    action: RegistrationAction,
    session: SessionDep,
    cancellation_reason: str | None = None,
    registration_request: RegistrationRequest = Depends(
        get_registration_request_dependency
    ),
    user: User = Depends(current_user),
) -> DataResponse[RegistrationRequestResponse]:
    if action == RegistrationAction.APPROVE:
        result = await registration_status.approve(registration_request, user, session)
    elif action == RegistrationAction.REJECT:
        result = await registration_status.reject(
            registration_request, user, session, cancellation_reason
        )
    elif action == RegistrationAction.CANCEL:
        result = await registration_status.cancel(registration_request, user, session)
    else:
        raise AppException("Invalid action", status_code=400)

    return DataResponse(data=result)
