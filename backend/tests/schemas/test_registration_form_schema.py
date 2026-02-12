from schemas.registration_form import (
    RegistrationFormCreate,
    RegistrationFormResponse,
    RegistrationFormUpdate,
)
from schemas.form_field import FormFieldCreate, FormFieldResponse
from enums import FormFieldType


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
