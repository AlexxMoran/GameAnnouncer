from core.search.base_filter import BaseFilter
from enums.registration_status import RegistrationStatus


class RegistrationRequestFilter(BaseFilter):
    """
    Filter for RegistrationRequest queries.

    Allows filtering only by status.
    """

    status: RegistrationStatus | None = None
