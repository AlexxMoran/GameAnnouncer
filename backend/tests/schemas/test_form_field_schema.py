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
    assert "DPS" in field.options
    assert "Support" in field.options


def test_form_field_update():
    update = FormFieldUpdate(label="Updated Label")
    assert update.label == "Updated Label"
    assert update.field_type is None


def test_form_field_update_all_fields():
    update = FormFieldUpdate(
        field_type=FormFieldType.TEXTAREA,
        label="Description",
        required=False,
        order=2,
        options=["Option A", "Option B"],
    )
    assert update.field_type == FormFieldType.TEXTAREA
    assert update.label == "Description"
    assert update.required is False
    assert update.options is not None


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
