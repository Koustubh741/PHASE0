"""
Issue Domain Entity
Core business logic for Issue management in GRC Platform
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from decimal import Decimal


class IssueStatus(Enum):
    """Issue status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    ESCALATED = "escalated"


class IssuePriority(Enum):
    """Issue priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueType(Enum):
    """Issue type enumeration"""
    COMPLIANCE_VIOLATION = "compliance_violation"
    CONTROL_FAILURE = "control_failure"
    RISK_REALIZATION = "risk_realization"
    AUDIT_FINDING = "audit_finding"
    REGULATORY_NOTIFICATION = "regulatory_notification"
    INCIDENT = "incident"
    EXCEPTION = "exception"
    OTHER = "other"


class IssueCategory(Enum):
    """Issue category enumeration"""
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    REGULATORY = "regulatory"
    SECURITY = "security"
    TECHNOLOGY = "technology"
    PROCESS = "process"
    THIRD_PARTY = "third_party"
    HUMAN_RESOURCES = "human_resources"


@dataclass
class IssueComment:
    """Issue comment value object"""
    id: UUID
    comment: str
    author_id: str
    author_name: str
    created_at: datetime
    is_internal: bool = False
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []


@dataclass
class IssueAction:
    """Issue action value object"""
    id: UUID
    action_type: str
    description: str
    assigned_to: str
    due_date: Optional[datetime] = None
    status: str = "pending"
    completed_at: Optional[datetime] = None
    completed_by: Optional[str] = None
    notes: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class IssueEvidence:
    """Issue evidence value object"""
    id: UUID
    evidence_type: str
    description: str
    file_path: Optional[str] = None
    url: Optional[str] = None
    collected_by: str
    collected_at: datetime
    verified: bool = False
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.collected_at is None:
            self.collected_at = datetime.utcnow()


@dataclass
class Issue:
    """Issue domain entity"""
    id: UUID
    title: str
    description: str
    issue_type: IssueType
    category: IssueCategory
    priority: IssuePriority
    status: IssueStatus
    organization_id: str
    reported_by: str
    assigned_to: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    # Issue details
    root_cause: Optional[str] = None
    impact_assessment: Optional[str] = None
    business_impact: Optional[str] = None
    affected_areas: List[str] = None
    affected_processes: List[str] = None
    affected_systems: List[str] = None
    
    # Dates
    detected_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    resolved_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None
    
    # Related entities
    related_risks: List[str] = None
    related_controls: List[str] = None
    related_policies: List[str] = None
    related_audits: List[str] = None
    
    # Actions and tracking
    actions: List[IssueAction] = None
    comments: List[IssueComment] = None
    evidence: List[IssueEvidence] = None
    
    # Financial impact
    financial_impact: Optional[Decimal] = None
    remediation_cost: Optional[Decimal] = None
    
    # Compliance
    regulatory_implications: List[str] = None
    compliance_framework: Optional[str] = None
    regulatory_notification_required: bool = False
    regulatory_notification_date: Optional[datetime] = None
    
    # Escalation
    escalated_to: Optional[str] = None
    escalation_reason: Optional[str] = None
    escalation_date: Optional[datetime] = None
    
    # Metadata
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    external_references: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.affected_areas is None:
            self.affected_areas = []
        if self.affected_processes is None:
            self.affected_processes = []
        if self.affected_systems is None:
            self.affected_systems = []
        if self.related_risks is None:
            self.related_risks = []
        if self.related_controls is None:
            self.related_controls = []
        if self.related_policies is None:
            self.related_policies = []
        if self.related_audits is None:
            self.related_audits = []
        if self.actions is None:
            self.actions = []
        if self.comments is None:
            self.comments = []
        if self.evidence is None:
            self.evidence = []
        if self.regulatory_implications is None:
            self.regulatory_implications = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.external_references is None:
            self.external_references = []
    
    @classmethod
    def create_new(
        cls,
        title: str,
        description: str,
        issue_type: IssueType,
        category: IssueCategory,
        priority: IssuePriority,
        organization_id: str,
        reported_by: str,
        assigned_to: Optional[str] = None,
        detected_date: Optional[datetime] = None,
        tags: List[str] = None
    ) -> "Issue":
        """Create a new issue"""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            title=title,
            description=description,
            issue_type=issue_type,
            category=category,
            priority=priority,
            status=IssueStatus.OPEN,
            organization_id=organization_id,
            reported_by=reported_by,
            assigned_to=assigned_to,
            created_at=now,
            updated_at=now,
            detected_date=detected_date or now,
            tags=tags or []
        )
    
    def assign(self, assigned_to: str, assigned_by: str) -> None:
        """Assign issue to a user"""
        if self.status not in [IssueStatus.OPEN, IssueStatus.IN_PROGRESS]:
            raise ValueError("Issue must be open or in progress to be assigned")
        
        self.assigned_to = assigned_to
        self.metadata["assigned_by"] = assigned_by
        self.metadata["assigned_at"] = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow()
    
    def start_work(self, started_by: str) -> None:
        """Start working on the issue"""
        if self.status != IssueStatus.OPEN:
            raise ValueError("Issue must be open to start work")
        
        self.status = IssueStatus.IN_PROGRESS
        self.metadata["work_started_by"] = started_by
        self.metadata["work_started_at"] = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow()
    
    def resolve(self, resolved_by: str, resolution_notes: str = "") -> None:
        """Resolve the issue"""
        if self.status not in [IssueStatus.OPEN, IssueStatus.IN_PROGRESS]:
            raise ValueError("Issue must be open or in progress to be resolved")
        
        self.status = IssueStatus.RESOLVED
        self.resolved_date = datetime.utcnow()
        self.metadata["resolved_by"] = resolved_by
        if resolution_notes:
            self.metadata["resolution_notes"] = resolution_notes
        
        self.updated_at = datetime.utcnow()
    
    def close(self, closed_by: str, closure_notes: str = "") -> None:
        """Close the issue"""
        if self.status not in [IssueStatus.RESOLVED, IssueStatus.OPEN]:
            raise ValueError("Issue must be resolved or open to be closed")
        
        self.status = IssueStatus.CLOSED
        self.closed_date = datetime.utcnow()
        self.metadata["closed_by"] = closed_by
        if closure_notes:
            self.metadata["closure_notes"] = closure_notes
        
        self.updated_at = datetime.utcnow()
    
    def cancel(self, cancelled_by: str, cancellation_reason: str) -> None:
        """Cancel the issue"""
        if self.status == IssueStatus.CLOSED:
            raise ValueError("Cannot cancel a closed issue")
        
        self.status = IssueStatus.CANCELLED
        self.metadata["cancelled_by"] = cancelled_by
        self.metadata["cancelled_at"] = datetime.utcnow().isoformat()
        self.metadata["cancellation_reason"] = cancellation_reason
        
        self.updated_at = datetime.utcnow()
    
    def escalate(self, escalated_to: str, escalation_reason: str, escalated_by: str) -> None:
        """Escalate the issue"""
        self.status = IssueStatus.ESCALATED
        self.escalated_to = escalated_to
        self.escalation_reason = escalation_reason
        self.escalation_date = datetime.utcnow()
        self.metadata["escalated_by"] = escalated_by
        
        self.updated_at = datetime.utcnow()
    
    def add_comment(self, comment: str, author_id: str, author_name: str, is_internal: bool = False) -> None:
        """Add comment to issue"""
        comment_obj = IssueComment(
            id=uuid4(),
            comment=comment,
            author_id=author_id,
            author_name=author_name,
            created_at=datetime.utcnow(),
            is_internal=is_internal
        )
        
        self.comments.append(comment_obj)
        self.updated_at = datetime.utcnow()
    
    def add_action(
        self,
        action_type: str,
        description: str,
        assigned_to: str,
        due_date: Optional[datetime] = None,
        notes: str = ""
    ) -> None:
        """Add action item to issue"""
        action = IssueAction(
            id=uuid4(),
            action_type=action_type,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
            notes=notes
        )
        
        self.actions.append(action)
        self.updated_at = datetime.utcnow()
    
    def complete_action(self, action_id: UUID, completed_by: str, notes: str = "") -> None:
        """Complete an action item"""
        for action in self.actions:
            if action.id == action_id:
                action.status = "completed"
                action.completed_at = datetime.utcnow()
                action.completed_by = completed_by
                if notes:
                    action.notes = notes
                action.updated_at = datetime.utcnow()
                break
        
        self.updated_at = datetime.utcnow()
    
    def add_evidence(
        self,
        evidence_type: str,
        description: str,
        collected_by: str,
        file_path: Optional[str] = None,
        url: Optional[str] = None
    ) -> None:
        """Add evidence to issue"""
        evidence = IssueEvidence(
            id=uuid4(),
            evidence_type=evidence_type,
            description=description,
            file_path=file_path,
            url=url,
            collected_by=collected_by
        )
        
        self.evidence.append(evidence)
        self.updated_at = datetime.utcnow()
    
    def verify_evidence(self, evidence_id: UUID, verified_by: str) -> None:
        """Verify evidence"""
        for evidence in self.evidence:
            if evidence.id == evidence_id:
                evidence.verified = True
                evidence.verified_by = verified_by
                evidence.verified_at = datetime.utcnow()
                break
        
        self.updated_at = datetime.utcnow()
    
    def set_root_cause(self, root_cause: str, analyzed_by: str) -> None:
        """Set root cause analysis"""
        self.root_cause = root_cause
        self.metadata["root_cause_analyzed_by"] = analyzed_by
        self.metadata["root_cause_analyzed_at"] = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow()
    
    def assess_impact(self, impact_assessment: str, business_impact: str, assessed_by: str) -> None:
        """Assess issue impact"""
        self.impact_assessment = impact_assessment
        self.business_impact = business_impact
        self.metadata["impact_assessed_by"] = assessed_by
        self.metadata["impact_assessed_at"] = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow()
    
    def set_financial_impact(self, financial_impact: Decimal, remediation_cost: Optional[Decimal] = None) -> None:
        """Set financial impact"""
        self.financial_impact = financial_impact
        if remediation_cost:
            self.remediation_cost = remediation_cost
        self.updated_at = datetime.utcnow()
    
    def add_regulatory_implication(self, implication: str) -> None:
        """Add regulatory implication"""
        if implication not in self.regulatory_implications:
            self.regulatory_implications.append(implication)
            self.updated_at = datetime.utcnow()
    
    def require_regulatory_notification(self, compliance_framework: str) -> None:
        """Mark issue as requiring regulatory notification"""
        self.regulatory_notification_required = True
        self.compliance_framework = compliance_framework
        self.updated_at = datetime.utcnow()
    
    def submit_regulatory_notification(self, notification_date: datetime) -> None:
        """Record regulatory notification submission"""
        self.regulatory_notification_date = notification_date
        self.updated_at = datetime.utcnow()
    
    def add_related_risk(self, risk_id: str) -> None:
        """Add related risk"""
        if risk_id not in self.related_risks:
            self.related_risks.append(risk_id)
            self.updated_at = datetime.utcnow()
    
    def add_related_control(self, control_id: str) -> None:
        """Add related control"""
        if control_id not in self.related_controls:
            self.related_controls.append(control_id)
            self.updated_at = datetime.utcnow()
    
    def add_related_policy(self, policy_id: str) -> None:
        """Add related policy"""
        if policy_id not in self.related_policies:
            self.related_policies.append(policy_id)
            self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> None:
        """Add tag to issue"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """Remove tag from issue"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update issue metadata"""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()
    
    def add_external_reference(self, reference: str) -> None:
        """Add external reference"""
        if reference not in self.external_references:
            self.external_references.append(reference)
            self.updated_at = datetime.utcnow()
    
    def is_overdue(self) -> bool:
        """Check if issue is overdue"""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status not in [IssueStatus.RESOLVED, IssueStatus.CLOSED, IssueStatus.CANCELLED]
    
    def get_age_days(self) -> int:
        """Get issue age in days"""
        return (datetime.utcnow() - self.created_at).days
    
    def get_pending_actions_count(self) -> int:
        """Get count of pending actions"""
        return len([action for action in self.actions if action.status == "pending"])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert issue to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "issue_type": self.issue_type.value,
            "category": self.category.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "organization_id": self.organization_id,
            "reported_by": self.reported_by,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "root_cause": self.root_cause,
            "impact_assessment": self.impact_assessment,
            "business_impact": self.business_impact,
            "affected_areas": self.affected_areas,
            "affected_processes": self.affected_processes,
            "affected_systems": self.affected_systems,
            "detected_date": self.detected_date.isoformat() if self.detected_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "resolved_date": self.resolved_date.isoformat() if self.resolved_date else None,
            "closed_date": self.closed_date.isoformat() if self.closed_date else None,
            "related_risks": self.related_risks,
            "related_controls": self.related_controls,
            "related_policies": self.related_policies,
            "related_audits": self.related_audits,
            "actions": [
                {
                    "id": str(action.id),
                    "action_type": action.action_type,
                    "description": action.description,
                    "assigned_to": action.assigned_to,
                    "due_date": action.due_date.isoformat() if action.due_date else None,
                    "status": action.status,
                    "completed_at": action.completed_at.isoformat() if action.completed_at else None,
                    "completed_by": action.completed_by,
                    "notes": action.notes,
                    "created_at": action.created_at.isoformat(),
                    "updated_at": action.updated_at.isoformat()
                }
                for action in self.actions
            ],
            "comments": [
                {
                    "id": str(comment.id),
                    "comment": comment.comment,
                    "author_id": comment.author_id,
                    "author_name": comment.author_name,
                    "created_at": comment.created_at.isoformat(),
                    "is_internal": comment.is_internal,
                    "attachments": comment.attachments
                }
                for comment in self.comments
            ],
            "evidence": [
                {
                    "id": str(evidence.id),
                    "evidence_type": evidence.evidence_type,
                    "description": evidence.description,
                    "file_path": evidence.file_path,
                    "url": evidence.url,
                    "collected_by": evidence.collected_by,
                    "collected_at": evidence.collected_at.isoformat(),
                    "verified": evidence.verified,
                    "verified_by": evidence.verified_by,
                    "verified_at": evidence.verified_at.isoformat() if evidence.verified_at else None
                }
                for evidence in self.evidence
            ],
            "financial_impact": float(self.financial_impact) if self.financial_impact else None,
            "remediation_cost": float(self.remediation_cost) if self.remediation_cost else None,
            "regulatory_implications": self.regulatory_implications,
            "compliance_framework": self.compliance_framework,
            "regulatory_notification_required": self.regulatory_notification_required,
            "regulatory_notification_date": self.regulatory_notification_date.isoformat() if self.regulatory_notification_date else None,
            "escalated_to": self.escalated_to,
            "escalation_reason": self.escalation_reason,
            "escalation_date": self.escalation_date.isoformat() if self.escalation_date else None,
            "tags": self.tags,
            "metadata": self.metadata,
            "external_references": self.external_references,
            "age_days": self.get_age_days(),
            "is_overdue": self.is_overdue(),
            "pending_actions_count": self.get_pending_actions_count()
        }

