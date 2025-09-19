"""
Manufacturing Agent Configuration
Configuration settings and constants for Manufacturing GRC Agent
"""

from typing import Dict, List, Any
from enum import Enum

class ManufacturingRegulationType(Enum):
    """Manufacturing regulation types"""
    ISO_9001 = "iso_9001"
    ISO_14001 = "iso_14001"
    OSHA = "osha"
    EPA = "epa"
    ROHS = "rohs"
    REACH = "reach"
    FDA = "fda"
    ANSI = "ansi"

class ManufacturingRiskCategory(Enum):
    """Manufacturing risk categories"""
    SAFETY_RISK = "safety_risk"
    QUALITY_RISK = "quality_risk"
    ENVIRONMENTAL_RISK = "environmental_risk"
    SUPPLY_CHAIN_RISK = "supply_chain_risk"
    OPERATIONAL_RISK = "operational_risk"
    REGULATORY_RISK = "regulatory_risk"
    EQUIPMENT_RISK = "equipment_risk"
    PROCESS_RISK = "process_risk"

class ManufacturingComplianceStatus(Enum):
    """Manufacturing compliance status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NOT_ASSESSED = "not_assessed"
    UNDER_REVIEW = "under_review"

# Manufacturing-specific configuration
MANUFACTURING_CONFIG = {
    "industry": "Industrial Manufacturing",
    "regulatory_bodies": [
        "ISO", "FDA", "EPA", "OSHA", "ANSI", "ASTM", "ASME", "IEEE",
        "NIST", "UL", "CE", "RoHS", "REACH", "IEC", "SAE"
    ],
    "quality_standards": {
        "iso_9001": {
            "quality_system": "required",
            "continuous_improvement": "required",
            "customer_focus": "required",
            "process_approach": "required",
            "management_review": "annual"
        },
        "iso_14001": {
            "environmental_management": "required",
            "environmental_policy": "required",
            "legal_compliance": "required",
            "environmental_objectives": "required"
        }
    },
    "safety_requirements": {
        "osha": {
            "safety_programs": "required",
            "hazard_communication": "required",
            "lockout_tagout": "required",
            "personal_protective_equipment": "required",
            "training_programs": "required"
        },
        "machine_safety": {
            "iso_13849": "required",
            "risk_assessment": "required",
            "safety_integration": "required",
            "functional_safety": "required"
        }
    },
    "environmental_standards": {
        "epa": {
            "air_emissions": "permitted",
            "water_discharge": "permitted",
            "waste_management": "required",
            "spill_prevention": "required",
            "environmental_monitoring": "required"
        },
        "rohs_reach": {
            "substance_restrictions": "monitored",
            "material_declaration": "required",
            "testing_requirements": "required",
            "documentation": "required"
        }
    },
    "risk_thresholds": {
        "safety_risk": {
            "fatality": "critical",
            "serious_injury": "high",
            "minor_injury": "medium",
            "near_miss": "low"
        },
        "quality_risk": {
            "recall": "critical",
            "rework": "high",
            "minor_defect": "medium",
            "inspection_finding": "low"
        },
        "environmental_risk": {
            "regulatory_violation": "critical",
            "permit_exceedance": "high",
            "minor_violation": "medium",
            "compliance_issue": "low"
        },
        "operational_risk": {
            "production_stop": "critical",
            "delayed_delivery": "high",
            "cost_increase": "medium",
            "efficiency_loss": "low"
        }
    },
    "compliance_frameworks": {
        "iso_9001": {
            "reporting_frequency": "annual",
            "deadline": "certification_renewal",
            "key_requirements": [
                "Quality Management System",
                "Process Approach",
                "Continuous Improvement",
                "Customer Focus"
            ]
        },
        "iso_14001": {
            "reporting_frequency": "annual",
            "deadline": "certification_renewal",
            "key_requirements": [
                "Environmental Management System",
                "Environmental Policy",
                "Legal Compliance",
                "Environmental Objectives"
            ]
        },
        "osha": {
            "reporting_frequency": "ongoing",
            "deadline": "immediate_incidents",
            "key_requirements": [
                "Safety Programs",
                "Hazard Communication",
                "Lockout/Tagout",
                "Personal Protective Equipment"
            ]
        }
    },
    "kpi_targets": {
        "quality": {
            "defect_rate": "<1%",
            "customer_satisfaction": ">4.0/5",
            "first_pass_yield": ">95%",
            "customer_complaints": "<10/month"
        },
        "safety": {
            "lost_time_injuries": "0",
            "recordable_injuries": "<5/year",
            "near_misses": ">100/year",
            "safety_training": "100%"
        },
        "environmental": {
            "energy_consumption": "reduction_5%",
            "waste_reduction": "reduction_10%",
            "carbon_emissions": "reduction_15%",
            "water_usage": "reduction_8%"
        },
        "operational": {
            "equipment_uptime": ">95%",
            "production_efficiency": ">90%",
            "on_time_delivery": ">98%",
            "inventory_turns": ">8"
        }
    }
}

# Manufacturing-specific prompts for AI analysis
MANUFACTURING_PROMPTS = {
    "iso_9001_compliance": """
    Analyze ISO 9001 compliance for the following manufacturing content:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'quality_management_system': 'QMS status',
        'process_approach': 'process implementation status',
        'continuous_improvement': 'improvement process status',
        'customer_focus': 'customer satisfaction status',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "safety_compliance": """
    Analyze safety compliance for the following manufacturing operations:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'safety_programs': 'safety program status',
        'hazard_communication': 'hazard communication status',
        'lockout_tagout': 'LOTO compliance status',
        'ppe_usage': 'PPE compliance status',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "environmental_compliance": """
    Analyze environmental compliance for the following manufacturing facility:
    {content}
    
    Provide a JSON response with:
    {{
        'compliance_status': 'compliant|non-compliant|partially-compliant',
        'air_emissions': 'emission compliance status',
        'water_discharge': 'discharge compliance status',
        'waste_management': 'waste management status',
        'spill_prevention': 'spill prevention status',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """,
    
    "quality_management": """
    Analyze quality management for the following manufacturing processes:
    {content}
    
    Provide a JSON response with:
    {{
        'quality_status': 'excellent|good|fair|poor',
        'defect_rate': 'calculated defect rate',
        'process_control': 'process control effectiveness',
        'customer_satisfaction': 'satisfaction score',
        'continuous_improvement': 'improvement implementation',
        'recommendations': ['list of recommendations'],
        'confidence_score': 0.95
    }}
    """
}

# Manufacturing-specific document categories for vector storage
MANUFACTURING_DOCUMENT_CATEGORIES = [
    "iso_9001",
    "iso_14001",
    "osha_compliance",
    "epa_regulations",
    "rohs_reach",
    "quality_management",
    "safety_procedures",
    "environmental_management",
    "supply_chain",
    "equipment_maintenance"
]

# Manufacturing-specific risk assessment templates
MANUFACTURING_RISK_TEMPLATES = {
    "safety_risk": {
        "description": "Risk of workplace injuries and fatalities",
        "assessment_criteria": [
            "Workplace safety culture",
            "Safety training effectiveness",
            "Equipment safety features",
            "Hazard identification processes"
        ],
        "mitigation_controls": [
            "Safety training programs",
            "PPE usage requirements",
            "Safety procedures",
            "Incident reporting systems"
        ]
    },
    "quality_risk": {
        "description": "Risk of producing defective products",
        "assessment_criteria": [
            "Process control effectiveness",
            "Quality inspection procedures",
            "Supplier quality management",
            "Customer feedback systems"
        ],
        "mitigation_controls": [
            "Quality control systems",
            "Process monitoring",
            "Testing procedures",
            "Inspection protocols"
        ]
    },
    "environmental_risk": {
        "description": "Risk from environmental impact and regulatory violations",
        "assessment_criteria": [
            "Environmental impact assessment",
            "Regulatory compliance status",
            "Waste management practices",
            "Emission control systems"
        ],
        "mitigation_controls": [
            "Emission control systems",
            "Waste management programs",
            "Environmental monitoring",
            "Compliance training"
        ]
    },
    "supply_chain_risk": {
        "description": "Risk from supplier disruptions and material shortages",
        "assessment_criteria": [
            "Supplier reliability",
            "Material availability",
            "Transportation risks",
            "Geopolitical factors"
        ],
        "mitigation_controls": [
            "Supplier diversification",
            "Inventory management",
            "Backup suppliers",
            "Risk monitoring"
        ]
    }
}
