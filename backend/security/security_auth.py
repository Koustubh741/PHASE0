#!/usr/bin/env python3
"""
Authentication and Authorization Module for BFSI API
Implements OAuth2/JWT with role-based access control
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
import logging

from security_config import security_config, Roles
from user_repository import user_repository

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token scheme
security_scheme = HTTPBearer()

class User(BaseModel):
    """User model for authentication"""
    user_id: str
    username: str
    email: str
    role: str
    permissions: List[str]
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None

class Token(BaseModel):
    """JWT Token model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    """Token data for JWT payload"""
    user_id: str
    username: str
    role: str
    permissions: List[str]
    exp: datetime

class AuthService:
    """Authentication service for BFSI compliance"""
    
    def __init__(self):
        self.secret_key = security_config.jwt_secret_key
        self.algorithm = security_config.jwt_algorithm
        self.access_token_expire_minutes = security_config.jwt_access_token_expire_minutes
        self.refresh_token_expire_days = security_config.jwt_refresh_token_expire_days
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> TokenData:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Validate token type
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
            
            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )
            
            return TokenData(
                user_id=payload.get("user_id"),
                username=payload.get("username"),
                role=payload.get("role"),
                permissions=payload.get("permissions", []),
                exp=datetime.fromtimestamp(exp) if exp else datetime.utcnow()
            )
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials using repository pattern"""
        try:
            # Get user data from repository
            user_data = user_repository.get_user_by_username(username)
            if not user_data:
                logger.warning(f"Authentication failed: User not found - {username}")
                return None
            
            # Check if user is active
            if not user_data.get("is_active", False):
                logger.warning(f"Authentication failed: Inactive user - {username}")
                return None
            
            # Verify password against pre-computed hash
            hashed_password = user_data.get("hashed_password")
            if not hashed_password:
                logger.error(f"Authentication failed: No password hash for user - {username}")
                return None
            
            if not self.verify_password(password, hashed_password):
                logger.warning(f"Authentication failed: Invalid password for user - {username}")
                return None
            
            # Update last login timestamp
            user_repository.update_last_login(username)
            
            # Parse created_at timestamp
            created_at_str = user_data.get("created_at")
            if isinstance(created_at_str, str):
                created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
            else:
                created_at = datetime.utcnow()
            
            logger.info(f"Authentication successful for user: {username}")
            
            return User(
                user_id=user_data["user_id"],
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"],
                permissions=Roles.PERMISSIONS.get(user_data["role"], []),
                is_active=user_data["is_active"],
                created_at=created_at
            )
            
        except Exception as e:
            logger.error(f"Authentication error for user {username}: {e}")
            return None

# Global auth service
auth_service = AuthService()

# Dependency for getting current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> User:
    """Get current authenticated user"""
    try:
        token = credentials.credentials
        token_data = auth_service.verify_token(token)
        
        # Get user data from repository
        user_data = user_repository.get_user_by_id(token_data.user_id)
        if not user_data:
            logger.error(f"User not found for token: {token_data.user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Check if user is still active
        if not user_data.get("is_active", False):
            logger.warning(f"Inactive user attempted access: {token_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )
        
        # Parse created_at timestamp
        created_at_str = user_data.get("created_at")
        if isinstance(created_at_str, str):
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        else:
            created_at = datetime.utcnow()
        
        # Parse last_login timestamp
        last_login = None
        last_login_str = user_data.get("last_login")
        if last_login_str and isinstance(last_login_str, str):
            last_login = datetime.fromisoformat(last_login_str.replace('Z', '+00:00'))
        elif last_login_str and isinstance(last_login_str, datetime):
            last_login = last_login_str
        
        logger.debug(f"Retrieved user from repository: {token_data.username}")
        
        return User(
            user_id=user_data["user_id"],
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            permissions=Roles.PERMISSIONS.get(user_data["role"], []),
            is_active=user_data["is_active"],
            created_at=created_at,
            last_login=last_login
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error"
        )

# Permission checking decorator
def require_permission(permission: str):
    """Decorator to require specific permission"""
    def permission_checker(current_user: User = Depends(get_current_user)):
        if not Roles.has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {permission}"
            )
        return current_user
    return permission_checker

# Role-based access control
def require_role(required_role: str):
    """Require specific role"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != Roles.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {required_role}"
            )
        return current_user
    return role_checker

# Admin only access
def require_admin(current_user: User = Depends(get_current_user)):
    """Require admin role"""
    if current_user.role != Roles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Compliance officer access
def require_compliance_access(current_user: User = Depends(get_current_user)):
    """Require compliance officer or admin access"""
    if current_user.role not in [Roles.ADMIN, Roles.COMPLIANCE_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compliance officer access required"
        )
    return current_user

# Audit access
def require_audit_access(current_user: User = Depends(get_current_user)):
    """Require auditor or admin access"""
    if current_user.role not in [Roles.ADMIN, Roles.AUDITOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auditor access required"
        )
    return current_user
