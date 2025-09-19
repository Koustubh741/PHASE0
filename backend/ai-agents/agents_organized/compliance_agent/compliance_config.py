"""
Compliance Agent Configuration
Configuration settings and constants for Compliance Agent
"""

from typing import Dict, List, Any
from enum import Enum

class ComplianceFrameworkType(Enum):
    """Compliance framework types"""
    GENERAL = "general"
    DATA_PROTECTION = "data_protection"
    SECURITY = "security"
    QUALITY = "quality"
    ENVIRONMENTAL = "environmental"
    FINANCIAL = "financial"
    HEALTHCARE = "healthcare"
    MANUFACTURING = "manufacturing"

class ComplianceStatus(Enum):
    """Compliance status types"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non-compliant"
    PARTIALLY_COMPLIANT = "partially-compliant"
    NOT_ASSESSED = "not-assessed"
    UNDER_REVIEW = "under-review"

class ViolationSeverity(Enum):
    """Violation severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

# Compliance-specific configuration
COMPLIANCE_CONFIG = {
    "agent_type": "General Compliance Monitoring",
    "supported_frameworks": [
        "GDPR", "CCPA", "HIPAA", "SOX", "PCI DSS", "ISO 27001", "NIST",
        "ISO 9001", "ISO 14001", "Basel III", "FCC", "FDA", "OSHA"
    ],
    "ai_capabilities": {
        "gpt4_integration": True,
        "vector_database_search": True,
        "document_classification": True,
        "pattern_recognition": True,
        "confidence_scoring": True
    },
    "performance_targets": {
        "compliance_check_accuracy": 95.0,  # percentage
        "violation_detection_rate": 90.0,  # percentage
        "policy_analysis_speed": 30,  # seconds
        "ai_confidence_score": 0.85,  # minimum confidence
        "batch_processing_throughput": 100  # documents per hour
    },
    "violation_patterns": {
        "security": [
            {"pattern": "password.*123", "type": "weak_password", "severity": "high"},
            {"pattern": "admin.*admin", "type": "default_credentials", "severity": "critical"},
            {"pattern": "http://", "type": "insecure_protocol", "severity": "medium"},
            {"pattern": "ssn.*\\d{3}-\\d{2}-\\d{4}", "type": "ssn_exposure", "severity": "critical"}
        ],
        "privacy": [
            {"pattern": "personal.*data", "type": "data_handling", "severity": "medium"},
            {"pattern": "consent.*required", "type": "consent_management", "severity": "high"},
            {"pattern": "data.*retention", "type": "retention_policy", "severity": "medium"}
        ],
        "quality": [
            {"pattern": "defect.*rate", "type": "quality_control", "severity": "medium"},
            {"pattern": "customer.*complaint", "type": "customer_satisfaction", "severity": "high"},
            {"pattern": "process.*improvement", "type": "continuous_improvement", "severity": "low"}
        ]
    },
    "document_categories": {
        "policies": ["policy", "procedure", "guideline", "standard"],
        "regulations": ["regulation", "compliance", "requirement", "mandate"],
        "reports": ["report", "assessment", "audit", "review"],
        "contracts": ["contract", "agreement", "terms", "conditions"],
        "training": ["training", "education", "certification", "competency"]
    }
}

# Compliance-specific prompts for AI analysis
COMPLIANCE_PROMPTS = {
    "general_compliance": """
    Analyze compliance for the following content against general compliance standards:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'violations': ['list of specific violations found'],
        'recommendations': ['list of recommendations for improvement'],
        'confidence': 0.95,
        'framework_applicable': 'identified framework'
    }}
    
    Be specific about violations and provide actionable recommendations.
    """,
    
    "data_protection": """
    Analyze data protection compliance for the following content:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'data_classification': 'classification assessment',
        'privacy_controls': 'privacy control effectiveness',
        'consent_management': 'consent management status',
        'data_retention': 'retention policy compliance',
        'breach_prevention': 'breach prevention measures',
        'recommendations': ['list of recommendations'],
        'confidence': 0.95
    }}
    """,
    
    "security_compliance": """
    Analyze security compliance for the following content:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'access_controls': 'access control effectiveness',
        'encryption': 'encryption implementation status',
        'monitoring': 'security monitoring effectiveness',
        'incident_response': 'incident response readiness',
        'vulnerability_management': 'vulnerability management status',
        'recommendations': ['list of recommendations'],
        'confidence': 0.95
    }}
    """,
    
    "quality_compliance": """
    Analyze quality compliance for the following content:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'quality_system': 'quality system effectiveness',
        'process_control': 'process control status',
        'continuous_improvement': 'improvement process status',
        'customer_satisfaction': 'customer satisfaction assessment',
        'documentation': 'documentation quality',
        'recommendations': ['list of recommendations'],
        'confidence': 0.95
    }}
    """
}

# Compliance-specific document categories for vector storage
COMPLIANCE_DOCUMENT_CATEGORIES = [
    "general_compliance",
    "data_protection",
    "security_standards",
    "quality_management",
    "environmental_compliance",
    "financial_regulations",
    "healthcare_compliance",
    "manufacturing_standards",
    "regulatory_reporting",
    "audit_documentation"
]

# Compliance-specific analysis templates
COMPLIANCE_ANALYSIS_TEMPLATES = {
    "policy_analysis": {
        "description": "Analyze policy document structure and compliance alignment",
        "analysis_criteria": [
            "Policy structure and organization",
            "Regulatory alignment",
            "Implementation clarity",
            "Enforcement mechanisms"
        ],
        "output_metrics": [
            "Structure score",
            "Compliance alignment score",
            "Implementation readiness",
            "Enforcement effectiveness"
        ]
    },
    "violation_detection": {
        "description": "Detect potential compliance violations in documents",
        "detection_methods": [
            "Pattern matching",
            "AI-powered analysis",
            "Contextual assessment",
            "Risk scoring"
        ],
        "output_metrics": [
            "Violation count",
            "Severity levels",
            "Risk scores",
            "Recommendation priority"
        ]
    },
    "compliance_assessment": {
        "description": "Comprehensive compliance assessment against frameworks",
        "assessment_areas": [
            "Regulatory compliance",
            "Policy adherence",
            "Process effectiveness",
            "Documentation quality"
        ],
        "output_metrics": [
            "Overall compliance score",
            "Framework-specific scores",
            "Gap analysis",
            "Improvement recommendations"
        ]
    }
}

# Compliance-specific KPI targets
COMPLIANCE_KPI_TARGETS = {
    "accuracy": {
        "compliance_check_accuracy": ">95%",
        "violation_detection_accuracy": ">90%",
        "policy_analysis_accuracy": ">92%",
        "framework_identification_accuracy": ">98%"
    },
    "performance": {
        "analysis_speed": "<30 seconds",
        "batch_processing_throughput": ">100 documents/hour",
        "system_uptime": ">99.9%",
        "response_time": "<5 seconds"
    },
    "quality": {
        "ai_confidence_score": ">0.85",
        "false_positive_rate": "<5%",
        "false_negative_rate": "<3%",
        "recommendation_acceptance_rate": ">80%"
    }
}
