"""
Authentication Data Transfer Objects
DTOs for authentication-related operations
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request DTO"""
    username: str = Field(..., min_length=1, max_length=255, description="Username or email")
    password: str = Field(..., min_length=1, description="Password")
    two_factor_token: Optional[str] = Field(None, description="Two-factor authentication token")
    remember_me: bool = Field(False, description="Remember user login")


class TokenResponse(BaseModel):
    """Token response DTO"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    user: dict = Field(..., description="User information")


class PasswordChangeRequest(BaseModel):
    """Password change request DTO"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")


class PasswordResetRequest(BaseModel):
    """Password reset request DTO"""
    email: EmailStr = Field(..., description="User email address")


class PasswordResetConfirmRequest(BaseModel):
    """Password reset confirmation DTO"""
    reset_token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")


class TwoFactorSetupRequest(BaseModel):
    """Two-factor authentication setup request DTO"""
    password: str = Field(..., description="Current password for verification")


class TwoFactorSetupResponse(BaseModel):
    """Two-factor authentication setup response DTO"""
    secret: str = Field(..., description="2FA secret key")
    qr_code_url: str = Field(..., description="QR code URL for authenticator app")
    backup_codes: list = Field(..., description="Backup codes")


class TwoFactorVerifyRequest(BaseModel):
    """Two-factor authentication verification request DTO"""
    token: str = Field(..., description="2FA token from authenticator app")
    backup_code: Optional[str] = Field(None, description="Backup code if token is lost")


class UserRegistrationRequest(BaseModel):
    """User registration request DTO"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., description="Confirm password")
    organization_id: str = Field(..., description="Organization ID")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    phone: Optional[str] = Field(None, description="Phone number")


class UserProfileUpdateRequest(BaseModel):
    """User profile update request DTO"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    phone: Optional[str] = Field(None, description="Phone number")


class SessionInfo(BaseModel):
    """Session information DTO"""
    user_id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email")
    role: str = Field(..., description="User role")
    organization_id: str = Field(..., description="Organization ID")
    permissions: dict = Field(..., description="User permissions")
    login_time: datetime = Field(..., description="Login timestamp")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")


class SecurityEventRequest(BaseModel):
    """Security event request DTO"""
    event_type: str = Field(..., description="Type of security event")
    description: str = Field(..., description="Event description")
    severity: str = Field(..., description="Event severity")
    metadata: Optional[dict] = Field(None, description="Additional event metadata")


class AuditLogFilter(BaseModel):
    """Audit log filter DTO"""
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    action: Optional[str] = Field(None, description="Filter by action")
    resource: Optional[str] = Field(None, description="Filter by resource")
    severity: Optional[str] = Field(None, description="Filter by severity")
    start_date: Optional[datetime] = Field(None, description="Filter from date")
    end_date: Optional[datetime] = Field(None, description="Filter to date")
    ip_address: Optional[str] = Field(None, description="Filter by IP address")
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")

