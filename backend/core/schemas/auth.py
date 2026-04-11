from pydantic import BaseModel, EmailStr, SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class RequestVerifyTokenRequest(BaseModel):
    email: EmailStr


class VerifyEmailRequest(BaseModel):
    token: SecretStr


class ResetPasswordRequest(BaseModel):
    token: SecretStr
    password: SecretStr
