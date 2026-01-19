from schemas.form_field_response import (
    FormFieldResponseCreate,
    FormFieldResponseResponse,
    FormFieldResponseUpdate,
)


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
