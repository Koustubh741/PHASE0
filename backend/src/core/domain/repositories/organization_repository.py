"""
Organization Repository Interface
Defines the contract for organization data persistence
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.organization import Organization


class OrganizationRepository(ABC):
    """Abstract repository for organization persistence operations"""
    
    @abstractmethod
    async def create(self, organization: Organization) -> Organization:
        """Create a new organization"""
        pass
    
    @abstractmethod
    async def get_by_id(self, org_id: str) -> Optional[Organization]:
        """Get organization by ID"""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Organization]:
        """Get organization by name"""
        pass
    
    @abstractmethod
    async def update(self, organization: Organization) -> Organization:
        """Update organization"""
        pass
    
    @abstractmethod
    async def delete(self, org_id: str) -> bool:
        """Delete organization"""
        pass
    
    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        """List organizations with pagination"""
        pass
    
    @abstractmethod
    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Organization]:
        """Search organizations by query"""
        pass
