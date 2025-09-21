"""
User Data Transfer Objects
DTOs for user management operations
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...domain.entities.user import User, UserRole, UserStatus


class UserCreateRequest(BaseModel):
    """User creation request DTO"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    role: str = Field(..., description="User role")
    organization_id: str = Field(..., description="Organization ID")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    phone: Optional[str] = Field(None, description="Phone number")
    password: str = Field(..., min_length=8, description="Password")
    
    @validator('role')
    def validate_role(cls, v):
        valid_roles = [role.value for role in UserRole]
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v


class UserUpdateRequest(BaseModel):
    """User update request DTO"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    phone: Optional[str] = Field(None, description="Phone number")


class UserResponse(BaseModel):
    """User response DTO"""
    id: UUID = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    full_name: str = Field(..., description="Full name")
    role: str = Field(..., description="User role")
    status: str = Field(..., description="User status")
    organization_id: str = Field(..., description="Organization ID")
    department: Optional[str] = Field(None, description="Department")
    job_title: Optional[str] = Field(None, description="Job title")
    phone: Optional[str] = Field(None, description="Phone number")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    email_verified: bool = Field(..., description="Email verification status")
    two_factor_enabled: bool = Field(..., description="Two-factor authentication status")
    permissions: Dict[str, bool] = Field(..., description="User permissions")
    
    @classmethod
    def from_user(cls, user: User) -> "UserResponse":
        """Create UserResponse from User entity"""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.get_full_name(),
            role=user.role.value,
            status=user.status.value,
            organization_id=user.organization_id,
            department=user.department,
            job_title=user.job_title,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            email_verified=user.email_verified,
            two_factor_enabled=user.two_factor_enabled,
            permissions=user.get_permissions().__dict__
        )


class UserListResponse(BaseModel):
    """User list response DTO"""
    users: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum number of records")


class UserRoleChangeRequest(BaseModel):
    """User role change request DTO"""
    role: str = Field(..., description="New user role")
    reason: str = Field(..., min_length=1, description="Reason for role change")
    
    @validator('role')
    def validate_role(cls, v):
        valid_roles = [role.value for role in UserRole]
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v


class UserStatusChangeRequest(BaseModel):
    """User status change request DTO"""
    status: str = Field(..., description="New user status")
    reason: str = Field(..., min_length=1, description="Reason for status change")
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = [status.value for status in UserStatus]
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v


class UserBulkUpdateRequest(BaseModel):
    """User bulk update request DTO"""
    user_ids: List[UUID] = Field(..., min_items=1, description="List of user IDs to update")
    updates: Dict[str, Any] = Field(..., description="Updates to apply")


class UserSearchRequest(BaseModel):
    """User search request DTO"""
    query: str = Field(..., min_length=1, description="Search query")
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters")


class UserStatisticsResponse(BaseModel):
    """User statistics response DTO"""
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    inactive_users: int = Field(..., description="Number of inactive users")
    suspended_users: int = Field(..., description="Number of suspended users")
    pending_activation: int = Field(..., description="Number of pending activation users")
    locked_users: int = Field(..., description="Number of locked users")
    users_by_role: Dict[str, int] = Field(..., description="User count by role")
    users_by_department: Dict[str, int] = Field(..., description="User count by department")
    recent_registrations: int = Field(..., description="Users registered in last 30 days")
    two_factor_enabled: int = Field(..., description="Users with 2FA enabled")
    email_verified: int = Field(..., description="Users with verified email")


class UserProfileRequest(BaseModel):
    """User profile update request DTO"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    phone: Optional[str] = Field(None, description="Phone number")


class UserPasswordChangeRequest(BaseModel):
    """User password change request DTO"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserPermissionsRequest(BaseModel):
    """User permissions request DTO"""
    user_id: UUID = Field(..., description="User ID")
    permissions: Dict[str, bool] = Field(..., description="Permission overrides")


class UserActivityRequest(BaseModel):
    """User activity request DTO"""
    user_id: UUID = Field(..., description="User ID")
    days_back: int = Field(30, ge=1, le=365, description="Number of days to look back")
    include_failed_logins: bool = Field(False, description="Include failed login attempts")


class UserActivityResponse(BaseModel):
    """User activity response DTO"""
    user_id: UUID = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    total_activities: int = Field(..., description="Total activities")
    successful_logins: int = Field(..., description="Successful logins")
    failed_logins: int = Field(..., description="Failed logins")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")
    activities: List[Dict[str, Any]] = Field(..., description="Recent activities")
