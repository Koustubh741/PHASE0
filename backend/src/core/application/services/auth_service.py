"""
Authentication Service
Handles user authentication, JWT tokens, and security operations
"""

import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from uuid import UUID

from ...config.settings import settings
from ...domain.entities.user import User, UserStatus, UserRole
from ...domain.repositories.user_repository import UserRepository
from ...domain.repositories.audit_log_repository import AuditLogRepository
from ...domain.entities.audit_log import AuditLog, AuditAction, AuditResource, AuditSeverity
from ..dto.auth_dto import LoginRequest, TokenResponse, PasswordResetRequest, PasswordChangeRequest


class AuthenticationError(Exception):
    """Authentication error exception"""
    pass


class AuthorizationError(Exception):
    """Authorization error exception"""
    pass


class AuthService:
    """Authentication service"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        audit_log_repository: AuditLogRepository
    ):
        self.user_repository = user_repository
        self.audit_log_repository = audit_log_repository
    
    async def authenticate_user(
        self,
        username: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[User, str]:
        """
        Authenticate user with username and password
        
        Args:
            username: Username or email
            password: Plain text password
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Tuple of (User, JWT token)
            
        Raises:
            AuthenticationError: If authentication fails
        """
        # Get user by username or email
        user = await self.user_repository.get_by_username(username)
        if not user:
            user = await self.user_repository.get_by_email(username)
        
        if not user:
            # Log failed login attempt
            await self._log_failed_login_attempt(username, ip_address, user_agent, "User not found")
            raise AuthenticationError("Invalid credentials")
        
        # Check if account is locked
        if user.is_locked():
            await self._log_failed_login_attempt(username, ip_address, user_agent, "Account locked")
            raise AuthenticationError("Account is locked. Please try again later.")
        
        # Check user status
        if user.status != UserStatus.ACTIVE:
            await self._log_failed_login_attempt(username, ip_address, user_agent, f"Account status: {user.status.value}")
            raise AuthenticationError("Account is not active")
        
        # Verify password
        if not user.verify_password(password):
            # Record failed login attempt
            user.record_login_attempt(successful=False)
            await self.user_repository.update(user)
            await self._log_failed_login_attempt(username, ip_address, user_agent, "Invalid password")
            raise AuthenticationError("Invalid credentials")
        
        # Record successful login
        user.record_login_attempt(successful=True)
        await self.user_repository.update(user)
        
        # Generate JWT token
        token = self._generate_jwt_token(user)
        
        # Log successful login
        await self._log_successful_login(user, ip_address, user_agent)
        
        return user, token
    
    async def authenticate_with_two_factor(
        self,
        username: str,
        password: str,
        two_factor_token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[User, str]:
        """
        Authenticate user with two-factor authentication
        
        Args:
            username: Username or email
            password: Plain text password
            two_factor_token: Two-factor authentication token
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Tuple of (User, JWT token)
            
        Raises:
            AuthenticationError: If authentication fails
        """
        # First authenticate with username/password
        user, _ = await self.authenticate_user(username, password, ip_address, user_agent)
        
        # Check if 2FA is enabled
        if not user.two_factor_enabled:
            raise AuthenticationError("Two-factor authentication is not enabled for this user")
        
        # Verify 2FA token
        if not user.verify_two_factor_token(two_factor_token):
            await self._log_failed_login_attempt(username, ip_address, user_agent, "Invalid 2FA token")
            raise AuthenticationError("Invalid two-factor authentication token")
        
        # Generate JWT token
        token = self._generate_jwt_token(user)
        
        # Log successful 2FA login
        await self._log_successful_login(user, ip_address, user_agent, "2FA")
        
        return user, token
    
    async def refresh_token(self, refresh_token: str) -> str:
        """
        Refresh JWT token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New JWT token
            
        Raises:
            AuthenticationError: If refresh fails
        """
        try:
            # Decode refresh token
            payload = jwt.decode(
                refresh_token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm]
            )
            
            user_id = payload.get("sub")
            if not user_id:
                raise AuthenticationError("Invalid refresh token")
            
            # Get user
            user = await self.user_repository.get_by_id(UUID(user_id))
            if not user or user.status != UserStatus.ACTIVE:
                raise AuthenticationError("Invalid refresh token")
            
            # Generate new token
            return self._generate_jwt_token(user)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Refresh token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid refresh token")
    
    async def logout_user(self, user: User, ip_address: Optional[str] = None) -> None:
        """
        Logout user
        
        Args:
            user: User to logout
            ip_address: Client IP address
        """
        # Log logout
        audit_log = AuditLog.create_user_logout(
            user_id=str(user.id),
            user_name=user.get_full_name(),
            organization_id=user.organization_id,
            ip_address=ip_address
        )
        await self.audit_log_repository.create(audit_log)
    
    async def change_password(
        self,
        user: User,
        old_password: str,
        new_password: str,
        ip_address: Optional[str] = None
    ) -> None:
        """
        Change user password
        
        Args:
            user: User changing password
            old_password: Current password
            new_password: New password
            ip_address: Client IP address
            
        Raises:
            AuthenticationError: If old password is incorrect
        """
        # Verify old password
        if not user.verify_password(old_password):
            raise AuthenticationError("Current password is incorrect")
        
        # Validate new password
        self._validate_password(new_password)
        
        # Set new password
        user.set_password(new_password)
        await self.user_repository.update(user)
        
        # Log password change
        audit_log = AuditLog.create_new(
            action=AuditAction.PASSWORD_CHANGE,
            resource=AuditResource.USER,
            description="User changed password",
            user_id=str(user.id),
            user_name=user.get_full_name(),
            organization_id=user.organization_id,
            ip_address=ip_address,
            severity=AuditSeverity.MEDIUM
        )
        await self.audit_log_repository.create(audit_log)
    
    async def initiate_password_reset(self, email: str, ip_address: Optional[str] = None) -> bool:
        """
        Initiate password reset process
        
        Args:
            email: User email
            ip_address: Client IP address
            
        Returns:
            True if reset token was sent, False if user not found
        """
        user = await self.user_repository.get_by_email(email)
        if not user:
            # Log attempt for non-existent user
            audit_log = AuditLog.create_security_event(
                action=AuditAction.PASSWORD_RESET,
                description=f"Password reset attempted for non-existent email: {email}",
                ip_address=ip_address,
                severity=AuditSeverity.MEDIUM
            )
            await self.audit_log_repository.create(audit_log)
            return False
        
        # Generate reset token
        reset_token = user.generate_password_reset_token()
        await self.user_repository.update(user)
        
        # Log password reset initiation
        audit_log = AuditLog.create_new(
            action=AuditAction.PASSWORD_RESET,
            resource=AuditResource.USER,
            description="Password reset initiated",
            user_id=str(user.id),
            user_name=user.get_full_name(),
            organization_id=user.organization_id,
            ip_address=ip_address,
            severity=AuditSeverity.MEDIUM,
            metadata={"reset_token_generated": True}
        )
        await self.audit_log_repository.create(audit_log)
        
        # TODO: Send password reset email
        # await self.email_service.send_password_reset_email(user.email, reset_token)
        
        return True
    
    async def reset_password(
        self,
        reset_token: str,
        new_password: str,
        ip_address: Optional[str] = None
    ) -> bool:
        """
        Reset password using reset token
        
        Args:
            reset_token: Password reset token
            new_password: New password
            ip_address: Client IP address
            
        Returns:
            True if password was reset successfully
        """
        # Find user with reset token
        # Note: This would require a query by reset token in the repository
        # For now, we'll assume we can find the user somehow
        
        # Validate new password
        self._validate_password(new_password)
        
        # Reset password
        success = user.reset_password(reset_token, new_password)
        if success:
            await self.user_repository.update(user)
            
            # Log password reset
            audit_log = AuditLog.create_new(
                action=AuditAction.PASSWORD_RESET,
                resource=AuditResource.USER,
                description="Password reset completed",
                user_id=str(user.id),
                user_name=user.get_full_name(),
                organization_id=user.organization_id,
                ip_address=ip_address,
                severity=AuditSeverity.HIGH
            )
            await self.audit_log_repository.create(audit_log)
        
        return success
    
    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token
            
        Returns:
            Token payload
            
        Raises:
            AuthenticationError: If token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
    
    async def get_current_user_from_token(self, token: str) -> Optional[User]:
        """
        Get current user from JWT token
        
        Args:
            token: JWT token
            
        Returns:
            User object or None
        """
        try:
            payload = self.verify_jwt_token(token)
            user_id = payload.get("sub")
            if user_id:
                return await self.user_repository.get_by_id(UUID(user_id))
        except AuthenticationError:
            pass
        return None
    
    def check_permission(self, user: User, permission: str) -> bool:
        """
        Check if user has specific permission
        
        Args:
            user: User to check
            permission: Permission name
            
        Returns:
            True if user has permission
        """
        return user.has_permission(permission)
    
    def require_permission(self, user: User, permission: str) -> None:
        """
        Require user to have specific permission
        
        Args:
            user: User to check
            permission: Permission name
            
        Raises:
            AuthorizationError: If user doesn't have permission
        """
        if not self.check_permission(user, permission):
            raise AuthorizationError(f"User does not have permission: {permission}")
    
    def _generate_jwt_token(self, user: User) -> str:
        """
        Generate JWT token for user
        
        Args:
            user: User to generate token for
            
        Returns:
            JWT token
        """
        now = datetime.utcnow()
        payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "organization_id": user.organization_id,
            "permissions": user.get_permissions().__dict__,
            "iat": now,
            "exp": now + timedelta(minutes=settings.security.access_token_expire_minutes),
            "jti": secrets.token_urlsafe(16)  # JWT ID for token revocation
        }
        
        return jwt.encode(payload, settings.security.secret_key, algorithm=settings.security.algorithm)
    
    def _validate_password(self, password: str) -> None:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            
        Raises:
            AuthenticationError: If password doesn't meet requirements
        """
        if len(password) < 8:
            raise AuthenticationError("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            raise AuthenticationError("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            raise AuthenticationError("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            raise AuthenticationError("Password must contain at least one number")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            raise AuthenticationError("Password must contain at least one special character")
    
    async def _log_successful_login(
        self,
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        auth_method: str = "password"
    ) -> None:
        """Log successful login"""
        audit_log = AuditLog.create_user_login(
            user_id=str(user.id),
            user_name=user.get_full_name(),
            organization_id=user.organization_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            metadata={"auth_method": auth_method}
        )
        await self.audit_log_repository.create(audit_log)
    
    async def _log_failed_login_attempt(
        self,
        username: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        reason: str = "Invalid credentials"
    ) -> None:
        """Log failed login attempt"""
        audit_log = AuditLog.create_user_login(
            user_id=None,
            user_name=username,
            organization_id=None,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            error_message=reason
        )
        await self.audit_log_repository.create(audit_log)

