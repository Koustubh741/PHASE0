"""
User Management API Endpoints
Handles user CRUD operations, role management, and user administration
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request, Query
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ....core.application.services.user_service import UserService
from ....core.application.services.audit_service import AuditService
from ....core.infrastructure.dependency_injection import get_user_service, get_auth_service, get_audit_service
from ....core.domain.entities.user import User, UserStatus, UserRole
from ....core.domain.entities.audit_log import AuditAction, AuditResource
from ....core.application.dto.user_dto import (
    UserCreateRequest, UserUpdateRequest, UserResponse, UserListResponse,
    UserRoleChangeRequest, UserStatusChangeRequest, UserBulkUpdateRequest,
    UserSearchRequest, UserStatisticsResponse
)
from ...middleware.auth_middleware import require_auth, require_admin, require_permission


router = APIRouter(prefix="/users", tags=["User Management"])


class UserController:
    """User management controller"""
    
    def __init__(
        self,
        user_service: UserService,
        audit_service: AuditService
    ):
        self.user_service = user_service
        self.audit_service = audit_service
    
    async def create_user(
        self,
        user_request: UserCreateRequest,
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> UserResponse:
        """
        Create a new user
        
        Args:
            user_request: User creation request
            current_user: Current authenticated user
            
        Returns:
            Created user information
        """
        try:
            # Validate organization access
            if user_request.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot create user in different organization"
                )
            
            # Create user
            user = await self.user_service.create_user(
                username=user_request.username,
                email=user_request.email,
                first_name=user_request.first_name,
                last_name=user_request.last_name,
                role=UserRole(user_request.role),
                organization_id=user_request.organization_id,
                department=user_request.department,
                job_title=user_request.job_title,
                phone=user_request.phone,
                password=user_request.password,
                created_by=str(current_user.id)
            )
            
            # Log user creation
            await self.audit_service.log_user_action(
                action=AuditAction.CREATE,
                description=f"Created user: {user.username}",
                user=current_user,
                metadata={
                    "created_user_id": str(user.id),
                    "created_user_email": user.email,
                    "created_user_role": user.role.value
                }
            )
            
            return UserResponse.from_user(user)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
    
    async def get_user(
        self,
        user_id: UUID,
        current_user: User = Depends(require_auth)
    ) -> UserResponse:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            current_user: Current authenticated user
            
        Returns:
            User information
        """
        # Check if user can view this user's information
        if str(current_user.id) != str(user_id) and not current_user.has_permission("can_manage_users"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot view other users' information"
            )
        
        user = await self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check organization access
        if user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found in your organization"
            )
        
        return UserResponse.from_user(user)
    
    async def update_user(
        self,
        user_id: UUID,
        user_request: UserUpdateRequest,
        current_user: User = Depends(require_auth)
    ) -> UserResponse:
        """
        Update user information
        
        Args:
            user_id: User ID to update
            user_request: User update request
            current_user: Current authenticated user
            
        Returns:
            Updated user information
        """
        # Check permissions
        can_manage_users = current_user.has_permission("can_manage_users")
        is_own_profile = str(current_user.id) == str(user_id)
        
        if not can_manage_users and not is_own_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot update other users' information"
            )
        
        # Get existing user
        user = await self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check organization access
        if user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found in your organization"
            )
        
        # Store old values for audit
        old_values = user.to_dict()
        
        try:
            # Update user
            updated_user = await self.user_service.update_user(
                user_id=user_id,
                updates=user_request.dict(exclude_unset=True),
                updated_by=str(current_user.id)
            )
            
            # Log user update
            await self.audit_service.log_user_action(
                action=AuditAction.UPDATE,
                description=f"Updated user: {user.username}",
                user=current_user,
                old_values=old_values,
                new_values=updated_user.to_dict(),
                metadata={
                    "updated_user_id": str(user_id),
                    "updated_fields": list(user_request.dict(exclude_unset=True).keys())
                }
            )
            
            return UserResponse.from_user(updated_user)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )
    
    async def delete_user(
        self,
        user_id: UUID,
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> Dict[str, str]:
        """
        Delete user
        
        Args:
            user_id: User ID to delete
            current_user: Current authenticated user
            
        Returns:
            Deletion confirmation
        """
        # Prevent self-deletion
        if str(current_user.id) == str(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        # Get user to delete
        user = await self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check organization access
        if user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found in your organization"
            )
        
        # Prevent deletion of admin users
        if user.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete admin users"
            )
        
        try:
            # Delete user
            await self.user_service.delete_user(user_id, str(current_user.id))
            
            # Log user deletion
            await self.audit_service.log_user_action(
                action=AuditAction.DELETE,
                description=f"Deleted user: {user.username}",
                user=current_user,
                metadata={
                    "deleted_user_id": str(user_id),
                    "deleted_user_email": user.email,
                    "deleted_user_role": user.role.value
                }
            )
            
            return {"message": "User deleted successfully"}
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
    
    async def list_users(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        role: Optional[str] = Query(None),
        status: Optional[str] = Query(None),
        department: Optional[str] = Query(None),
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> UserListResponse:
        """
        List users with filtering and pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            role: Filter by role
            status: Filter by status
            department: Filter by department
            current_user: Current authenticated user
            
        Returns:
            List of users
        """
        try:
            # Build filters
            filters = {}
            if role:
                filters["role"] = UserRole(role)
            if status:
                filters["status"] = UserStatus(status)
            if department:
                filters["department"] = department
            
            # Get users
            users = await self.user_service.list_users(
                organization_id=current_user.organization_id,
                skip=skip,
                limit=limit,
                filters=filters
            )
            
            # Get total count
            total = await self.user_service.count_users(
                organization_id=current_user.organization_id,
                filters=filters
            )
            
            return UserListResponse(
                users=[UserResponse.from_user(user) for user in users],
                total=total,
                skip=skip,
                limit=limit
            )
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to list users"
            )
    
    async def search_users(
        self,
        search_request: UserSearchRequest,
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> UserListResponse:
        """
        Search users
        
        Args:
            search_request: Search criteria
            current_user: Current authenticated user
            
        Returns:
            Search results
        """
        try:
            users = await self.user_service.search_users(
                query=search_request.query,
                organization_id=current_user.organization_id,
                skip=search_request.skip,
                limit=search_request.limit,
                filters=search_request.filters
            )
            
            total = await self.user_service.count_users(
                organization_id=current_user.organization_id,
                filters=search_request.filters,
                search_query=search_request.query
            )
            
            return UserListResponse(
                users=[UserResponse.from_user(user) for user in users],
                total=total,
                skip=search_request.skip,
                limit=search_request.limit
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search users"
            )
    
    async def change_user_role(
        self,
        user_id: UUID,
        role_request: UserRoleChangeRequest,
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> UserResponse:
        """
        Change user role
        
        Args:
            user_id: User ID
            role_request: Role change request
            current_user: Current authenticated user
            
        Returns:
            Updated user information
        """
        user = await self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check organization access
        if user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found in your organization"
            )
        
        # Store old values
        old_values = {"role": user.role.value}
        
        try:
            # Change role
            updated_user = await self.user_service.change_user_role(
                user_id=user_id,
                new_role=UserRole(role_request.role),
                changed_by=str(current_user.id),
                reason=role_request.reason
            )
            
            # Log role change
            await self.audit_service.log_user_action(
                action=AuditAction.ROLE_CHANGE,
                description=f"Changed role for user: {user.username}",
                user=current_user,
                old_values=old_values,
                new_values={"role": updated_user.role.value},
                metadata={
                    "user_id": str(user_id),
                    "reason": role_request.reason
                }
            )
            
            return UserResponse.from_user(updated_user)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change user role"
            )
    
    async def change_user_status(
        self,
        user_id: UUID,
        status_request: UserStatusChangeRequest,
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> UserResponse:
        """
        Change user status
        
        Args:
            user_id: User ID
            status_request: Status change request
            current_user: Current authenticated user
            
        Returns:
            Updated user information
        """
        user = await self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check organization access
        if user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found in your organization"
            )
        
        # Store old values
        old_values = {"status": user.status.value}
        
        try:
            # Change status
            updated_user = await self.user_service.change_user_status(
                user_id=user_id,
                new_status=UserStatus(status_request.status),
                changed_by=str(current_user.id),
                reason=status_request.reason
            )
            
            # Log status change
            await self.audit_service.log_user_action(
                action=AuditAction.UPDATE,
                description=f"Changed status for user: {user.username}",
                user=current_user,
                old_values=old_values,
                new_values={"status": updated_user.status.value},
                metadata={
                    "user_id": str(user_id),
                    "reason": status_request.reason
                }
            )
            
            return UserResponse.from_user(updated_user)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change user status"
            )
    
    async def bulk_update_users(
        self,
        bulk_request: UserBulkUpdateRequest,
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> Dict[str, Any]:
        """
        Bulk update users
        
        Args:
            bulk_request: Bulk update request
            current_user: Current authenticated user
            
        Returns:
            Bulk update results
        """
        try:
            results = await self.user_service.bulk_update_users(
                user_ids=bulk_request.user_ids,
                updates=bulk_request.updates,
                updated_by=str(current_user.id)
            )
            
            # Log bulk update
            await self.audit_service.log_user_action(
                action=AuditAction.UPDATE,
                description=f"Bulk updated {len(bulk_request.user_ids)} users",
                user=current_user,
                metadata={
                    "user_ids": [str(uid) for uid in bulk_request.user_ids],
                    "updates": bulk_request.updates,
                    "successful_updates": results["successful"],
                    "failed_updates": results["failed"]
                }
            )
            
            return results
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to bulk update users"
            )
    
    async def get_user_statistics(
        self,
        current_user: User = Depends(require_permission("can_manage_users"))
    ) -> UserStatisticsResponse:
        """
        Get user statistics
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            User statistics
        """
        try:
            stats = await self.user_service.get_user_statistics(
                organization_id=current_user.organization_id
            )
            
            return UserStatisticsResponse(**stats)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get user statistics"
            )


# Create controller instance (would be injected in real implementation)
user_controller = None


def get_user_controller(
    user_service: UserService = Depends(get_user_service),
    audit_service: AuditService = Depends(get_audit_service)
) -> UserController:
    """Get user controller instance with dependency injection"""
    return UserController(user_service, audit_service)


# API Routes
@router.post("", response_model=UserResponse)
async def create_user(
    user_request: UserCreateRequest,
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """Create a new user"""
    controller = get_user_controller()
    return await controller.create_user(user_request, current_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(require_auth)
):
    """Get user by ID"""
    controller = get_user_controller()
    return await controller.get_user(user_id, current_user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_request: UserUpdateRequest,
    current_user: User = Depends(require_auth)
):
    """Update user information"""
    controller = get_user_controller()
    return await controller.update_user(user_id, user_request, current_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """Delete user"""
    controller = get_user_controller()
    return await controller.delete_user(user_id, current_user)


@router.get("", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """List users with filtering and pagination"""
    controller = get_user_controller()
    return await controller.list_users(skip, limit, role, status, department, current_user)


@router.post("/search", response_model=UserListResponse)
async def search_users(
    search_request: UserSearchRequest,
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """Search users"""
    controller = get_user_controller()
    return await controller.search_users(search_request, current_user)


@router.patch("/{user_id}/role", response_model=UserResponse)
async def change_user_role(
    user_id: UUID,
    role_request: UserRoleChangeRequest,
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """Change user role"""
    controller = get_user_controller()
    return await controller.change_user_role(user_id, role_request, current_user)


@router.patch("/{user_id}/status", response_model=UserResponse)
async def change_user_status(
    user_id: UUID,
    status_request: UserStatusChangeRequest,
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """Change user status"""
    controller = get_user_controller()
    return await controller.change_user_status(user_id, status_request, current_user)


@router.post("/bulk-update")
async def bulk_update_users(
    bulk_request: UserBulkUpdateRequest,
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """Bulk update users"""
    controller = get_user_controller()
    return await controller.bulk_update_users(bulk_request, current_user)


@router.get("/statistics", response_model=UserStatisticsResponse)
async def get_user_statistics(
    current_user: User = Depends(require_permission("can_manage_users"))
):
    """Get user statistics"""
    controller = get_user_controller()
    return await controller.get_user_statistics(current_user)
