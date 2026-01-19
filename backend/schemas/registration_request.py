from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegistrationRequestBase(BaseModel):
    announcement_id: int = Field(..., description="The ID of the announcement")


class RegistrationRequestCreate(RegistrationRequestBase):
    pass


class RegistrationRequestUpdate(BaseModel):
    status: Optional[str] = Field(
        None, description="The status of the registration request"
    )


class RegistrationRequestResponse(RegistrationRequestBase):
    id: int
    user_id: int = Field(
        ..., description="The ID of the user who made the registration request"
    )
    status: str = Field(..., description="The status of the registration request")
    cancellation_reason: str | None = Field(
        None, description="Reason for cancellation/decline of the registration request"
    )
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
