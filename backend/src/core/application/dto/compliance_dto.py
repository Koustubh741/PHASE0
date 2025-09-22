"""
Compliance Framework Data Transfer Objects
DTOs for compliance framework operations
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class ComplianceFramework(str, Enum):
    """Compliance framework enumeration"""
    SOX = "sox"
    GDPR = "gdpr"
    PCI_DSS = "pci_dss"
    HIPAA = "hipaa"
    ISO27001 = "iso27001"
    NIST = "nist"
    COSO = "coso"
    COBIT = "cobit"


class ComplianceStatus(str, Enum):
    """Compliance status enumeration"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"
    PENDING = "pending"
    EXEMPT = "exempt"


class RequirementType(str, Enum):
    """Requirement type enumeration"""
    CONTROL = "control"
    POLICY = "policy"
    PROCEDURE = "procedure"
    TRAINING = "training"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    MONITORING = "monitoring"


class AssessmentStatus(str, Enum):
    """Assessment status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FrameworkResponse(BaseModel):
    """Compliance framework response"""
    framework: str = Field(..., description="Framework identifier")
    name: str = Field(..., description="Framework name")
    description: str = Field(..., description="Framework description")
    requirements_count: int = Field(..., description="Number of requirements")
    last_updated: str = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "framework": "sox",
                "name": "SOX",
                "description": "Sarbanes-Oxley Act - Financial reporting and internal controls",
                "requirements_count": 15,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }


class RequirementResponse(BaseModel):
    """Compliance requirement response"""
    requirement_id: str = Field(..., description="Requirement ID")
    framework: str = Field(..., description="Framework")
    section: str = Field(..., description="Section")
    subsection: str = Field(..., description="Subsection")
    title: str = Field(..., description="Requirement title")
    description: str = Field(..., description="Requirement description")
    requirement_type: str = Field(..., description="Requirement type")
    priority: str = Field(..., description="Priority level")
    implementation_guidance: str = Field(..., description="Implementation guidance")
    testing_procedures: List[str] = Field(..., description="Testing procedures")
    evidence_requirements: List[str] = Field(..., description="Evidence requirements")
    applicable_to: List[str] = Field(..., description="Applicable departments/roles")
    effective_date: datetime = Field(..., description="Effective date")
    last_updated: datetime = Field(..., description="Last update timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "requirement_id": "123e4567-e89b-12d3-a456-426614174000",
                "framework": "sox",
                "section": "302",
                "subsection": "a",
                "title": "Certification of Financial Statements",
                "description": "CEO and CFO must certify financial statements",
                "requirement_type": "control",
                "priority": "high",
                "implementation_guidance": "Implement quarterly certification process",
                "testing_procedures": ["Review certification documents", "Verify signatory authority"],
                "evidence_requirements": ["Signed certifications", "Board resolutions"],
                "applicable_to": ["finance", "accounting", "audit"],
                "effective_date": "2024-01-15T10:30:00Z",
                "last_updated": "2024-01-15T10:30:00Z",
                "metadata": {"framework_version": "2024.1"}
            }
        }


class AssessmentRequest(BaseModel):
    """Request to create a compliance assessment"""
    framework: str = Field(..., description="Framework to assess")
    organization_id: str = Field(..., description="Organization ID")
    assessor_id: str = Field(..., description="Assessor ID")
    scope: List[str] = Field(..., description="Assessment scope")
    methodology: str = Field("standard", description="Assessment methodology")
    
    class Config:
        json_schema_extra = {
            "example": {
                "framework": "sox",
                "organization_id": "org-123",
                "assessor_id": "user-456",
                "scope": ["finance", "accounting", "audit"],
                "methodology": "standard"
            }
        }


class AssessmentResponse(BaseModel):
    """Compliance assessment response"""
    assessment_id: str = Field(..., description="Assessment ID")
    framework: str = Field(..., description="Framework")
    organization_id: str = Field(..., description="Organization ID")
    assessor_id: str = Field(..., description="Assessor ID")
    status: str = Field(..., description="Assessment status")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    scope: List[str] = Field(..., description="Assessment scope")
    methodology: str = Field(..., description="Assessment methodology")
    findings: List[Dict[str, Any]] = Field(default_factory=list, description="Assessment findings")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    overall_score: float = Field(0.0, description="Overall score")
    compliance_percentage: float = Field(0.0, description="Compliance percentage")
    risk_level: str = Field("unknown", description="Risk level")
    next_assessment_date: Optional[datetime] = Field(None, description="Next assessment date")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "assessment_id": "789e0123-e89b-12d3-a456-426614174000",
                "framework": "sox",
                "organization_id": "org-123",
                "assessor_id": "user-456",
                "status": "completed",
                "start_date": "2024-01-15T10:30:00Z",
                "end_date": "2024-01-15T12:30:00Z",
                "scope": ["finance", "accounting", "audit"],
                "methodology": "standard",
                "findings": [],
                "recommendations": [],
                "overall_score": 0.85,
                "compliance_percentage": 85.0,
                "risk_level": "medium",
                "next_assessment_date": "2025-01-15T10:30:00Z",
                "metadata": {}
            }
        }


class GapResponse(BaseModel):
    """Compliance gap response"""
    gap_id: str = Field(..., description="Gap ID")
    framework: str = Field(..., description="Framework")
    requirement_id: str = Field(..., description="Requirement ID")
    gap_description: str = Field(..., description="Gap description")
    severity: str = Field(..., description="Gap severity")
    impact_assessment: str = Field(..., description="Impact assessment")
    remediation_plan: str = Field(..., description="Remediation plan")
    responsible_party: str = Field(..., description="Responsible party")
    target_date: datetime = Field(..., description="Target date")
    status: str = Field(..., description="Gap status")
    evidence: List[str] = Field(default_factory=list, description="Evidence")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gap_id": "456e7890-e89b-12d3-a456-426614174000",
                "framework": "sox",
                "requirement_id": "123e4567-e89b-12d3-a456-426614174000",
                "gap_description": "Missing quarterly certification process",
                "severity": "high",
                "impact_assessment": "High impact on compliance posture",
                "remediation_plan": "Implement quarterly certification process",
                "responsible_party": "Compliance Team",
                "target_date": "2024-02-15T10:30:00Z",
                "status": "open",
                "evidence": [],
                "metadata": {"assessment_id": "789e0123-e89b-12d3-a456-426614174000"}
            }
        }


class ComplianceDashboardResponse(BaseModel):
    """Compliance dashboard response"""
    framework_scores: Dict[str, Dict[str, Any]] = Field(..., description="Framework scores")
    total_assessments: int = Field(..., description="Total assessments")
    active_gaps: int = Field(..., description="Active gaps")
    overall_compliance: float = Field(..., description="Overall compliance score")
    last_updated: str = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "framework_scores": {
                    "sox": {
                        "compliance_percentage": 85.0,
                        "risk_level": "medium",
                        "last_assessment": "2024-01-15T12:30:00Z"
                    },
                    "gdpr": {
                        "compliance_percentage": 92.0,
                        "risk_level": "low",
                        "last_assessment": "2024-01-10T14:30:00Z"
                    }
                },
                "total_assessments": 5,
                "active_gaps": 3,
                "overall_compliance": 0.88,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }


class PerformanceMetricsResponse(BaseModel):
    """Performance metrics response"""
    total_frameworks: int = Field(..., description="Total frameworks")
    total_requirements: int = Field(..., description="Total requirements")
    total_assessments: int = Field(..., description="Total assessments")
    total_gaps: int = Field(..., description="Total gaps")
    compliance_score: float = Field(..., description="Overall compliance score")
    assessment_completion_rate: float = Field(..., description="Assessment completion rate")
    last_updated: str = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_frameworks": 8,
                "total_requirements": 45,
                "total_assessments": 12,
                "total_gaps": 5,
                "compliance_score": 0.88,
                "assessment_completion_rate": 0.75,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }
