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
from domains.registration.services.lifecycle import RegistrationLifecycleService
from core.permissions import authorize_action
from enums.registration_trigger import RegistrationTrigger

router = APIRouter(prefix="/registration_requests", tags=["registration_requests"])


class RegistrationAction(str, Enum):
    APPROVE = RegistrationTrigger.APPROVE.value
    REJECT = RegistrationTrigger.REJECT.value
    CANCEL = RegistrationTrigger.CANCEL.value


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
    await session.commit()
    await session.refresh(registration_request)
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
    authorize_action(user, registration_request, action.value)

    lifecycle = RegistrationLifecycleService(
        registration_request, registration_request.announcement, session
    )

    if action == RegistrationAction.APPROVE:
        result = await lifecycle.approve()
    elif action == RegistrationAction.REJECT:
        result = await lifecycle.reject(reason=cancellation_reason)
    elif action == RegistrationAction.CANCEL:
        result = await lifecycle.cancel()
    else:
        raise AppException("Invalid action", status_code=400)

    await session.commit()
    await session.refresh(result)
    return DataResponse(data=result)
