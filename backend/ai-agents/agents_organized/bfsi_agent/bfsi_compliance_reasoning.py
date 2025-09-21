"""
Enhanced BFSI Compliance Reasoning System
Intelligent compliance analysis with regulatory knowledge base and automated reasoning
"""

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
import numpy as np
from collections import defaultdict
import math

# Configure logging
logger = logging.getLogger(__name__)

class ComplianceFramework(Enum):
    """Compliance frameworks"""
    BASEL_III = "basel_iii"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    CCPA = "ccpa"
    AML_KYC = "aml_kyc"
    MIFID_II = "mifid_ii"
    GLBA = "glba"

class ComplianceStatus(Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    AT_RISK = "at_risk"
    UNKNOWN = "unknown"

class CompliancePriority(Enum):
    """Compliance priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class ComplianceRequirement:
    """Compliance requirement with reasoning attributes"""
    requirement_id: str
    framework: ComplianceFramework
    title: str
    description: str
    category: str
    priority: CompliancePriority
    deadline: Optional[datetime]
    applicability: List[str]  # Business units/processes
    dependencies: List[str]
    evidence_required: List[str]
    reasoning_logic: str
    exceptions: List[str]
    monitoring_frequency: str

@dataclass
class ComplianceViolation:
    """Compliance violation with reasoning"""
    violation_id: str
    requirement_id: str
    violation_type: str
    severity: str
    description: str
    root_cause: str
    impact_assessment: Dict[str, Any]
    remediation_plan: List[str]
    timeline: int  # days
    responsible_party: str
    status: str
    reasoning: str

@dataclass
class ComplianceAssessment:
    """Comprehensive compliance assessment"""
    assessment_id: str
    framework: ComplianceFramework
    overall_status: ComplianceStatus
    compliance_score: float
    requirements_met: int
    requirements_total: int
    violations: List[ComplianceViolation]
    gaps: List[Dict[str, Any]]
    recommendations: List[str]
    next_review_date: datetime
    reasoning_summary: str
    timestamp: datetime

@dataclass
class RegulatoryChange:
    """Regulatory change with impact analysis"""
    change_id: str
    framework: ComplianceFramework
    title: str
    description: str
    effective_date: datetime
    impact_level: str
    affected_requirements: List[str]
    implementation_requirements: List[str]
    compliance_deadline: datetime
    reasoning: str

class BFSIComplianceReasoning:
    """
    Enhanced BFSI Compliance Reasoning System with intelligent regulatory analysis
    """
    
    def __init__(self):
        self.system_id = "bfsi_compliance_reasoning"
        self.compliance_requirements: Dict[str, ComplianceRequirement] = {}
        self.regulatory_changes: Dict[str, RegulatoryChange] = {}
        self.assessment_history: List[ComplianceAssessment] = []
        self.violation_history: List[ComplianceViolation] = []
        
        # Initialize compliance frameworks
        self._initialize_compliance_frameworks()
        self._initialize_compliance_requirements()
        self._initialize_regulatory_changes()
        
        logger.info("BFSI Compliance Reasoning System initialized with intelligent regulatory analysis")
    
    def _initialize_compliance_frameworks(self):
        """Initialize BFSI compliance frameworks"""
        self.compliance_frameworks = {
            "basel_iii": {
                "name": "Basel III",
                "description": "International banking regulation for capital adequacy and liquidity",
                "requirements": [
                    "capital_adequacy_ratio",
                    "leverage_ratio",
                    "liquidity_coverage_ratio",
                    "net_stable_funding_ratio"
                ],
                "monitoring_frequency": "quarterly",
                "reporting_requirements": ["capital_adequacy_report", "liquidity_report"]
            },
            "sox": {
                "name": "Sarbanes-Oxley Act",
                "description": "Corporate governance and financial reporting requirements",
                "requirements": [
                    "internal_controls",
                    "financial_reporting",
                    "audit_committee",
                    "whistleblower_protection"
                ],
                "monitoring_frequency": "annual",
                "reporting_requirements": ["internal_control_report", "audit_report"]
            },
            "pci_dss": {
                "name": "PCI DSS",
                "description": "Payment card industry data security standards",
                "requirements": [
                    "network_security",
                    "data_protection",
                    "access_control",
                    "monitoring"
                ],
                "monitoring_frequency": "quarterly",
                "reporting_requirements": ["compliance_report", "security_assessment"]
            },
            "aml_kyc": {
                "name": "AML/KYC",
                "description": "Anti-money laundering and know your customer requirements",
                "requirements": [
                    "customer_due_diligence",
                    "transaction_monitoring",
                    "suspicious_activity_reporting",
                    "record_keeping"
                ],
                "monitoring_frequency": "continuous",
                "reporting_requirements": ["suspicious_activity_report", "currency_transaction_report"]
            }
        }
    
    def _initialize_compliance_requirements(self):
        """Initialize compliance requirements"""
        requirements_data = [
            {
                "requirement_id": "basel_capital_adequacy",
                "framework": ComplianceFramework.BASEL_III,
                "title": "Capital Adequacy Ratio",
                "description": "Maintain minimum capital ratios as per Basel III",
                "category": "capital_management",
                "priority": CompliancePriority.CRITICAL,
                "deadline": None,
                "applicability": ["banking_operations", "risk_management"],
                "dependencies": ["risk_calculation", "capital_calculation"],
                "evidence_required": ["capital_ratios", "risk_weighted_assets"],
                "reasoning_logic": "Capital ratios below minimum indicate insufficient capital buffer",
                "exceptions": ["temporary_waivers", "regulatory_approval"],
                "monitoring_frequency": "quarterly"
            },
            {
                "requirement_id": "sox_internal_controls",
                "framework": ComplianceFramework.SOX,
                "title": "Internal Controls",
                "description": "Maintain effective internal controls over financial reporting",
                "category": "governance",
                "priority": CompliancePriority.HIGH,
                "deadline": None,
                "applicability": ["financial_reporting", "internal_audit"],
                "dependencies": ["control_framework", "testing_procedures"],
                "evidence_required": ["control_documentation", "testing_results"],
                "reasoning_logic": "Weak internal controls increase risk of financial misstatements",
                "exceptions": ["material_weaknesses", "significant_deficiencies"],
                "monitoring_frequency": "annual"
            },
            {
                "requirement_id": "pci_data_protection",
                "framework": ComplianceFramework.PCI_DSS,
                "title": "Data Protection",
                "description": "Protect cardholder data through encryption and access controls",
                "category": "data_security",
                "priority": CompliancePriority.HIGH,
                "deadline": None,
                "applicability": ["payment_processing", "data_management"],
                "dependencies": ["encryption_standards", "access_controls"],
                "evidence_required": ["encryption_certificates", "access_logs"],
                "reasoning_logic": "Inadequate data protection increases risk of data breaches",
                "exceptions": ["legacy_systems", "third_party_vendors"],
                "monitoring_frequency": "quarterly"
            },
            {
                "requirement_id": "aml_transaction_monitoring",
                "framework": ComplianceFramework.AML_KYC,
                "title": "Transaction Monitoring",
                "description": "Monitor transactions for suspicious activity",
                "category": "aml_compliance",
                "priority": CompliancePriority.CRITICAL,
                "deadline": None,
                "applicability": ["transaction_processing", "aml_operations"],
                "dependencies": ["monitoring_systems", "risk_profiles"],
                "evidence_required": ["monitoring_reports", "alert_resolution"],
                "reasoning_logic": "Inadequate monitoring increases risk of money laundering",
                "exceptions": ["false_positives", "system_limitations"],
                "monitoring_frequency": "continuous"
            }
        ]
        
        for req_data in requirements_data:
            self.compliance_requirements[req_data["requirement_id"]] = ComplianceRequirement(**req_data)
    
    def _initialize_regulatory_changes(self):
        """Initialize regulatory changes"""
        changes_data = [
            {
                "change_id": "basel_iv_implementation",
                "framework": ComplianceFramework.BASEL_III,
                "title": "Basel IV Implementation",
                "description": "Implementation of Basel IV capital requirements",
                "effective_date": datetime(2025, 1, 1),
                "impact_level": "high",
                "affected_requirements": ["capital_adequacy_ratio", "risk_weighted_assets"],
                "implementation_requirements": ["model_updates", "system_changes", "training"],
                "compliance_deadline": datetime(2025, 1, 1),
                "reasoning": "Basel IV introduces more stringent capital requirements and risk calculations"
            },
            {
                "change_id": "gdpr_enhancements",
                "framework": ComplianceFramework.GDPR,
                "title": "GDPR Enhanced Requirements",
                "description": "Enhanced data protection requirements under GDPR",
                "effective_date": datetime(2024, 6, 1),
                "impact_level": "medium",
                "affected_requirements": ["data_protection", "privacy_rights", "consent_management"],
                "implementation_requirements": ["privacy_policy_updates", "consent_mechanisms", "data_mapping"],
                "compliance_deadline": datetime(2024, 6, 1),
                "reasoning": "Enhanced GDPR requirements focus on stronger data protection and privacy rights"
            }
        ]
        
        for change_data in changes_data:
            self.regulatory_changes[change_data["change_id"]] = RegulatoryChange(**change_data)
    
    async def assess_compliance(self, framework: ComplianceFramework, context: Dict[str, Any]) -> ComplianceAssessment:
        """Perform comprehensive compliance assessment"""
        logger.info(f"Assessing compliance for {framework.value}")
        
        # Get relevant requirements
        relevant_requirements = [req for req in self.compliance_requirements.values() 
                               if req.framework == framework]
        
        # Assess each requirement
        requirements_met = 0
        violations = []
        gaps = []
        
        for requirement in relevant_requirements:
            compliance_status = await self._assess_requirement_compliance(requirement, context)
            
            if compliance_status["status"] == ComplianceStatus.COMPLIANT:
                requirements_met += 1
            elif compliance_status["status"] == ComplianceStatus.NON_COMPLIANT:
                violation = await self._create_violation(requirement, compliance_status, context)
                violations.append(violation)
            elif compliance_status["status"] == ComplianceStatus.PARTIALLY_COMPLIANT:
                gap = await self._identify_compliance_gap(requirement, compliance_status, context)
                gaps.append(gap)
        
        # Calculate compliance score
        compliance_score = (requirements_met / len(relevant_requirements)) * 100 if relevant_requirements else 0
        
        # Determine overall status
        overall_status = self._determine_overall_status(compliance_score, violations, gaps)
        
        # Generate recommendations
        recommendations = await self._generate_compliance_recommendations(compliance_score, violations, gaps, context)
        
        # Generate reasoning summary
        reasoning_summary = await self._generate_reasoning_summary(compliance_score, violations, gaps, context)
        
        # Calculate next review date
        next_review_date = await self._calculate_next_review_date(framework, context)
        
        assessment = ComplianceAssessment(
            assessment_id=str(uuid.uuid4()),
            framework=framework,
            overall_status=overall_status,
            compliance_score=compliance_score,
            requirements_met=requirements_met,
            requirements_total=len(relevant_requirements),
            violations=violations,
            gaps=gaps,
            recommendations=recommendations,
            next_review_date=next_review_date,
            reasoning_summary=reasoning_summary,
            timestamp=datetime.now()
        )
        
        self.assessment_history.append(assessment)
        return assessment
    
    async def _assess_requirement_compliance(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance with a specific requirement"""
        # Simulate compliance assessment based on context
        compliance_data = context.get("compliance_data", {})
        requirement_data = compliance_data.get(requirement.requirement_id, {})
        
        # Check if requirement is applicable
        if not self._is_requirement_applicable(requirement, context):
            return {
                "status": ComplianceStatus.COMPLIANT,
                "reasoning": "Requirement not applicable to current context",
                "evidence": []
            }
        
        # Check dependencies
        dependencies_met = await self._check_dependencies(requirement, context)
        if not dependencies_met:
            return {
                "status": ComplianceStatus.NON_COMPLIANT,
                "reasoning": "Dependencies not met",
                "evidence": []
            }
        
        # Check evidence
        evidence_status = await self._check_evidence(requirement, context)
        if not evidence_status["complete"]:
            return {
                "status": ComplianceStatus.PARTIALLY_COMPLIANT,
                "reasoning": f"Evidence incomplete: {evidence_status['missing']}",
                "evidence": evidence_status["available"]
            }
        
        # Check compliance logic
        compliance_result = await self._evaluate_compliance_logic(requirement, context)
        
        return {
            "status": compliance_result["status"],
            "reasoning": compliance_result["reasoning"],
            "evidence": evidence_status["available"]
        }
    
    def _is_requirement_applicable(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> bool:
        """Check if requirement is applicable to current context"""
        business_units = context.get("business_units", [])
        processes = context.get("processes", [])
        
        # Check if any applicable business units or processes match
        for applicable in requirement.applicability:
            if applicable in business_units or applicable in processes:
                return True
        
        return False
    
    async def _check_dependencies(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> bool:
        """Check if requirement dependencies are met"""
        dependencies = requirement.dependencies
        compliance_data = context.get("compliance_data", {})
        
        for dependency in dependencies:
            if dependency not in compliance_data:
                return False
            
            dependency_status = compliance_data[dependency].get("status", "unknown")
            if dependency_status not in ["compliant", "met"]:
                return False
        
        return True
    
    async def _check_evidence(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if required evidence is available"""
        required_evidence = requirement.evidence_required
        available_evidence = context.get("evidence", {})
        
        available = []
        missing = []
        
        for evidence_type in required_evidence:
            if evidence_type in available_evidence:
                available.append(evidence_type)
            else:
                missing.append(evidence_type)
        
        return {
            "complete": len(missing) == 0,
            "available": available,
            "missing": missing
        }
    
    async def _evaluate_compliance_logic(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate compliance using reasoning logic"""
        # Simulate compliance evaluation based on requirement type
        if requirement.framework == ComplianceFramework.BASEL_III:
            return await self._evaluate_basel_compliance(requirement, context)
        elif requirement.framework == ComplianceFramework.SOX:
            return await self._evaluate_sox_compliance(requirement, context)
        elif requirement.framework == ComplianceFramework.PCI_DSS:
            return await self._evaluate_pci_compliance(requirement, context)
        elif requirement.framework == ComplianceFramework.AML_KYC:
            return await self._evaluate_aml_compliance(requirement, context)
        else:
            return {
                "status": ComplianceStatus.UNKNOWN,
                "reasoning": "Unknown compliance framework"
            }
    
    async def _evaluate_basel_compliance(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Basel III compliance"""
        if requirement.requirement_id == "basel_capital_adequacy":
            # Check capital ratios
            capital_data = context.get("capital_data", {})
            tier_1_ratio = capital_data.get("tier_1_ratio", 0)
            total_capital_ratio = capital_data.get("total_capital_ratio", 0)
            
            if tier_1_ratio >= 6.0 and total_capital_ratio >= 8.0:
                return {
                    "status": ComplianceStatus.COMPLIANT,
                    "reasoning": f"Capital ratios meet requirements: Tier 1: {tier_1_ratio}%, Total: {total_capital_ratio}%"
                }
            else:
                return {
                    "status": ComplianceStatus.NON_COMPLIANT,
                    "reasoning": f"Capital ratios below requirements: Tier 1: {tier_1_ratio}%, Total: {total_capital_ratio}%"
                }
        
        return {
            "status": ComplianceStatus.COMPLIANT,
            "reasoning": "Basel III requirement met"
        }
    
    async def _evaluate_sox_compliance(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate SOX compliance"""
        if requirement.requirement_id == "sox_internal_controls":
            # Check internal controls effectiveness
            controls_data = context.get("controls_data", {})
            effectiveness = controls_data.get("effectiveness", 0)
            
            if effectiveness >= 0.95:
                return {
                    "status": ComplianceStatus.COMPLIANT,
                    "reasoning": f"Internal controls effective: {effectiveness:.2%}"
                }
            elif effectiveness >= 0.80:
                return {
                    "status": ComplianceStatus.PARTIALLY_COMPLIANT,
                    "reasoning": f"Internal controls partially effective: {effectiveness:.2%}"
                }
            else:
                return {
                    "status": ComplianceStatus.NON_COMPLIANT,
                    "reasoning": f"Internal controls ineffective: {effectiveness:.2%}"
                }
        
        return {
            "status": ComplianceStatus.COMPLIANT,
            "reasoning": "SOX requirement met"
        }
    
    async def _evaluate_pci_compliance(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate PCI DSS compliance"""
        if requirement.requirement_id == "pci_data_protection":
            # Check data protection measures
            security_data = context.get("security_data", {})
            encryption_status = security_data.get("encryption", False)
            access_controls = security_data.get("access_controls", False)
            
            if encryption_status and access_controls:
                return {
                    "status": ComplianceStatus.COMPLIANT,
                    "reasoning": "Data protection measures in place"
                }
            else:
                return {
                    "status": ComplianceStatus.NON_COMPLIANT,
                    "reasoning": "Data protection measures insufficient"
                }
        
        return {
            "status": ComplianceStatus.COMPLIANT,
            "reasoning": "PCI DSS requirement met"
        }
    
    async def _evaluate_aml_compliance(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate AML/KYC compliance"""
        if requirement.requirement_id == "aml_transaction_monitoring":
            # Check transaction monitoring
            aml_data = context.get("aml_data", {})
            monitoring_active = aml_data.get("monitoring_active", False)
            alerts_resolved = aml_data.get("alerts_resolved", 0)
            alerts_total = aml_data.get("alerts_total", 0)
            
            if monitoring_active and alerts_resolved >= alerts_total * 0.95:
                return {
                    "status": ComplianceStatus.COMPLIANT,
                    "reasoning": "Transaction monitoring effective"
                }
            else:
                return {
                    "status": ComplianceStatus.NON_COMPLIANT,
                    "reasoning": "Transaction monitoring ineffective"
                }
        
        return {
            "status": ComplianceStatus.COMPLIANT,
            "reasoning": "AML/KYC requirement met"
        }
    
    async def _create_violation(self, requirement: ComplianceRequirement, compliance_status: Dict[str, Any], context: Dict[str, Any]) -> ComplianceViolation:
        """Create compliance violation"""
        violation = ComplianceViolation(
            violation_id=str(uuid.uuid4()),
            requirement_id=requirement.requirement_id,
            violation_type="compliance_violation",
            severity="high" if requirement.priority == CompliancePriority.CRITICAL else "medium",
            description=f"Non-compliance with {requirement.title}",
            root_cause=compliance_status["reasoning"],
            impact_assessment=await self._assess_violation_impact(requirement, context),
            remediation_plan=await self._create_remediation_plan(requirement, context),
            timeline=30,  # Default 30 days
            responsible_party="Compliance Officer",
            status="open",
            reasoning=compliance_status["reasoning"]
        )
        
        self.violation_history.append(violation)
        return violation
    
    async def _identify_compliance_gap(self, requirement: ComplianceRequirement, compliance_status: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Identify compliance gap"""
        return {
            "requirement_id": requirement.requirement_id,
            "requirement_title": requirement.title,
            "gap_description": compliance_status["reasoning"],
            "severity": "medium",
            "remediation_required": True,
            "timeline": 60,  # 60 days
            "responsible_party": "Compliance Team"
        }
    
    def _determine_overall_status(self, compliance_score: float, violations: List[ComplianceViolation], gaps: List[Dict[str, Any]]) -> ComplianceStatus:
        """Determine overall compliance status"""
        if compliance_score >= 95 and not violations and not gaps:
            return ComplianceStatus.COMPLIANT
        elif compliance_score >= 80 and len(violations) == 0:
            return ComplianceStatus.PARTIALLY_COMPLIANT
        elif violations or compliance_score < 80:
            return ComplianceStatus.NON_COMPLIANT
        else:
            return ComplianceStatus.AT_RISK
    
    async def _generate_compliance_recommendations(self, compliance_score: float, violations: List[ComplianceViolation], gaps: List[Dict[str, Any]], context: Dict[str, Any]) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        # Score-based recommendations
        if compliance_score < 80:
            recommendations.append("CRITICAL: Immediate compliance improvement required")
            recommendations.append("Conduct comprehensive compliance review")
            recommendations.append("Implement enhanced monitoring and controls")
        elif compliance_score < 95:
            recommendations.append("Implement additional compliance measures")
            recommendations.append("Strengthen existing controls")
            recommendations.append("Increase monitoring frequency")
        
        # Violation-based recommendations
        if violations:
            recommendations.append(f"Address {len(violations)} compliance violations immediately")
            for violation in violations:
                recommendations.append(f"Resolve violation: {violation.description}")
        
        # Gap-based recommendations
        if gaps:
            recommendations.append(f"Close {len(gaps)} compliance gaps")
            for gap in gaps:
                recommendations.append(f"Address gap: {gap['gap_description']}")
        
        # General recommendations
        recommendations.extend([
            "Regular compliance training for staff",
            "Update compliance policies and procedures",
            "Enhance compliance monitoring systems",
            "Conduct regular compliance audits"
        ])
        
        return recommendations
    
    async def _generate_reasoning_summary(self, compliance_score: float, violations: List[ComplianceViolation], gaps: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Generate reasoning summary for compliance assessment"""
        summary_parts = []
        
        # Overall score reasoning
        if compliance_score >= 95:
            summary_parts.append("High compliance score indicates strong regulatory adherence")
        elif compliance_score >= 80:
            summary_parts.append("Moderate compliance score suggests room for improvement")
        else:
            summary_parts.append("Low compliance score indicates significant regulatory risks")
        
        # Violation reasoning
        if violations:
            summary_parts.append(f"{len(violations)} violations identified requiring immediate attention")
        
        # Gap reasoning
        if gaps:
            summary_parts.append(f"{len(gaps)} compliance gaps identified needing remediation")
        
        # Context-specific reasoning
        if context.get("recent_changes"):
            summary_parts.append("Recent regulatory changes may impact compliance status")
        
        return " | ".join(summary_parts)
    
    async def _calculate_next_review_date(self, framework: ComplianceFramework, context: Dict[str, Any]) -> datetime:
        """Calculate next compliance review date"""
        framework_info = self.compliance_frameworks.get(framework.value, {})
        monitoring_frequency = framework_info.get("monitoring_frequency", "quarterly")
        
        if monitoring_frequency == "continuous":
            return datetime.now() + timedelta(days=1)
        elif monitoring_frequency == "quarterly":
            return datetime.now() + timedelta(days=90)
        elif monitoring_frequency == "annual":
            return datetime.now() + timedelta(days=365)
        else:
            return datetime.now() + timedelta(days=30)
    
    async def _assess_violation_impact(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess impact of compliance violation"""
        impact = {
            "regulatory_risk": "high" if requirement.priority == CompliancePriority.CRITICAL else "medium",
            "financial_impact": "high" if requirement.priority == CompliancePriority.CRITICAL else "medium",
            "reputational_risk": "high" if requirement.priority == CompliancePriority.CRITICAL else "medium",
            "operational_impact": "medium"
        }
        
        return impact
    
    async def _create_remediation_plan(self, requirement: ComplianceRequirement, context: Dict[str, Any]) -> List[str]:
        """Create remediation plan for violation"""
        plan = [
            "Immediate assessment of current state",
            "Development of remediation strategy",
            "Implementation of corrective measures",
            "Testing and validation of fixes",
            "Documentation of remediation actions",
            "Monitoring and verification of compliance"
        ]
        
        return plan
    
    async def analyze_regulatory_changes(self, framework: ComplianceFramework) -> List[RegulatoryChange]:
        """Analyze regulatory changes for a framework"""
        relevant_changes = [change for change in self.regulatory_changes.values() 
                          if change.framework == framework]
        
        # Sort by effective date
        relevant_changes.sort(key=lambda x: x.effective_date)
        
        return relevant_changes
    
    async def get_compliance_statistics(self) -> Dict[str, Any]:
        """Get compliance statistics"""
        if not self.assessment_history:
            return {"total_assessments": 0}
        
        frameworks = defaultdict(int)
        compliance_scores = []
        violation_counts = []
        
        for assessment in self.assessment_history:
            frameworks[assessment.framework.value] += 1
            compliance_scores.append(assessment.compliance_score)
            violation_counts.append(len(assessment.violations))
        
        return {
            "total_assessments": len(self.assessment_history),
            "framework_distribution": dict(frameworks),
            "average_compliance_score": sum(compliance_scores) / len(compliance_scores),
            "highest_compliance_score": max(compliance_scores),
            "lowest_compliance_score": min(compliance_scores),
            "average_violations": sum(violation_counts) / len(violation_counts),
            "total_violations": sum(violation_counts)
        }
