from base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class FormFieldResponse(Base):
    __tablename__ = "form_field_responses"

    registration_request_id: Mapped[int] = mapped_column(
        ForeignKey("registration_requests.id", ondelete="CASCADE"), nullable=False
    )
    form_field_id: Mapped[int] = mapped_column(
        ForeignKey("form_fields.id", ondelete="CASCADE"), nullable=False
    )
