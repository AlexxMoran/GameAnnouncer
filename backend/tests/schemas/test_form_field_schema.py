from schemas.form_field import (
    FormFieldCreate,
    FormFieldResponse,
    FormFieldUpdate,
)
from enums import FormFieldType


def test_form_field_create():
    field = FormFieldCreate(
        field_type=FormFieldType.TEXT,
        label="Nickname",
        key="nickname",
        required=True,
        order=0,
    )
    assert field.field_type == FormFieldType.TEXT
    assert field.label == "Nickname"
    assert field.key == "nickname"
    assert field.required is True
    assert field.options is None


def test_form_field_create_with_options():
    field = FormFieldCreate(
        field_type=FormFieldType.SELECT,
        label="Game Role",
        key="role",
        required=True,
        order=1,
        options={"choices": ["Tank", "DPS", "Support"]},
    )
    assert field.field_type == FormFieldType.SELECT
    assert field.options is not None
    assert "choices" in field.options


def test_form_field_update():
    update = FormFieldUpdate(label="Updated Label")
    assert update.label == "Updated Label"
    assert update.field_type is None
    assert update.key is None


def test_form_field_update_all_fields():
    update = FormFieldUpdate(
        field_type=FormFieldType.TEXTAREA,
        label="Description",
        key="desc",
        required=False,
        order=2,
        options={"max_length": 500},
    )
    assert update.field_type == FormFieldType.TEXTAREA
    assert update.label == "Description"
    assert update.key == "desc"
    assert update.required is False
    assert update.options is not None


def test_form_field_response():
    field = FormFieldResponse(
        id=1,
        form_id=10,
        field_type=FormFieldType.NUMBER,
        label="Age",
        key="age",
        required=True,
        order=0,
    )
    assert field.id == 1
    assert field.form_id == 10
    assert field.field_type == FormFieldType.NUMBER
    assert field.label == "Age"
