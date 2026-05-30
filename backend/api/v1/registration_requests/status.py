from enum import Enum

from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import DataResponse
from core.users import current_user
from enums.registration_trigger import RegistrationTrigger
from exceptions import AppException
from modules.registration.models import RegistrationRequest
from modules.registration.queries import RegistrationRequestQueries
from modules.registration.schemas.responses import RegistrationRequestResponse
from modules.users.model import User
from operations.change_registration_request_status.contract import (
    ChangeRegistrationRequestStatusContract,
)
from operations.change_registration_request_status.scenario import (
    ChangeRegistrationRequestStatusScenario,
)

from .dependencies import get_registration_request_dependency

router = APIRouter()


class RegistrationAction(str, Enum):
    APPROVE = RegistrationTrigger.APPROVE.value
    REJECT = RegistrationTrigger.REJECT.value
    CANCEL = RegistrationTrigger.CANCEL.value


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
