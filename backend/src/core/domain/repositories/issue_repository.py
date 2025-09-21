"""
Issue Repository Interface
Abstract repository for Issue entity operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ..entities.issue import Issue, IssueStatus, IssuePriority, IssueType, IssueCategory


class IssueRepository(ABC):
    """Abstract issue repository interface"""
    
    @abstractmethod
    async def create(self, issue: Issue) -> Issue:
        """Create a new issue"""
        pass
    
    @abstractmethod
    async def get_by_id(self, issue_id: UUID) -> Optional[Issue]:
        """Get issue by ID"""
        pass
    
    @abstractmethod
    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by organization with pagination"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: IssueStatus, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by status with pagination"""
        pass
    
    @abstractmethod
    async def get_by_priority(self, priority: IssuePriority, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by priority with pagination"""
        pass
    
    @abstractmethod
    async def get_by_type(self, issue_type: IssueType, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by type with pagination"""
        pass
    
    @abstractmethod
    async def get_by_category(self, category: IssueCategory, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by category with pagination"""
        pass
    
    @abstractmethod
    async def get_by_assignee(self, assigned_to: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues assigned to a user"""
        pass
    
    @abstractmethod
    async def get_by_reporter(self, reported_by: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues reported by a user"""
        pass
    
    @abstractmethod
    async def update(self, issue: Issue) -> Issue:
        """Update issue"""
        pass
    
    @abstractmethod
    async def delete(self, issue_id: UUID) -> bool:
        """Delete issue"""
        pass
    
    @abstractmethod
    async def search(self, query: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Search issues by title, description, or tags"""
        pass
    
    @abstractmethod
    async def get_open_issues(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get open issues"""
        pass
    
    @abstractmethod
    async def get_critical_issues(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get critical priority issues"""
        pass
    
    @abstractmethod
    async def get_overdue_issues(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get overdue issues"""
        pass
    
    @abstractmethod
    async def get_escalated_issues(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get escalated issues"""
        pass
    
    @abstractmethod
    async def get_issues_by_tag(self, tag: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues by tag"""
        pass
    
    @abstractmethod
    async def get_issues_with_pending_actions(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues with pending actions"""
        pass
    
    @abstractmethod
    async def get_issues_created_after(self, created_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues created after specific date"""
        pass
    
    @abstractmethod
    async def get_issues_updated_after(self, updated_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues updated after specific date"""
        pass
    
    @abstractmethod
    async def get_issues_resolved_after(self, resolved_after: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues resolved after specific date"""
        pass
    
    @abstractmethod
    async def get_issues_by_related_risk(self, risk_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues related to a specific risk"""
        pass
    
    @abstractmethod
    async def get_issues_by_related_control(self, control_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues related to a specific control"""
        pass
    
    @abstractmethod
    async def get_issues_by_related_policy(self, policy_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues related to a specific policy"""
        pass
    
    @abstractmethod
    async def get_issues_requiring_regulatory_notification(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues requiring regulatory notification"""
        pass
    
    @abstractmethod
    async def get_issue_statistics(self, organization_id: str) -> Dict[str, Any]:
        """Get issue statistics for organization"""
        pass
    
    @abstractmethod
    async def get_issue_trends(self, organization_id: str, days_back: int = 90) -> Dict[str, Any]:
        """Get issue trends over time"""
        pass
    
    @abstractmethod
    async def get_issue_aging_report(self, organization_id: str) -> Dict[str, Any]:
        """Get issue aging report"""
        pass
    
    @abstractmethod
    async def bulk_update_status(self, issue_ids: List[UUID], status: IssueStatus, updated_by: str) -> int:
        """Bulk update issue status"""
        pass
    
    @abstractmethod
    async def bulk_assign_issues(self, issue_ids: List[UUID], assigned_to: str, assigned_by: str) -> int:
        """Bulk assign issues to a user"""
        pass
    
    @abstractmethod
    async def get_issues_requiring_attention(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Issue]:
        """Get issues requiring attention (overdue, critical, escalated)"""
        pass

