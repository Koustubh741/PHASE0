"""
Policy Domain Entity
Core business logic for Policy management in GRC Platform
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4


class PolicyStatus(Enum):
    """Policy status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNDER_REVIEW = "under_review"
    ARCHIVED = "archived"


class PolicyType(Enum):
    """Policy type enumeration"""
    COMPLIANCE = "compliance"
    SECURITY = "security"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    GOVERNANCE = "governance"


@dataclass
class PolicyVersion:
    """Policy version value object"""
    version_number: str
    created_at: datetime
    created_by: str
    change_summary: str
    content: str
    is_active: bool = False


@dataclass
class Policy:
    """Policy domain entity"""
    id: UUID
    title: str
    description: str
    content: str
    policy_type: PolicyType
    status: PolicyStatus
    organization_id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    versions: List[PolicyVersion] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.versions is None:
            self.versions = []
    
    @classmethod
    def create_new(
        cls,
        title: str,
        description: str,
        content: str,
        policy_type: PolicyType,
        organization_id: str,
        owner_id: str,
        effective_date: Optional[datetime] = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> "Policy":
        """Create a new policy"""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            title=title,
            description=description,
            content=content,
            policy_type=policy_type,
            status=PolicyStatus.DRAFT,
            organization_id=organization_id,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
            effective_date=effective_date,
            tags=tags or [],
            metadata=metadata or {}
        )
    
    def activate(self) -> None:
        """Activate the policy"""
        if self.status != PolicyStatus.DRAFT:
            raise ValueError("Only draft policies can be activated")
        self.status = PolicyStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the policy"""
        if self.status not in [PolicyStatus.ACTIVE, PolicyStatus.UNDER_REVIEW]:
            raise ValueError("Only active or under review policies can be deactivated")
        self.status = PolicyStatus.INACTIVE
        self.updated_at = datetime.utcnow()
    
    def archive(self) -> None:
        """Archive the policy"""
        self.status = PolicyStatus.ARCHIVED
        self.updated_at = datetime.utcnow()
    
    def start_review(self) -> None:
        """Start policy review process"""
        if self.status != PolicyStatus.ACTIVE:
            raise ValueError("Only active policies can be put under review")
        self.status = PolicyStatus.UNDER_REVIEW
        self.updated_at = datetime.utcnow()
    
    def update_content(self, new_content: str, updated_by: str, change_summary: str) -> None:
        """Update policy content with version tracking"""
        if self.status == PolicyStatus.ARCHIVED:
            raise ValueError("Cannot update archived policies")
        
        # Deactivate existing active versions first
        for v in self.versions:
            v.is_active = False
        
        # Create new version with the NEW content
        version = PolicyVersion(
            version_number=f"{len(self.versions) + 1}.0",
            created_at=datetime.utcnow(),
            created_by=updated_by,
            change_summary=change_summary,
            content=new_content,  # Store the NEW content, not the old
            is_active=True
        )
        
        # Add new version
        self.versions.append(version)
        
        # Update content
        self.content = new_content
        self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the policy"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the policy"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update policy metadata"""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()
    
    def is_expired(self) -> bool:
        """Check if policy is expired"""
        if self.expiry_date is None:
            return False
        return datetime.utcnow() > self.expiry_date
    
    def is_effective(self) -> bool:
        """Check if policy is currently effective"""
        if self.status != PolicyStatus.ACTIVE:
            return False
        if self.effective_date and datetime.utcnow() < self.effective_date:
            return False
        if self.is_expired():
            return False
        return True
    
    def get_current_version(self) -> Optional[PolicyVersion]:
        """Get the current active version"""
        for version in self.versions:
            if version.is_active:
                return version
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert policy to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "policy_type": self.policy_type.value,
            "status": self.status.value,
            "organization_id": self.organization_id,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "tags": self.tags,
            "metadata": self.metadata,
            "versions": [
                {
                    "version_number": v.version_number,
                    "created_at": v.created_at.isoformat(),
                    "created_by": v.created_by,
                    "change_summary": v.change_summary,
                    "content": v.content,
                    "is_active": v.is_active
                }
                for v in self.versions
            ]
        }
