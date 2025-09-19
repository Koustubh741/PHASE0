"""
Healthcare Agent Configuration
Configuration settings and constants for Healthcare GRC Agent
"""

from typing import Dict, List, Any
from enum import Enum

class HealthcareRegulationType(Enum):
    """Healthcare regulation types"""
    HIPAA = "hipaa"
    HITECH = "hitech"
    JOINT_COMMISSION = "joint_commission"
    CMS = "cms"
    FDA = "fda"
    CLIA = "clia"
    ISO_15189 = "iso_15189"
    JCAHO = "jcaho"

class HealthcareRiskCategory(Enum):
    """Healthcare risk categories"""
    PATIENT_SAFETY_RISK = "patient_safety_risk"
    CLINICAL_RISK = "clinical_risk"
    REGULATORY_RISK = "regulatory_risk"
    OPERATIONAL_RISK = "operational_risk"
    PRIVACY_RISK = "privacy_risk"
    QUALITY_RISK = "quality_risk"
    MEDICATION_RISK = "medication_risk"
    INFECTION_CONTROL_RISK = "infection_control_risk"

class HealthcareComplianceStatus(Enum):
    """Healthcare compliance status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially-compliant"
    NOT_ASSESSED = "not-assessed"
    UNDER_REVIEW = "under-review"

# Healthcare-specific configuration
HEALTHCARE_CONFIG = {
    "industry": "Healthcare and Life Sciences",
    "regulatory_bodies": [
        "FDA", "CMS", "HIPAA", "HITECH", "JCAHO", "ACHA", "CDC", "WHO",
        "ISO", "ICH", "EMA", "Health Canada", "TGA", "PMDA"
    ],
    "patient_safety_standards": {
        "joint_commission": {
            "patient_safety_goals": "required",
            "medication_management": "required",
            "infection_control": "required",
            "fall_prevention": "required",
            "patient_identification": "required"
        },
        "cms_requirements": {
            "quality_measures": "required",
            "patient_satisfaction": "required",
            "readmission_reduction": "required",
            "value_based_purchasing": "required"
        }
    },
    "privacy_security_requirements": {
        "hipaa": {
            "privacy_rule": "required",
            "security_rule": "required",
            "breach_notification": "required",
            "business_associate_agreements": "required",
            "patient_rights": "required"
        },
        "hitech": {
            "meaningful_use": "required",
            "ehr_certification": "required",
            "health_information_exchange": "required",
            "patient_access": "required"
        }
    },
    "clinical_standards": {
        "fda": {
            "good_clinical_practice": "required",
            "adverse_event_reporting": "required",
            "clinical_trial_compliance": "required",
            "medical_device_reporting": "required"
        },
        "clia": {
            "laboratory_standards": "required",
            "quality_control": "required",
            "proficiency_testing": "required",
            "personnel_qualifications": "required"
        }
    },
    "risk_thresholds": {
        "patient_safety": {
            "patient_harm": "critical",
            "near_miss": "high",
            "incident": "medium",
            "concern": "low"
        },
        "clinical_risk": {
            "severe_harm": "critical",
            "moderate_harm": "high",
            "minor_harm": "medium",
            "no_harm": "low"
        },
        "regulatory_risk": {
            "criminal_penalties": "critical",
            "civil_penalties": "high",
            "corrective_action": "medium",
            "warning": "low"
        },
        "operational_risk": {
            "service_disruption": "critical",
            "delayed_service": "high",
            "minor_impact": "medium",
            "no_impact": "low"
        }
    },
    "compliance_frameworks": {
        "hipaa": {
            "reporting_frequency": "ongoing",
            "deadline": "immediate_breach",
            "key_requirements": [
                "Privacy Rule Compliance",
                "Security Rule Implementation",
                "Breach Notification Procedures",
                "Business Associate Agreements"
            ]
        },
        "joint_commission": {
            "reporting_frequency": "annual",
            "deadline": "survey_cycle",
            "key_requirements": [
                "Patient Safety Goals",
                "Medication Management",
                "Infection Prevention",
                "Patient Rights"
            ]
        },
        "cms": {
            "reporting_frequency": "quarterly",
            "deadline": "quarter_end",
            "key_requirements": [
                "Quality Reporting",
                "Value-Based Purchasing",
                "Readmission Reduction",
                "Patient Satisfaction"
            ]
        }
    },
    "kpi_targets": {
        "patient_safety": {
            "medication_errors": "0",
            "healthcare_associated_infections": "<2%",
            "patient_falls": "<3/1000",
            "surgical_site_infections": "<1%"
        },
        "quality": {
            "patient_satisfaction": ">4.0/5",
            "readmission_rate": "<15%",
            "mortality_rate": "<5%",
            "length_of_stay": "optimized"
        },
        "compliance": {
            "hipaa_violations": "0",
            "regulatory_filings": "100%",
            "audit_findings": "0",
            "training_completion": "100%"
        },
        "operational": {
            "staff_turnover": "<10%",
            "equipment_uptime": ">95%",
            "patient_wait_time": "<30min",
            "bed_occupancy": "85-90%"
        }
    }
}

# Healthcare-specific prompts for AI analysis
HEALTHCARE_PROMPTS = {
    "hipaa_compliance": """
    Analyze HIPAA compliance for the following healthcare content:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'privacy_rule': 'privacy rule compliance status',
        'security_rule': 'security rule compliance status',
        'breach_notification': 'breach notification readiness',
        'business_associate_agreements': 'BAA compliance status',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "patient_safety": """
    Analyze patient safety for the following healthcare operations:
    {content}
    
    Provide a JSON response with:
    {{
        'safety_status': 'excellent|good|fair|poor',
        'medication_safety': 'medication safety assessment',
        'infection_control': 'infection control effectiveness',
        'fall_prevention': 'fall prevention measures',
        'patient_identification': 'identification process status',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "clinical_quality": """
    Analyze clinical quality for the following healthcare services:
    {content}
    
    Provide a JSON response with:
    {{
        'quality_status': 'excellent|good|fair|poor',
        'clinical_outcomes': 'outcome assessment',
        'patient_satisfaction': 'satisfaction score',
        'readmission_rates': 'readmission rate analysis',
        'mortality_rates': 'mortality rate assessment',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "regulatory_compliance": """
    Analyze regulatory compliance for the following healthcare organization:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'joint_commission': 'Joint Commission compliance',
        'cms_requirements': 'CMS compliance status',
        'fda_regulations': 'FDA compliance status',
        'state_licensing': 'state licensing compliance',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """
}

# Healthcare-specific document categories for vector storage
HEALTHCARE_DOCUMENT_CATEGORIES = [
    "hipaa_compliance",
    "patient_safety",
    "clinical_quality",
    "joint_commission",
    "cms_requirements",
    "fda_regulations",
    "clia_laboratory",
    "medication_management",
    "infection_control",
    "regulatory_reporting"
]

# Healthcare-specific risk assessment templates
HEALTHCARE_RISK_TEMPLATES = {
    "patient_safety_risk": {
        "description": "Risk from medication errors, infections, and patient harm",
        "assessment_criteria": [
            "Medication administration processes",
            "Infection control procedures",
            "Patient identification systems",
            "Fall prevention measures"
        ],
        "mitigation_controls": [
            "Barcode scanning systems",
            "Hand hygiene protocols",
            "Patient identification procedures",
            "Safety training programs"
        ]
    },
    "clinical_risk": {
        "description": "Risk from diagnostic errors and adverse clinical outcomes",
        "assessment_criteria": [
            "Clinical decision support systems",
            "Diagnostic accuracy processes",
            "Treatment protocols",
            "Clinical monitoring systems"
        ],
        "mitigation_controls": [
            "Clinical guidelines",
            "Second opinion processes",
            "Quality assurance programs",
            "Clinical training"
        ]
    },
    "regulatory_risk": {
        "description": "Risk from regulatory violations and compliance failures",
        "assessment_criteria": [
            "Regulatory compliance monitoring",
            "Documentation accuracy",
            "Reporting timeliness",
            "Training effectiveness"
        ],
        "mitigation_controls": [
            "Compliance monitoring systems",
            "Documentation management",
            "Regulatory training",
            "Audit procedures"
        ]
    },
    "privacy_risk": {
        "description": "Risk from patient data breaches and privacy violations",
        "assessment_criteria": [
            "Data access controls",
            "Encryption implementation",
            "Breach detection systems",
            "Staff training"
        ],
        "mitigation_controls": [
            "Access control systems",
            "Data encryption",
            "Monitoring systems",
            "Privacy training"
        ]
    }
}
