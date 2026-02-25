from datetime import datetime, timezone
from domains.registration.schemas import (
    RegistrationRequestCreate,
    RegistrationRequestResponse,
    RegistrationRequestUpdate,
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


def test_registration_form_create():
    fields = [
        FormFieldCreate(
            field_type=FormFieldType.TEXT,
            label="Nickname",
            required=True,
            order=0,
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
            order=0,
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
        order=0,
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
        order=0,
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
        order=1,
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
        order=0,
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
