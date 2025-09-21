"""
Control Repository Interface
Abstract repository for Control entity operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ..entities.control import Control, ControlStatus, ControlType, ControlNature, TestResult


class ControlRepository(ABC):
    """Abstract control repository interface"""
    
    @abstractmethod
    async def create(self, control: Control) -> Control:
        """Create a new control"""
        pass
    
    @abstractmethod
    async def get_by_id(self, control_id: UUID) -> Optional[Control]:
        """Get control by ID"""
        pass
    
    @abstractmethod
    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by organization with pagination"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: ControlStatus, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by status with pagination"""
        pass
    
    @abstractmethod
    async def get_by_type(self, control_type: ControlType, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by type with pagination"""
        pass
    
    @abstractmethod
    async def get_by_nature(self, nature: ControlNature, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by nature with pagination"""
        pass
    
    @abstractmethod
    async def get_by_owner(self, owner_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by owner with pagination"""
        pass
    
    @abstractmethod
    async def update(self, control: Control) -> Control:
        """Update control"""
        pass
    
    @abstractmethod
    async def delete(self, control_id: UUID) -> bool:
        """Delete control"""
        pass
    
    @abstractmethod
    async def search(self, query: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Search controls by title, description, or objective"""
        pass
    
    @abstractmethod
    async def get_effective_controls(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get effective controls"""
        pass
    
    @abstractmethod
    async def get_ineffective_controls(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get ineffective controls"""
        pass
    
    @abstractmethod
    async def get_overdue_for_testing(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls overdue for testing"""
        pass
    
    @abstractmethod
    async def get_controls_due_for_testing(self, days_ahead: int, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls due for testing within specified days"""
        pass
    
    @abstractmethod
    async def get_controls_by_tag(self, tag: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by tag"""
        pass
    
    @abstractmethod
    async def get_controls_by_regulation(self, regulation: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by applicable regulation"""
        pass
    
    @abstractmethod
    async def get_controls_by_framework(self, framework: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by applicable framework"""
        pass
    
    @abstractmethod
    async def get_controls_by_risk_mitigated(self, risk_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls that mitigate a specific risk"""
        pass
    
    @abstractmethod
    async def get_controls_with_failed_tests(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls with failed test results"""
        pass
    
    @abstractmethod
    async def get_controls_created_after(self, created_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls created after specific date"""
        pass
    
    @abstractmethod
    async def get_controls_updated_after(self, updated_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls updated after specific date"""
        pass
    
    @abstractmethod
    async def get_control_statistics(self, organization_id: str) -> Dict[str, Any]:
        """Get control statistics for organization"""
        pass
    
    @abstractmethod
    async def get_control_effectiveness_summary(self, organization_id: str) -> Dict[str, Any]:
        """Get control effectiveness summary"""
        pass
    
    @abstractmethod
    async def get_controls_by_test_result(self, test_result: TestResult, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls by latest test result"""
        pass
    
    @abstractmethod
    async def get_controls_with_low_effectiveness(self, min_rating: int, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls with low effectiveness rating"""
        pass
    
    @abstractmethod
    async def bulk_update_status(self, control_ids: List[UUID], status: ControlStatus, updated_by: str) -> int:
        """Bulk update control status"""
        pass
    
    @abstractmethod
    async def get_control_test_trends(self, organization_id: str, days_back: int = 90) -> Dict[str, Any]:
        """Get control test trends over time"""
        pass
    
    @abstractmethod
    async def get_controls_requiring_attention(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Control]:
        """Get controls requiring attention (overdue, failed tests, low effectiveness)"""
        pass

