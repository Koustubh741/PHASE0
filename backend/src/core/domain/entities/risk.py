"""
Risk Domain Entity
Core business logic for Risk management in GRC Platform
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from decimal import Decimal


class RiskStatus(Enum):
    """Risk status enumeration"""
    IDENTIFIED = "identified"
    ASSESSED = "assessed"
    TREATED = "treated"
    MONITORED = "monitored"
    CLOSED = "closed"
    ESCALATED = "escalated"


class RiskCategory(Enum):
    """Risk category enumeration"""
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    STRATEGIC = "strategic"
    COMPLIANCE = "compliance"
    REPUTATIONAL = "reputational"
    TECHNOLOGY = "technology"
    CYBERSECURITY = "cybersecurity"
    THIRD_PARTY = "third_party"
    REGULATORY = "regulatory"
    ENVIRONMENTAL = "environmental"


class RiskLikelihood(Enum):
    """Risk likelihood enumeration"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class RiskImpact(Enum):
    """Risk impact enumeration"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class TreatmentStrategy(Enum):
    """Risk treatment strategy enumeration"""
    AVOID = "avoid"
    MITIGATE = "mitigate"
    TRANSFER = "transfer"
    ACCEPT = "accept"


@dataclass
class RiskAssessment:
    """Risk assessment value object"""
    likelihood: RiskLikelihood
    impact: RiskImpact
    assessed_by: str
    assessed_at: datetime
    notes: str
    confidence_level: int = 5  # 1-10 scale
    
    @property
    def risk_score(self) -> int:
        """Calculate risk score based on likelihood and impact"""
        likelihood_scores = {
            RiskLikelihood.VERY_LOW: 1,
            RiskLikelihood.LOW: 2,
            RiskLikelihood.MEDIUM: 3,
            RiskLikelihood.HIGH: 4,
            RiskLikelihood.VERY_HIGH: 5
        }
        
        impact_scores = {
            RiskImpact.VERY_LOW: 1,
            RiskImpact.LOW: 2,
            RiskImpact.MEDIUM: 3,
            RiskImpact.HIGH: 4,
            RiskImpact.VERY_HIGH: 5
        }
        
        return likelihood_scores[self.likelihood] * impact_scores[self.impact]
    
    @property
    def risk_level(self) -> str:
        """Get risk level based on score"""
        if self.risk_score <= 4:
            return "low"
        elif self.risk_score <= 9:
            return "medium"
        elif self.risk_score <= 16:
            return "high"
        else:
            return "critical"


@dataclass
class RiskTreatment:
    """Risk treatment value object"""
    strategy: TreatmentStrategy
    description: str
    owner: str
    target_date: Optional[datetime] = None
    cost_estimate: Optional[Decimal] = None
    status: str = "planned"
    notes: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class RiskMitigation:
    """Risk mitigation measure value object"""
    title: str
    description: str
    owner: str
    due_date: Optional[datetime] = None
    status: str = "pending"
    completion_percentage: int = 0
    notes: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class Risk:
    """Risk domain entity"""
    id: UUID
    title: str
    description: str
    category: RiskCategory
    status: RiskStatus
    organization_id: str
    owner_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    # Risk details
    source: Optional[str] = None
    business_impact: Optional[str] = None
    affected_assets: List[str] = None
    affected_processes: List[str] = None
    affected_systems: List[str] = None
    
    # Assessment
    current_assessment: Optional[RiskAssessment] = None
    previous_assessments: List[RiskAssessment] = None
    
    # Treatment
    treatment_strategy: Optional[TreatmentStrategy] = None
    treatment_plan: Optional[str] = None
    treatments: List[RiskTreatment] = None
    mitigations: List[RiskMitigation] = None
    
    # Monitoring
    next_review_date: Optional[datetime] = None
    review_frequency_days: int = 90
    escalation_threshold: Optional[int] = None
    
    # Metadata
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    external_references: List[str] = None
    
    def __post_init__(self):
        if self.affected_assets is None:
            self.affected_assets = []
        if self.affected_processes is None:
            self.affected_processes = []
        if self.affected_systems is None:
            self.affected_systems = []
        if self.previous_assessments is None:
            self.previous_assessments = []
        if self.treatments is None:
            self.treatments = []
        if self.mitigations is None:
            self.mitigations = []
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
        category: RiskCategory,
        organization_id: str,
        owner_id: str,
        created_by: str,
        source: Optional[str] = None,
        business_impact: Optional[str] = None,
        tags: List[str] = None
    ) -> "Risk":
        """Create a new risk"""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            title=title,
            description=description,
            category=category,
            status=RiskStatus.IDENTIFIED,
            organization_id=organization_id,
            owner_id=owner_id,
            created_by=created_by,
            created_at=now,
            updated_at=now,
            source=source,
            business_impact=business_impact,
            tags=tags or []
        )
    
    def assess_risk(
        self,
        likelihood: RiskLikelihood,
        impact: RiskImpact,
        assessed_by: str,
        notes: str = "",
        confidence_level: int = 5
    ) -> None:
        """Assess the risk"""
        if self.status not in [RiskStatus.IDENTIFIED, RiskStatus.ASSESSED]:
            raise ValueError("Risk must be in identified or assessed status to be assessed")
        
        # Move previous assessment to history
        if self.current_assessment:
            self.previous_assessments.append(self.current_assessment)
        
        # Create new assessment
        self.current_assessment = RiskAssessment(
            likelihood=likelihood,
            impact=impact,
            assessed_by=assessed_by,
            assessed_at=datetime.utcnow(),
            notes=notes,
            confidence_level=confidence_level
        )
        
        self.status = RiskStatus.ASSESSED
        self.updated_at = datetime.utcnow()
    
    def add_treatment(
        self,
        strategy: TreatmentStrategy,
        description: str,
        owner: str,
        target_date: Optional[datetime] = None,
        cost_estimate: Optional[Decimal] = None,
        notes: str = ""
    ) -> None:
        """Add risk treatment"""
        treatment = RiskTreatment(
            strategy=strategy,
            description=description,
            owner=owner,
            target_date=target_date,
            cost_estimate=cost_estimate,
            notes=notes
        )
        
        self.treatments.append(treatment)
        self.treatment_strategy = strategy
        self.status = RiskStatus.TREATED
        self.updated_at = datetime.utcnow()
    
    def add_mitigation(
        self,
        title: str,
        description: str,
        owner: str,
        due_date: Optional[datetime] = None,
        notes: str = ""
    ) -> None:
        """Add risk mitigation"""
        mitigation = RiskMitigation(
            title=title,
            description=description,
            owner=owner,
            due_date=due_date,
            notes=notes
        )
        
        self.mitigations.append(mitigation)
        self.updated_at = datetime.utcnow()
    
    def update_mitigation_status(self, mitigation_index: int, status: str, completion_percentage: int = None, notes: str = "") -> None:
        """Update mitigation status"""
        if 0 <= mitigation_index < len(self.mitigations):
            mitigation = self.mitigations[mitigation_index]
            mitigation.status = status
            mitigation.updated_at = datetime.utcnow()
            
            if completion_percentage is not None:
                mitigation.completion_percentage = completion_percentage
            
            if notes:
                mitigation.notes = notes
            
            self.updated_at = datetime.utcnow()
        else:
            raise ValueError("Invalid mitigation index")
    
    def close_risk(self, closed_by: str, closure_notes: str = "") -> None:
        """Close the risk"""
        if self.status not in [RiskStatus.TREATED, RiskStatus.MONITORED]:
            raise ValueError("Risk must be treated or monitored to be closed")
        
        self.status = RiskStatus.CLOSED
        self.metadata["closed_by"] = closed_by
        self.metadata["closed_at"] = datetime.utcnow().isoformat()
        if closure_notes:
            self.metadata["closure_notes"] = closure_notes
        
        self.updated_at = datetime.utcnow()
    
    def escalate_risk(self, escalated_by: str, escalation_reason: str) -> None:
        """Escalate the risk"""
        self.status = RiskStatus.ESCALATED
        self.metadata["escalated_by"] = escalated_by
        self.metadata["escalated_at"] = datetime.utcnow().isoformat()
        self.metadata["escalation_reason"] = escalation_reason
        
        self.updated_at = datetime.utcnow()
    
    def schedule_review(self, review_date: datetime, frequency_days: int = 90) -> None:
        """Schedule risk review"""
        self.next_review_date = review_date
        self.review_frequency_days = frequency_days
        self.status = RiskStatus.MONITORED
        self.updated_at = datetime.utcnow()
    
    def is_overdue_for_review(self) -> bool:
        """Check if risk is overdue for review"""
        if not self.next_review_date:
            return False
        return datetime.utcnow() > self.next_review_date
    
    def get_risk_score(self) -> Optional[int]:
        """Get current risk score"""
        if self.current_assessment:
            return self.current_assessment.risk_score
        return None
    
    def get_risk_level(self) -> Optional[str]:
        """Get current risk level"""
        if self.current_assessment:
            return self.current_assessment.risk_level
        return None
    
    def add_tag(self, tag: str) -> None:
        """Add tag to risk"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """Remove tag from risk"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update risk metadata"""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()
    
    def add_external_reference(self, reference: str) -> None:
        """Add external reference"""
        if reference not in self.external_references:
            self.external_references.append(reference)
            self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert risk to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "status": self.status.value,
            "organization_id": self.organization_id,
            "owner_id": self.owner_id,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "source": self.source,
            "business_impact": self.business_impact,
            "affected_assets": self.affected_assets,
            "affected_processes": self.affected_processes,
            "affected_systems": self.affected_systems,
            "current_assessment": {
                "likelihood": self.current_assessment.likelihood.value,
                "impact": self.current_assessment.impact.value,
                "risk_score": self.current_assessment.risk_score,
                "risk_level": self.current_assessment.risk_level,
                "assessed_by": self.current_assessment.assessed_by,
                "assessed_at": self.current_assessment.assessed_at.isoformat(),
                "notes": self.current_assessment.notes,
                "confidence_level": self.current_assessment.confidence_level
            } if self.current_assessment else None,
            "treatment_strategy": self.treatment_strategy.value if self.treatment_strategy else None,
            "treatment_plan": self.treatment_plan,
            "treatments": [
                {
                    "strategy": t.strategy.value,
                    "description": t.description,
                    "owner": t.owner,
                    "target_date": t.target_date.isoformat() if t.target_date else None,
                    "cost_estimate": float(t.cost_estimate) if t.cost_estimate else None,
                    "status": t.status,
                    "notes": t.notes,
                    "created_at": t.created_at.isoformat(),
                    "updated_at": t.updated_at.isoformat()
                }
                for t in self.treatments
            ],
            "mitigations": [
                {
                    "title": m.title,
                    "description": m.description,
                    "owner": m.owner,
                    "due_date": m.due_date.isoformat() if m.due_date else None,
                    "status": m.status,
                    "completion_percentage": m.completion_percentage,
                    "notes": m.notes,
                    "created_at": m.created_at.isoformat(),
                    "updated_at": m.updated_at.isoformat()
                }
                for m in self.mitigations
            ],
            "next_review_date": self.next_review_date.isoformat() if self.next_review_date else None,
            "review_frequency_days": self.review_frequency_days,
            "escalation_threshold": self.escalation_threshold,
            "tags": self.tags,
            "metadata": self.metadata,
            "external_references": self.external_references,
            "risk_score": self.get_risk_score(),
            "risk_level": self.get_risk_level(),
            "is_overdue_for_review": self.is_overdue_for_review()
        }

