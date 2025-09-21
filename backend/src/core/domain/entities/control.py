"""
Control Domain Entity
Core business logic for Control management in GRC Platform
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from decimal import Decimal


class ControlStatus(Enum):
    """Control status enumeration"""
    DESIGNED = "designed"
    IMPLEMENTED = "implemented"
    OPERATING = "operating"
    EFFECTIVE = "effective"
    INEFFECTIVE = "ineffective"
    RETIRED = "retired"


class ControlType(Enum):
    """Control type enumeration"""
    PREVENTIVE = "preventive"
    DETECTIVE = "detective"
    CORRECTIVE = "corrective"
    COMPENSATING = "compensating"


class ControlNature(Enum):
    """Control nature enumeration"""
    AUTOMATED = "automated"
    MANUAL = "manual"
    IT_DEPENDENT = "it_dependent"


class ControlFrequency(Enum):
    """Control frequency enumeration"""
    CONTINUOUS = "continuous"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    AS_NEEDED = "as_needed"


class TestResult(Enum):
    """Test result enumeration"""
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    NOT_TESTED = "not_tested"
    EXCEPTION = "exception"


@dataclass
class ControlTest:
    """Control test value object"""
    test_name: str
    test_type: str
    description: str
    tester: str
    test_date: datetime
    result: TestResult
    findings: str = ""
    recommendations: str = ""
    evidence: List[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class ControlOwner:
    """Control owner value object"""
    user_id: str
    role: str
    assigned_date: datetime
    is_primary: bool = True
    notes: str = ""


@dataclass
class Control:
    """Control domain entity"""
    id: UUID
    title: str
    description: str
    control_type: ControlType
    control_nature: ControlNature
    frequency: ControlFrequency
    status: ControlStatus
    organization_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    # Control details
    objective: Optional[str] = None
    risk_mitigated: List[str] = None
    applicable_regulations: List[str] = None
    applicable_frameworks: List[str] = None
    
    # Implementation
    implementation_date: Optional[datetime] = None
    implementation_notes: str = ""
    cost_estimate: Optional[Decimal] = None
    
    # Testing
    last_test_date: Optional[datetime] = None
    next_test_date: Optional[datetime] = None
    test_frequency_days: int = 90
    tests: List[ControlTest] = None
    
    # Ownership
    owners: List[ControlOwner] = None
    primary_owner: Optional[str] = None
    
    # Effectiveness
    effectiveness_rating: Optional[int] = None  # 1-5 scale
    effectiveness_notes: str = ""
    last_effectiveness_review: Optional[datetime] = None
    
    # Dependencies
    dependent_controls: List[str] = None
    supporting_processes: List[str] = None
    supporting_systems: List[str] = None
    
    # Metadata
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    external_references: List[str] = None
    
    def __post_init__(self):
        if self.risk_mitigated is None:
            self.risk_mitigated = []
        if self.applicable_regulations is None:
            self.applicable_regulations = []
        if self.applicable_frameworks is None:
            self.applicable_frameworks = []
        if self.tests is None:
            self.tests = []
        if self.owners is None:
            self.owners = []
        if self.dependent_controls is None:
            self.dependent_controls = []
        if self.supporting_processes is None:
            self.supporting_processes = []
        if self.supporting_systems is None:
            self.supporting_systems = []
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
        control_type: ControlType,
        control_nature: ControlNature,
        frequency: ControlFrequency,
        organization_id: str,
        created_by: str,
        objective: Optional[str] = None,
        risk_mitigated: List[str] = None,
        tags: List[str] = None
    ) -> "Control":
        """Create a new control"""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            title=title,
            description=description,
            control_type=control_type,
            control_nature=control_nature,
            frequency=frequency,
            status=ControlStatus.DESIGNED,
            organization_id=organization_id,
            created_by=created_by,
            created_at=now,
            updated_at=now,
            objective=objective,
            risk_mitigated=risk_mitigated or [],
            tags=tags or []
        )
    
    def implement(self, implementation_notes: str = "", cost_estimate: Optional[Decimal] = None) -> None:
        """Mark control as implemented"""
        if self.status != ControlStatus.DESIGNED:
            raise ValueError("Only designed controls can be implemented")
        
        self.status = ControlStatus.IMPLEMENTED
        self.implementation_date = datetime.utcnow()
        self.implementation_notes = implementation_notes
        if cost_estimate:
            self.cost_estimate = cost_estimate
        
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate control for operation"""
        if self.status != ControlStatus.IMPLEMENTED:
            raise ValueError("Only implemented controls can be activated")
        
        self.status = ControlStatus.OPERATING
        self.updated_at = datetime.utcnow()
    
    def add_owner(self, user_id: str, role: str, is_primary: bool = False, notes: str = "") -> None:
        """Add control owner"""
        # If this is a primary owner, remove primary status from others
        if is_primary:
            for owner in self.owners:
                owner.is_primary = False
        
        owner = ControlOwner(
            user_id=user_id,
            role=role,
            assigned_date=datetime.utcnow(),
            is_primary=is_primary,
            notes=notes
        )
        
        self.owners.append(owner)
        
        if is_primary:
            self.primary_owner = user_id
        
        self.updated_at = datetime.utcnow()
    
    def remove_owner(self, user_id: str) -> None:
        """Remove control owner"""
        self.owners = [owner for owner in self.owners if owner.user_id != user_id]
        
        if self.primary_owner == user_id:
            self.primary_owner = None
            # Assign new primary owner if available
            if self.owners:
                self.owners[0].is_primary = True
                self.primary_owner = self.owners[0].user_id
        
        self.updated_at = datetime.utcnow()
    
    def add_test(
        self,
        test_name: str,
        test_type: str,
        description: str,
        tester: str,
        result: TestResult,
        findings: str = "",
        recommendations: str = "",
        evidence: List[str] = None
    ) -> None:
        """Add control test"""
        test = ControlTest(
            test_name=test_name,
            test_type=test_type,
            description=description,
            tester=tester,
            test_date=datetime.utcnow(),
            result=result,
            findings=findings,
            recommendations=recommendations,
            evidence=evidence or []
        )
        
        self.tests.append(test)
        self.last_test_date = test.test_date
        
        # Schedule next test
        self.next_test_date = test.test_date + timedelta(days=self.test_frequency_days)
        
        # Update status based on test result
        if result == TestResult.PASS and self.status == ControlStatus.OPERATING:
            self.status = ControlStatus.EFFECTIVE
        elif result == TestResult.FAIL:
            self.status = ControlStatus.INEFFECTIVE
        
        self.updated_at = datetime.utcnow()
    
    def schedule_test(self, test_date: datetime) -> None:
        """Schedule control test"""
        self.next_test_date = test_date
        self.updated_at = datetime.utcnow()
    
    def is_overdue_for_testing(self) -> bool:
        """Check if control is overdue for testing"""
        if not self.next_test_date:
            return False
        return datetime.utcnow() > self.next_test_date
    
    def assess_effectiveness(self, rating: int, notes: str = "", reviewer: str = "") -> None:
        """Assess control effectiveness"""
        if not 1 <= rating <= 5:
            raise ValueError("Effectiveness rating must be between 1 and 5")
        
        self.effectiveness_rating = rating
        self.effectiveness_notes = notes
        self.last_effectiveness_review = datetime.utcnow()
        
        if reviewer:
            self.metadata["last_effectiveness_reviewer"] = reviewer
        
        # Update status based on effectiveness
        if rating >= 4:
            self.status = ControlStatus.EFFECTIVE
        elif rating <= 2:
            self.status = ControlStatus.INEFFECTIVE
        
        self.updated_at = datetime.utcnow()
    
    def retire(self, retirement_reason: str = "") -> None:
        """Retire the control"""
        self.status = ControlStatus.RETIRED
        self.metadata["retired_at"] = datetime.utcnow().isoformat()
        if retirement_reason:
            self.metadata["retirement_reason"] = retirement_reason
        
        self.updated_at = datetime.utcnow()
    
    def add_risk_mitigated(self, risk_id: str) -> None:
        """Add risk that this control mitigates"""
        if risk_id not in self.risk_mitigated:
            self.risk_mitigated.append(risk_id)
            self.updated_at = datetime.utcnow()
    
    def remove_risk_mitigated(self, risk_id: str) -> None:
        """Remove risk from mitigation list"""
        if risk_id in self.risk_mitigated:
            self.risk_mitigated.remove(risk_id)
            self.updated_at = datetime.utcnow()
    
    def add_applicable_regulation(self, regulation: str) -> None:
        """Add applicable regulation"""
        if regulation not in self.applicable_regulations:
            self.applicable_regulations.append(regulation)
            self.updated_at = datetime.utcnow()
    
    def add_applicable_framework(self, framework: str) -> None:
        """Add applicable framework"""
        if framework not in self.applicable_frameworks:
            self.applicable_frameworks.append(framework)
            self.updated_at = datetime.utcnow()
    
    def add_dependent_control(self, control_id: str) -> None:
        """Add dependent control"""
        if control_id not in self.dependent_controls:
            self.dependent_controls.append(control_id)
            self.updated_at = datetime.utcnow()
    
    def add_supporting_process(self, process: str) -> None:
        """Add supporting process"""
        if process not in self.supporting_processes:
            self.supporting_processes.append(process)
            self.updated_at = datetime.utcnow()
    
    def add_supporting_system(self, system: str) -> None:
        """Add supporting system"""
        if system not in self.supporting_systems:
            self.supporting_systems.append(system)
            self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> None:
        """Add tag to control"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """Remove tag from control"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update control metadata"""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()
    
    def add_external_reference(self, reference: str) -> None:
        """Add external reference"""
        if reference not in self.external_references:
            self.external_references.append(reference)
            self.updated_at = datetime.utcnow()
    
    def get_latest_test_result(self) -> Optional[TestResult]:
        """Get the result of the most recent test"""
        if not self.tests:
            return None
        return max(self.tests, key=lambda t: t.test_date).result
    
    def get_test_success_rate(self) -> float:
        """Calculate test success rate"""
        if not self.tests:
            return 0.0
        
        passed_tests = sum(1 for test in self.tests if test.result == TestResult.PASS)
        return passed_tests / len(self.tests) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert control to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "control_type": self.control_type.value,
            "control_nature": self.control_nature.value,
            "frequency": self.frequency.value,
            "status": self.status.value,
            "organization_id": self.organization_id,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "objective": self.objective,
            "risk_mitigated": self.risk_mitigated,
            "applicable_regulations": self.applicable_regulations,
            "applicable_frameworks": self.applicable_frameworks,
            "implementation_date": self.implementation_date.isoformat() if self.implementation_date else None,
            "implementation_notes": self.implementation_notes,
            "cost_estimate": float(self.cost_estimate) if self.cost_estimate else None,
            "last_test_date": self.last_test_date.isoformat() if self.last_test_date else None,
            "next_test_date": self.next_test_date.isoformat() if self.next_test_date else None,
            "test_frequency_days": self.test_frequency_days,
            "owners": [
                {
                    "user_id": owner.user_id,
                    "role": owner.role,
                    "assigned_date": owner.assigned_date.isoformat(),
                    "is_primary": owner.is_primary,
                    "notes": owner.notes
                }
                for owner in self.owners
            ],
            "primary_owner": self.primary_owner,
            "effectiveness_rating": self.effectiveness_rating,
            "effectiveness_notes": self.effectiveness_notes,
            "last_effectiveness_review": self.last_effectiveness_review.isoformat() if self.last_effectiveness_review else None,
            "dependent_controls": self.dependent_controls,
            "supporting_processes": self.supporting_processes,
            "supporting_systems": self.supporting_systems,
            "tests": [
                {
                    "test_name": test.test_name,
                    "test_type": test.test_type,
                    "description": test.description,
                    "tester": test.tester,
                    "test_date": test.test_date.isoformat(),
                    "result": test.result.value,
                    "findings": test.findings,
                    "recommendations": test.recommendations,
                    "evidence": test.evidence,
                    "created_at": test.created_at.isoformat(),
                    "updated_at": test.updated_at.isoformat()
                }
                for test in self.tests
            ],
            "tags": self.tags,
            "metadata": self.metadata,
            "external_references": self.external_references,
            "latest_test_result": self.get_latest_test_result().value if self.get_latest_test_result() else None,
            "test_success_rate": self.get_test_success_rate(),
            "is_overdue_for_testing": self.is_overdue_for_testing()
        }

