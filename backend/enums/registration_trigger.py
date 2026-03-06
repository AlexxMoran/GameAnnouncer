from enum import Enum


class RegistrationTrigger(str, Enum):
    """
    Lifecycle triggers for the registration request state machine.

    APPROVE and REJECT are organizer-facing.
    CANCEL is user-facing.
    EXPIRE and SYSTEM_REJECT are system-only.
    """

    APPROVE = "approve"
    REJECT = "reject"
    CANCEL = "cancel"
    EXPIRE = "expire"
    SYSTEM_REJECT = "system_reject"
