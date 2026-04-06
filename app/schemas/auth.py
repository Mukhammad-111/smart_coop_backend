import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.push_token import PushPlatform


class RegisterRequest(BaseModel):
    email: EmailStr = Field(max_length=255)
    first_name: str = Field(max_length=100, min_length=2)
    last_name: str = Field(max_length=100, min_length=2)
    password: str = Field(max_length=255, min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

    model_config = ConfigDict(from_attributes=True)


class LogoutRequest(BaseModel):
    token: str | None = None


class MessageResponse(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)


class PushTokenRequest(BaseModel):
    token: str = Field(..., min_length=60, max_length=500)
    platform: PushPlatform


class PushTokenDeleteRequest(BaseModel):
    token: str = Field(..., min_length=60, max_length=500)