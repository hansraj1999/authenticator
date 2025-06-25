from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime


class SignUPRequest(BaseModel):
    # Name, email, password (and optionally phone).

    name: str
    email: EmailStr
    password: str  # must be at least 8 characters
    phone: str = Optional
    service_name: str = "shorturl"

    @field_validator("password")
    def password_must_be_at_least_8_chars(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class SignUPResponse(BaseModel):
    id: str
    name: str
    email: str
    service_name: str
    last_generated_otp_sent_at: str
    message: str = (
        "User created successfully Kindly check your email to verify your account"
    )


class VerifyOTPRequest(BaseModel):
    user_id: str
    otp: str
    service_name: Optional[str] = "shorturl"

    @field_validator("otp")
    def otp_must_be_at_least_4_chars(cls, v):
        if len(v) < 4:
            raise ValueError("OTP must be at least 4 characters")
        return v


class VerifyOTPPResponse(BaseModel):
    id: str
    name: str
    email: str
    service_name: str
    message: str = "OTP verified successfully"


class GetAllUsersRequest(BaseModel):
    page: int
    page_size: int

    @field_validator("page")
    def page_must_be_at_least_4_chars(cls, v):
        if v < 1:
            raise ValueError("Page must be at least 1")
        return v

    @field_validator("page_size")
    def page_size_must_be_at_least_4_chars(cls, v):
        if v < 1:
            raise ValueError("Page size must be at least 1")
        return v


class GetAllSessionsRequest(BaseModel):
    page: int
    page_size: int
    is_active: Optional[bool] = None

    @field_validator("page")
    def page_must_be_at_least_4_chars(cls, v):
        if v < 1:
            raise ValueError("Page must be at least 1")
        return v

    @field_validator("page_size")
    def page_size_must_be_at_least_4_chars(cls, v):
        if v < 1:
            raise ValueError("Page size must be at least 1")
        return v


class UserResponse(BaseModel):
    id: str
    name: Optional[str]
    email: str
    is_email_verified: bool
    created_at: datetime
    updated_at: datetime
    service_name: str
    last_generated_otp: Optional[str]
    last_generated_otp_sent_at: Optional[datetime]
    password_hash: str

    class Config:
        orm_mode = True


class GetAllUsersResponse(BaseModel):
    users: List[UserResponse]

    class Config:
        orm_mode = True


class SessionResponse(BaseModel):
    id: str
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class GetAllSessionsResponse(BaseModel):
    sessions: List[SessionResponse]

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    keep_signed_in: bool
    service_name: str = "shorturl"

    @field_validator("password")
    def password_must_be_at_least_8_chars(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginResponse(BaseModel):
    id: str
    name: str
    service_name: str
    token: str
    message: str = "User logged in successfully"
    expires_at: Optional[datetime] = None


class LogoutResponse(BaseModel):
    message: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr  # reset token or OTP
    new_password: str
    service_name: Optional[str] = "shorturl"


class ResetPasswordResponse(BaseModel):
    message: str
