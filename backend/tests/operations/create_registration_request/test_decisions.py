import pytest

from exceptions import ValidationException
from operations.create_registration_request.decisions import (
    CreateRegistrationRequestDecisions,
)
from operations.create_registration_request.structures import (
    CreateRegistrationRequestSnapshot,
    RegistrationFormFieldSnapshot,
)


def _snapshot(**overrides) -> CreateRegistrationRequestSnapshot:
    data = {
        "announcement_id": 1,
        "user_id": 1,
        "request_data": {"announcement_id": 1},
        "form_responses": [],
        "is_registration_open": True,
        "has_existing_active_request": False,
        "form_fields": [],
    }
    data.update(overrides)
    return CreateRegistrationRequestSnapshot(**data)


def test_decision_allows_open_registration_without_form():
    decision = CreateRegistrationRequestDecisions().make(_snapshot())

    assert decision.user_id == 1
    assert decision.request_data == {"announcement_id": 1}


def test_decision_rejects_closed_registration():
    with pytest.raises(ValidationException, match="currently closed"):
        CreateRegistrationRequestDecisions().make(_snapshot(is_registration_open=False))


def test_decision_rejects_missing_required_form_response():
    with pytest.raises(ValidationException, match="Missing required fields"):
        CreateRegistrationRequestDecisions().make(
            _snapshot(
                form_fields=[
                    RegistrationFormFieldSnapshot(
                        id=1,
                        label="Discord",
                        required=True,
                    )
                ]
            )
        )
