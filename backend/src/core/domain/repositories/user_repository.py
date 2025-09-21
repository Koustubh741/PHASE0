"""
User Repository Interface
Abstract repository for User entity operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ..entities.user import User, UserStatus, UserRole


class UserRepository(ABC):
    """Abstract user repository interface"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by organization with pagination"""
        pass
    
    @abstractmethod
    async def get_by_role(self, role: UserRole, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role with pagination"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: UserStatus, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by status with pagination"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete user"""
        pass
    
    @abstractmethod
    async def search(self, query: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by name, email, or username"""
        pass
    
    @abstractmethod
    async def get_active_users_count(self, organization_id: str) -> int:
        """Get count of active users in organization"""
        pass
    
    @abstractmethod
    async def get_users_by_department(self, department: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by department"""
        pass
    
    @abstractmethod
    async def get_locked_users(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get locked users"""
        pass
    
    @abstractmethod
    async def get_users_with_failed_logins(self, organization_id: str, min_failed_attempts: int = 1, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users with failed login attempts"""
        pass
    
    @abstractmethod
    async def get_users_created_after(self, created_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users created after specific date"""
        pass
    
    @abstractmethod
    async def get_users_last_login_after(self, last_login_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users with last login after specific date"""
        pass
    
    @abstractmethod
    async def get_users_with_two_factor_enabled(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users with two-factor authentication enabled"""
        pass
    
    @abstractmethod
    async def bulk_update_status(self, user_ids: List[UUID], status: UserStatus, updated_by: str) -> int:
        """Bulk update user status"""
        pass
    
    @abstractmethod
    async def exists_by_username(self, username: str, exclude_user_id: Optional[UUID] = None) -> bool:
        """Check if username exists"""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str, exclude_user_id: Optional[UUID] = None) -> bool:
        """Check if email exists"""
        pass
    
    @abstractmethod
    async def get_user_statistics(self, organization_id: str) -> Dict[str, Any]:
        """Get user statistics for organization"""
        pass

