"""
Audit Log Repository Interface
Abstract repository for Audit Log entity operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ..entities.audit_log import AuditLog, AuditAction, AuditResource, AuditSeverity


class AuditLogRepository(ABC):
    """Abstract audit log repository interface"""
    
    @abstractmethod
    async def create(self, audit_log: AuditLog) -> AuditLog:
        """Create a new audit log entry"""
        pass
    
    @abstractmethod
    async def get_by_id(self, audit_log_id: UUID) -> Optional[AuditLog]:
        """Get audit log by ID"""
        pass
    
    @abstractmethod
    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by organization with pagination"""
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by user with pagination"""
        pass
    
    @abstractmethod
    async def get_by_action(self, action: AuditAction, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by action with pagination"""
        pass
    
    @abstractmethod
    async def get_by_resource(self, resource: AuditResource, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by resource with pagination"""
        pass
    
    @abstractmethod
    async def get_by_severity(self, severity: AuditSeverity, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by severity with pagination"""
        pass
    
    @abstractmethod
    async def get_by_resource_id(self, resource_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs for a specific resource"""
        pass
    
    @abstractmethod
    async def get_by_date_range(self, start_date: datetime, end_date: datetime, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs within date range"""
        pass
    
    @abstractmethod
    async def get_failed_actions(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get failed audit actions"""
        pass
    
    @abstractmethod
    async def get_security_events(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get security-related audit events"""
        pass
    
    @abstractmethod
    async def get_login_attempts(self, user_id: Optional[str], organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get login attempts (successful and failed)"""
        pass
    
    @abstractmethod
    async def get_user_activity(self, user_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get user activity audit logs"""
        pass
    
    @abstractmethod
    async def get_data_access_logs(self, resource_type: AuditResource, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get data access audit logs"""
        pass
    
    @abstractmethod
    async def get_export_logs(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get data export audit logs"""
        pass
    
    @abstractmethod
    async def search(self, query: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Search audit logs by description, user name, or IP address"""
        pass
    
    @abstractmethod
    async def get_audit_statistics(self, organization_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get audit log statistics"""
        pass
    
    @abstractmethod
    async def get_user_activity_summary(self, user_id: str, organization_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get user activity summary"""
        pass
    
    @abstractmethod
    async def get_security_event_summary(self, organization_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get security event summary"""
        pass
    
    @abstractmethod
    async def get_failed_login_attempts(self, user_id: str, organization_id: str, hours_back: int = 24) -> List[AuditLog]:
        """Get failed login attempts for a user within time period"""
        pass
    
    @abstractmethod
    async def get_privilege_escalation_events(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get privilege escalation events"""
        pass
    
    @abstractmethod
    async def get_data_modification_logs(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get data modification audit logs"""
        pass
    
    @abstractmethod
    async def get_audit_trail_for_resource(self, resource_type: AuditResource, resource_id: str, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get complete audit trail for a specific resource"""
        pass
    
    @abstractmethod
    async def cleanup_old_logs(self, cutoff_date: datetime, organization_id: str) -> int:
        """Clean up old audit logs"""
        pass
    
    @abstractmethod
    async def get_anomalous_activity(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get potentially anomalous activity"""
        pass

