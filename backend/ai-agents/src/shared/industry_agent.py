"""
Shared Industry Agent Components
Base classes and types for industry-specific GRC agents
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime


class IndustryType(Enum):
    """Industry types supported by the GRC system"""
    BFSI = "BFSI"
    HEALTHCARE = "HEALTHCARE"
    MANUFACTURING = "MANUFACTURING"
    TELECOM = "TELECOM"
    ENERGY = "ENERGY"
    RETAIL = "RETAIL"


class GRCOperationType(Enum):
    """GRC operation types"""
    RISK_ASSESSMENT = "risk_assessment"
    COMPLIANCE_CHECK = "compliance_check"
    POLICY_REVIEW = "policy_review"
    AUDIT_SCHEDULING = "audit_scheduling"
    INCIDENT_RESPONSE = "incident_response"
    REGULATORY_REPORTING = "regulatory_reporting"


@dataclass
class IndustryAgentConfig:
    """Configuration for industry agents"""
    agent_id: str
    name: str
    industry_type: IndustryType
    max_concurrent_operations: int = 10
    operation_timeout: int = 300
    monitoring_enabled: bool = True
    alert_thresholds: Dict[str, float] = None
    
    def __post_init__(self):
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                "compliance_score": 80.0,
                "risk_score": 70.0,
                "uptime_percentage": 95.0
            }


class IndustryAgent(ABC):
    """
    Abstract base class for industry-specific GRC agents
    Provides common functionality and interface for all industry agents
    """
    
    def __init__(self, industry_type: IndustryType, agent_id: str, name: str):
        self.industry_type = industry_type
        self.agent_id = agent_id
        self.name = name
        self.status = "active"
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.operation_count = 0
        self.error_count = 0
        
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages from MCP broker"""
        pass
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific GRC tasks"""
        pass
    
    @abstractmethod
    async def perform_grc_operation(self, operation_type: GRCOperationType, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform GRC operations specific to the industry"""
        pass
    
    # Abstract methods for GRC operations
    @abstractmethod
    def _analyze_policy(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze policy compliance and effectiveness"""
        pass
    
    @abstractmethod
    def _assess_incident_impact(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact of a security or compliance incident"""
        pass
    
    @abstractmethod
    def _assign_audit_resources(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assign resources for audit activities"""
        pass
    
    @abstractmethod
    def _calculate_compliance_score(self, compliance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall compliance score"""
        pass
    
    @abstractmethod
    def _check_compliance_status(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check current compliance status"""
        pass
    
    @abstractmethod
    def _check_policy_compliance_alignment(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if policy aligns with compliance requirements"""
        pass
    
    @abstractmethod
    def _create_audit_plan(self, audit_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive audit plan"""
        pass
    
    @abstractmethod
    def _execute_incident_response_actions(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute incident response actions"""
        pass
    
    @abstractmethod
    def _generate_compliance_report(self, report_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compliance report"""
        pass
    
    @abstractmethod
    def _generate_incident_response_plan(self, incident_type: str) -> Dict[str, Any]:
        """Generate incident response plan"""
        pass
    
    @abstractmethod
    def _generate_policy_review_report(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate policy review report"""
        pass
    
    @abstractmethod
    def _generate_regulatory_report(self, regulatory_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate regulatory report"""
        pass
    
    @abstractmethod
    def _get_compliance_requirements(self, entity_type: str) -> Dict[str, Any]:
        """Get compliance requirements for entity type"""
        pass
    
    @abstractmethod
    def _get_policy_details(self, policy_id: str) -> Dict[str, Any]:
        """Get detailed policy information"""
        pass
    
    @abstractmethod
    def _schedule_audit_activities(self, audit_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule audit activities"""
        pass
    
    @abstractmethod
    def _submit_regulatory_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit regulatory report"""
        pass
    
    @abstractmethod
    def _validate_regulatory_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate regulatory report before submission"""
        pass
    
    # Industry-specific abstract methods
    @abstractmethod
    async def _assess_industry_risks(self, business_unit: str, risk_scope: str) -> Dict[str, Any]:
        """Assess industry-specific risks"""
        pass
    
    @abstractmethod
    async def _calculate_risk_scores(self, risks: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk scores for the industry"""
        pass
    
    @abstractmethod
    async def _generate_risk_recommendations(self, risks: Dict[str, Any], risk_scores: Dict[str, Any]) -> List[str]:
        """Generate risk recommendations for the industry"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "industry_type": self.industry_type.value,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "operation_count": self.operation_count,
            "error_count": self.error_count
        }
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def increment_operation_count(self):
        """Increment operation counter"""
        self.operation_count += 1
        self.update_activity()
    
    def increment_error_count(self):
        """Increment error counter"""
        self.error_count += 1
        self.update_activity()

