"""
Policy Repository Interface
Abstract repository for Policy entity operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ..entities.policy import Policy, PolicyStatus, PolicyType


class PolicyRepository(ABC):
    """Abstract policy repository interface"""
    
    @abstractmethod
    async def create(self, policy: Policy) -> Policy:
        """Create a new policy"""
        pass
    
    @abstractmethod
    async def get_by_id(self, policy_id: UUID) -> Optional[Policy]:
        """Get policy by ID"""
        pass
    
    @abstractmethod
    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies by organization with pagination"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: PolicyStatus, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies by status with pagination"""
        pass
    
    @abstractmethod
    async def get_by_type(self, policy_type: PolicyType, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies by type with pagination"""
        pass
    
    @abstractmethod
    async def get_by_owner(self, owner_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies by owner with pagination"""
        pass
    
    @abstractmethod
    async def update(self, policy: Policy) -> Policy:
        """Update policy"""
        pass
    
    @abstractmethod
    async def delete(self, policy_id: UUID) -> bool:
        """Delete policy"""
        pass
    
    @abstractmethod
    async def search(self, query: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Search policies by title, description, or content"""
        pass
    
    @abstractmethod
    async def get_active_policies(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get active policies"""
        pass
    
    @abstractmethod
    async def get_draft_policies(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get draft policies"""
        pass
    
    @abstractmethod
    async def get_expired_policies(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get expired policies"""
        pass
    
    @abstractmethod
    async def get_policies_expiring_soon(self, days_ahead: int, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies expiring within specified days"""
        pass
    
    @abstractmethod
    async def get_policies_under_review(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies under review"""
        pass
    
    @abstractmethod
    async def get_policies_by_tag(self, tag: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies by tag"""
        pass
    
    @abstractmethod
    async def get_policies_created_after(self, created_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies created after specific date"""
        pass
    
    @abstractmethod
    async def get_policies_updated_after(self, updated_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies updated after specific date"""
        pass
    
    @abstractmethod
    async def get_policies_with_versions(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Get policies that have version history"""
        pass
    
    @abstractmethod
    async def get_policy_statistics(self, organization_id: str) -> Dict[str, Any]:
        """Get policy statistics for organization"""
        pass
    
    @abstractmethod
    async def get_effective_policies_count(self, organization_id: str) -> int:
        """Get count of effective policies"""
        pass
    
    @abstractmethod
    async def bulk_update_status(self, policy_ids: List[UUID], status: PolicyStatus, updated_by: str) -> int:
        """Bulk update policy status"""
        pass
    
    @abstractmethod
    async def archive_old_policies(self, cutoff_date: datetime, organization_id: str) -> int:
        """Archive policies older than cutoff date"""
        pass

