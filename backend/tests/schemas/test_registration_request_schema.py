from datetime import datetime, timezone
from schemas.registration_request import (
    RegistrationRequestCreate,
    RegistrationRequestResponse,
    RegistrationRequestUpdate,
)


def test_registration_request_create():
    create = RegistrationRequestCreate(announcement_id=10)
    assert create.announcement_id == 10


def test_registration_request_response():
    now = datetime.now(timezone.utc)
    resp = RegistrationRequestResponse(
        id=1,
        announcement_id=10,
        user_id=2,
        status="pending",
        created_at=now,
        updated_at=now,
    )
    assert resp.user_id == 2
    assert resp.status == "pending"
    assert resp.cancellation_reason is None


def test_registration_request_response_with_cancellation_reason():
    now = datetime.now(timezone.utc)
    resp = RegistrationRequestResponse(
        id=1,
        announcement_id=10,
        user_id=2,
        status="cancelled",
        cancellation_reason="User cancelled",
        created_at=now,
        updated_at=now,
    )
    assert resp.cancellation_reason == "User cancelled"


def test_registration_request_update():
    update = RegistrationRequestUpdate(status="approved")
    assert update.status == "approved"
