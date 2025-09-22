"""
Authentication Middleware
Handles JWT authentication and authorization for API endpoints
"""

from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import jwt
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from config.settings import settings
except ImportError:
    # Fallback for direct execution
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    from config.settings import settings
from ...core.domain.entities.user import User
from ...core.application.services.auth_service import AuthService, AuthenticationError, AuthorizationError


# Security scheme
security = HTTPBearer(auto_error=False)


class AuthMiddleware:
    """Authentication middleware"""
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
    
    async def get_current_user(
        self,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
        request: Request = None
    ) -> Optional[User]:
        """
        Get current user from JWT token
        
        Args:
            credentials: JWT credentials from Authorization header
            request: FastAPI request object
            
        Returns:
            Current user or None if not authenticated
        """
        if not credentials:
            return None
        
        try:
            token = credentials.credentials
            user = await self.auth_service.get_current_user_from_token(token)
            
            # Log API access
            if user and request:
                await self._log_api_access(user, request)
            
            return user
        except AuthenticationError:
            return None
        except Exception:
            return None
    
    async def require_authentication(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        request: Request = None
    ) -> User:
        """
        Require user authentication
        
        Args:
            credentials: JWT credentials from Authorization header
            request: FastAPI request object
            
        Returns:
            Authenticated user
            
        Raises:
            HTTPException: If authentication fails
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            token = credentials.credentials
            user = await self.auth_service.get_current_user_from_token(token)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check if user is active
            if user.status.value != "active":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User account is not active"
                )
            
            # Log API access
            if request:
                await self._log_api_access(user, request)
            
            return user
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def require_permission(self, permission: str):
        """
        Create dependency that requires specific permission
        
        Args:
            permission: Permission name required
            
        Returns:
            Dependency function
        """
        async def permission_dependency(
            current_user: User = Depends(self.require_authentication)
        ) -> User:
            try:
                self.auth_service.require_permission(current_user, permission)
                return current_user
            except AuthorizationError as e:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=str(e)
                )
        
        return permission_dependency
    
    def require_role(self, *roles: str):
        """
        Create dependency that requires specific role(s)
        
        Args:
            roles: Required role(s)
            
        Returns:
            Dependency function
        """
        async def role_dependency(
            current_user: User = Depends(self.require_authentication)
        ) -> User:
            if current_user.role.value not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required role: {', '.join(roles)}"
                )
            return current_user
        
        return role_dependency
    
    def require_admin(self):
        """Create dependency that requires admin role"""
        return self.require_role("admin")
    
    def require_auditor(self):
        """Create dependency that requires auditor role"""
        return self.require_role("auditor")
    
    def require_risk_owner(self):
        """Create dependency that requires risk owner role"""
        return self.require_role("risk_owner")
    
    def require_control_owner(self):
        """Create dependency that requires control owner role"""
        return self.require_role("control_owner")
    
    async def _log_api_access(self, user: User, request: Request) -> None:
        """Log API access for audit purposes"""
        try:
            from ...core.application.services.audit_service import AuditService
            from ...core.domain.repositories.audit_log_repository import AuditLogRepository
            
            # Get audit service (this would be injected in real implementation)
            # audit_service = await get_audit_service()
            
            # For now, we'll skip logging to avoid circular dependencies
            # In a real implementation, this would be handled by dependency injection
            pass
            
        except Exception:
            # Don't fail the request if logging fails
            pass
    
    def get_client_ip(self, request: Request) -> Optional[str]:
        """Get client IP address from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct connection IP
        if hasattr(request.client, "host"):
            return request.client.host
        
        return None
    
    def get_user_agent(self, request: Request) -> Optional[str]:
        """Get user agent from request"""
        return request.headers.get("User-Agent")


# Global auth middleware instance
auth_middleware = None


def get_auth_middleware() -> AuthMiddleware:
    """Get auth middleware instance"""
    global auth_middleware
    if auth_middleware is None:
        # This would be properly injected in a real implementation
        auth_service = None  # Would be injected
        auth_middleware = AuthMiddleware(auth_service)
    return auth_middleware


# Common dependencies
def get_current_user() -> Optional[User]:
    """Get current user (optional authentication)"""
    return Depends(get_auth_middleware().get_current_user)


def require_auth() -> User:
    """Require authentication"""
    return Depends(get_auth_middleware().require_authentication)


def require_admin() -> User:
    """Require admin role"""
    return Depends(get_auth_middleware().require_admin())


def require_auditor() -> User:
    """Require auditor role"""
    return Depends(get_auth_middleware().require_auditor())


def require_risk_owner() -> User:
    """Require risk owner role"""
    return Depends(get_auth_middleware().require_risk_owner())


def require_control_owner() -> User:
    """Require control owner role"""
    return Depends(get_auth_middleware().require_control_owner())


def require_permission(permission: str) -> User:
    """Require specific permission"""
    return Depends(get_auth_middleware().require_permission(permission))

