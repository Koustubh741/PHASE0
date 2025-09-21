"""
User Domain Entity
Core business logic for User management in GRC Platform
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
import hashlib
import secrets


class UserStatus(Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_ACTIVATION = "pending_activation"
    LOCKED = "locked"


class UserRole(Enum):
    """User role enumeration"""
    ADMIN = "admin"
    AUDITOR = "auditor"
    RISK_OWNER = "risk_owner"
    CONTROL_OWNER = "control_owner"
    COMPLIANCE_MANAGER = "compliance_manager"
    POLICY_OWNER = "policy_owner"
    VIEWER = "viewer"


@dataclass
class UserPermissions:
    """User permissions value object"""
    can_create_policies: bool = False
    can_edit_policies: bool = False
    can_delete_policies: bool = False
    can_approve_policies: bool = False
    can_create_risks: bool = False
    can_edit_risks: bool = False
    can_assign_risks: bool = False
    can_create_controls: bool = False
    can_edit_controls: bool = False
    can_manage_users: bool = False
    can_view_audit_logs: bool = False
    can_export_data: bool = False
    can_manage_workflows: bool = False
    
    @classmethod
    def for_role(cls, role: UserRole) -> "UserPermissions":
        """Get permissions for a specific role"""
        permissions_map = {
            UserRole.ADMIN: cls(
                can_create_policies=True,
                can_edit_policies=True,
                can_delete_policies=True,
                can_approve_policies=True,
                can_create_risks=True,
                can_edit_risks=True,
                can_assign_risks=True,
                can_create_controls=True,
                can_edit_controls=True,
                can_manage_users=True,
                can_view_audit_logs=True,
                can_export_data=True,
                can_manage_workflows=True
            ),
            UserRole.AUDITOR: cls(
                can_view_audit_logs=True,
                can_export_data=True,
                can_edit_risks=True,
                can_edit_controls=True
            ),
            UserRole.RISK_OWNER: cls(
                can_create_risks=True,
                can_edit_risks=True,
                can_assign_risks=True,
                can_create_controls=True,
                can_edit_controls=True
            ),
            UserRole.CONTROL_OWNER: cls(
                can_create_controls=True,
                can_edit_controls=True,
                can_create_risks=True,
                can_edit_risks=True
            ),
            UserRole.COMPLIANCE_MANAGER: cls(
                can_create_policies=True,
                can_edit_policies=True,
                can_approve_policies=True,
                can_view_audit_logs=True,
                can_manage_workflows=True
            ),
            UserRole.POLICY_OWNER: cls(
                can_create_policies=True,
                can_edit_policies=True,
                can_approve_policies=True
            ),
            UserRole.VIEWER: cls()
        }
        return permissions_map.get(role, cls())


@dataclass
class User:
    """User domain entity"""
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    organization_id: str
    department: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_hash: Optional[str] = None
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    email_verification_token: Optional[str] = None
    email_verified: bool = False
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def create_new(
        cls,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        role: UserRole,
        organization_id: str,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
        phone: Optional[str] = None,
        password: Optional[str] = None
    ) -> "User":
        """Create a new user"""
        now = datetime.utcnow()
        
        # Generate email verification token
        email_verification_token = secrets.token_urlsafe(32)
        
        user = cls(
            id=uuid4(),
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            status=UserStatus.PENDING_ACTIVATION,
            organization_id=organization_id,
            department=department,
            job_title=job_title,
            phone=phone,
            created_at=now,
            updated_at=now,
            email_verification_token=email_verification_token,
            email_verified=False
        )
        
        if password:
            user.set_password(password)
        
        return user
    
    def set_password(self, password: str) -> None:
        """Set user password with secure hashing"""
        import bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        self.updated_at = datetime.utcnow()
    
    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        if not self.password_hash:
            return False
        
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def activate(self) -> None:
        """Activate user account"""
        if self.status not in [UserStatus.PENDING_ACTIVATION, UserStatus.INACTIVE]:
            raise ValueError("User cannot be activated from current status")
        
        self.status = UserStatus.ACTIVE
        self.email_verified = True
        self.email_verification_token = None
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate user account"""
        if self.status == UserStatus.ADMIN:
            raise ValueError("Cannot deactivate admin users")
        
        self.status = UserStatus.INACTIVE
        self.updated_at = datetime.utcnow()
    
    def suspend(self, reason: str = None) -> None:
        """Suspend user account"""
        if self.status == UserStatus.ADMIN:
            raise ValueError("Cannot suspend admin users")
        
        self.status = UserStatus.SUSPENDED
        if reason:
            self.metadata["suspension_reason"] = reason
        self.updated_at = datetime.utcnow()
    
    def lock_account(self, duration_minutes: int = 30) -> None:
        """Lock user account due to failed login attempts"""
        self.status = UserStatus.LOCKED
        self.locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.updated_at = datetime.utcnow()
    
    def unlock_account(self) -> None:
        """Unlock user account"""
        if self.status == UserStatus.LOCKED:
            self.status = UserStatus.ACTIVE
            self.locked_until = None
            self.failed_login_attempts = 0
            self.updated_at = datetime.utcnow()
    
    def record_login_attempt(self, successful: bool) -> None:
        """Record login attempt"""
        if successful:
            self.failed_login_attempts = 0
            self.last_login = datetime.utcnow()
            if self.status == UserStatus.LOCKED and self.locked_until and datetime.utcnow() > self.locked_until:
                self.unlock_account()
        else:
            self.failed_login_attempts += 1
            if self.failed_login_attempts >= 5:
                self.lock_account()
        
        self.updated_at = datetime.utcnow()
    
    def generate_password_reset_token(self) -> str:
        """Generate password reset token"""
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        self.updated_at = datetime.utcnow()
        return self.password_reset_token
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password with token"""
        if (not self.password_reset_token or 
            self.password_reset_token != token or
            not self.password_reset_expires or
            datetime.utcnow() > self.password_reset_expires):
            return False
        
        self.set_password(new_password)
        self.password_reset_token = None
        self.password_reset_expires = None
        self.updated_at = datetime.utcnow()
        return True
    
    def change_role(self, new_role: UserRole, changed_by: str) -> None:
        """Change user role"""
        if self.role == UserRole.ADMIN and new_role != UserRole.ADMIN:
            # Log admin role change
            self.metadata[f"role_change_{datetime.utcnow().isoformat()}"] = {
                "from": self.role.value,
                "to": new_role.value,
                "changed_by": changed_by
            }
        
        self.role = new_role
        self.updated_at = datetime.utcnow()
    
    def get_permissions(self) -> UserPermissions:
        """Get user permissions based on role"""
        return UserPermissions.for_role(self.role)
    
    def has_permission(self, permission_name: str) -> bool:
        """Check if user has specific permission"""
        permissions = self.get_permissions()
        return getattr(permissions, permission_name, False)
    
    def update_profile(self, **kwargs) -> None:
        """Update user profile information"""
        allowed_fields = ['first_name', 'last_name', 'department', 'job_title', 'phone']
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(self, field, value)
        
        self.updated_at = datetime.utcnow()
    
    def enable_two_factor(self) -> str:
        """Enable two-factor authentication"""
        import pyotp
        secret = pyotp.random_base32()
        self.two_factor_secret = secret
        self.two_factor_enabled = True
        self.updated_at = datetime.utcnow()
        return secret
    
    def disable_two_factor(self) -> None:
        """Disable two-factor authentication"""
        self.two_factor_enabled = False
        self.two_factor_secret = None
        self.updated_at = datetime.utcnow()
    
    def verify_two_factor_token(self, token: str) -> bool:
        """Verify two-factor authentication token"""
        if not self.two_factor_enabled or not self.two_factor_secret:
            return False
        
        import pyotp
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token, valid_window=1)
    
    def is_locked(self) -> bool:
        """Check if account is locked"""
        return (self.status == UserStatus.LOCKED and 
                self.locked_until and 
                datetime.utcnow() < self.locked_until)
    
    def get_full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary (excluding sensitive data)"""
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "role": self.role.value,
            "status": self.status.value,
            "organization_id": self.organization_id,
            "department": self.department,
            "job_title": self.job_title,
            "phone": self.phone,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "email_verified": self.email_verified,
            "two_factor_enabled": self.two_factor_enabled,
            "metadata": self.metadata
        }
    
    def to_dict_with_permissions(self) -> Dict[str, Any]:
        """Convert user to dictionary including permissions"""
        user_dict = self.to_dict()
        user_dict["permissions"] = self.get_permissions().__dict__
        return user_dict

