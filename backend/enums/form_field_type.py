from enum import Enum


class FormFieldType(str, Enum):
    """Types of form fields for registration forms."""

    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    SELECT = "select"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    BOOLEAN = "boolean"
    DATE = "date"
