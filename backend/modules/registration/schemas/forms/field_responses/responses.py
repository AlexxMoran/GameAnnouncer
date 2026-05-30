from pydantic import ConfigDict, computed_field

from modules.registration.schemas.forms.field_responses.base import (
    FormFieldResponseBase,
)
from modules.registration.schemas.forms.fields.responses import FormFieldResponse


class FormFieldResponseResponse(FormFieldResponseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    registration_request_id: int
    form_field: FormFieldResponse | None = None

    @computed_field
    @property
    def label(self) -> str | None:
        """The question/label shown to the user (e.g. 'Nickname in Game')."""
        return self.form_field.label if self.form_field else None
