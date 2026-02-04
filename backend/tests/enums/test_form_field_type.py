from enums.form_field_type import FormFieldType


def test_form_field_type_has_all_types():
    assert FormFieldType.TEXT == "text"
    assert FormFieldType.TEXTAREA == "textarea"
    assert FormFieldType.NUMBER == "number"
    assert FormFieldType.SELECT == "select"
    assert FormFieldType.RADIO == "radio"
    assert FormFieldType.CHECKBOX == "checkbox"
    assert FormFieldType.BOOLEAN == "boolean"
    assert FormFieldType.DATE == "date"


def test_form_field_type_is_string_enum():
    assert isinstance(FormFieldType.TEXT, str)
    assert isinstance(FormFieldType.SELECT, str)


def test_form_field_type_values():
    values = [e.value for e in FormFieldType]
    assert "text" in values
    assert "textarea" in values
    assert "number" in values
    assert "select" in values
    assert "radio" in values
    assert "checkbox" in values
    assert "boolean" in values
    assert "date" in values
    assert len(values) == 8
