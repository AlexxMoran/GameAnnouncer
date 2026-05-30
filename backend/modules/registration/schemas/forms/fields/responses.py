from pydantic import ConfigDict

from modules.registration.schemas.forms.fields.base import FormFieldBase


class FormFieldResponse(FormFieldBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    form_id: int
