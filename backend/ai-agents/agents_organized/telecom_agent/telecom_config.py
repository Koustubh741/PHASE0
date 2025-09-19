"""
Telecom Agent Configuration
Configuration settings and constants for Telecom GRC Agent
"""

from typing import Dict, List, Any
from enum import Enum

class TelecomRegulationType(Enum):
    """Telecom regulation types"""
    FCC_RULES = "fcc_rules"
    NIST_CSF = "nist_csf"
    GDPR = "gdpr"
    CCPA = "ccpa"
    ISO_27001 = "iso_27001"
    SOX = "sox"
    E911 = "e911"
    SPECTRUM_MANAGEMENT = "spectrum_management"

class TelecomRiskCategory(Enum):
    """Telecom risk categories"""
    NETWORK_SECURITY_RISK = "network_security_risk"
    CYBERSECURITY_RISK = "cybersecurity_risk"
    SPECTRUM_RISK = "spectrum_risk"
    REGULATORY_COMPLIANCE_RISK = "regulatory_compliance_risk"
    SERVICE_QUALITY_RISK = "service_quality_risk"
    TECHNOLOGY_RISK = "technology_risk"
    OPERATIONAL_RISK = "operational_risk"
    PRIVACY_RISK = "privacy_risk"

class TelecomComplianceStatus(Enum):
    """Telecom compliance status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NOT_ASSESSED = "not_assessed"
    UNDER_REVIEW = "under_review"

# Telecom-specific configuration
TELECOM_CONFIG = {
    "industry": "Telecommunications and Communications",
    "regulatory_bodies": [
        "FCC", "ITU", "ETSI", "3GPP", "IEEE", "IETF", "GSMA",
        "NIST", "ISO", "ANSI", "TIA", "ATIS"
    ],
    "network_requirements": {
        "fcc": {
            "call_completion_rate": 98.0,  # percentage
            "network_availability": 99.9,  # percentage
            "e911_response_time": 10,  # seconds
            "location_accuracy": 50,  # meters
            "spectrum_efficiency": "required"
        }
    },
    "security_requirements": {
        "nist_csf": {
            "identify": "required",
            "protect": "required", 
            "detect": "required",
            "respond": "required",
            "recover": "required"
        },
        "incident_response": {
            "notification_time": 24,  # hours
            "recovery_time": 4,  # hours
            "reporting_requirements": "fcc_form_477"
        }
    },
    "service_quality_standards": {
        "qos_requirements": {
            "call_completion_rate": ">98%",
            "network_availability": ">99.9%",
            "data_throughput": "minimum_guaranteed_speed",
            "latency": "<100ms"
        },
        "emergency_services": {
            "e911_requirements": {
                "location_accuracy": "within_50_meters",
                "response_time": "<10_seconds",
                "reliability": ">99.5%",
                "backup_systems": "required"
            }
        }
    },
    "risk_thresholds": {
        "network_risk": {
            "critical": 0.01,
            "high": 0.05,
            "medium": 0.1,
            "low": 0.2
        },
        "regulatory_risk": {
            "high_penalty": 1000000,
            "medium_penalty": 100000,
            "low_penalty": 10000
        },
        "service_quality": {
            "outage_threshold": 0.1,  # percentage
            "latency_threshold": 100,  # milliseconds
            "throughput_threshold": 100  # Mbps
        }
    },
    "compliance_frameworks": {
        "fcc": {
            "reporting_frequency": "annual",
            "deadline": "march_31",
            "key_requirements": [
                "Radio Frequency License Compliance",
                "Service Quality Standards",
                "Emergency Services (E911)",
                "Spectrum Efficiency"
            ]
        },
        "nist_csf": {
            "reporting_frequency": "quarterly",
            "deadline": "quarter_end",
            "key_requirements": [
                "Identify", "Protect", "Detect", "Respond", "Recover"
            ]
        },
        "iso_27001": {
            "reporting_frequency": "annual",
            "deadline": "certification_renewal",
            "key_requirements": [
                "Information Security Management System",
                "Risk Assessment",
                "Security Controls",
                "Continuous Improvement"
            ]
        }
    },
    "kpi_targets": {
        "network": {
            "network_availability": ">99.9%",
            "call_completion_rate": ">98%",
            "data_throughput": ">100Mbps",
            "network_latency": "<100ms"
        },
        "security": {
            "cyber_incidents": "0",
            "vulnerability_remediation": "<30days",
            "security_training": "100%",
            "penetration_tests": "quarterly"
        },
        "compliance": {
            "regulatory_filings": "100%",
            "audit_findings": "0",
            "policy_compliance": ">95%",
            "license_compliance": "100%"
        },
        "service": {
            "customer_satisfaction": ">4.0/5",
            "service_restoration_time": "<4hours",
            "billing_accuracy": ">99.9%",
            "churn_rate": "<5%"
        }
    }
}

# Telecom-specific prompts for AI analysis
TELECOM_PROMPTS = {
    "fcc_compliance": """
    Analyze FCC compliance for the following telecom content:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'license_compliance': 'license status',
        'service_quality_standards': 'quality assessment',
        'emergency_services': 'E911 compliance status',
        'spectrum_management': 'spectrum compliance',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "network_security": """
    Analyze network security for the following telecom infrastructure:
    {content}
    
    Provide a JSON response with:
    {{
        'security_status': 'secure|vulnerable|critical',
        'cybersecurity_framework': 'NIST CSF implementation status',
        'incident_response': 'response capability assessment',
        'vulnerability_management': 'vulnerability status',
        'monitoring_systems': 'monitoring effectiveness',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "service_quality": """
    Analyze service quality for the following telecom services:
    {content}
    
    Provide a JSON response with:
    {{
        'quality_status': 'excellent|good|fair|poor',
        'network_performance': 'performance metrics',
        'customer_satisfaction': 'satisfaction score',
        'service_reliability': 'reliability assessment',
        'qos_compliance': 'QoS compliance status',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "spectrum_management": """
    Analyze spectrum management for the following telecom operations:
    {content}
    
    Provide a JSON response with:
    {{
        'spectrum_status': 'compliant|non-compliant|partially-compliant',
        'license_usage': 'usage compliance',
        'interference_management': 'interference status',
        'efficiency_metrics': 'spectrum efficiency',
        'coverage_requirements': 'coverage compliance',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """
}

# Telecom-specific document categories for vector storage
TELECOM_DOCUMENT_CATEGORIES = [
    "fcc_compliance",
    "network_security",
    "spectrum_management",
    "service_quality",
    "cybersecurity_framework",
    "emergency_services",
    "regulatory_reporting",
    "network_operations",
    "customer_privacy",
    "infrastructure_management"
]

# Telecom-specific risk assessment templates
TELECOM_RISK_TEMPLATES = {
    "network_security_risk": {
        "description": "Risk of cyber attacks on network infrastructure and customer data",
        "assessment_criteria": [
            "Network architecture security",
            "Access control effectiveness",
            "Monitoring and detection capabilities",
            "Incident response readiness"
        ],
        "mitigation_controls": [
            "Multi-layer security",
            "Intrusion detection systems",
            "Security monitoring",
            "Regular security assessments"
        ]
    },
    "regulatory_compliance_risk": {
        "description": "Risk of violating FCC licensing and regulatory requirements",
        "assessment_criteria": [
            "License compliance status",
            "Regulatory filing accuracy",
            "Service quality standards",
            "Emergency services reliability"
        ],
        "mitigation_controls": [
            "License monitoring",
            "Compliance tracking",
            "Regular audits",
            "Regulatory training"
        ]
    },
    "service_quality_risk": {
        "description": "Risk of network service disruptions and quality degradation",
        "assessment_criteria": [
            "Network redundancy",
            "Equipment reliability",
            "Maintenance procedures",
            "Performance monitoring"
        ],
        "mitigation_controls": [
            "Redundant infrastructure",
            "Backup systems",
            "Proactive monitoring",
            "Rapid response procedures"
        ]
    },
    "technology_risk": {
        "description": "Risk from new technology adoption and integration challenges",
        "assessment_criteria": [
            "Technology maturity",
            "Integration complexity",
            "Vendor reliability",
            "Migration risks"
        ],
        "mitigation_controls": [
            "Technology assessment",
            "Pilot testing",
            "Vendor management",
            "Gradual migration"
        ]
    }
}
