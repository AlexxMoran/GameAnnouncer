from datetime import datetime, timezone
from schemas.registration_request import (
    RegistrationRequestCreate,
    RegistrationRequestResponse,
)


def test_registration_request_create_and_response():
    create = RegistrationRequestCreate(announcement_id=10)
    assert create.announcement_id == 10
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
