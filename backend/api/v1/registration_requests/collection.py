from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.schemas.base import DataResponse
from core.users import current_user
from exceptions import AppException
from modules.registration.queries import RegistrationRequestQueries
from modules.registration.schemas.mutations import RegistrationRequestCreate
from modules.registration.schemas.responses import RegistrationRequestResponse
from modules.users.model import User
from operations.create_registration_request.contract import (
    CreateRegistrationRequestContract,
)
from operations.create_registration_request.scenario import (
    CreateRegistrationRequestScenario,
)

router = APIRouter()


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
