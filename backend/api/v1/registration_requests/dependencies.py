from exceptions import AppException
from core.deps import SessionDep
from modules.registration.models import RegistrationRequest
from modules.registration.queries import RegistrationRequestQueries


async def get_registration_request_dependency(
    session: SessionDep,
    registration_request_id: int,
) -> RegistrationRequest:
    queries = RegistrationRequestQueries(session)
    registration_request = await queries.find_by_id(registration_request_id)
    if not registration_request:
        raise AppException("Registration Request not found", status_code=404)
    return registration_request
