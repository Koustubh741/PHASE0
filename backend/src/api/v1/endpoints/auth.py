"""
Authentication API Endpoints
Handles user authentication, authorization, and session management
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer
from typing import Dict, Any

from ....core.application.services.auth_service import AuthService, AuthenticationError, AuthorizationError
from ....core.application.services.audit_service import AuditService
from ....core.infrastructure.dependency_injection import get_auth_service, get_audit_service
from ....core.domain.entities.user import User
from ....core.domain.entities.audit_log import AuditAction, AuditResource, AuditSeverity
from ....core.application.dto.auth_dto import (
    LoginRequest, TokenResponse, PasswordChangeRequest, PasswordResetRequest,
    PasswordResetConfirmRequest, TwoFactorSetupRequest, TwoFactorSetupResponse,
    TwoFactorVerifyRequest, UserRegistrationRequest, UserProfileUpdateRequest,
    SessionInfo, AuditLogFilter
)
from ...middleware.auth_middleware import require_auth, get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


class AuthController:
    """Authentication controller"""
    
    def __init__(
        self,
        auth_service: AuthService,
        audit_service: AuditService
    ):
        self.auth_service = auth_service
        self.audit_service = audit_service
    
    async def login(
        self,
        login_request: LoginRequest,
        request: Request
    ) -> TokenResponse:
        """
        User login endpoint
        
        Args:
            login_request: Login credentials
            request: FastAPI request object
            
        Returns:
            JWT token response
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            # Get client information
            client_ip = self._get_client_ip(request)
            user_agent = request.headers.get("User-Agent")
            
            # Authenticate user
            if login_request.two_factor_token:
                user, token = await self.auth_service.authenticate_with_two_factor(
                    username=login_request.username,
                    password=login_request.password,
                    two_factor_token=login_request.two_factor_token,
                    ip_address=client_ip,
                    user_agent=user_agent
                )
            else:
                user, token = await self.auth_service.authenticate_user(
                    username=login_request.username,
                    password=login_request.password,
                    ip_address=client_ip,
                    user_agent=user_agent
                )
            
            # Create token response
            from ....config.settings import settings
            return TokenResponse(
                access_token=token,
                token_type="bearer",
                expires_in=settings.security.access_token_expire_minutes * 60,
                user=user.to_dict_with_permissions()
            )
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed"
            )
    
    async def logout(
        self,
        current_user: User = Depends(require_auth),
        request: Request = None
    ) -> Dict[str, str]:
        """
        User logout endpoint
        
        Args:
            current_user: Authenticated user
            request: FastAPI request object
            
        Returns:
            Logout confirmation
        """
        client_ip = self._get_client_ip(request) if request else None
        
        await self.auth_service.logout_user(
            user=current_user,
            ip_address=client_ip
        )
        
        return {"message": "Successfully logged out"}
    
    async def refresh_token(
        self,
        refresh_token: str,
        request: Request
    ) -> TokenResponse:
        """
        Refresh JWT token
        
        Args:
            refresh_token: Valid refresh token
            request: FastAPI request object
            
        Returns:
            New JWT token response
        """
        try:
            new_token = await self.auth_service.refresh_token(refresh_token)
            
            # Get user from token to include in response
            user = await self.auth_service.get_current_user_from_token(new_token)
            
            from ....config.settings import settings
            return TokenResponse(
                access_token=new_token,
                token_type="bearer",
                expires_in=settings.security.access_token_expire_minutes * 60,
                user=user.to_dict_with_permissions() if user else {}
            )
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
    
    async def change_password(
        self,
        password_request: PasswordChangeRequest,
        current_user: User = Depends(require_auth),
        request: Request = None
    ) -> Dict[str, str]:
        """
        Change user password
        
        Args:
            password_request: Password change request
            current_user: Authenticated user
            request: FastAPI request object
            
        Returns:
            Success message
        """
        if password_request.new_password != password_request.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password and confirmation do not match"
            )
        
        try:
            client_ip = self._get_client_ip(request) if request else None
            
            await self.auth_service.change_password(
                user=current_user,
                old_password=password_request.current_password,
                new_password=password_request.new_password,
                ip_address=client_ip
            )
            
            return {"message": "Password changed successfully"}
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    async def initiate_password_reset(
        self,
        reset_request: PasswordResetRequest,
        request: Request
    ) -> Dict[str, str]:
        """
        Initiate password reset process
        
        Args:
            reset_request: Password reset request
            request: FastAPI request object
            
        Returns:
            Success message
        """
        client_ip = self._get_client_ip(request) if request else None
        
        success = await self.auth_service.initiate_password_reset(
            email=reset_request.email,
            ip_address=client_ip
        )
        
        # Always return success message for security (don't reveal if email exists)
        return {"message": "If the email exists, a password reset link has been sent"}
    
    async def reset_password(
        self,
        reset_request: PasswordResetConfirmRequest,
        request: Request
    ) -> Dict[str, str]:
        """
        Reset password using reset token
        
        Args:
            reset_request: Password reset confirmation request
            request: FastAPI request object
            
        Returns:
            Success message
        """
        if reset_request.new_password != reset_request.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password and confirmation do not match"
            )
        
        client_ip = self._get_client_ip(request) if request else None
        
        success = await self.auth_service.reset_password(
            reset_token=reset_request.reset_token,
            new_password=reset_request.new_password,
            ip_address=client_ip
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        return {"message": "Password reset successfully"}
    
    async def setup_two_factor(
        self,
        setup_request: TwoFactorSetupRequest,
        current_user: User = Depends(require_auth),
        request: Request = None
    ) -> TwoFactorSetupResponse:
        """
        Setup two-factor authentication
        
        Args:
            setup_request: 2FA setup request
            current_user: Authenticated user
            request: FastAPI request object
            
        Returns:
            2FA setup response with secret and QR code
        """
        # Verify current password
        if not current_user.verify_password(setup_request.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password"
            )
        
        # Enable 2FA
        secret = current_user.enable_two_factor()
        
        # Generate QR code URL (in real implementation, use a QR code library)
        qr_code_url = f"otpauth://totp/GRC-Platform:{current_user.email}?secret={secret}&issuer=GRC-Platform"
        
        # Generate backup codes
        import secrets
        backup_codes = [secrets.token_hex(4).upper() for _ in range(10)]
        
        # TODO: Store backup codes securely
        
        return TwoFactorSetupResponse(
            secret=secret,
            qr_code_url=qr_code_url,
            backup_codes=backup_codes
        )
    
    async def verify_two_factor(
        self,
        verify_request: TwoFactorVerifyRequest,
        current_user: User = Depends(require_auth)
    ) -> Dict[str, str]:
        """
        Verify two-factor authentication token
        
        Args:
            verify_request: 2FA verification request
            current_user: Authenticated user
            
        Returns:
            Verification result
        """
        if not current_user.two_factor_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Two-factor authentication is not enabled"
            )
        
        # Verify token or backup code
        if verify_request.backup_code:
            # TODO: Verify backup code
            pass
        else:
            if not current_user.verify_two_factor_token(verify_request.token):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid two-factor authentication token"
                )
        
        return {"message": "Two-factor authentication verified"}
    
    async def get_current_session(
        self,
        current_user: User = Depends(require_auth),
        request: Request = None
    ) -> SessionInfo:
        """
        Get current user session information
        
        Args:
            current_user: Authenticated user
            request: FastAPI request object
            
        Returns:
            Session information
        """
        return SessionInfo(
            user_id=str(current_user.id),
            username=current_user.username,
            email=current_user.email,
            role=current_user.role.value,
            organization_id=current_user.organization_id,
            permissions=current_user.get_permissions().__dict__,
            login_time=current_user.last_login or current_user.created_at,
            last_activity=current_user.updated_at,
            ip_address=self._get_client_ip(request) if request else None,
            user_agent=request.headers.get("User-Agent") if request else None
        )
    
    async def get_audit_logs(
        self,
        filter_request: AuditLogFilter,
        current_user: User = Depends(require_auth)
    ) -> Dict[str, Any]:
        """
        Get audit logs for current user
        
        Args:
            filter_request: Audit log filter
            current_user: Authenticated user
            
        Returns:
            Filtered audit logs
        """
        # Check if user has permission to view audit logs
        if not current_user.has_permission("can_view_audit_logs"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied: cannot view audit logs"
            )
        
        # Get audit logs
        logs = await self.audit_service.get_audit_trail(
            organization_id=current_user.organization_id,
            resource_type=None,  # Would map from filter_request.resource
            resource_id=filter_request.resource_id,
            user_id=filter_request.user_id,
            action=None,  # Would map from filter_request.action
            start_date=filter_request.start_date,
            end_date=filter_request.end_date,
            skip=filter_request.skip,
            limit=filter_request.limit
        )
        
        return {
            "logs": [log.to_dict() for log in logs],
            "total": len(logs),
            "skip": filter_request.skip,
            "limit": filter_request.limit
        }
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"


# Dependency injection for auth controller
def get_auth_controller(
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service)
) -> AuthController:
    """Get auth controller instance with dependency injection"""
    return AuthController(auth_service, audit_service)


# API Routes
@router.post("/login", response_model=TokenResponse)
async def login(
    login_request: LoginRequest,
    controller: AuthController = Depends(get_auth_controller),
    request: Request = None
):
    """User login endpoint"""
    return await controller.login(login_request, request)


@router.post("/logout")
async def logout(
    controller: AuthController = Depends(get_auth_controller),
    current_user: User = Depends(require_auth),
    request: Request = None
):
    """User logout endpoint"""
    return await controller.logout(current_user, request)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    controller: AuthController = Depends(get_auth_controller),
    request: Request = None
):
    """Refresh JWT token endpoint"""
    return await controller.refresh_token(refresh_token, request)


@router.post("/change-password")
async def change_password(
    password_request: PasswordChangeRequest,
    controller: AuthController = Depends(get_auth_controller),
    current_user: User = Depends(require_auth),
    request: Request = None
):
    """Change user password endpoint"""
    return await controller.change_password(password_request, current_user, request)


@router.post("/reset-password")
async def initiate_password_reset(
    reset_request: PasswordResetRequest,
    controller: AuthController = Depends(get_auth_controller),
    request: Request = None
):
    """Initiate password reset endpoint"""
    return await controller.initiate_password_reset(reset_request, request)


@router.post("/reset-password/confirm")
async def reset_password(
    reset_request: PasswordResetConfirmRequest,
    controller: AuthController = Depends(get_auth_controller),
    request: Request = None
):
    """Reset password endpoint"""
    return await controller.reset_password(reset_request, request)


@router.post("/2fa/setup", response_model=TwoFactorSetupResponse)
async def setup_two_factor(
    setup_request: TwoFactorSetupRequest,
    controller: AuthController = Depends(get_auth_controller),
    current_user: User = Depends(require_auth),
    request: Request = None
):
    """Setup two-factor authentication endpoint"""
    return await controller.setup_two_factor(setup_request, current_user, request)


@router.post("/2fa/verify")
async def verify_two_factor(
    verify_request: TwoFactorVerifyRequest,
    controller: AuthController = Depends(get_auth_controller),
    current_user: User = Depends(require_auth)
):
    """Verify two-factor authentication endpoint"""
    return await controller.verify_two_factor(verify_request, current_user)


@router.get("/session", response_model=SessionInfo)
async def get_current_session(
    controller: AuthController = Depends(get_auth_controller),
    current_user: User = Depends(require_auth),
    request: Request = None
):
    """Get current session information endpoint"""
    return await controller.get_current_session(current_user, request)


@router.post("/audit-logs")
async def get_audit_logs(
    filter_request: AuditLogFilter,
    controller: AuthController = Depends(get_auth_controller),
    current_user: User = Depends(require_auth)
):
    """Get audit logs endpoint"""
    return await controller.get_audit_logs(filter_request, current_user)

