import pytest

from enums.registration_status import RegistrationStatus
from enums.registration_trigger import RegistrationTrigger
from exceptions import ValidationException
from operations.change_registration_request_status.decisions import (
    ChangeRegistrationRequestStatusDecisions,
)
from operations.change_registration_request_status.structures import (
    ChangeRegistrationRequestStatusSnapshot,
)


def _snapshot(status: RegistrationStatus) -> ChangeRegistrationRequestStatusSnapshot:
    return ChangeRegistrationRequestStatusSnapshot(
        registration_request_id=1,
        announcement_id=1,
        user_id=1,
        status=status,
        cancellation_reason=None,
    )


def test_approve_pending_creates_participant_and_checks_capacity():
    decision = ChangeRegistrationRequestStatusDecisions(
        RegistrationTrigger.APPROVE
    ).make(_snapshot(RegistrationStatus.PENDING))

    assert decision.new_status == RegistrationStatus.APPROVED
    assert decision.create_participant is True
    assert decision.check_capacity is True


def test_cancel_approved_removes_participant():
    decision = ChangeRegistrationRequestStatusDecisions(
        RegistrationTrigger.CANCEL
    ).make(_snapshot(RegistrationStatus.APPROVED))

    assert decision.new_status == RegistrationStatus.CANCELLED
    assert decision.delete_participant is True


def test_invalid_transition_raises():
    with pytest.raises(ValidationException):
        ChangeRegistrationRequestStatusDecisions(RegistrationTrigger.APPROVE).make(
            _snapshot(RegistrationStatus.REJECTED)
        )
