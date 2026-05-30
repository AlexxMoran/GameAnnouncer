from pydantic import BaseModel, Field


class RegistrationRequestBase(BaseModel):
    announcement_id: int = Field(..., description="The ID of the announcement")
