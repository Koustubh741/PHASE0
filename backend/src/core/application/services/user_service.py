"""
User Service
Handles user business logic and operations
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...domain.entities.user import User, UserStatus, UserRole, UserPermissions
from ...domain.repositories.user_repository import UserRepository
from ...domain.repositories.audit_log_repository import AuditLogRepository


class UserService:
    """User service for business logic"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        audit_log_repository: AuditLogRepository
    ):
        self.user_repository = user_repository
        self.audit_log_repository = audit_log_repository
    
    async def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        role: UserRole,
        organization_id: str,
        created_by: str,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
        phone: Optional[str] = None,
        password: Optional[str] = None
    ) -> User:
        """
        Create a new user
        
        Args:
            username: Username
            email: Email address
            first_name: First name
            last_name: Last name
            role: User role
            organization_id: Organization ID
            created_by: ID of user creating this user
            department: Department
            job_title: Job title
            phone: Phone number
            password: Password (optional, will need to be set later)
            
        Returns:
            Created user
            
        Raises:
            ValueError: If validation fails
        """
        # Validate username uniqueness
        if await self.user_repository.exists_by_username(username):
            raise ValueError("Username already exists")
        
        # Validate email uniqueness
        if await self.user_repository.exists_by_email(email):
            raise ValueError("Email already exists")
        
        # Validate organization access (in real implementation)
        # await self._validate_organization_access(organization_id, created_by)
        
        # Create user
        user = User.create_new(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            organization_id=organization_id,
            department=department,
            job_title=job_title,
            phone=phone,
            password=password
        )
        
        # Save user
        created_user = await self.user_repository.create(user)
        
        return created_user
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User or None if not found
        """
        return await self.user_repository.get_by_id(user_id)
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            username: Username
            
        Returns:
            User or None if not found
        """
        return await self.user_repository.get_by_username(username)
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            email: Email address
            
        Returns:
            User or None if not found
        """
        return await self.user_repository.get_by_email(email)
    
    async def update_user(
        self,
        user_id: UUID,
        updates: Dict[str, Any],
        updated_by: str
    ) -> User:
        """
        Update user information
        
        Args:
            user_id: User ID
            updates: Updates to apply
            updated_by: ID of user making the update
            
        Returns:
            Updated user
            
        Raises:
            ValueError: If validation fails
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate updates
        await self._validate_user_updates(user, updates)
        
        # Apply updates
        for field, value in updates.items():
            if hasattr(user, field) and field not in ['id', 'created_at', 'created_by']:
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        
        # Save updated user
        updated_user = await self.user_repository.update(user)
        
        return updated_user
    
    async def delete_user(self, user_id: UUID, deleted_by: str) -> bool:
        """
        Delete user
        
        Args:
            user_id: User ID
            deleted_by: ID of user performing the deletion
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If user cannot be deleted
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Prevent deletion of admin users
        if user.role == UserRole.ADMIN:
            raise ValueError("Cannot delete admin users")
        
        # Prevent self-deletion
        if str(user.id) == deleted_by:
            raise ValueError("Cannot delete your own account")
        
        # Check if user has any dependencies (in real implementation)
        # await self._check_user_dependencies(user_id)
        
        # Delete user
        success = await self.user_repository.delete(user_id)
        
        return success
    
    async def list_users(
        self,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        """
        List users with filtering
        
        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional filters
            
        Returns:
            List of users
        """
        if not filters:
            return await self.user_repository.get_by_organization(
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        # Apply filters
        if "role" in filters:
            return await self.user_repository.get_by_role(
                role=filters["role"],
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        if "status" in filters:
            return await self.user_repository.get_by_status(
                status=filters["status"],
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        if "department" in filters:
            return await self.user_repository.get_users_by_department(
                department=filters["department"],
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        # Default to organization filter
        return await self.user_repository.get_by_organization(
            organization_id=organization_id,
            skip=skip,
            limit=limit
        )
    
    async def search_users(
        self,
        query: str,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        """
        Search users
        
        Args:
            query: Search query
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional additional filters
            
        Returns:
            List of matching users
        """
        users = await self.user_repository.search(
            query=query,
            organization_id=organization_id,
            skip=skip,
            limit=limit
        )
        
        # Apply additional filters if provided
        if filters:
            users = self._apply_filters(users, filters)
        
        return users
    
    async def count_users(
        self,
        organization_id: str,
        filters: Optional[Dict[str, Any]] = None,
        search_query: Optional[str] = None
    ) -> int:
        """
        Count users
        
        Args:
            organization_id: Organization ID
            filters: Optional filters
            search_query: Optional search query
            
        Returns:
            Number of users
        """
        if search_query:
            # For search queries, we need to get the results and count them
            # In a real implementation, this would be optimized at the database level
            users = await self.user_repository.search(
                query=search_query,
                organization_id=organization_id,
                skip=0,
                limit=10000  # Large limit to get all results for counting
            )
            if filters:
                users = self._apply_filters(users, filters)
            return len(users)
        
        # For regular queries, we can use more efficient counting
        if not filters:
            # This would need to be implemented in the repository
            return await self.user_repository.get_active_users_count(organization_id)
        
        # Apply filters and count
        if "role" in filters:
            users = await self.user_repository.get_by_role(
                role=filters["role"],
                organization_id=organization_id,
                skip=0,
                limit=10000
            )
            return len(users)
        
        if "status" in filters:
            users = await self.user_repository.get_by_status(
                status=filters["status"],
                organization_id=organization_id,
                skip=0,
                limit=10000
            )
            return len(users)
        
        return 0
    
    async def change_user_role(
        self,
        user_id: UUID,
        new_role: UserRole,
        changed_by: str,
        reason: str
    ) -> User:
        """
        Change user role
        
        Args:
            user_id: User ID
            new_role: New role
            changed_by: ID of user making the change
            reason: Reason for the change
            
        Returns:
            Updated user
            
        Raises:
            ValueError: If change is not allowed
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate role change
        await self._validate_role_change(user, new_role, changed_by)
        
        # Change role
        user.change_role(new_role, changed_by)
        
        # Save updated user
        updated_user = await self.user_repository.update(user)
        
        return updated_user
    
    async def change_user_status(
        self,
        user_id: UUID,
        new_status: UserStatus,
        changed_by: str,
        reason: str
    ) -> User:
        """
        Change user status
        
        Args:
            user_id: User ID
            new_status: New status
            changed_by: ID of user making the change
            reason: Reason for the change
            
        Returns:
            Updated user
            
        Raises:
            ValueError: If change is not allowed
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate status change
        await self._validate_status_change(user, new_status, changed_by)
        
        # Change status
        if new_status == UserStatus.ACTIVE:
            user.activate()
        elif new_status == UserStatus.INACTIVE:
            user.deactivate()
        elif new_status == UserStatus.SUSPENDED:
            user.suspend(reason)
        
        # Save updated user
        updated_user = await self.user_repository.update(user)
        
        return updated_user
    
    async def bulk_update_users(
        self,
        user_ids: List[UUID],
        updates: Dict[str, Any],
        updated_by: str
    ) -> Dict[str, Any]:
        """
        Bulk update users
        
        Args:
            user_ids: List of user IDs
            updates: Updates to apply
            updated_by: ID of user making the updates
            
        Returns:
            Update results
        """
        successful = 0
        failed = 0
        errors = []
        
        for user_id in user_ids:
            try:
                await self.update_user(user_id, updates, updated_by)
                successful += 1
            except Exception as e:
                failed += 1
                errors.append({
                    "user_id": str(user_id),
                    "error": str(e)
                })
        
        return {
            "successful": successful,
            "failed": failed,
            "errors": errors,
            "total": len(user_ids)
        }
    
    async def get_user_statistics(self, organization_id: str) -> Dict[str, Any]:
        """
        Get user statistics for organization
        
        Args:
            organization_id: Organization ID
            
        Returns:
            User statistics
        """
        stats = await self.user_repository.get_user_statistics(organization_id)
        return stats
    
    async def get_users_with_failed_logins(
        self,
        organization_id: str,
        min_failed_attempts: int = 1,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """
        Get users with failed login attempts
        
        Args:
            organization_id: Organization ID
            min_failed_attempts: Minimum failed attempts
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of users with failed logins
        """
        return await self.user_repository.get_users_with_failed_logins(
            organization_id=organization_id,
            min_failed_attempts=min_failed_attempts,
            skip=skip,
            limit=limit
        )
    
    async def get_locked_users(
        self,
        organization_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """
        Get locked users
        
        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of locked users
        """
        return await self.user_repository.get_locked_users(
            organization_id=organization_id,
            skip=skip,
            limit=limit
        )
    
    async def unlock_user(self, user_id: UUID, unlocked_by: str) -> User:
        """
        Unlock user account
        
        Args:
            user_id: User ID
            unlocked_by: ID of user performing the unlock
            
        Returns:
            Updated user
            
        Raises:
            ValueError: If user not found or not locked
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if user.status != UserStatus.LOCKED:
            raise ValueError("User is not locked")
        
        user.unlock_account()
        
        updated_user = await self.user_repository.update(user)
        
        return updated_user
    
    def _apply_filters(self, users: List[User], filters: Dict[str, Any]) -> List[User]:
        """
        Apply additional filters to user list
        
        Args:
            users: List of users
            filters: Filters to apply
            
        Returns:
            Filtered list of users
        """
        filtered_users = users
        
        if "role" in filters:
            filtered_users = [
                user for user in filtered_users
                if user.role == filters["role"]
            ]
        
        if "status" in filters:
            filtered_users = [
                user for user in filtered_users
                if user.status == filters["status"]
            ]
        
        if "department" in filters:
            filtered_users = [
                user for user in filtered_users
                if user.department == filters["department"]
            ]
        
        if "two_factor_enabled" in filters:
            filtered_users = [
                user for user in filtered_users
                if user.two_factor_enabled == filters["two_factor_enabled"]
            ]
        
        if "email_verified" in filters:
            filtered_users = [
                user for user in filtered_users
                if user.email_verified == filters["email_verified"]
            ]
        
        return filtered_users
    
    async def _validate_user_updates(self, user: User, updates: Dict[str, Any]) -> None:
        """
        Validate user updates
        
        Args:
            user: User being updated
            updates: Updates to validate
            
        Raises:
            ValueError: If validation fails
        """
        # Validate email uniqueness if email is being changed
        if "email" in updates and updates["email"] != user.email:
            if await self.user_repository.exists_by_email(updates["email"], exclude_user_id=user.id):
                raise ValueError("Email already exists")
        
        # Validate username uniqueness if username is being changed
        if "username" in updates and updates["username"] != user.username:
            if await self.user_repository.exists_by_username(updates["username"], exclude_user_id=user.id):
                raise ValueError("Username already exists")
        
        # Validate role changes
        if "role" in updates:
            new_role = UserRole(updates["role"])
            await self._validate_role_change(user, new_role, "system")
    
    async def _validate_role_change(
        self,
        user: User,
        new_role: UserRole,
        changed_by: str
    ) -> None:
        """
        Validate role change
        
        Args:
            user: User whose role is being changed
            new_role: New role
            changed_by: ID of user making the change
            
        Raises:
            ValueError: If role change is not allowed
        """
        # Prevent changing role of admin users unless done by another admin
        if user.role == UserRole.ADMIN and changed_by != "system":
            # In real implementation, check if changed_by is admin
            pass
        
        # Prevent regular users from becoming admins
        if new_role == UserRole.ADMIN and changed_by != "system":
            # In real implementation, check if changed_by is admin
            pass
    
    async def _validate_status_change(
        self,
        user: User,
        new_status: UserStatus,
        changed_by: str
    ) -> None:
        """
        Validate status change
        
        Args:
            user: User whose status is being changed
            new_status: New status
            changed_by: ID of user making the change
            
        Raises:
            ValueError: If status change is not allowed
        """
        # Prevent changing status of admin users unless done by another admin
        if user.role == UserRole.ADMIN and changed_by != "system":
            # In real implementation, check if changed_by is admin
            pass
        
        # Prevent self-deactivation
        if str(user.id) == changed_by and new_status == UserStatus.INACTIVE:
            raise ValueError("Cannot deactivate your own account")
