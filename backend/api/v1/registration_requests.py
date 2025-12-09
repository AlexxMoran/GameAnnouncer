from fastapi import APIRouter, Depends, HTTPException
from enum import Enum
from schemas.registration_request import (
    RegistrationRequestCreate,
    RegistrationRequestResponse,
)
from schemas.base import DataResponse
from core.deps import SessionDep
from models.registration_request import RegistrationRequest
from models.user import User
from api.v1.crud.registration_request import registration_request_crud
from api.v1.announcements import get_announcement_dependency
from core.users import current_user


router = APIRouter(prefix="/registration_requests", tags=["registration_requests"])


class RegistrationAction(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    CANCEL = "cancel"


async def get_registration_request_dependency(
    session: SessionDep,
    registration_request_id: int,
) -> RegistrationRequest:
    registration_request = await registration_request_crud.get_by_id(
        session=session,
        registration_request_id=registration_request_id,
    )
    if not registration_request:
        raise HTTPException(status_code=404, detail="Registration Request not found")

    return registration_request


@router.get(
    "/{registration_request_id}",
    response_model=DataResponse[RegistrationRequestResponse],
)
async def get_registration_request(
    registration_request: RegistrationRequest = Depends(
        get_registration_request_dependency
    ),
):
    return DataResponse(data=registration_request)


@router.post("", response_model=DataResponse[RegistrationRequestResponse])
async def create(
    session: SessionDep,
    registration_request_in: RegistrationRequestCreate,
    user: User = Depends(current_user),
):
    await get_announcement_dependency(session, registration_request_in.announcement_id)

    existing_request = await registration_request_crud.get_by_user_and_announcement(
        session=session,
        user_id=user.id,
        announcement_id=registration_request_in.announcement_id,
    )
    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="Registration request already exists for this user and announcement.",
        )

    registration_request = await registration_request_crud.create(
        session=session, registration_request_in=registration_request_in, user=user
    )

    return DataResponse(data=registration_request)


@router.patch(
    "/{registration_request_id}/{action}",
    response_model=DataResponse[RegistrationRequestResponse],
)
async def update_registration_request_status(
    action: RegistrationAction,
    session: SessionDep,
    registration_request: RegistrationRequest = Depends(
        get_registration_request_dependency
    ),
    current_user: User = Depends(current_user),
):
    if action == RegistrationAction.APPROVE:
        result = await registration_request_crud.approve(
            session, registration_request, current_user
        )
    elif action == RegistrationAction.REJECT:
        result = await registration_request_crud.reject(
            session, registration_request, current_user
        )
    elif action == RegistrationAction.CANCEL:
        result = await registration_request_crud.cancel(
            session, registration_request, current_user
        )

    return DataResponse(data=result)
