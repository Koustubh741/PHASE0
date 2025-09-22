#!/usr/bin/env python3
"""
BFSI Gap Analysis Service
Comprehensive policy gap analysis and mitigation system for clients
"""

import os
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GapSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ComplianceFramework(Enum):
    SOX = "sox"
    BASEL_III = "basel_iii"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    AML_KYC = "aml_kyc"
    MIFID_II = "mifid_ii"
    DODD_FRANK = "dodd_frank"
    CCPA = "ccpa"

class PolicyStatus(Enum):
    IMPLEMENTED = "implemented"
    PARTIAL = "partial"
    MISSING = "missing"
    OUTDATED = "outdated"

@dataclass
class PolicyGap:
    gap_id: str
    policy_name: str
    framework: ComplianceFramework
    severity: GapSeverity
    description: str
    current_status: PolicyStatus
    required_actions: List[str]
    mitigation_strategies: List[str]
    estimated_effort: str
    business_impact: str
    regulatory_impact: str
    priority_score: int
    due_date: Optional[datetime]
    assigned_owner: Optional[str]
    created_date: datetime
    last_updated: datetime

@dataclass
class GapAnalysisReport:
    report_id: str
    organization_name: str
    analysis_date: datetime
    total_policies: int
    implemented_policies: int
    partial_policies: int
    missing_policies: int
    outdated_policies: int
    compliance_score: float
    critical_gaps: int
    high_priority_gaps: int
    medium_priority_gaps: int
    low_priority_gaps: int
    gaps: List[PolicyGap]
    recommendations: List[str]
    next_review_date: datetime
    executive_summary: str

class BFSIGapAnalysisService:
    """
    Comprehensive BFSI Gap Analysis Service
    Provides policy gap analysis, compliance assessment, and mitigation strategies
    """
    
    def __init__(self, db_path: str = "bfsi_policies.db"):
        self.db_path = db_path
        self.ensure_database()
        
        # Standard BFSI compliance frameworks and requirements
        self.compliance_frameworks = {
            ComplianceFramework.SOX: {
                "name": "Sarbanes-Oxley Act",
                "requirements": [
                    "Internal controls over financial reporting",
                    "Management assessment of internal controls",
                    "Auditor attestation of internal controls",
                    "Disclosure controls and procedures",
                    "Code of ethics for senior financial officers",
                    "Whistleblower protection",
                    "Document retention policies",
                    "Risk assessment procedures"
                ],
                "priority": "critical"
            },
            ComplianceFramework.BASEL_III: {
                "name": "Basel III Capital Requirements",
                "requirements": [
                    "Minimum capital requirements",
                    "Capital conservation buffer",
                    "Countercyclical capital buffer",
                    "Leverage ratio requirements",
                    "Liquidity coverage ratio",
                    "Net stable funding ratio",
                    "Risk management framework",
                    "Stress testing procedures"
                ],
                "priority": "critical"
            },
            ComplianceFramework.PCI_DSS: {
                "name": "Payment Card Industry Data Security Standard",
                "requirements": [
                    "Secure network and systems maintenance",
                    "Protection of cardholder data",
                    "Vulnerability management program",
                    "Strong access control measures",
                    "Regular network monitoring and testing",
                    "Information security policy"
                ],
                "priority": "high"
            },
            ComplianceFramework.GDPR: {
                "name": "General Data Protection Regulation",
                "requirements": [
                    "Data protection by design and default",
                    "Data subject rights management",
                    "Privacy impact assessments",
                    "Data breach notification procedures",
                    "Consent management systems",
                    "Data processing agreements",
                    "Privacy policy documentation",
                    "Data retention policies"
                ],
                "priority": "high"
            }
        }
        
        logger.info("BFSI Gap Analysis Service initialized")

    def ensure_database(self):
        """Ensure database tables exist for gap analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create gap analysis tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS policy_gaps (
                gap_id TEXT PRIMARY KEY,
                policy_name TEXT NOT NULL,
                framework TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                current_status TEXT NOT NULL,
                required_actions TEXT,
                mitigation_strategies TEXT,
                estimated_effort TEXT,
                business_impact TEXT,
                regulatory_impact TEXT,
                priority_score INTEGER,
                due_date TEXT,
                assigned_owner TEXT,
                created_date TEXT,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gap_analysis_reports (
                report_id TEXT PRIMARY KEY,
                organization_name TEXT NOT NULL,
                analysis_date TEXT NOT NULL,
                total_policies INTEGER,
                implemented_policies INTEGER,
                partial_policies INTEGER,
                missing_policies INTEGER,
                outdated_policies INTEGER,
                compliance_score REAL,
                critical_gaps INTEGER,
                high_priority_gaps INTEGER,
                medium_priority_gaps INTEGER,
                low_priority_gaps INTEGER,
                recommendations TEXT,
                next_review_date TEXT,
                executive_summary TEXT,
                created_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    async def perform_comprehensive_gap_analysis(self, 
                                                organization_name: str,
                                                organization_policies: List[Dict[str, Any]] = None) -> GapAnalysisReport:
        """Perform comprehensive gap analysis for an organization"""
        
        logger.info(f"Starting comprehensive gap analysis for {organization_name}")
        
        # Get organization's current policies
        if organization_policies is None:
            organization_policies = self._get_organization_policies()
        
        # Analyze each compliance framework
        all_gaps = []
        framework_scores = {}
        
        for framework, framework_info in self.compliance_frameworks.items():
            logger.info(f"Analyzing {framework.value} compliance")
            
            # Find gaps for this framework
            framework_gaps = await self._analyze_framework_gaps(
                framework, 
                framework_info, 
                organization_policies
            )
            
            all_gaps.extend(framework_gaps)
            
            # Calculate framework compliance score
            framework_score = self._calculate_framework_score(framework_gaps, framework_info)
            framework_scores[framework.value] = framework_score
        
        # Calculate overall compliance score
        overall_compliance_score = sum(framework_scores.values()) / len(framework_scores)
        
        # Categorize gaps by severity
        gap_counts = self._categorize_gaps(all_gaps)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(all_gaps, framework_scores)
        
        # Create executive summary
        executive_summary = self._generate_executive_summary(
            organization_name, 
            overall_compliance_score, 
            gap_counts, 
            all_gaps
        )
        
        # Create gap analysis report
        report = GapAnalysisReport(
            report_id=str(uuid.uuid4()),
            organization_name=organization_name,
            analysis_date=datetime.now(),
            total_policies=len(organization_policies),
            implemented_policies=gap_counts["implemented"],
            partial_policies=gap_counts["partial"],
            missing_policies=gap_counts["missing"],
            outdated_policies=gap_counts["outdated"],
            compliance_score=overall_compliance_score,
            critical_gaps=gap_counts["critical"],
            high_priority_gaps=gap_counts["high"],
            medium_priority_gaps=gap_counts["medium"],
            low_priority_gaps=gap_counts["low"],
            gaps=all_gaps,
            recommendations=recommendations,
            next_review_date=datetime.now() + timedelta(days=90),
            executive_summary=executive_summary
        )
        
        # Save report to database
        self._save_gap_analysis_report(report)
        
        logger.info(f"Gap analysis completed for {organization_name}")
        return report

    async def _analyze_framework_gaps(self, 
                                     framework: ComplianceFramework, 
                                     framework_info: Dict[str, Any],
                                     organization_policies: List[Dict[str, Any]]) -> List[PolicyGap]:
        """Analyze gaps for a specific compliance framework"""
        
        gaps = []
        requirements = framework_info["requirements"]
        
        for requirement in requirements:
            # Check if organization has policy covering this requirement
            policy_match = self._find_matching_policy(requirement, organization_policies)
            
            if not policy_match:
                # Missing policy - create gap
                gap = PolicyGap(
                    gap_id=str(uuid.uuid4()),
                    policy_name=f"{framework.value.upper()} - {requirement}",
                    framework=framework,
                    severity=GapSeverity.HIGH if framework_info["priority"] == "critical" else GapSeverity.MEDIUM,
                    description=f"Missing policy for {requirement}",
                    current_status=PolicyStatus.MISSING,
                    required_actions=self._generate_required_actions(requirement, framework),
                    mitigation_strategies=self._generate_mitigation_strategies(requirement, framework),
                    estimated_effort=self._estimate_effort(requirement, framework),
                    business_impact=self._assess_business_impact(requirement, framework),
                    regulatory_impact=self._assess_regulatory_impact(requirement, framework),
                    priority_score=self._calculate_priority_score(requirement, framework),
                    due_date=datetime.now() + timedelta(days=30),
                    assigned_owner=None,
                    created_date=datetime.now(),
                    last_updated=datetime.now()
                )
                gaps.append(gap)
                
            elif policy_match["status"] == "partial":
                # Partial implementation - create gap
                gap = PolicyGap(
                    gap_id=str(uuid.uuid4()),
                    policy_name=f"{framework.value.upper()} - {requirement}",
                    framework=framework,
                    severity=GapSeverity.MEDIUM,
                    description=f"Partial implementation of {requirement}",
                    current_status=PolicyStatus.PARTIAL,
                    required_actions=self._generate_required_actions(requirement, framework, partial=True),
                    mitigation_strategies=self._generate_mitigation_strategies(requirement, framework, partial=True),
                    estimated_effort=self._estimate_effort(requirement, framework, partial=True),
                    business_impact=self._assess_business_impact(requirement, framework),
                    regulatory_impact=self._assess_regulatory_impact(requirement, framework),
                    priority_score=self._calculate_priority_score(requirement, framework),
                    due_date=datetime.now() + timedelta(days=60),
                    assigned_owner=None,
                    created_date=datetime.now(),
                    last_updated=datetime.now()
                )
                gaps.append(gap)
        
        return gaps

    def _find_matching_policy(self, requirement: str, organization_policies: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find if organization has a policy covering the requirement"""
        
        # Simple keyword matching - in production, use NLP/ML for better matching
        requirement_keywords = requirement.lower().split()
        
        for policy in organization_policies:
            policy_content = policy.get("content", "").lower()
            policy_title = policy.get("title", "").lower()
            
            # Check if policy covers this requirement
            keyword_matches = sum(1 for keyword in requirement_keywords if keyword in policy_content or keyword in policy_title)
            
            if keyword_matches >= len(requirement_keywords) * 0.6:  # 60% keyword match
                return {
                    "policy": policy,
                    "status": "implemented" if keyword_matches >= len(requirement_keywords) * 0.8 else "partial"
                }
        
        return None

    def _generate_required_actions(self, requirement: str, framework: ComplianceFramework, partial: bool = False) -> List[str]:
        """Generate required actions for addressing a gap"""
        
        base_actions = [
            f"Develop comprehensive policy document for {requirement}",
            f"Implement controls and procedures for {requirement}",
            f"Train staff on {requirement} requirements",
            f"Establish monitoring and reporting mechanisms",
            f"Conduct regular compliance assessments"
        ]
        
        if partial:
            base_actions.insert(0, f"Review and enhance existing policy for {requirement}")
        
        # Add framework-specific actions
        if framework == ComplianceFramework.SOX:
            base_actions.extend([
                "Establish internal control documentation",
                "Implement management assessment procedures",
                "Set up auditor coordination processes"
            ])
        elif framework == ComplianceFramework.BASEL_III:
            base_actions.extend([
                "Implement capital adequacy monitoring",
                "Establish stress testing procedures",
                "Set up liquidity risk management"
            ])
        
        return base_actions

    def _generate_mitigation_strategies(self, requirement: str, framework: ComplianceFramework, partial: bool = False) -> List[str]:
        """Generate mitigation strategies for addressing gaps"""
        
        strategies = [
            f"Immediate implementation of {requirement} policy",
            f"Phased rollout of {requirement} controls",
            f"Third-party compliance consulting for {requirement}",
            f"Technology solution implementation for {requirement}",
            f"Staff augmentation for {requirement} compliance"
        ]
        
        if partial:
            strategies.insert(0, f"Gap analysis and enhancement of existing {requirement} implementation")
        
        return strategies

    def _estimate_effort(self, requirement: str, framework: ComplianceFramework, partial: bool = False) -> str:
        """Estimate effort required to address gap"""
        
        if partial:
            return "2-4 weeks"
        
        # Framework-specific effort estimates
        effort_estimates = {
            ComplianceFramework.SOX: "8-12 weeks",
            ComplianceFramework.BASEL_III: "12-16 weeks",
            ComplianceFramework.PCI_DSS: "6-10 weeks",
            ComplianceFramework.GDPR: "8-12 weeks"
        }
        
        return effort_estimates.get(framework, "6-10 weeks")

    def _assess_business_impact(self, requirement: str, framework: ComplianceFramework) -> str:
        """Assess business impact of the gap"""
        
        impact_assessments = {
            ComplianceFramework.SOX: "High - Financial reporting and audit implications",
            ComplianceFramework.BASEL_III: "Critical - Capital adequacy and regulatory capital requirements",
            ComplianceFramework.PCI_DSS: "High - Payment processing and data security",
            ComplianceFramework.GDPR: "High - Data protection and privacy compliance"
        }
        
        return impact_assessments.get(framework, "Medium - Operational and compliance implications")

    def _assess_regulatory_impact(self, requirement: str, framework: ComplianceFramework) -> str:
        """Assess regulatory impact of the gap"""
        
        regulatory_impacts = {
            ComplianceFramework.SOX: "Critical - SEC enforcement and penalties",
            ComplianceFramework.BASEL_III: "Critical - Banking regulator sanctions",
            ComplianceFramework.PCI_DSS: "High - Payment card industry penalties",
            ComplianceFramework.GDPR: "High - Data protection authority fines"
        }
        
        return regulatory_impacts.get(framework, "Medium - Regulatory scrutiny and potential penalties")

    def _calculate_priority_score(self, requirement: str, framework: ComplianceFramework) -> int:
        """Calculate priority score for the gap (1-100)"""
        
        base_score = 50
        
        # Framework priority adjustments
        if framework in [ComplianceFramework.SOX, ComplianceFramework.BASEL_III]:
            base_score += 30
        elif framework in [ComplianceFramework.PCI_DSS, ComplianceFramework.GDPR]:
            base_score += 20
        
        # Requirement-specific adjustments
        if "capital" in requirement.lower() or "risk" in requirement.lower():
            base_score += 20
        elif "data" in requirement.lower() or "privacy" in requirement.lower():
            base_score += 15
        
        return min(base_score, 100)

    def _calculate_framework_score(self, gaps: List[PolicyGap], framework_info: Dict[str, Any]) -> float:
        """Calculate compliance score for a framework"""
        
        total_requirements = len(framework_info["requirements"])
        if total_requirements == 0:
            return 100.0
        
        # Count implemented requirements (no gaps)
        implemented_requirements = total_requirements - len(gaps)
        
        # Calculate score
        score = (implemented_requirements / total_requirements) * 100
        
        return round(score, 2)

    def _categorize_gaps(self, gaps: List[PolicyGap]) -> Dict[str, int]:
        """Categorize gaps by status and severity"""
        
        counts = {
            "implemented": 0,
            "partial": 0,
            "missing": 0,
            "outdated": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for gap in gaps:
            # Count by status
            if gap.current_status == PolicyStatus.IMPLEMENTED:
                counts["implemented"] += 1
            elif gap.current_status == PolicyStatus.PARTIAL:
                counts["partial"] += 1
            elif gap.current_status == PolicyStatus.MISSING:
                counts["missing"] += 1
            elif gap.current_status == PolicyStatus.OUTDATED:
                counts["outdated"] += 1
            
            # Count by severity
            if gap.severity == GapSeverity.CRITICAL:
                counts["critical"] += 1
            elif gap.severity == GapSeverity.HIGH:
                counts["high"] += 1
            elif gap.severity == GapSeverity.MEDIUM:
                counts["medium"] += 1
            elif gap.severity == GapSeverity.LOW:
                counts["low"] += 1
        
        return counts

    async def _generate_recommendations(self, gaps: List[PolicyGap], framework_scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on gap analysis"""
        
        recommendations = []
        
        # Overall recommendations
        if len(gaps) > 0:
            recommendations.append("Immediate action required to address compliance gaps")
            recommendations.append("Prioritize critical and high-severity gaps for immediate remediation")
            recommendations.append("Establish governance structure for ongoing compliance monitoring")
        
        # Framework-specific recommendations
        for framework, score in framework_scores.items():
            if score < 70:
                recommendations.append(f"Urgent attention required for {framework} compliance (Score: {score}%)")
            elif score < 85:
                recommendations.append(f"Improvement needed for {framework} compliance (Score: {score}%)")
        
        # Gap-specific recommendations
        critical_gaps = [gap for gap in gaps if gap.severity == GapSeverity.CRITICAL]
        if critical_gaps:
            recommendations.append(f"Address {len(critical_gaps)} critical compliance gaps immediately")
        
        high_priority_gaps = [gap for gap in gaps if gap.severity == GapSeverity.HIGH]
        if high_priority_gaps:
            recommendations.append(f"Plan remediation for {len(high_priority_gaps)} high-priority gaps within 60 days")
        
        return recommendations

    def _generate_executive_summary(self, 
                                  organization_name: str, 
                                  compliance_score: float, 
                                  gap_counts: Dict[str, int],
                                  gaps: List[PolicyGap]) -> str:
        """Generate executive summary of gap analysis"""
        
        summary = f"""
EXECUTIVE SUMMARY - BFSI COMPLIANCE GAP ANALYSIS
Organization: {organization_name}
Analysis Date: {datetime.now().strftime('%Y-%m-%d')}

OVERALL COMPLIANCE SCORE: {compliance_score:.1f}%

COMPLIANCE STATUS:
- Implemented Policies: {gap_counts['implemented']}
- Partial Implementation: {gap_counts['partial']}
- Missing Policies: {gap_counts['missing']}
- Outdated Policies: {gap_counts['outdated']}

CRITICAL FINDINGS:
- Critical Gaps: {gap_counts['critical']}
- High Priority Gaps: {gap_counts['high']}
- Medium Priority Gaps: {gap_counts['medium']}
- Low Priority Gaps: {gap_counts['low']}

RECOMMENDATIONS:
1. Immediate action required for {gap_counts['critical']} critical gaps
2. High-priority remediation for {gap_counts['high']} high-severity gaps
3. Comprehensive compliance program enhancement
4. Regular monitoring and assessment procedures

NEXT STEPS:
- Develop remediation plan for identified gaps
- Assign ownership and timelines for gap closure
- Implement ongoing compliance monitoring
- Schedule next assessment in 90 days
        """
        
        return summary.strip()

    def _get_organization_policies(self) -> List[Dict[str, Any]]:
        """Get organization's current policies from database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Use the actual database schema
        cursor.execute('''
            SELECT title, content, policy_type, framework, source_file, file_type, created_at
            FROM policies
            ORDER BY created_at DESC
        ''')
        
        policies = []
        for row in cursor.fetchall():
            policies.append({
                "title": row[0],
                "content": row[1],
                "category": row[2],  # policy_type maps to category
                "framework": row[3],
                "source_file": row[4],
                "file_type": row[5],
                "created_date": row[6]
            })
        
        conn.close()
        return policies

    def _save_gap_analysis_report(self, report: GapAnalysisReport):
        """Save gap analysis report to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save report
        cursor.execute('''
            INSERT INTO gap_analysis_reports 
            (report_id, organization_name, analysis_date, total_policies, implemented_policies,
             partial_policies, missing_policies, outdated_policies, compliance_score,
             critical_gaps, high_priority_gaps, medium_priority_gaps, low_priority_gaps,
             recommendations, next_review_date, executive_summary, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report.report_id,
            report.organization_name,
            report.analysis_date.isoformat(),
            report.total_policies,
            report.implemented_policies,
            report.partial_policies,
            report.missing_policies,
            report.outdated_policies,
            report.compliance_score,
            report.critical_gaps,
            report.high_priority_gaps,
            report.medium_priority_gaps,
            report.low_priority_gaps,
            json.dumps(report.recommendations),
            report.next_review_date.isoformat(),
            report.executive_summary,
            datetime.now().isoformat()
        ))
        
        # Save individual gaps
        for gap in report.gaps:
            cursor.execute('''
                INSERT INTO policy_gaps 
                (gap_id, policy_name, framework, severity, description, current_status,
                 required_actions, mitigation_strategies, estimated_effort, business_impact,
                 regulatory_impact, priority_score, due_date, assigned_owner, created_date, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                gap.gap_id,
                gap.policy_name,
                gap.framework.value,
                gap.severity.value,
                gap.description,
                gap.current_status.value,
                json.dumps(gap.required_actions),
                json.dumps(gap.mitigation_strategies),
                gap.estimated_effort,
                gap.business_impact,
                gap.regulatory_impact,
                gap.priority_score,
                gap.due_date.isoformat() if gap.due_date else None,
                gap.assigned_owner,
                gap.created_date.isoformat(),
                gap.last_updated.isoformat()
            ))
        
        conn.commit()
        conn.close()

    def get_gap_analysis_report(self, report_id: str) -> Optional[GapAnalysisReport]:
        """Retrieve a gap analysis report by ID"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM gap_analysis_reports WHERE report_id = ?
        ''', (report_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        # Get gaps for this report
        cursor.execute('''
            SELECT * FROM policy_gaps WHERE gap_id IN (
                SELECT gap_id FROM policy_gaps ORDER BY priority_score DESC
            )
        ''')
        
        gaps = []
        for gap_row in cursor.fetchall():
            gap = PolicyGap(
                gap_id=gap_row[0],
                policy_name=gap_row[1],
                framework=ComplianceFramework(gap_row[2]),
                severity=GapSeverity(gap_row[3]),
                description=gap_row[4],
                current_status=PolicyStatus(gap_row[5]),
                required_actions=json.loads(gap_row[6]) if gap_row[6] else [],
                mitigation_strategies=json.loads(gap_row[7]) if gap_row[7] else [],
                estimated_effort=gap_row[8],
                business_impact=gap_row[9],
                regulatory_impact=gap_row[10],
                priority_score=gap_row[11],
                due_date=datetime.fromisoformat(gap_row[12]) if gap_row[12] else None,
                assigned_owner=gap_row[13],
                created_date=datetime.fromisoformat(gap_row[14]),
                last_updated=datetime.fromisoformat(gap_row[15])
            )
            gaps.append(gap)
        
        conn.close()
        
        # Reconstruct report
        report = GapAnalysisReport(
            report_id=row[0],
            organization_name=row[1],
            analysis_date=datetime.fromisoformat(row[2]),
            total_policies=row[3],
            implemented_policies=row[4],
            partial_policies=row[5],
            missing_policies=row[6],
            outdated_policies=row[7],
            compliance_score=row[8],
            critical_gaps=row[9],
            high_priority_gaps=row[10],
            medium_priority_gaps=row[11],
            low_priority_gaps=row[12],
            gaps=gaps,
            recommendations=json.loads(row[13]) if row[13] else [],
            next_review_date=datetime.fromisoformat(row[14]),
            executive_summary=row[15]
        )
        
        return report

    def get_all_gap_analysis_reports(self) -> List[Dict[str, Any]]:
        """Get all gap analysis reports"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT report_id, organization_name, analysis_date, compliance_score,
                   critical_gaps, high_priority_gaps, medium_priority_gaps, low_priority_gaps
            FROM gap_analysis_reports
            ORDER BY analysis_date DESC
        ''')
        
        reports = []
        for row in cursor.fetchall():
            reports.append({
                "report_id": row[0],
                "organization_name": row[1],
                "analysis_date": row[2],
                "compliance_score": row[3],
                "critical_gaps": row[4],
                "high_priority_gaps": row[5],
                "medium_priority_gaps": row[6],
                "low_priority_gaps": row[7]
            })
        
        conn.close()
        return reports

# Example usage and testing
async def main():
    """Example usage of the BFSI Gap Analysis Service"""
    
    # Initialize service
    gap_service = BFSIGapAnalysisService()
    
    # Perform gap analysis
    print("🔍 Starting BFSI Gap Analysis...")
    
    report = await gap_service.perform_comprehensive_gap_analysis(
        organization_name="Sample Financial Institution"
    )
    
    print(f"\n📊 Gap Analysis Results:")
    print(f"Organization: {report.organization_name}")
    print(f"Compliance Score: {report.compliance_score:.1f}%")
    print(f"Total Gaps: {len(report.gaps)}")
    print(f"Critical Gaps: {report.critical_gaps}")
    print(f"High Priority Gaps: {report.high_priority_gaps}")
    
    print(f"\n📋 Executive Summary:")
    print(report.executive_summary)
    
    print(f"\n🎯 Top Priority Gaps:")
    for i, gap in enumerate(report.gaps[:5], 1):
        print(f"{i}. {gap.policy_name} ({gap.severity.value}) - {gap.description}")
    
    print(f"\n✅ Gap Analysis Complete!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

