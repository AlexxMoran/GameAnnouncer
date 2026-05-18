from exceptions import ValidationException
from operations.create_registration_request.structures import (
    CreateRegistrationRequestDecision,
    CreateRegistrationRequestSnapshot,
)


class CreateRegistrationRequestDecisions:
    """Business rules for creating a registration request."""

    def make(
        self,
        snapshot: CreateRegistrationRequestSnapshot,
    ) -> CreateRegistrationRequestDecision:
        self._validate(snapshot)

        return CreateRegistrationRequestDecision(
            request_data=snapshot.request_data,
            user_id=snapshot.user_id,
            form_responses=snapshot.form_responses,
        )

    def _validate(self, snapshot: CreateRegistrationRequestSnapshot) -> None:
        if not snapshot.is_registration_open:
            raise ValidationException(
                "Registration is currently closed for this announcement"
            )

        if snapshot.has_existing_active_request:
            raise ValidationException(
                "Registration request already exists for this user and announcement"
            )

        if not snapshot.form_fields and snapshot.form_responses:
            raise ValidationException(
                "This announcement does not have a registration form. No form responses are required."
            )

        if snapshot.form_fields:
            self._validate_form_responses(snapshot)

    @staticmethod
    def _validate_form_responses(snapshot: CreateRegistrationRequestSnapshot) -> None:
        field_ids = {field.id for field in snapshot.form_fields}
        required_field_ids = {
            field.id for field in snapshot.form_fields if field.required
        }
        provided_field_ids = {
            response.form_field_id for response in snapshot.form_responses
        }

        invalid_field_ids = provided_field_ids - field_ids
        if invalid_field_ids:
            raise ValidationException(
                f"Invalid form field IDs: {invalid_field_ids}. "
                "These fields do not belong to this announcement's registration form."
            )

        missing_required_fields = required_field_ids - provided_field_ids
        if missing_required_fields:
            missing_labels = [
                field.label
                for field in snapshot.form_fields
                if field.id in missing_required_fields
            ]
            raise ValidationException(
                f"Missing required fields: {', '.join(missing_labels)}"
            )
