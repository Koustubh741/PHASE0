"""
Audit Log Domain Entity
Core business logic for Audit Log management in GRC Platform
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


class AuditAction(Enum):
    """Audit action enumeration"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    ROLE_CHANGE = "role_change"
    PERMISSION_CHANGE = "permission_change"
    EXPORT = "export"
    IMPORT = "import"
    APPROVE = "approve"
    REJECT = "reject"
    ESCALATE = "escalate"
    ASSIGN = "assign"
    DELEGATE = "delegate"
    ARCHIVE = "archive"
    RESTORE = "restore"


class AuditResource(Enum):
    """Audit resource enumeration"""
    USER = "user"
    ROLE = "role"
    POLICY = "policy"
    RISK = "risk"
    CONTROL = "control"
    ISSUE = "issue"
    AUDIT_LOG = "audit_log"
    COMPLIANCE_REPORT = "compliance_report"
    WORKFLOW = "workflow"
    ORGANIZATION = "organization"
    SYSTEM = "system"


class AuditSeverity(Enum):
    """Audit severity enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditLog:
    """Audit log domain entity"""
    id: UUID
    action: AuditAction
    resource: AuditResource
    resource_id: Optional[str]
    user_id: Optional[str]
    user_name: Optional[str]
    organization_id: Optional[str]
    timestamp: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    session_id: Optional[str]
    
    # Action details
    description: str
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    severity: AuditSeverity = AuditSeverity.MEDIUM
    
    # Context
    source_system: Optional[str] = None
    source_module: Optional[str] = None
    correlation_id: Optional[str] = None
    
    # Result
    success: bool = True
    error_message: Optional[str] = None
    
    # Additional metadata
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def create_new(
        cls,
        action: AuditAction,
        resource: AuditResource,
        description: str,
        user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        organization_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        severity: AuditSeverity = AuditSeverity.MEDIUM,
        source_system: Optional[str] = None,
        source_module: Optional[str] = None,
        correlation_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "AuditLog":
        """Create a new audit log entry"""
        return cls(
            id=uuid4(),
            action=action,
            resource=resource,
            resource_id=resource_id,
            user_id=user_id,
            user_name=user_name,
            organization_id=organization_id,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            description=description,
            old_values=old_values,
            new_values=new_values,
            severity=severity,
            source_system=source_system,
            source_module=source_module,
            correlation_id=correlation_id,
            success=success,
            error_message=error_message,
            metadata=metadata or {}
        )
    
    @classmethod
    def create_user_login(
        cls,
        user_id: str,
        user_name: str,
        organization_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> "AuditLog":
        """Create audit log for user login"""
        action = AuditAction.LOGIN if success else AuditAction.LOGIN_FAILED
        description = f"User {'successfully logged in' if success else 'failed to log in'}"
        
        return cls.create_new(
            action=action,
            resource=AuditResource.USER,
            description=description,
            user_id=user_id,
            user_name=user_name,
            organization_id=organization_id,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            severity=AuditSeverity.MEDIUM if success else AuditSeverity.HIGH,
            success=success,
            error_message=error_message
        )
    
    @classmethod
    def create_user_logout(
        cls,
        user_id: str,
        user_name: str,
        organization_id: str,
        ip_address: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> "AuditLog":
        """Create audit log for user logout"""
        return cls.create_new(
            action=AuditAction.LOGOUT,
            resource=AuditResource.USER,
            description="User logged out",
            user_id=user_id,
            user_name=user_name,
            organization_id=organization_id,
            ip_address=ip_address,
            session_id=session_id,
            severity=AuditSeverity.LOW
        )
    
    @classmethod
    def create_crud_action(
        cls,
        action: AuditAction,
        resource: AuditResource,
        resource_id: str,
        description: str,
        user_id: str,
        user_name: str,
        organization_id: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> "AuditLog":
        """Create audit log for CRUD actions"""
        severity = AuditSeverity.MEDIUM
        if action == AuditAction.DELETE:
            severity = AuditSeverity.HIGH
        
        return cls.create_new(
            action=action,
            resource=resource,
            resource_id=resource_id,
            description=description,
            user_id=user_id,
            user_name=user_name,
            organization_id=organization_id,
            old_values=old_values,
            new_values=new_values,
            severity=severity,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )
    
    @classmethod
    def create_security_event(
        cls,
        action: AuditAction,
        description: str,
        user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        organization_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        severity: AuditSeverity = AuditSeverity.HIGH,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "AuditLog":
        """Create audit log for security events"""
        return cls.create_new(
            action=action,
            resource=AuditResource.SYSTEM,
            description=description,
            user_id=user_id,
            user_name=user_name,
            organization_id=organization_id,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            severity=severity,
            metadata=metadata
        )
    
    @classmethod
    def create_data_export(
        cls,
        resource: AuditResource,
        description: str,
        user_id: str,
        user_name: str,
        organization_id: str,
        export_details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> "AuditLog":
        """Create audit log for data export"""
        return cls.create_new(
            action=AuditAction.EXPORT,
            resource=resource,
            description=description,
            user_id=user_id,
            user_name=user_name,
            organization_id=organization_id,
            severity=AuditSeverity.HIGH,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            metadata=export_details or {}
        )
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to audit log"""
        self.metadata[key] = value
    
    def get_changes_summary(self) -> Optional[str]:
        """Get summary of changes made"""
        if not self.old_values or not self.new_values:
            return None
        
        changes = []
        all_keys = set(self.old_values.keys()) | set(self.new_values.keys())
        
        for key in all_keys:
            old_val = self.old_values.get(key)
            new_val = self.new_values.get(key)
            
            if old_val != new_val:
                changes.append(f"{key}: {old_val} -> {new_val}")
        
        return "; ".join(changes) if changes else None
    
    def is_successful(self) -> bool:
        """Check if the action was successful"""
        return self.success and not self.error_message
    
    def is_security_related(self) -> bool:
        """Check if this is a security-related event"""
        security_actions = [
            AuditAction.LOGIN,
            AuditAction.LOGOUT,
            AuditAction.LOGIN_FAILED,
            AuditAction.PASSWORD_CHANGE,
            AuditAction.PASSWORD_RESET,
            AuditAction.ROLE_CHANGE,
            AuditAction.PERMISSION_CHANGE
        ]
        
        return self.action in security_actions or self.severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]
    
    def requires_immediate_attention(self) -> bool:
        """Check if this event requires immediate attention"""
        return (self.severity == AuditSeverity.CRITICAL or 
                (self.action == AuditAction.LOGIN_FAILED and self.severity == AuditSeverity.HIGH) or
                (self.action == AuditAction.DELETE and self.severity == AuditSeverity.HIGH))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary"""
        return {
            "id": str(self.id),
            "action": self.action.value,
            "resource": self.resource.value,
            "resource_id": self.resource_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "organization_id": self.organization_id,
            "timestamp": self.timestamp.isoformat(),
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
            "description": self.description,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "severity": self.severity.value,
            "source_system": self.source_system,
            "source_module": self.source_module,
            "correlation_id": self.correlation_id,
            "success": self.success,
            "error_message": self.error_message,
            "metadata": self.metadata,
            "changes_summary": self.get_changes_summary(),
            "is_successful": self.is_successful(),
            "is_security_related": self.is_security_related(),
            "requires_immediate_attention": self.requires_immediate_attention()
        }
    
    def to_summary_dict(self) -> Dict[str, Any]:
        """Convert audit log to summary dictionary (for lists)"""
        return {
            "id": str(self.id),
            "action": self.action.value,
            "resource": self.resource.value,
            "resource_id": self.resource_id,
            "user_name": self.user_name,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "severity": self.severity.value,
            "success": self.success,
            "ip_address": self.ip_address,
            "is_security_related": self.is_security_related()
        }

