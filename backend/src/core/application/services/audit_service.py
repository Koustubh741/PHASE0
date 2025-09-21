"""
Audit Service
Handles comprehensive audit trail logging for all GRC operations
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta

from ...domain.entities.user import User
from ...domain.entities.audit_log import AuditLog, AuditAction, AuditResource, AuditSeverity
from ...domain.repositories.audit_log_repository import AuditLogRepository


class AuditService:
    """Audit service for comprehensive audit trail logging"""
    
    def __init__(self, audit_log_repository: AuditLogRepository):
        self.audit_log_repository = audit_log_repository
    
    async def log_user_action(
        self,
        action: AuditAction,
        description: str,
        user: User,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """
        Log user-related actions
        
        Args:
            action: Audit action
            description: Action description
            user: User performing the action
            old_values: Previous values (for updates)
            new_values: New values (for updates)
            metadata: Additional metadata
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_user_action(
            action=action,
            resource=AuditResource.USER,
            resource_id=str(user.id),
            user=user,
            description=description,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def log_policy_action(
        self,
        action: AuditAction,
        policy_id: str,
        description: str,
        user: User,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """
        Log policy-related actions
        
        Args:
            action: Audit action
            policy_id: Policy ID
            description: Action description
            user: User performing the action
            old_values: Previous values (for updates)
            new_values: New values (for updates)
            metadata: Additional metadata
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_resource_action(
            action=action,
            resource=AuditResource.POLICY,
            resource_id=policy_id,
            user=user,
            description=description,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def log_risk_action(
        self,
        action: AuditAction,
        risk_id: str,
        description: str,
        user: User,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """
        Log risk-related actions
        
        Args:
            action: Audit action
            risk_id: Risk ID
            description: Action description
            user: User performing the action
            old_values: Previous values (for updates)
            new_values: New values (for updates)
            metadata: Additional metadata
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_resource_action(
            action=action,
            resource=AuditResource.RISK,
            resource_id=risk_id,
            user=user,
            description=description,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def log_control_action(
        self,
        action: AuditAction,
        control_id: str,
        description: str,
        user: User,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """
        Log control-related actions
        
        Args:
            action: Audit action
            control_id: Control ID
            description: Action description
            user: User performing the action
            old_values: Previous values (for updates)
            new_values: New values (for updates)
            metadata: Additional metadata
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_resource_action(
            action=action,
            resource=AuditResource.CONTROL,
            resource_id=control_id,
            user=user,
            description=description,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def log_issue_action(
        self,
        action: AuditAction,
        issue_id: str,
        description: str,
        user: User,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """
        Log issue-related actions
        
        Args:
            action: Audit action
            issue_id: Issue ID
            description: Action description
            user: User performing the action
            old_values: Previous values (for updates)
            new_values: New values (for updates)
            metadata: Additional metadata
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_resource_action(
            action=action,
            resource=AuditResource.ISSUE,
            resource_id=issue_id,
            user=user,
            description=description,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def log_workflow_action(
        self,
        action: AuditAction,
        workflow_id: str,
        description: str,
        user: User,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """
        Log workflow-related actions
        
        Args:
            action: Audit action
            workflow_id: Workflow ID
            description: Action description
            user: User performing the action
            old_values: Previous values (for updates)
            new_values: New values (for updates)
            metadata: Additional metadata
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_resource_action(
            action=action,
            resource=AuditResource.WORKFLOW,
            resource_id=workflow_id,
            user=user,
            description=description,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def log_security_event(
        self,
        action: AuditAction,
        description: str,
        severity: AuditSeverity,
        user: Optional[User] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """
        Log security-related events
        
        Args:
            action: Audit action
            description: Event description
            severity: Event severity
            user: User involved (if any)
            ip_address: Client IP address
            user_agent: Client user agent
            metadata: Additional metadata
            success: Whether the action was successful
            error_message: Error message (if any)
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_security_event(
            action=action,
            resource=AuditResource.SYSTEM,
            resource_id="security_event",
            user=user,
            description=description,
            severity=severity,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata or {},
            success=success,
            error_message=error_message
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def log_system_event(
        self,
        action: AuditAction,
        description: str,
        severity: AuditSeverity = AuditSeverity.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Log system-related events
        
        Args:
            action: Audit action
            description: Event description
            severity: Event severity
            metadata: Additional metadata
            
        Returns:
            Created audit log
        """
        audit_log = AuditLog.create_system_event(
            action=action,
            description=description,
            severity=severity,
            metadata=metadata or {}
        )
        
        return await self.audit_log_repository.create(audit_log)
    
    async def get_audit_logs(
        self,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[AuditLog]:
        """
        Get audit logs with filtering
        
        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional filters
            
        Returns:
            List of audit logs
        """
        return await self.audit_log_repository.get_by_organization(
            organization_id=organization_id,
            skip=skip,
            limit=limit,
            filters=filters
        )
    
    async def get_user_audit_logs(
        self,
        user_id: str,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        days_back: int = 30
    ) -> List[AuditLog]:
        """
        Get audit logs for a specific user
        
        Args:
            user_id: User ID
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            days_back: Number of days to look back
            
        Returns:
            List of user audit logs
        """
        start_date = datetime.utcnow() - timedelta(days=days_back)
        
        return await self.audit_log_repository.get_by_user(
            user_id=user_id,
            organization_id=organization_id,
            start_date=start_date,
            skip=skip,
            limit=limit
        )
    
    async def get_resource_audit_logs(
        self,
        resource: AuditResource,
        resource_id: str,
        organization_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """
        Get audit logs for a specific resource
        
        Args:
            resource: Resource type
            resource_id: Resource ID
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of resource audit logs
        """
        return await self.audit_log_repository.get_by_resource(
            resource=resource,
            resource_id=resource_id,
            organization_id=organization_id,
            skip=skip,
            limit=limit
        )
    
    async def search_audit_logs(
        self,
        query: str,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[AuditLog]:
        """
        Search audit logs
        
        Args:
            query: Search query
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional additional filters
            
        Returns:
            List of matching audit logs
        """
        return await self.audit_log_repository.search(
            query=query,
            organization_id=organization_id,
            skip=skip,
            limit=limit,
            filters=filters
        )
    
    async def get_audit_statistics(
        self,
        organization_id: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Get audit statistics
        
        Args:
            organization_id: Organization ID
            days_back: Number of days to look back
            
        Returns:
            Audit statistics
        """
        start_date = datetime.utcnow() - timedelta(days=days_back)
        
        return await self.audit_log_repository.get_statistics(
            organization_id=organization_id,
            start_date=start_date
        )
    
    async def get_failed_login_attempts(
        self,
        organization_id: str,
        hours_back: int = 24,
        limit: int = 100
    ) -> List[AuditLog]:
        """
        Get failed login attempts
        
        Args:
            organization_id: Organization ID
            hours_back: Number of hours to look back
            limit: Maximum number of records
            
        Returns:
            List of failed login attempts
        """
        start_date = datetime.utcnow() - timedelta(hours=hours_back)
        
        return await self.audit_log_repository.get_failed_logins(
            organization_id=organization_id,
            start_date=start_date,
            limit=limit
        )
    
    async def get_security_events(
        self,
        organization_id: str,
        severity: Optional[AuditSeverity] = None,
        hours_back: int = 24,
        limit: int = 100
    ) -> List[AuditLog]:
        """
        Get security events
        
        Args:
            organization_id: Organization ID
            severity: Filter by severity
            hours_back: Number of hours to look back
            limit: Maximum number of records
            
        Returns:
            List of security events
        """
        start_date = datetime.utcnow() - timedelta(hours=hours_back)
        
        filters = {"resource": AuditResource.SYSTEM.value}
        if severity:
            filters["severity"] = severity.value
        
        return await self.audit_log_repository.get_by_organization(
            organization_id=organization_id,
            skip=0,
            limit=limit,
            filters=filters,
            start_date=start_date
        )
    
    async def export_audit_logs(
        self,
        organization_id: str,
        start_date: datetime,
        end_date: datetime,
        format: str = "json",
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Export audit logs
        
        Args:
            organization_id: Organization ID
            start_date: Start date
            end_date: End date
            format: Export format (json, csv, xml)
            filters: Optional filters
            
        Returns:
            Export information
        """
        # Get audit logs for the date range
        audit_logs = await self.audit_log_repository.get_by_date_range(
            organization_id=organization_id,
            start_date=start_date,
            end_date=end_date,
            filters=filters
        )
        
        # Log the export action
        await self.log_system_event(
            action=AuditAction.EXPORT,
            description=f"Audit logs exported: {len(audit_logs)} records",
            metadata={
                "export_format": format,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "record_count": len(audit_logs)
            }
        )
        
        return {
            "export_id": str(UUID()),
            "format": format,
            "record_count": len(audit_logs),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def cleanup_old_audit_logs(
        self,
        organization_id: str,
        retention_days: int = 365
    ) -> Dict[str, Any]:
        """
        Clean up old audit logs based on retention policy
        
        Args:
            organization_id: Organization ID
            retention_days: Number of days to retain
            
        Returns:
            Cleanup information
        """
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        # Get count of logs to be deleted
        old_logs = await self.audit_log_repository.get_by_date_range(
            organization_id=organization_id,
            start_date=datetime.min,
            end_date=cutoff_date
        )
        
        deleted_count = len(old_logs)
        
        # Delete old logs
        if deleted_count > 0:
            await self.audit_log_repository.delete_old_logs(
                organization_id=organization_id,
                cutoff_date=cutoff_date
            )
        
        # Log the cleanup action
        await self.log_system_event(
            action=AuditAction.DELETE,
            description=f"Audit log cleanup completed: {deleted_count} records deleted",
            metadata={
                "retention_days": retention_days,
                "cutoff_date": cutoff_date.isoformat(),
                "deleted_count": deleted_count
            }
        )
        
        return {
            "deleted_count": deleted_count,
            "retention_days": retention_days,
            "cutoff_date": cutoff_date.isoformat(),
            "completed_at": datetime.utcnow().isoformat()
        }