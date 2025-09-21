"""
Policy Data Transfer Objects
DTOs for policy management operations
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...domain.entities.policy import Policy, PolicyStatus, PolicyType


class PolicyCreateRequest(BaseModel):
    """Policy creation request DTO"""
    title: str = Field(..., min_length=1, max_length=255, description="Policy title")
    description: str = Field(..., min_length=1, description="Policy description")
    content: str = Field(..., min_length=1, description="Policy content")
    policy_type: str = Field(..., description="Policy type")
    effective_date: Optional[datetime] = Field(None, description="Effective date")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date")
    tags: List[str] = Field(default_factory=list, description="Policy tags")
    
    @validator('policy_type')
    def validate_policy_type(cls, v):
        valid_types = [ptype.value for ptype in PolicyType]
        if v not in valid_types:
            raise ValueError(f'Policy type must be one of: {", ".join(valid_types)}')
        return v


class PolicyUpdateRequest(BaseModel):
    """Policy update request DTO"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Policy title")
    description: Optional[str] = Field(None, min_length=1, description="Policy description")
    content: Optional[str] = Field(None, min_length=1, description="Policy content")
    effective_date: Optional[datetime] = Field(None, description="Effective date")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date")
    tags: Optional[List[str]] = Field(None, description="Policy tags")


class PolicyResponse(BaseModel):
    """Policy response DTO"""
    id: UUID = Field(..., description="Policy ID")
    title: str = Field(..., description="Policy title")
    description: str = Field(..., description="Policy description")
    content: str = Field(..., description="Policy content")
    policy_type: str = Field(..., description="Policy type")
    status: str = Field(..., description="Policy status")
    organization_id: str = Field(..., description="Organization ID")
    owner_id: str = Field(..., description="Owner ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    effective_date: Optional[datetime] = Field(None, description="Effective date")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date")
    tags: List[str] = Field(..., description="Policy tags")
    metadata: Dict[str, Any] = Field(..., description="Policy metadata")
    versions: List[Dict[str, Any]] = Field(..., description="Policy versions")
    is_effective: bool = Field(..., description="Whether policy is currently effective")
    is_expired: bool = Field(..., description="Whether policy is expired")
    
    @classmethod
    def from_policy(cls, policy: Policy) -> "PolicyResponse":
        """Create PolicyResponse from Policy entity"""
        return cls(
            id=policy.id,
            title=policy.title,
            description=policy.description,
            content=policy.content,
            policy_type=policy.policy_type.value,
            status=policy.status.value,
            organization_id=policy.organization_id,
            owner_id=policy.owner_id,
            created_at=policy.created_at,
            updated_at=policy.updated_at,
            effective_date=policy.effective_date,
            expiry_date=policy.expiry_date,
            tags=policy.tags,
            metadata=policy.metadata,
            versions=[
                {
                    "version_number": v.version_number,
                    "created_at": v.created_at.isoformat(),
                    "created_by": v.created_by,
                    "change_summary": v.change_summary,
                    "content": v.content,
                    "is_active": v.is_active
                }
                for v in policy.versions
            ],
            is_effective=policy.is_effective(),
            is_expired=policy.is_expired()
        )


class PolicyListResponse(BaseModel):
    """Policy list response DTO"""
    policies: List[PolicyResponse] = Field(..., description="List of policies")
    total: int = Field(..., description="Total number of policies")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum number of records")


class PolicyVersionRequest(BaseModel):
    """Policy version creation request DTO"""
    content: str = Field(..., min_length=1, description="New policy content")
    change_summary: str = Field(..., min_length=1, description="Summary of changes")


class PolicyApprovalRequest(BaseModel):
    """Policy approval request DTO"""
    approved: bool = Field(..., description="Whether policy is approved")
    notes: str = Field(..., min_length=1, description="Approval/rejection notes")


class PolicySearchRequest(BaseModel):
    """Policy search request DTO"""
    query: str = Field(..., min_length=1, description="Search query")
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters")


class PolicyStatisticsResponse(BaseModel):
    """Policy statistics response DTO"""
    total_policies: int = Field(..., description="Total number of policies")
    active_policies: int = Field(..., description="Number of active policies")
    draft_policies: int = Field(..., description="Number of draft policies")
    under_review: int = Field(..., description="Number of policies under review")
    expired_policies: int = Field(..., description="Number of expired policies")
    policies_by_type: Dict[str, int] = Field(..., description="Policy count by type")
    policies_by_status: Dict[str, int] = Field(..., description="Policy count by status")
    recent_policies: int = Field(..., description="Policies created in last 30 days")
    expiring_soon: int = Field(..., description="Policies expiring in next 30 days")


class PolicyStatusChangeRequest(BaseModel):
    """Policy status change request DTO"""
    status: str = Field(..., description="New policy status")
    reason: str = Field(..., min_length=1, description="Reason for status change")
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = [status.value for status in PolicyStatus]
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v


class PolicyBulkUpdateRequest(BaseModel):
    """Policy bulk update request DTO"""
    policy_ids: List[UUID] = Field(..., min_items=1, description="List of policy IDs to update")
    updates: Dict[str, Any] = Field(..., description="Updates to apply")


class PolicyTagRequest(BaseModel):
    """Policy tag request DTO"""
    tags: List[str] = Field(..., min_items=1, description="Tags to add or remove")


class PolicyExportRequest(BaseModel):
    """Policy export request DTO"""
    policy_ids: Optional[List[UUID]] = Field(None, description="Specific policies to export")
    format: str = Field("json", description="Export format")
    include_versions: bool = Field(False, description="Include policy versions")
    
    @validator('format')
    def validate_format(cls, v):
        valid_formats = ["json", "pdf", "docx"]
        if v not in valid_formats:
            raise ValueError(f'Format must be one of: {", ".join(valid_formats)}')
        return v


class PolicyImportRequest(BaseModel):
    """Policy import request DTO"""
    file_path: str = Field(..., description="Path to import file")
    format: str = Field("json", description="Import format")
    overwrite_existing: bool = Field(False, description="Overwrite existing policies")
    
    @validator('format')
    def validate_format(cls, v):
        valid_formats = ["json", "csv", "xlsx"]
        if v not in valid_formats:
            raise ValueError(f'Format must be one of: {", ".join(valid_formats)}')
        return v
