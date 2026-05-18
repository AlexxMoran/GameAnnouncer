from enum import Enum

from fastapi import APIRouter, Depends

from exceptions import AppException
from core.schemas.base import DataResponse
from core.deps import SessionDep
from modules.users.model import User
from core.users import current_user

from modules.registration.models import RegistrationRequest
from modules.registration.queries import RegistrationRequestQueries
from modules.registration.schemas import (
    RegistrationRequestCreate,
    RegistrationRequestResponse,
)
from operations.create_registration_request.contract import (
    CreateRegistrationRequestContract,
)
from operations.create_registration_request.scenario import (
    CreateRegistrationRequestScenario,
)
from operations.change_registration_request_status.contract import (
    ChangeRegistrationRequestStatusContract,
)
from operations.change_registration_request_status.scenario import (
    ChangeRegistrationRequestStatusScenario,
)
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
    queries = RegistrationRequestQueries(session)
    registration_request = await queries.find_by_id(registration_request_id)
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
    registration_request = await CreateRegistrationRequestScenario(session).run(
        CreateRegistrationRequestContract(
            registration_request_in=registration_request_in,
            user_id=user.id,
        )
    )
    await session.commit()
    queries = RegistrationRequestQueries(session)
    result = await queries.find_by_id(registration_request.id)
    if result is None:
        raise AppException(
            "Registration request not found after commit", status_code=500
        )
    return DataResponse(data=result)


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

    result = await ChangeRegistrationRequestStatusScenario(session).run(
        ChangeRegistrationRequestStatusContract(
            registration_request_id=registration_request.id,
            trigger=RegistrationTrigger(action.value),
            cancellation_reason=cancellation_reason,
        )
    )

    await session.commit()
    queries = RegistrationRequestQueries(session)
    refreshed = await queries.find_by_id(result.id)
    if refreshed is None:
        raise AppException(
            "Registration request not found after update", status_code=500
        )
    return DataResponse(data=refreshed)
