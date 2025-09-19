"""
BFSI Agent Configuration
Optimized configuration settings and constants for BFSI GRC Agent
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum, auto
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

class BFSIRegulationType(Enum):
    """BFSI regulation types with priority levels"""
    # Core Banking Regulations
    BASEL_III = "basel_iii"
    BASEL_IV = "basel_iv"
    
    # Financial Reporting
    SOX = "sox"
    IFRS = "ifrs"
    GAAP = "gaap"
    
    # Data Security & Privacy
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    CCPA = "ccpa"
    GLBA = "glba"
    
    # Anti-Money Laundering
    AML_KYC = "aml_kyc"
    FATCA = "fatca"
    CRS = "crs"
    
    # Trading & Markets
    MIFID_II = "mifid_ii"
    EMIR = "emir"
    SFTR = "sftr"
    
    # Insurance
    SOLVENCY_II = "solvency_ii"
    IAIS = "iais"
    
    # Regional Regulations
    DODD_FRANK = "dodd_frank"
    PSD2 = "psd2"
    OPEN_BANKING = "open_banking"

class BFSIRiskCategory(Enum):
    """BFSI risk categories with severity levels"""
    # Financial Risks
    CREDIT_RISK = "credit_risk"
    MARKET_RISK = "market_risk"
    LIQUIDITY_RISK = "liquidity_risk"
    INTEREST_RATE_RISK = "interest_rate_risk"
    CURRENCY_RISK = "currency_risk"
    
    # Operational Risks
    OPERATIONAL_RISK = "operational_risk"
    CYBER_SECURITY_RISK = "cyber_security_risk"
    MODEL_RISK = "model_risk"
    THIRD_PARTY_RISK = "third_party_risk"
    
    # Strategic Risks
    REGULATORY_RISK = "regulatory_risk"
    REPUTATIONAL_RISK = "reputational_risk"
    CONCENTRATION_RISK = "concentration_risk"
    CLIMATE_RISK = "climate_risk"

class BFSIComplianceStatus(Enum):
    """BFSI compliance status with confidence levels"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NOT_ASSESSED = "not_assessed"
    UNDER_REVIEW = "under_review"
    EXEMPT = "exempt"
    GRANDFATHERED = "grandfathered"

class BFSISeverityLevel(Enum):
    """Risk severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"

@dataclass
class RegulationConfig:
    """Configuration for a specific regulation"""
    name: str
    reporting_frequency: str
    deadline: str
    key_requirements: List[str]
    priority: int = 1
    applicable_entities: List[str] = None
    penalty_threshold: float = 0.0
    
    def __post_init__(self):
        if self.applicable_entities is None:
            self.applicable_entities = ["all"]

# Optimized BFSI Configuration with structured data classes
@dataclass
class CapitalRequirements:
    """Basel III capital requirements"""
    tier_1_capital_ratio: float = 6.0
    total_capital_ratio: float = 8.0
    leverage_ratio: float = 3.0
    liquidity_coverage_ratio: float = 100.0
    net_stable_funding_ratio: float = 100.0
    countercyclical_buffer: float = 2.5
    systemic_risk_buffer: float = 1.0

@dataclass
class RiskThresholds:
    """Risk assessment thresholds"""
    credit_risk: Dict[str, float] = None
    market_risk: Dict[str, Union[int, float]] = None
    operational_risk: Dict[str, float] = None
    liquidity_risk: Dict[str, float] = None
    
    def __post_init__(self):
        if self.credit_risk is None:
            self.credit_risk = {"high": 0.1, "medium": 0.05, "low": 0.01}
        if self.market_risk is None:
            self.market_risk = {"var_breach_limit": 4, "var_confidence_level": 99.0}
        if self.operational_risk is None:
            self.operational_risk = {
            "high_loss_threshold": 1000000,
            "medium_loss_threshold": 100000,
            "low_loss_threshold": 10000
        }
        if self.liquidity_risk is None:
            self.liquidity_risk = {
                "liquidity_ratio_min": 0.25,
                "cash_flow_coverage": 1.2
            }

@dataclass
class KPITargets:
    """Key Performance Indicator targets"""
    financial: Dict[str, str] = None
    risk: Dict[str, str] = None
    compliance: Dict[str, str] = None
    operational: Dict[str, str] = None
    
    def __post_init__(self):
        if self.financial is None:
            self.financial = {
            "capital_adequacy_ratio": ">12%",
            "leverage_ratio": ">5%",
            "liquidity_coverage_ratio": ">100%",
                "net_stable_funding_ratio": ">100%",
                "return_on_equity": ">10%",
                "cost_income_ratio": "<60%"
            }
        if self.risk is None:
            self.risk = {
            "var_breaches": "<4/year",
            "operational_losses": "<$10M",
            "credit_losses": "<1%",
                "cyber_incidents": "0",
                "model_errors": "<2%"
            }
        if self.compliance is None:
            self.compliance = {
            "regulatory_filings": "100%",
            "audit_findings": "0",
            "policy_compliance": ">95%",
                "training_completion": "100%",
                "incident_response_time": "<24h"
            }
        if self.operational is None:
            self.operational = {
                "system_uptime": ">99.9%",
                "transaction_processing_time": "<2s",
                "customer_satisfaction": ">90%",
                "employee_turnover": "<10%"
            }

# Main BFSI Configuration
BFSI_CONFIG = {
    "industry": "Banking, Financial Services, Insurance",
    "version": "2.0",
    "last_updated": datetime.now().isoformat(),
    
    "regulatory_bodies": {
        "international": [
            "Basel Committee on Banking Supervision (BCBS)",
            "Financial Stability Board (FSB)",
            "International Association of Insurance Supervisors (IAIS)"
        ],
        "us": [
            "Federal Reserve (FRB)", "Office of the Comptroller of the Currency (OCC)",
            "Federal Deposit Insurance Corporation (FDIC)", "Securities and Exchange Commission (SEC)",
            "Commodity Futures Trading Commission (CFTC)", "Financial Industry Regulatory Authority (FINRA)"
        ],
        "eu": [
            "European Banking Authority (EBA)", "European Securities and Markets Authority (ESMA)",
            "European Insurance and Occupational Pensions Authority (EIOPA)"
        ]
    },
    
    "capital_requirements": CapitalRequirements(),
    "risk_thresholds": RiskThresholds(),
    "kpi_targets": KPITargets(),
    
    "compliance_frameworks": {
        BFSIRegulationType.BASEL_III.value: RegulationConfig(
            name="Basel III",
            reporting_frequency="quarterly",
            deadline="month_end",
            key_requirements=[
                "Capital Adequacy Ratio", "Leverage Ratio",
                "Liquidity Coverage Ratio", "Net Stable Funding Ratio",
                "Countercyclical Buffer", "Systemic Risk Buffer"
            ],
            priority=1,
            applicable_entities=["banks", "systemically_important_financial_institutions"],
            penalty_threshold=1000000.0
        ),
        BFSIRegulationType.SOX.value: RegulationConfig(
            name="Sarbanes-Oxley Act",
            reporting_frequency="quarterly",
            deadline="45_days",
            key_requirements=[
                "Internal Controls Assessment", "Financial Reporting Controls",
                "Management Certification", "Auditor Independence"
            ],
            priority=1,
            applicable_entities=["public_companies"],
            penalty_threshold=5000000.0
        ),
        BFSIRegulationType.PCI_DSS.value: RegulationConfig(
            name="PCI DSS",
            reporting_frequency="annual",
            deadline="year_end",
            key_requirements=[
                "Network Security", "Data Protection", "Access Controls",
                "Monitoring and Testing", "Information Security Policy"
            ],
            priority=2,
            applicable_entities=["payment_processors", "merchants"],
            penalty_threshold=100000.0
        ),
        BFSIRegulationType.GDPR.value: RegulationConfig(
            name="General Data Protection Regulation",
            reporting_frequency="ongoing",
            deadline="immediate",
            key_requirements=[
                "Data Protection Impact Assessment", "Privacy by Design",
                "Data Subject Rights", "Breach Notification", "Data Processing Records"
            ],
            priority=1,
            applicable_entities=["all_entities_processing_eu_data"],
            penalty_threshold=20000000.0
        )
    }
}

# Enhanced BFSI AI Analysis Prompts
@dataclass
class AnalysisPrompt:
    """Structured analysis prompt with metadata"""
    name: str
    description: str
    template: str
    output_schema: Dict[str, Any]
    confidence_threshold: float = 0.8
    max_tokens: int = 2000
    
    def format_prompt(self, content: str, **kwargs) -> str:
        """Format the prompt with content and additional parameters"""
        return self.template.format(content=content, **kwargs)

# Optimized BFSI Analysis Prompts
BFSI_PROMPTS = {
    "basel_iii_analysis": AnalysisPrompt(
        name="Basel III Compliance Analysis",
        description="Comprehensive Basel III capital adequacy and liquidity analysis",
        template="""
        As a BFSI compliance expert, analyze the following content for Basel III compliance:
        
        Content: {content}
        
        Context: {context}
        Entity Type: {entity_type}
        Reporting Period: {reporting_period}
        
        Analyze the following Basel III requirements:
        1. Capital Adequacy Ratio (CAR) - Minimum 8%
        2. Tier 1 Capital Ratio - Minimum 6%
        3. Leverage Ratio - Minimum 3%
        4. Liquidity Coverage Ratio (LCR) - Minimum 100%
        5. Net Stable Funding Ratio (NSFR) - Minimum 100%
        6. Countercyclical Buffer - 0-2.5%
        7. Systemic Risk Buffer - 0-3.5%
        
        Provide detailed analysis with specific calculations and regulatory references.
        """,
        output_schema={
            "compliance_status": "compliant|non_compliant|partially_compliant|not_assessed",
            "capital_adequacy_ratio": "float",
            "tier_1_capital_ratio": "float", 
            "leverage_ratio": "float",
            "liquidity_coverage_ratio": "float",
            "net_stable_funding_ratio": "float",
            "countercyclical_buffer": "float",
            "systemic_risk_buffer": "float",
            "requirements_met": ["list of met requirements"],
            "requirements_failed": ["list of failed requirements"],
            "risk_factors": ["list of identified risk factors"],
            "recommendations": ["list of specific recommendations"],
            "regulatory_references": ["list of relevant regulations"],
            "confidence_score": "float",
            "analysis_timestamp": "datetime",
            "next_review_date": "datetime"
        },
        confidence_threshold=0.85
    ),
    
    "sox_compliance": AnalysisPrompt(
        name="SOX Compliance Analysis",
        description="Sarbanes-Oxley Act compliance assessment",
        template="""
        As a financial compliance expert, analyze the following content for SOX compliance:
        
        Content: {content}
        
        Focus on:
        1. Internal Controls over Financial Reporting (ICFR)
        2. Management Assessment of Internal Controls
        3. Auditor Independence Requirements
        4. Financial Reporting Controls
        5. Disclosure Controls and Procedures
        
        Evaluate control effectiveness, identify deficiencies, and assess material weaknesses.
        """,
        output_schema={
            "compliance_status": "compliant|non_compliant|partially_compliant|not_assessed",
            "internal_controls_assessment": "string",
            "financial_reporting_controls": "string",
            "management_certification": "string",
            "auditor_independence": "string",
            "material_weaknesses": ["list of material weaknesses"],
            "significant_deficiencies": ["list of significant deficiencies"],
            "control_deficiencies": ["list of control deficiencies"],
            "recommendations": ["list of recommendations"],
            "confidence_score": "float"
        }
    ),
    
    "pci_dss_security": AnalysisPrompt(
        name="PCI DSS Security Analysis",
        description="Payment Card Industry Data Security Standard compliance",
        template="""
        As a cybersecurity expert, analyze the following content for PCI DSS compliance:
        
        Content: {content}
        
        Evaluate the 12 PCI DSS requirements:
        1. Install and maintain a firewall
        2. Do not use vendor-supplied defaults
        3. Protect stored cardholder data
        4. Encrypt transmission of cardholder data
        5. Use and regularly update anti-virus software
        6. Develop and maintain secure systems
        7. Restrict access to cardholder data
        8. Assign unique ID to each person
        9. Restrict physical access to cardholder data
        10. Track and monitor network access
        11. Regularly test security systems
        12. Maintain information security policy
        
        Assess current security posture and identify gaps.
        """,
        output_schema={
            "compliance_status": "compliant|non_compliant|partially_compliant|not_assessed",
            "network_security": "string",
            "data_protection": "string",
            "access_controls": "string",
            "monitoring_systems": "string",
            "security_policy": "string",
            "requirements_met": ["list of met requirements"],
            "requirements_failed": ["list of failed requirements"],
            "security_gaps": ["list of security gaps"],
            "vulnerabilities": ["list of vulnerabilities"],
            "recommendations": ["list of recommendations"],
            "confidence_score": "float"
        }
    ),
    
    "aml_kyc_analysis": AnalysisPrompt(
        name="AML/KYC Compliance Analysis",
        description="Anti-Money Laundering and Know Your Customer compliance",
        template="""
        As an AML/KYC expert, analyze the following content for compliance:
        
        Content: {content}
        
        Evaluate:
        1. Customer Due Diligence (CDD) procedures
        2. Enhanced Due Diligence (EDD) for high-risk customers
        3. Transaction monitoring systems
        4. Suspicious Activity Detection
        5. Sanctions screening
        6. Politically Exposed Persons (PEP) screening
        7. Risk assessment procedures
        8. Record keeping requirements
        
        Assess the effectiveness of AML controls and identify potential risks.
        """,
        output_schema={
            "compliance_status": "compliant|non_compliant|partially_compliant|not_assessed",
            "customer_due_diligence": "string",
            "transaction_monitoring": "string",
            "suspicious_activity_detection": "string",
            "sanctions_screening": "string",
            "pep_screening": "string",
            "risk_assessment": "string",
            "record_keeping": "string",
            "aml_controls_effectiveness": "string",
            "identified_risks": ["list of identified risks"],
            "suspicious_activities": ["list of suspicious activities"],
            "recommendations": ["list of recommendations"],
            "confidence_score": "float"
        }
    ),
    
    "cyber_security_risk": AnalysisPrompt(
        name="Cybersecurity Risk Assessment",
        description="Comprehensive cybersecurity risk analysis",
        template="""
        As a cybersecurity risk expert, analyze the following content for cyber risks:
        
        Content: {content}
        
        Assess:
        1. Network security posture
        2. Data protection measures
        3. Access control systems
        4. Incident response capabilities
        5. Security awareness and training
        6. Third-party risk management
        7. Cloud security controls
        8. Mobile device security
        9. IoT security
        10. Supply chain security
        
        Identify vulnerabilities, threats, and potential impacts.
        """,
        output_schema={
            "risk_level": "critical|high|medium|low|minimal",
            "network_security": "string",
            "data_protection": "string",
            "access_controls": "string",
            "incident_response": "string",
            "vulnerabilities": ["list of vulnerabilities"],
            "threats": ["list of threats"],
            "potential_impacts": ["list of potential impacts"],
            "security_controls": ["list of security controls"],
            "recommendations": ["list of recommendations"],
            "confidence_score": "float"
        }
    ),
    
    "operational_risk": AnalysisPrompt(
        name="Operational Risk Assessment",
        description="Operational risk identification and assessment",
        template="""
        As an operational risk expert, analyze the following content:
        
        Content: {content}
        
        Evaluate:
        1. Process risks
        2. People risks
        3. System risks
        4. External risks
        5. Legal and regulatory risks
        6. Reputational risks
        7. Business continuity risks
        8. Model risks
        
        Assess likelihood, impact, and control effectiveness.
        """,
        output_schema={
            "risk_level": "critical|high|medium|low|minimal",
            "process_risks": ["list of process risks"],
            "people_risks": ["list of people risks"],
            "system_risks": ["list of system risks"],
            "external_risks": ["list of external risks"],
            "likelihood_assessment": "string",
            "impact_assessment": "string",
            "control_effectiveness": "string",
            "mitigation_measures": ["list of mitigation measures"],
            "recommendations": ["list of recommendations"],
            "confidence_score": "float"
        }
    )
}

# Enhanced BFSI Document Categories
BFSI_DOCUMENT_CATEGORIES = {
    "regulatory": [
        "basel_iii", "basel_iv", "sox_compliance", "pci_dss", "gdpr", "ccpa",
        "mifid_ii", "emir", "dodd_frank", "psd2", "open_banking"
    ],
    "risk_management": [
        "credit_risk", "market_risk", "operational_risk", "liquidity_risk",
        "cyber_security_risk", "model_risk", "reputational_risk", "climate_risk"
    ],
    "compliance": [
        "aml_kyc", "fatca", "crs", "sanctions_screening", "pep_screening",
        "regulatory_reporting", "audit_documentation", "policy_management"
    ],
    "operational": [
        "capital_adequacy", "stress_testing", "scenario_analysis",
        "business_continuity", "incident_management", "vendor_management"
    ],
    "governance": [
        "board_governance", "risk_appetite", "risk_tolerance",
        "esg_compliance", "sustainability_reporting"
    ]
}

# Enhanced Risk Assessment Templates
@dataclass
class RiskTemplate:
    """Structured risk assessment template"""
    name: str
    description: str
    risk_category: BFSIRiskCategory
    severity_levels: Dict[str, str]
    assessment_criteria: List[str]
    mitigation_controls: List[str]
    key_indicators: List[str]
    regulatory_requirements: List[str]
    escalation_thresholds: Dict[str, float]
    
    def get_risk_score(self, criteria_scores: Dict[str, float]) -> float:
        """Calculate weighted risk score based on criteria"""
        weights = {criterion: 1.0 for criterion in self.assessment_criteria}
        return sum(weights.get(criterion, 0) * score for criterion, score in criteria_scores.items())

BFSI_RISK_TEMPLATES = {
    "credit_risk": RiskTemplate(
        name="Credit Risk Assessment",
        description="Risk of counterparty default in trading and lending activities",
        risk_category=BFSIRiskCategory.CREDIT_RISK,
        severity_levels={
            "critical": "Default probability >10% or exposure >$100M",
            "high": "Default probability 5-10% or exposure $50-100M",
            "medium": "Default probability 1-5% or exposure $10-50M",
            "low": "Default probability 0.1-1% or exposure $1-10M",
            "minimal": "Default probability <0.1% or exposure <$1M"
        },
        assessment_criteria=[
            "Counterparty credit rating",
            "Exposure limits",
            "Collateral requirements",
            "Credit monitoring frequency",
            "Industry concentration",
            "Geographic concentration",
            "Maturity profile",
            "Recovery rates"
        ],
        mitigation_controls=[
            "Credit limits and monitoring",
            "Collateral requirements and margining",
            "Credit insurance and guarantees",
            "Diversification strategies",
            "Regular credit reviews",
            "Early warning systems",
            "Stress testing",
            "Portfolio optimization"
        ],
        key_indicators=[
            "Credit loss ratio",
            "Non-performing loans ratio",
            "Provision coverage ratio",
            "Credit concentration ratio",
            "Recovery rates"
        ],
        regulatory_requirements=[
            "Basel III capital requirements",
            "IFRS 9 expected credit losses",
            "CCAR stress testing",
            "CECL current expected credit losses"
        ],
        escalation_thresholds={
            "high_risk_exposure": 10000000.0,
            "concentration_limit": 0.1,
            "loss_threshold": 1000000.0
        }
    ),
    
    "market_risk": RiskTemplate(
        name="Market Risk Assessment",
        description="Risk from changes in market prices affecting portfolio value",
        risk_category=BFSIRiskCategory.MARKET_RISK,
        severity_levels={
            "critical": "VaR breach >4 times/year or loss >$50M",
            "high": "VaR breach 2-4 times/year or loss $10-50M",
            "medium": "VaR breach 1-2 times/year or loss $1-10M",
            "low": "VaR breach <1 time/year or loss <$1M",
            "minimal": "No VaR breaches and minimal exposure"
        },
        assessment_criteria=[
            "Portfolio exposure",
            "Market volatility",
            "Correlation risks",
            "Liquidity risks",
            "Interest rate sensitivity",
            "Currency exposure",
            "Commodity exposure",
            "Equity exposure"
        ],
        mitigation_controls=[
            "Hedging strategies",
            "Position limits",
            "Stress testing",
            "Diversification",
            "Dynamic hedging",
            "Portfolio rebalancing",
            "Liquidity management",
            "Risk budgeting"
        ],
        key_indicators=[
            "Value at Risk (VaR)",
            "Expected Shortfall (ES)",
            "Maximum Drawdown",
            "Sharpe Ratio",
            "Beta coefficient"
        ],
        regulatory_requirements=[
            "Basel III market risk framework",
            "Fundamental Review of Trading Book (FRTB)",
            "MiFID II position limits",
            "EMIR clearing requirements"
        ],
        escalation_thresholds={
            "var_breach_limit": 4.0,
            "loss_threshold": 10000000.0,
            "concentration_limit": 0.2
        }
    ),
    
    "operational_risk": RiskTemplate(
        name="Operational Risk Assessment",
        description="Risk from inadequate or failed internal processes, people, and systems",
        risk_category=BFSIRiskCategory.OPERATIONAL_RISK,
        severity_levels={
            "critical": "Loss >$100M or system failure >24h",
            "high": "Loss $10-100M or system failure 4-24h",
            "medium": "Loss $1-10M or system failure 1-4h",
            "low": "Loss $100K-1M or system failure <1h",
            "minimal": "Loss <$100K and no system failures"
        },
        assessment_criteria=[
            "Process complexity",
            "System reliability",
            "Staff competency",
            "External dependencies",
            "Technology risks",
            "Vendor risks",
            "Regulatory changes",
            "Business continuity"
        ],
        mitigation_controls=[
            "Process documentation",
            "System redundancy",
            "Staff training",
            "Business continuity planning",
            "Vendor management",
            "Change management",
            "Incident response",
            "Risk monitoring"
        ],
        key_indicators=[
            "Operational loss ratio",
            "System uptime",
            "Incident frequency",
            "Recovery time",
            "Staff turnover"
        ],
        regulatory_requirements=[
            "Basel III operational risk framework",
            "SOX internal controls",
            "PCI DSS security requirements",
            "GDPR data protection"
        ],
        escalation_thresholds={
            "loss_threshold": 1000000.0,
            "downtime_threshold": 4.0,
            "incident_frequency": 10.0
        }
    ),
    
    "cyber_security_risk": RiskTemplate(
        name="Cybersecurity Risk Assessment",
        description="Risk from cyber threats and data breaches",
        risk_category=BFSIRiskCategory.CYBER_SECURITY_RISK,
        severity_levels={
            "critical": "Data breach >1M records or system compromise",
            "high": "Data breach 100K-1M records or significant downtime",
            "medium": "Data breach 10K-100K records or moderate impact",
            "low": "Data breach <10K records or minimal impact",
            "minimal": "No breaches and strong security posture"
        },
        assessment_criteria=[
            "Network security posture",
            "Data protection measures",
            "Access control systems",
            "Incident response capabilities",
            "Security awareness",
            "Third-party risks",
            "Cloud security",
            "Mobile device security"
        ],
        mitigation_controls=[
            "Multi-factor authentication",
            "Encryption at rest and in transit",
            "Regular security assessments",
            "Employee training",
            "Incident response planning",
            "Vendor security requirements",
            "Network segmentation",
            "Continuous monitoring"
        ],
        key_indicators=[
            "Security incident frequency",
            "Mean time to detection",
            "Mean time to response",
            "Vulnerability remediation time",
            "Security awareness scores"
        ],
        regulatory_requirements=[
            "PCI DSS requirements",
            "GDPR data protection",
            "SOX IT controls",
            "FFIEC cybersecurity framework"
        ],
        escalation_thresholds={
            "breach_threshold": 10000.0,
            "downtime_threshold": 1.0,
            "vulnerability_critical": 5.0
        }
    ),
    
    "liquidity_risk": RiskTemplate(
        name="Liquidity Risk Assessment",
        description="Risk of inability to meet short-term financial obligations",
        risk_category=BFSIRiskCategory.LIQUIDITY_RISK,
        severity_levels={
            "critical": "LCR <100% or funding gap >$1B",
            "high": "LCR 100-110% or funding gap $500M-1B",
            "medium": "LCR 110-120% or funding gap $100-500M",
            "low": "LCR 120-150% or funding gap $10-100M",
            "minimal": "LCR >150% and minimal funding gap"
        },
        assessment_criteria=[
            "Liquidity coverage ratio",
            "Net stable funding ratio",
            "Cash flow projections",
            "Funding sources",
            "Asset liquidity",
            "Contingency funding",
            "Market access",
            "Stress scenarios"
        ],
        mitigation_controls=[
            "Liquidity buffers",
            "Diversified funding sources",
            "Contingency funding plans",
            "Asset liquidity management",
            "Regular stress testing",
            "Liquidity monitoring",
            "Central bank facilities",
            "Interbank relationships"
        ],
        key_indicators=[
            "Liquidity Coverage Ratio (LCR)",
            "Net Stable Funding Ratio (NSFR)",
            "Loan-to-deposit ratio",
            "Cash flow coverage",
            "Funding concentration"
        ],
        regulatory_requirements=[
            "Basel III liquidity requirements",
            "LCR and NSFR reporting",
            "Contingency funding plans",
            "Liquidity stress testing"
        ],
        escalation_thresholds={
            "lcr_threshold": 100.0,
            "nsfr_threshold": 100.0,
            "funding_gap": 100000000.0
        }
    )
}

# Utility Functions for Configuration Management
class BFSIConfigManager:
    """Utility class for managing BFSI configuration"""
    
    @staticmethod
    def get_regulation_config(regulation: BFSIRegulationType) -> Optional[RegulationConfig]:
        """Get configuration for a specific regulation"""
        return BFSI_CONFIG["compliance_frameworks"].get(regulation.value)
    
    @staticmethod
    def get_risk_template(risk_type: str) -> Optional[RiskTemplate]:
        """Get risk assessment template for a specific risk type"""
        return BFSI_RISK_TEMPLATES.get(risk_type)
    
    @staticmethod
    def get_analysis_prompt(prompt_type: str) -> Optional[AnalysisPrompt]:
        """Get analysis prompt for a specific analysis type"""
        return BFSI_PROMPTS.get(prompt_type)
    
    @staticmethod
    def validate_config() -> Dict[str, List[str]]:
        """Validate configuration integrity and return any issues"""
        issues = {"errors": [], "warnings": []}
        
        # Validate regulation configurations
        for reg_type, config in BFSI_CONFIG["compliance_frameworks"].items():
            if not isinstance(config, RegulationConfig):
                issues["errors"].append(f"Invalid configuration for {reg_type}")
            elif not config.key_requirements:
                issues["warnings"].append(f"No key requirements defined for {reg_type}")
        
        # Validate risk templates
        for risk_type, template in BFSI_RISK_TEMPLATES.items():
            if not isinstance(template, RiskTemplate):
                issues["errors"].append(f"Invalid risk template for {risk_type}")
            elif not template.assessment_criteria:
                issues["warnings"].append(f"No assessment criteria for {risk_type}")
        
        # Validate analysis prompts
        for prompt_type, prompt in BFSI_PROMPTS.items():
            if not isinstance(prompt, AnalysisPrompt):
                issues["errors"].append(f"Invalid analysis prompt for {prompt_type}")
            elif not prompt.output_schema:
                issues["warnings"].append(f"No output schema for {prompt_type}")
        
        return issues
    
    @staticmethod
    def get_applicable_regulations(entity_type: str, region: str = "global") -> List[BFSIRegulationType]:
        """Get regulations applicable to a specific entity type and region"""
        applicable = []
        
        for reg_type in BFSIRegulationType:
            config = BFSI_CONFIG["compliance_frameworks"].get(reg_type.value)
            if config and ("all" in config.applicable_entities or entity_type in config.applicable_entities):
                applicable.append(reg_type)
        
        return applicable
    
    @staticmethod
    def calculate_risk_score(risk_type: str, criteria_scores: Dict[str, float]) -> Tuple[float, str]:
        """Calculate risk score and determine severity level"""
        template = BFSI_RISK_TEMPLATES.get(risk_type)
        if not template:
            return 0.0, "unknown"
        
        score = template.get_risk_score(criteria_scores)
        
        # Determine severity level based on score
        if score >= 0.8:
            severity = "critical"
        elif score >= 0.6:
            severity = "high"
        elif score >= 0.4:
            severity = "medium"
        elif score >= 0.2:
            severity = "low"
        else:
            severity = "minimal"
        
        return score, severity
    
    @staticmethod
    def export_config(format_type: str = "json") -> str:
        """Export configuration in specified format"""
        if format_type.lower() == "json":
            return json.dumps(BFSI_CONFIG, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    @staticmethod
    def get_kpi_targets(category: str) -> Dict[str, str]:
        """Get KPI targets for a specific category"""
        kpi_targets = BFSI_CONFIG["kpi_targets"]
        return getattr(kpi_targets, category, {})
    
    @staticmethod
    def get_risk_thresholds(risk_category: str) -> Dict[str, Union[int, float]]:
        """Get risk thresholds for a specific risk category"""
        risk_thresholds = BFSI_CONFIG["risk_thresholds"]
        return getattr(risk_thresholds, risk_category, {})
    
    @staticmethod
    def get_document_categories(category_type: str = None) -> Union[Dict[str, List[str]], List[str]]:
        """Get document categories, optionally filtered by type"""
        if category_type:
            return BFSI_DOCUMENT_CATEGORIES.get(category_type, [])
        return BFSI_DOCUMENT_CATEGORIES

# Configuration validation and utility functions
def validate_bfsi_config() -> bool:
    """Validate the entire BFSI configuration"""
    manager = BFSIConfigManager()
    issues = manager.validate_config()
    
    if issues["errors"]:
        logger.error(f"Configuration validation failed: {issues['errors']}")
        return False
    
    if issues["warnings"]:
        logger.warning(f"Configuration warnings: {issues['warnings']}")
    
    logger.info("BFSI configuration validation passed")
    return True

def get_regulation_priority(regulation: BFSIRegulationType) -> int:
    """Get priority level for a regulation"""
    config = BFSIConfigManager.get_regulation_config(regulation)
    return config.priority if config else 0

def is_high_priority_regulation(regulation: BFSIRegulationType) -> bool:
    """Check if a regulation is high priority"""
    return get_regulation_priority(regulation) == 1

# Initialize configuration validation on import
if __name__ == "__main__":
    validate_bfsi_config()
