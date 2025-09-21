"""
BFSI Configuration and Constants
Configuration management for BFSI GRC operations
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional


class BFSIRegulationType(Enum):
    """BFSI Regulation Types"""
    BASEL_III = "basel_iii"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    GLBA = "glba"
    CCPA = "ccpa"
    GDPR = "gdpr"
    AML_KYC = "aml_kyc"
    FATCA = "fatca"
    MIFID_II = "mifid_ii"


class BFSIRiskCategory(Enum):
    """BFSI Risk Categories"""
    CREDIT_RISK = "credit_risk"
    MARKET_RISK = "market_risk"
    OPERATIONAL_RISK = "operational_risk"
    LIQUIDITY_RISK = "liquidity_risk"
    REPUTATIONAL_RISK = "reputational_risk"
    REGULATORY_RISK = "regulatory_risk"
    CYBER_RISK = "cyber_risk"
    FRAUD_RISK = "fraud_risk"
    AML_RISK = "aml_risk"


class BFSIComplianceStatus(Enum):
    """BFSI Compliance Status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"
    NOT_APPLICABLE = "not_applicable"


class BFSISeverityLevel(Enum):
    """BFSI Severity Levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BFSIRegulationConfig:
    """Configuration for BFSI regulations"""
    regulation_id: str
    regulation_name: str
    regulation_type: BFSIRegulationType
    applicable_entities: List[str]
    compliance_requirements: List[str]
    reporting_frequency: str
    audit_frequency: str
    penalty_structure: Dict[str, Any]
    effective_date: datetime
    last_updated: datetime
    status: str = "active"
    
    def __post_init__(self):
        if not self.applicable_entities:
            self.applicable_entities = ["bank", "credit_union", "fintech"]
        if not self.compliance_requirements:
            self.compliance_requirements = ["documentation", "monitoring", "reporting"]


@dataclass
class BFSIRiskThreshold:
    """Risk threshold configuration"""
    risk_category: BFSIRiskCategory
    low_threshold: float
    medium_threshold: float
    high_threshold: float
    critical_threshold: float
    measurement_unit: str = "percentage"
    review_frequency: str = "monthly"
    
    def get_risk_level(self, value: float) -> BFSISeverityLevel:
        """Get risk level based on value"""
        if value >= self.critical_threshold:
            return BFSISeverityLevel.CRITICAL
        elif value >= self.high_threshold:
            return BFSISeverityLevel.HIGH
        elif value >= self.medium_threshold:
            return BFSISeverityLevel.MEDIUM
        else:
            return BFSISeverityLevel.LOW


@dataclass
class BFSIComplianceFramework:
    """BFSI Compliance Framework"""
    framework_id: str
    framework_name: str
    applicable_regulations: List[BFSIRegulationType]
    compliance_requirements: List[str]
    audit_requirements: List[str]
    reporting_requirements: List[str]
    risk_categories: List[BFSIRiskCategory]
    kpis: Dict[str, Any]
    review_cycle: str = "quarterly"
    
    def __post_init__(self):
        if not self.applicable_regulations:
            self.applicable_regulations = [BFSIRegulationType.BASEL_III]
        if not self.compliance_requirements:
            self.compliance_requirements = ["documentation", "monitoring", "reporting"]


class BFSIConfigManager:
    """BFSI Configuration Manager"""
    
    def __init__(self):
        self.regulations: Dict[str, BFSIRegulationConfig] = {}
        self.risk_thresholds: Dict[BFSIRiskCategory, BFSIRiskThreshold] = {}
        self.compliance_frameworks: Dict[str, BFSIComplianceFramework] = {}
        self.last_updated = datetime.now()
        
        # Initialize default configurations
        self._initialize_default_configurations()
    
    def _initialize_default_configurations(self):
        """Initialize default BFSI configurations"""
        # Basel III Configuration
        self.regulations["basel_iii"] = BFSIRegulationConfig(
            regulation_id="basel_iii",
            regulation_name="Basel III",
            regulation_type=BFSIRegulationType.BASEL_III,
            applicable_entities=["bank", "credit_union"],
            compliance_requirements=[
                "capital_adequacy_ratio",
                "liquidity_coverage_ratio",
                "net_stable_funding_ratio",
                "leverage_ratio"
            ],
            reporting_frequency="quarterly",
            audit_frequency="annual",
            penalty_structure={
                "non_compliance": "regulatory_action",
                "minor_violation": "warning_letter",
                "major_violation": "cease_and_desist"
            },
            effective_date=datetime(2013, 1, 1),
            last_updated=datetime.now()
        )
        
        # SOX Configuration
        self.regulations["sox"] = BFSIRegulationConfig(
            regulation_id="sox",
            regulation_name="Sarbanes-Oxley Act",
            regulation_type=BFSIRegulationType.SOX,
            applicable_entities=["public_company", "bank"],
            compliance_requirements=[
                "internal_controls",
                "financial_reporting",
                "audit_committee",
                "whistleblower_protection"
            ],
            reporting_frequency="quarterly",
            audit_frequency="annual",
            penalty_structure={
                "non_compliance": "criminal_penalties",
                "minor_violation": "civil_penalties",
                "major_violation": "criminal_prosecution"
            },
            effective_date=datetime(2002, 7, 30),
            last_updated=datetime.now()
        )
        
        # Risk Thresholds
        self.risk_thresholds[BFSIRiskCategory.CREDIT_RISK] = BFSIRiskThreshold(
            risk_category=BFSIRiskCategory.CREDIT_RISK,
            low_threshold=0.0,
            medium_threshold=3.0,
            high_threshold=6.0,
            critical_threshold=8.0
        )
        
        self.risk_thresholds[BFSIRiskCategory.OPERATIONAL_RISK] = BFSIRiskThreshold(
            risk_category=BFSIRiskCategory.OPERATIONAL_RISK,
            low_threshold=0.0,
            medium_threshold=2.0,
            high_threshold=4.0,
            critical_threshold=6.0
        )
        
        # Compliance Frameworks
        self.compliance_frameworks["banking_framework"] = BFSIComplianceFramework(
            framework_id="banking_framework",
            framework_name="Banking Compliance Framework",
            applicable_regulations=[
                BFSIRegulationType.BASEL_III,
                BFSIRegulationType.SOX,
                BFSIRegulationType.GLBA
            ],
            compliance_requirements=[
                "capital_adequacy",
                "liquidity_management",
                "risk_management",
                "internal_controls"
            ],
            audit_requirements=[
                "annual_audit",
                "quarterly_review",
                "regulatory_examination"
            ],
            reporting_requirements=[
                "quarterly_reports",
                "annual_reports",
                "regulatory_filings"
            ],
            risk_categories=[
                BFSIRiskCategory.CREDIT_RISK,
                BFSIRiskCategory.OPERATIONAL_RISK,
                BFSIRiskCategory.MARKET_RISK
            ],
            kpis={
                "capital_adequacy_ratio": {"target": 8.0, "current": 10.2},
                "liquidity_coverage_ratio": {"target": 100.0, "current": 125.0},
                "operational_risk_loss": {"target": 0, "current": 2}
            }
        )
    
    def get_regulation_config(self, regulation_id: str) -> Optional[BFSIRegulationConfig]:
        """Get regulation configuration by ID"""
        return self.regulations.get(regulation_id)
    
    def get_risk_threshold(self, risk_category: BFSIRiskCategory) -> Optional[BFSIRiskThreshold]:
        """Get risk threshold for category"""
        return self.risk_thresholds.get(risk_category)
    
    def get_compliance_framework(self, framework_id: str) -> Optional[BFSIComplianceFramework]:
        """Get compliance framework by ID"""
        return self.compliance_frameworks.get(framework_id)
    
    def update_regulation_config(self, regulation_id: str, config: BFSIRegulationConfig):
        """Update regulation configuration"""
        self.regulations[regulation_id] = config
        self.last_updated = datetime.now()
    
    def add_risk_threshold(self, risk_category: BFSIRiskCategory, threshold: BFSIRiskThreshold):
        """Add or update risk threshold"""
        self.risk_thresholds[risk_category] = threshold
        self.last_updated = datetime.now()
    
    def get_all_regulations(self) -> List[BFSIRegulationConfig]:
        """Get all regulation configurations"""
        return list(self.regulations.values())
    
    def get_all_risk_thresholds(self) -> List[BFSIRiskThreshold]:
        """Get all risk thresholds"""
        return list(self.risk_thresholds.values())
    
    def get_all_frameworks(self) -> List[BFSIComplianceFramework]:
        """Get all compliance frameworks"""
        return list(self.compliance_frameworks.values())


# BFSI Configuration Constants
BFSI_CONFIG = {
    "compliance_frameworks": [
        "Basel III", "SOX", "PCI DSS", "GLBA", "CCPA", "GDPR", "AML/KYC", "FATCA", "MiFID II"
    ],
    "risk_categories": [
        "credit_risk", "market_risk", "operational_risk", "liquidity_risk",
        "reputational_risk", "regulatory_risk", "cyber_risk", "fraud_risk", "aml_risk"
    ],
    "regulatory_bodies": [
        "Basel Committee", "BCBS", "FDIC", "OCC", "FRB", "CFTC", "SEC",
        "FINRA", "PCI DSS", "SOX", "GLBA", "CCPA", "GDPR", "MiFID II"
    ],
    "risk_thresholds": {
        "credit_risk": {"low": 0.0, "medium": 3.0, "high": 6.0, "critical": 8.0},
        "operational_risk": {"low": 0.0, "medium": 2.0, "high": 4.0, "critical": 6.0},
        "market_risk": {"low": 0.0, "medium": 2.5, "high": 5.0, "critical": 7.5},
        "liquidity_risk": {"low": 0.0, "medium": 1.5, "high": 3.0, "critical": 5.0}
    },
    "compliance_requirements": {
        "capital_adequacy": {
            "tier_1_capital": 6.0,
            "total_capital": 8.0,
            "leverage_ratio": 3.0,
            "liquidity_coverage_ratio": 100.0,
            "net_stable_funding_ratio": 100.0
        },
        "operational_risk": {
            "ama_requirements": {
                "data_quality": "high",
                "model_validation": "annual",
                "scenario_analysis": "quarterly",
                "external_data": "required"
            }
        },
        "market_risk": {
            "var_requirements": {
                "confidence_level": 99.0,
                "holding_period": 10,
                "backtesting": "daily",
                "stress_testing": "monthly"
            }
        }
    }
}

BFSI_PROMPTS = {
    "risk_assessment": "Perform comprehensive risk assessment for BFSI operations including credit, market, operational, and liquidity risks.",
    "compliance_check": "Conduct thorough compliance check against applicable BFSI regulations including Basel III, SOX, PCI DSS, and other relevant frameworks.",
    "policy_review": "Review and analyze BFSI policies for compliance with regulatory requirements and industry best practices.",
    "audit_scheduling": "Schedule and coordinate BFSI audit activities including regulatory examinations and internal audits.",
    "incident_response": "Execute incident response procedures for BFSI security and compliance incidents.",
    "regulatory_reporting": "Generate and submit regulatory reports to appropriate BFSI regulatory bodies."
}

BFSI_DOCUMENT_CATEGORIES = {
    "regulatory_documents": [
        "basel_iii_reports", "sox_documentation", "pci_dss_assessments",
        "glba_compliance", "ccpa_documentation", "gdpr_compliance"
    ],
    "risk_documents": [
        "risk_assessments", "stress_test_reports", "scenario_analysis",
        "operational_risk_reports", "credit_risk_models"
    ],
    "compliance_documents": [
        "compliance_reports", "audit_reports", "regulatory_filings",
        "policy_documents", "procedure_manuals"
    ],
    "operational_documents": [
        "incident_reports", "security_assessments", "business_continuity_plans",
        "disaster_recovery_plans", "training_materials"
    ]
}

