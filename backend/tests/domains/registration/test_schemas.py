from datetime import datetime, timezone

from domains.announcements.schemas import AnnouncementForRegistrationResponse
from domains.games.schemas import GameForAnnouncementResponse
from domains.participants.schemas import AnnouncementParticipantResponse
from domains.registration.schemas import (
    RegistrationRequestCreate,
    RegistrationRequestResponse,
    RegistrationRequestUpdate,
)
from domains.registration.form_schemas import (
    RegistrationFormCreate,
    RegistrationFormResponse,
    RegistrationFormUpdate,
    FormFieldCreate,
    FormFieldResponse,
    FormFieldUpdate,
    FormFieldResponseCreate,
    FormFieldResponseResponse,
    FormFieldResponseUpdate,
)
from enums import FormFieldType


def _make_participant(n: int = 1) -> AnnouncementParticipantResponse:
    now = datetime.now(timezone.utc)
    return AnnouncementParticipantResponse(
        id=n,
        announcement_id=1,
        user_id=n,
        created_at=now,
        updated_at=now,
    )


def _make_game_response(**overrides) -> GameForAnnouncementResponse:
    data = {"id": 1, "name": "CS2", "image_url": None, "category": "FPS"}
    data.update(overrides)
    return GameForAnnouncementResponse(**data)


def _make_announcement_for_registration(
    **overrides,
) -> AnnouncementForRegistrationResponse:
    data = {
        "id": 1,
        "title": "Spring Cup",
        "content": None,
        "format": "single_elimination",
        "registration_end_at": datetime.now(timezone.utc),
        "game": _make_game_response(),
        "participants": [],
    }
    data.update(overrides)
    return AnnouncementForRegistrationResponse(**data)


def test_announcement_for_registration_response_participants_count_empty():
    ann = _make_announcement_for_registration(participants=[])
    assert ann.participants_count == 0


def test_announcement_for_registration_response_participants_count_with_participants():
    participants = [_make_participant(n) for n in range(1, 4)]
    ann = _make_announcement_for_registration(participants=participants)
    assert ann.participants_count == 3


def test_announcement_for_registration_response_contains_game():
    game = _make_game_response(id=5, name="Dota 2", category="MOBA")
    ann = _make_announcement_for_registration(game=game)
    assert ann.game.id == 5
    assert ann.game.name == "Dota 2"
    assert ann.game.category == "MOBA"


def test_announcement_for_registration_response_participants_excluded_from_serialization():
    participants = [_make_participant(n) for n in range(1, 3)]
    ann = _make_announcement_for_registration(participants=participants)
    serialized = ann.model_dump()
    assert "participants" not in serialized
    assert serialized["participants_count"] == 2


def test_registration_request_create():
    create = RegistrationRequestCreate(announcement_id=10)
    assert create.announcement_id == 10


def test_registration_request_response():
    now = datetime.now(timezone.utc)
    ann = _make_announcement_for_registration()
    resp = RegistrationRequestResponse(
        id=1,
        announcement_id=ann.id,
        user_id=2,
        status="pending",
        announcement=ann,
        created_at=now,
        updated_at=now,
    )
    assert resp.user_id == 2
    assert resp.status == "pending"
    assert resp.cancellation_reason is None
    assert resp.announcement.id == ann.id
    assert resp.announcement.game.name == "CS2"


def test_registration_request_response_with_cancellation_reason():
    now = datetime.now(timezone.utc)
    ann = _make_announcement_for_registration()
    resp = RegistrationRequestResponse(
        id=1,
        announcement_id=ann.id,
        user_id=2,
        status="cancelled",
        cancellation_reason="User cancelled",
        announcement=ann,
        created_at=now,
        updated_at=now,
    )
    assert resp.cancellation_reason == "User cancelled"


def test_registration_request_response_announcement_participants_count():
    now = datetime.now(timezone.utc)
    ann = _make_announcement_for_registration(
        participants=[_make_participant(n) for n in range(1, 3)]
    )
    resp = RegistrationRequestResponse(
        id=1,
        announcement_id=ann.id,
        user_id=2,
        status="approved",
        announcement=ann,
        created_at=now,
        updated_at=now,
    )
    assert resp.announcement.participants_count == 2


def test_registration_request_update():
    update = RegistrationRequestUpdate(status="approved")
    assert update.status == "approved"


def test_registration_form_create():
    fields = [
        FormFieldCreate(
            field_type=FormFieldType.TEXT,
            label="Nickname",
            required=True,
        )
    ]
    form = RegistrationFormCreate(fields=fields)
    assert len(form.fields) == 1
    assert form.fields[0].label == "Nickname"


def test_registration_form_create_empty_fields():
    form = RegistrationFormCreate()
    assert form.fields == []


def test_registration_form_update():
    fields = [
        FormFieldCreate(
            field_type=FormFieldType.TEXT,
            label="Updated Field",
            required=False,
        )
    ]
    update = RegistrationFormUpdate(fields=fields)
    assert update.fields is not None
    assert len(update.fields) == 1


def test_registration_form_update_none_fields():
    update = RegistrationFormUpdate()
    assert update.fields is None


def test_registration_form_response():
    field = FormFieldResponse(
        id=1,
        form_id=1,
        field_type=FormFieldType.TEXT,
        label="Test Field",
        required=True,
    )
    resp = RegistrationFormResponse(id=1, announcement_id=10, fields=[field])
    assert resp.id == 1
    assert resp.announcement_id == 10
    assert len(resp.fields) == 1
    assert resp.fields[0].label == "Test Field"


def test_form_field_create():
    field = FormFieldCreate(
        field_type=FormFieldType.TEXT,
        label="Nickname",
        required=True,
    )
    assert field.field_type == FormFieldType.TEXT
    assert field.label == "Nickname"
    assert field.required is True
    assert field.options is None


def test_form_field_create_with_options():
    field = FormFieldCreate(
        field_type=FormFieldType.SELECT,
        label="Game Role",
        required=True,
        options=["Tank", "DPS", "Support"],
    )
    assert field.field_type == FormFieldType.SELECT
    assert field.options is not None
    assert "Tank" in field.options


def test_form_field_update():
    update = FormFieldUpdate(label="Updated Label")
    assert update.label == "Updated Label"
    assert update.field_type is None


def test_form_field_response():
    field = FormFieldResponse(
        id=1,
        form_id=10,
        field_type=FormFieldType.NUMBER,
        label="Age",
        required=True,
    )
    assert field.id == 1
    assert field.form_id == 10
    assert field.field_type == FormFieldType.NUMBER
    assert field.label == "Age"


def test_form_field_response_create():
    response = FormFieldResponseCreate(form_field_id=5, value="John Doe")
    assert response.form_field_id == 5
    assert response.value == "John Doe"


def test_form_field_response_update():
    update = FormFieldResponseUpdate(value="Jane Doe")
    assert update.value == "Jane Doe"


def test_form_field_response_update_none():
    update = FormFieldResponseUpdate()
    assert update.value is None


def test_form_field_response_response():
    response = FormFieldResponseResponse(
        id=1, registration_request_id=10, form_field_id=5, value="Test Value"
    )
    assert response.id == 1
    assert response.registration_request_id == 10
    assert response.form_field_id == 5
    assert response.value == "Test Value"
