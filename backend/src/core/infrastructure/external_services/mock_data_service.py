#!/usr/bin/env python3
"""
Mock Data Service for BFSI GRC Platform
Provides sample data without requiring database connection
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class MockDataService:
    """Mock data service for BFSI GRC platform"""
    
    def __init__(self):
        self.organization_id = "org-123"
        self.sample_data = self._generate_sample_data()
    
    def _generate_sample_data(self) -> Dict[str, Any]:
        """Generate comprehensive BFSI sample data"""
        return {
            "policies": [
                {
                    "id": "POL-BFSI-001",
                    "title": "Basel III Capital Requirements Policy",
                    "description": "Comprehensive policy for Basel III capital adequacy, leverage ratio, and liquidity requirements for BFSI operations",
                    "category": "Capital Management",
                    "status": "Active",
                    "version": "2.1",
                    "effective_date": "2024-01-01",
                    "review_date": "2024-12-31",
                    "owner_id": "user-001",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "POL-BFSI-002",
                    "title": "KYC Customer Due Diligence Policy",
                    "description": "Know Your Customer procedures for customer onboarding and ongoing monitoring",
                    "category": "Compliance",
                    "status": "Active",
                    "version": "3.0",
                    "effective_date": "2024-01-15",
                    "review_date": "2024-12-31",
                    "owner_id": "user-002",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "POL-BFSI-003",
                    "title": "Credit Risk Management Policy",
                    "description": "Framework for credit risk assessment, monitoring, and mitigation in BFSI lending operations",
                    "category": "Risk Management",
                    "status": "Active",
                    "version": "1.8",
                    "effective_date": "2024-02-01",
                    "review_date": "2024-12-31",
                    "owner_id": "user-003",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "POL-BFSI-004",
                    "title": "Operational Risk Management Policy",
                    "description": "Guidelines for identifying, assessing, and managing operational risks in banking operations",
                    "category": "Risk Management",
                    "status": "Active",
                    "version": "2.2",
                    "effective_date": "2024-01-20",
                    "review_date": "2024-12-31",
                    "owner_id": "user-004",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "POL-BFSI-005",
                    "title": "Regulatory Reporting Policy",
                    "description": "Procedures for regulatory reporting and compliance documentation",
                    "category": "Compliance",
                    "status": "Active",
                    "version": "1.5",
                    "effective_date": "2024-01-10",
                    "review_date": "2024-12-31",
                    "owner_id": "user-005",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ],
            "risks": [
                {
                    "id": "RISK-BFSI-001",
                    "title": "Basel III Non-Compliance Risk",
                    "description": "Risk of failing to meet Basel III capital adequacy requirements leading to regulatory penalties",
                    "category": "Compliance Risk",
                    "risk_level": "High",
                    "probability": 0.3,
                    "impact": 0.9,
                    "status": "Active",
                    "owner_id": "user-001",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "RISK-BFSI-002",
                    "title": "Credit Portfolio Concentration Risk",
                    "description": "High concentration of credit exposure in technology sector increasing portfolio vulnerability",
                    "category": "Credit Risk",
                    "risk_level": "Medium",
                    "probability": 0.6,
                    "impact": 0.7,
                    "status": "Active",
                    "owner_id": "user-003",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "RISK-BFSI-003",
                    "title": "KYC Compliance Risk",
                    "description": "Risk of failing to meet Know Your Customer requirements leading to regulatory sanctions",
                    "category": "Compliance Risk",
                    "risk_level": "Medium",
                    "probability": 0.4,
                    "impact": 0.6,
                    "status": "Active",
                    "owner_id": "user-002",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "RISK-BFSI-004",
                    "title": "Liquidity Shortfall Risk",
                    "description": "Insufficient liquid assets to meet short-term obligations during stress scenarios",
                    "category": "Liquidity Risk",
                    "risk_level": "Medium",
                    "probability": 0.5,
                    "impact": 0.6,
                    "status": "Active",
                    "owner_id": "user-004",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "RISK-BFSI-005",
                    "title": "Cybersecurity Breach Risk",
                    "description": "Risk of cyber attacks compromising customer data and banking systems",
                    "category": "Operational Risk",
                    "risk_level": "High",
                    "probability": 0.7,
                    "impact": 0.8,
                    "status": "Active",
                    "owner_id": "user-006",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ],
            "compliance_assessments": [
                {
                    "id": "COMP-BFSI-001",
                    "title": "Basel III Capital Adequacy Assessment",
                    "description": "Comprehensive assessment of capital adequacy ratios and Basel III compliance",
                    "framework": "Basel III",
                    "status": "In Progress",
                    "score": 7.2,
                    "target_score": 9.0,
                    "assessor_id": "user-001",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "COMP-BFSI-002",
                    "title": "KYC Program Assessment",
                    "description": "Evaluation of Know Your Customer program effectiveness",
                    "framework": "KYC",
                    "status": "Completed",
                    "score": 8.5,
                    "target_score": 9.0,
                    "assessor_id": "user-002",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "COMP-BFSI-003",
                    "title": "Credit Risk Management Assessment",
                    "description": "Assessment of credit risk management framework and processes",
                    "framework": "Basel III",
                    "status": "In Progress",
                    "score": 6.8,
                    "target_score": 8.5,
                    "assessor_id": "user-003",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ],
            "workflows": [
                {
                    "id": "WF-BFSI-001",
                    "name": "Basel III Capital Planning Workflow",
                    "description": "Annual capital planning and stress testing workflow for Basel III compliance",
                    "status": "Active",
                    "priority": "High",
                    "assignee_id": "user-001",
                    "due_date": "2024-12-31",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "WF-BFSI-002",
                    "name": "Customer Onboarding KYC Workflow",
                    "description": "Customer due diligence workflow for customer onboarding",
                    "status": "Active",
                    "priority": "High",
                    "assignee_id": "user-002",
                    "due_date": "2024-10-15",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "WF-BFSI-003",
                    "name": "Credit Risk Review Workflow",
                    "description": "Quarterly credit portfolio review and risk assessment workflow",
                    "status": "Active",
                    "priority": "Medium",
                    "assignee_id": "user-003",
                    "due_date": "2024-09-30",
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ],
            "ai_agents": [
                {
                    "id": "AGENT-BFSI-001",
                    "agent_name": "BFSI Compliance Agent",
                    "agent_type": "Compliance",
                    "industry": "BFSI",
                    "status": "Active",
                    "last_activity": datetime.now().isoformat(),
                    "performance_score": 0.94,
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "AGENT-BFSI-002",
                    "agent_name": "BFSI Risk Assessment Agent",
                    "agent_type": "Risk",
                    "industry": "BFSI",
                    "status": "Active",
                    "last_activity": datetime.now().isoformat(),
                    "performance_score": 0.91,
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "AGENT-BFSI-003",
                    "agent_name": "BFSI Regulatory Reporting Agent",
                    "agent_type": "Reporting",
                    "industry": "BFSI",
                    "status": "Active",
                    "last_activity": datetime.now().isoformat(),
                    "performance_score": 0.87,
                    "organization_id": self.organization_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ]
        }
    
    def get_policies(self) -> List[Dict[str, Any]]:
        """Get all policies"""
        return self.sample_data["policies"]
    
    def get_risks(self) -> List[Dict[str, Any]]:
        """Get all risks"""
        return self.sample_data["risks"]
    
    def get_compliance_assessments(self) -> List[Dict[str, Any]]:
        """Get all compliance assessments"""
        return self.sample_data["compliance_assessments"]
    
    def get_workflows(self) -> List[Dict[str, Any]]:
        """Get all workflows"""
        return self.sample_data["workflows"]
    
    def get_ai_agents(self) -> List[Dict[str, Any]]:
        """Get all AI agents"""
        return self.sample_data["ai_agents"]
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary statistics"""
        return {
            "total_policies": len(self.sample_data["policies"]),
            "total_risks": len(self.sample_data["risks"]),
            "total_compliance_assessments": len(self.sample_data["compliance_assessments"]),
            "total_workflows": len(self.sample_data["workflows"]),
            "total_ai_agents": len(self.sample_data["ai_agents"]),
            "active_policies": len([p for p in self.sample_data["policies"] if p["status"] == "Active"]),
            "high_risks": len([r for r in self.sample_data["risks"] if r["risk_level"] == "High"]),
            "completed_assessments": len([a for a in self.sample_data["compliance_assessments"] if a["status"] == "Completed"]),
            "active_workflows": len([w for w in self.sample_data["workflows"] if w["status"] == "Active"]),
            "active_agents": len([a for a in self.sample_data["ai_agents"] if a["status"] == "Active"]),
            "organization_id": self.organization_id,
            "last_updated": datetime.now().isoformat()
        }

# Global instance
mock_data_service = MockDataService()
