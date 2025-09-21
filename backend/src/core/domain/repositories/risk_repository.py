"""
Risk Repository Interface
Abstract repository for Risk entity operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ..entities.risk import Risk, RiskStatus, RiskCategory, RiskLikelihood, RiskImpact


class RiskRepository(ABC):
    """Abstract risk repository interface"""
    
    @abstractmethod
    async def create(self, risk: Risk) -> Risk:
        """Create a new risk"""
        pass
    
    @abstractmethod
    async def get_by_id(self, risk_id: UUID) -> Optional[Risk]:
        """Get risk by ID"""
        pass
    
    @abstractmethod
    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by organization with pagination"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: RiskStatus, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by status with pagination"""
        pass
    
    @abstractmethod
    async def get_by_category(self, category: RiskCategory, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by category with pagination"""
        pass
    
    @abstractmethod
    async def get_by_owner(self, owner_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by owner with pagination"""
        pass
    
    @abstractmethod
    async def update(self, risk: Risk) -> Risk:
        """Update risk"""
        pass
    
    @abstractmethod
    async def delete(self, risk_id: UUID) -> bool:
        """Delete risk"""
        pass
    
    @abstractmethod
    async def search(self, query: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Search risks by title, description, or tags"""
        pass
    
    @abstractmethod
    async def get_high_risk_risks(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get high-risk risks"""
        pass
    
    @abstractmethod
    async def get_critical_risks(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get critical risks"""
        pass
    
    @abstractmethod
    async def get_escalated_risks(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get escalated risks"""
        pass
    
    @abstractmethod
    async def get_overdue_for_review(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks overdue for review"""
        pass
    
    @abstractmethod
    async def get_risks_due_for_review(self, days_ahead: int, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks due for review within specified days"""
        pass
    
    @abstractmethod
    async def get_risks_by_tag(self, tag: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by tag"""
        pass
    
    @abstractmethod
    async def get_risks_by_likelihood(self, likelihood: RiskLikelihood, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by likelihood"""
        pass
    
    @abstractmethod
    async def get_risks_by_impact(self, impact: RiskImpact, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by impact"""
        pass
    
    @abstractmethod
    async def get_risks_created_after(self, created_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks created after specific date"""
        pass
    
    @abstractmethod
    async def get_risks_updated_after(self, updated_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks updated after specific date"""
        pass
    
    @abstractmethod
    async def get_risk_statistics(self, organization_id: str) -> Dict[str, Any]:
        """Get risk statistics for organization"""
        pass
    
    @abstractmethod
    async def get_risk_heatmap_data(self, organization_id: str) -> Dict[str, Any]:
        """Get risk heatmap data (likelihood vs impact matrix)"""
        pass
    
    @abstractmethod
    async def get_risks_by_treatment_strategy(self, strategy: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks by treatment strategy"""
        pass
    
    @abstractmethod
    async def get_risks_with_treatments(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Get risks that have treatment plans"""
        pass
    
    @abstractmethod
    async def bulk_update_status(self, risk_ids: List[UUID], status: RiskStatus, updated_by: str) -> int:
        """Bulk update risk status"""
        pass
    
    @abstractmethod
    async def get_risk_trends(self, organization_id: str, days_back: int = 90) -> Dict[str, Any]:
        """Get risk trends over time"""
        pass

