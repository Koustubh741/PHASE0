#!/usr/bin/env python3
"""
Real Data API Testing Suite for GRC Platform
Tests all APIs with real BFSI data scenarios instead of mock data
"""

import os
import sys
import asyncio
import aiohttp
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealDataAPITester:
    def __init__(self):
        self.base_url = "http://localhost:3001"
        self.ai_agents_url = "http://localhost:8000"
        self.session = None
        self.auth_token = None
        self.user_id = None
        self.organization_id = "org-123"
        
        # Database configuration
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'grc_platform'),
            'user': os.getenv('DB_USER', 'grc_user'),
            'password': os.getenv('DB_PASSWORD', 'grc_password')
        }
        
        self.test_results = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def get_real_data_from_db(self, table: str, filters: Dict = None):
        """Get real data from database for testing"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = f"SELECT * FROM {table}"
            params = []
            
            if filters:
                where_clauses = []
                for key, value in filters.items():
                    where_clauses.append(f"{key} = %s")
                    params.append(value)
                query += " WHERE " + " AND ".join(where_clauses)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"Error getting data from {table}: {e}")
            return []
    
    async def test_authentication_apis(self):
        """Test authentication APIs with real user data"""
        logger.info("🔐 Testing Authentication APIs with Real User Data")
        
        # Get real users from database
        real_users = self.get_real_data_from_db("users", {"organization_id": self.organization_id})
        
        if not real_users:
            logger.error("❌ No real users found in database")
            return False
        
        test_user = real_users[0]
        login_data = {
            "email": test_user["email"],
            "password": "password123"  # Default test password
        }
        
        try:
            # Test login
            async with self.session.post(f"{self.base_url}/api/auth/login", 
                                       json=login_data) as response:
                if response.status == 200:
                    login_result = await response.json()
                    self.auth_token = login_result.get("data", {}).get("token")
                    self.user_id = login_result.get("data", {}).get("user", {}).get("id")
                    
                    logger.info(f"✅ Login successful for real user: {test_user['email']}")
                    logger.info(f"   User ID: {self.user_id}")
                    logger.info(f"   Role: {test_user['role']}")
                    
                    return True
                else:
                    logger.error(f"❌ Login failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Authentication API error: {e}")
            return False
    
    async def test_risk_apis_with_real_data(self):
        """Test risk APIs with real BFSI risk data"""
        logger.info("⚠️ Testing Risk APIs with Real BFSI Data")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get real risks from database
        real_risks = self.get_real_data_from_db("risks", {"organization_id": self.organization_id})
        
        if not real_risks:
            logger.error("❌ No real risks found in database")
            return False
        
        test_results = []
        
        try:
            # Test 1: Get all risks
            async with self.session.get(f"{self.base_url}/api/risks", headers=headers) as response:
                if response.status == 200:
                    risks_result = await response.json()
                    logger.info(f"✅ Get all risks: {len(risks_result.get('data', []))} risks retrieved")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get all risks failed: {response.status}")
                    test_results.append(False)
            
            # Test 2: Get specific risk by ID
            test_risk = real_risks[0]
            async with self.session.get(f"{self.base_url}/api/risks/{test_risk['id']}", 
                                      headers=headers) as response:
                if response.status == 200:
                    risk_result = await response.json()
                    logger.info(f"✅ Get risk by ID: {test_risk['title']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get risk by ID failed: {response.status}")
                    test_results.append(False)
            
            # Test 3: Update risk with real scenario
            update_data = {
                "status": "mitigated",
                "mitigation_plan": "Enhanced monitoring and additional controls implemented",
                "last_reviewed": datetime.now().isoformat()
            }
            
            async with self.session.put(f"{self.base_url}/api/risks/{test_risk['id']}", 
                                      json=update_data, headers=headers) as response:
                if response.status == 200:
                    update_result = await response.json()
                    logger.info(f"✅ Update risk: {test_risk['title']} status updated")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Update risk failed: {response.status}")
                    test_results.append(False)
            
            # Test 4: Create new risk with real BFSI scenario
            new_risk_data = {
                "title": "Interest Rate Risk - Rising Rate Environment",
                "description": "Exposure to rising interest rates affecting net interest margin and bond portfolio valuation",
                "category": "Market Risk",
                "risk_level": "Medium",
                "probability": 0.7,
                "impact": 0.6,
                "mitigation_plan": "Implement interest rate hedging strategies and duration management",
                "owner_id": self.user_id,
                "organization_id": self.organization_id
            }
            
            async with self.session.post(f"{self.base_url}/api/risks", 
                                       json=new_risk_data, headers=headers) as response:
                if response.status == 201:
                    new_risk_result = await response.json()
                    logger.info(f"✅ Create new risk: {new_risk_data['title']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Create new risk failed: {response.status}")
                    test_results.append(False)
            
            # Test 5: Risk statistics
            async with self.session.get(f"{self.base_url}/api/risks/stats", headers=headers) as response:
                if response.status == 200:
                    stats_result = await response.json()
                    logger.info(f"✅ Risk statistics: {stats_result.get('data', {})}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Risk statistics failed: {response.status}")
                    test_results.append(False)
            
            return all(test_results)
            
        except Exception as e:
            logger.error(f"❌ Risk APIs error: {e}")
            return False
    
    async def test_compliance_apis_with_real_data(self):
        """Test compliance APIs with real BFSI compliance data"""
        logger.info("✅ Testing Compliance APIs with Real BFSI Data")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get real compliance assessments from database
        real_compliance = self.get_real_data_from_db("compliance_assessments", 
                                                   {"organization_id": self.organization_id})
        
        if not real_compliance:
            logger.error("❌ No real compliance assessments found in database")
            return False
        
        test_results = []
        
        try:
            # Test 1: Get all compliance assessments
            async with self.session.get(f"{self.base_url}/api/compliance", headers=headers) as response:
                if response.status == 200:
                    compliance_result = await response.json()
                    logger.info(f"✅ Get all compliance: {len(compliance_result.get('data', []))} assessments retrieved")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get all compliance failed: {response.status}")
                    test_results.append(False)
            
            # Test 2: Get specific compliance assessment
            test_compliance = real_compliance[0]
            async with self.session.get(f"{self.base_url}/api/compliance/{test_compliance['id']}", 
                                      headers=headers) as response:
                if response.status == 200:
                    comp_result = await response.json()
                    logger.info(f"✅ Get compliance by ID: {test_compliance['title']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get compliance by ID failed: {response.status}")
                    test_results.append(False)
            
            # Test 3: Update compliance assessment
            update_data = {
                "score": 8.5,
                "status": "completed",
                "completion_date": datetime.now().isoformat(),
                "notes": "Assessment completed with satisfactory results"
            }
            
            async with self.session.put(f"{self.base_url}/api/compliance/{test_compliance['id']}", 
                                      json=update_data, headers=headers) as response:
                if response.status == 200:
                    update_result = await response.json()
                    logger.info(f"✅ Update compliance: {test_compliance['title']} updated")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Update compliance failed: {response.status}")
                    test_results.append(False)
            
            # Test 4: Create new Basel III compliance assessment
            new_compliance_data = {
                "title": "Basel III Capital Adequacy Assessment Q1 2025",
                "description": "Quarterly assessment of capital adequacy ratios and Basel III compliance",
                "framework": "Basel III",
                "requirements": [
                    "Tier 1 Capital Ratio ≥ 6%",
                    "Total Capital Ratio ≥ 8%",
                    "Leverage Ratio ≥ 3%",
                    "LCR ≥ 100%",
                    "NSFR ≥ 100%"
                ],
                "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "assessor_id": self.user_id,
                "organization_id": self.organization_id
            }
            
            async with self.session.post(f"{self.base_url}/api/compliance", 
                                       json=new_compliance_data, headers=headers) as response:
                if response.status == 201:
                    new_comp_result = await response.json()
                    logger.info(f"✅ Create new compliance: {new_compliance_data['title']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Create new compliance failed: {response.status}")
                    test_results.append(False)
            
            # Test 5: Compliance statistics
            async with self.session.get(f"{self.base_url}/api/compliance/stats", headers=headers) as response:
                if response.status == 200:
                    stats_result = await response.json()
                    logger.info(f"✅ Compliance statistics: {stats_result.get('data', {})}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Compliance statistics failed: {response.status}")
                    test_results.append(False)
            
            return all(test_results)
            
        except Exception as e:
            logger.error(f"❌ Compliance APIs error: {e}")
            return False
    
    async def test_policy_apis_with_real_data(self):
        """Test policy APIs with real BFSI policy data"""
        logger.info("📋 Testing Policy APIs with Real BFSI Data")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get real policies from database
        real_policies = self.get_real_data_from_db("policies", {"organization_id": self.organization_id})
        
        if not real_policies:
            logger.error("❌ No real policies found in database")
            return False
        
        test_results = []
        
        try:
            # Test 1: Get all policies
            async with self.session.get(f"{self.base_url}/api/policies", headers=headers) as response:
                if response.status == 200:
                    policies_result = await response.json()
                    logger.info(f"✅ Get all policies: {len(policies_result.get('data', []))} policies retrieved")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get all policies failed: {response.status}")
                    test_results.append(False)
            
            # Test 2: Get specific policy
            test_policy = real_policies[0]
            async with self.session.get(f"{self.base_url}/api/policies/{test_policy['id']}", 
                                      headers=headers) as response:
                if response.status == 200:
                    policy_result = await response.json()
                    logger.info(f"✅ Get policy by ID: {test_policy['title']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get policy by ID failed: {response.status}")
                    test_results.append(False)
            
            # Test 3: Update policy
            update_data = {
                "status": "under_review",
                "review_notes": "Policy under review for Basel III updates",
                "last_reviewed": datetime.now().isoformat()
            }
            
            async with self.session.put(f"{self.base_url}/api/policies/{test_policy['id']}", 
                                      json=update_data, headers=headers) as response:
                if response.status == 200:
                    update_result = await response.json()
                    logger.info(f"✅ Update policy: {test_policy['title']} updated")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Update policy failed: {response.status}")
                    test_results.append(False)
            
            # Test 4: Create new AML/KYC policy
            new_policy_data = {
                "title": "Enhanced AML/KYC Customer Due Diligence Policy 2024",
                "description": "Comprehensive policy for customer due diligence and anti-money laundering procedures",
                "category": "Compliance",
                "content": """
                This policy establishes enhanced due diligence procedures for customer onboarding and ongoing monitoring.
                
                Key Requirements:
                1. Customer identification and verification
                2. Risk-based customer categorization
                3. Enhanced due diligence for high-risk customers
                4. Ongoing monitoring and transaction screening
                5. Suspicious activity reporting procedures
                
                Regulatory Framework:
                - Bank Secrecy Act (BSA)
                - USA PATRIOT Act
                - FinCEN regulations
                - OFAC sanctions screening
                """,
                "owner_id": self.user_id,
                "organization_id": self.organization_id,
                "effective_date": datetime.now().isoformat(),
                "review_date": (datetime.now() + timedelta(days=365)).isoformat()
            }
            
            async with self.session.post(f"{self.base_url}/api/policies", 
                                       json=new_policy_data, headers=headers) as response:
                if response.status == 201:
                    new_policy_result = await response.json()
                    logger.info(f"✅ Create new policy: {new_policy_data['title']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Create new policy failed: {response.status}")
                    test_results.append(False)
            
            return all(test_results)
            
        except Exception as e:
            logger.error(f"❌ Policy APIs error: {e}")
            return False
    
    async def test_workflow_apis_with_real_data(self):
        """Test workflow APIs with real BFSI workflow data"""
        logger.info("⚙️ Testing Workflow APIs with Real BFSI Data")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get real workflows from database
        real_workflows = self.get_real_data_from_db("workflows", {"organization_id": self.organization_id})
        
        if not real_workflows:
            logger.error("❌ No real workflows found in database")
            return False
        
        test_results = []
        
        try:
            # Test 1: Get all workflows
            async with self.session.get(f"{self.base_url}/api/workflows", headers=headers) as response:
                if response.status == 200:
                    workflows_result = await response.json()
                    logger.info(f"✅ Get all workflows: {len(workflows_result.get('data', []))} workflows retrieved")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get all workflows failed: {response.status}")
                    test_results.append(False)
            
            # Test 2: Get specific workflow
            test_workflow = real_workflows[0]
            async with self.session.get(f"{self.base_url}/api/workflows/{test_workflow['id']}", 
                                      headers=headers) as response:
                if response.status == 200:
                    workflow_result = await response.json()
                    logger.info(f"✅ Get workflow by ID: {test_workflow['name']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Get workflow by ID failed: {response.status}")
                    test_results.append(False)
            
            # Test 3: Update workflow
            update_data = {
                "status": "in_progress",
                "progress": 75,
                "last_updated": datetime.now().isoformat()
            }
            
            async with self.session.put(f"{self.base_url}/api/workflows/{test_workflow['id']}", 
                                      json=update_data, headers=headers) as response:
                if response.status == 200:
                    update_result = await response.json()
                    logger.info(f"✅ Update workflow: {test_workflow['name']} updated")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Update workflow failed: {response.status}")
                    test_results.append(False)
            
            # Test 4: Create new regulatory reporting workflow
            new_workflow_data = {
                "name": "Quarterly Regulatory Reporting Workflow",
                "description": "Automated workflow for quarterly regulatory reporting preparation and submission",
                "steps": [
                    {
                        "step_name": "Data Collection",
                        "description": "Collect financial data and risk metrics",
                        "assignee_id": self.user_id,
                        "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
                        "priority": "high"
                    },
                    {
                        "step_name": "Report Preparation",
                        "description": "Prepare regulatory reports and validate data",
                        "assignee_id": self.user_id,
                        "due_date": (datetime.now() + timedelta(days=10)).isoformat(),
                        "priority": "high"
                    },
                    {
                        "step_name": "Review and Approval",
                        "description": "Management review and approval of reports",
                        "assignee_id": self.user_id,
                        "due_date": (datetime.now() + timedelta(days=15)).isoformat(),
                        "priority": "critical"
                    },
                    {
                        "step_name": "Submission",
                        "description": "Submit reports to regulatory authorities",
                        "assignee_id": self.user_id,
                        "due_date": (datetime.now() + timedelta(days=20)).isoformat(),
                        "priority": "critical"
                    }
                ],
                "organization_id": self.organization_id
            }
            
            async with self.session.post(f"{self.base_url}/api/workflows", 
                                       json=new_workflow_data, headers=headers) as response:
                if response.status == 201:
                    new_workflow_result = await response.json()
                    logger.info(f"✅ Create new workflow: {new_workflow_data['name']}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Create new workflow failed: {response.status}")
                    test_results.append(False)
            
            return all(test_results)
            
        except Exception as e:
            logger.error(f"❌ Workflow APIs error: {e}")
            return False
    
    async def test_ai_agent_apis_with_real_data(self):
        """Test AI agent APIs with real BFSI scenarios"""
        logger.info("🤖 Testing AI Agent APIs with Real BFSI Scenarios")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        test_results = []
        
        try:
            # Test 1: BFSI Risk Assessment
            risk_assessment_data = {
                "business_unit": "commercial_lending",
                "risk_scope": "credit",
                "portfolio_data": {
                    "total_exposure": 500000000,
                    "default_rate": 0.025,
                    "concentration_ratio": 0.35,
                    "geographic_spread": 0.6,
                    "sector_diversification": 0.4
                }
            }
            
            async with self.session.post(f"{self.ai_agents_url}/api/risk-assessment", 
                                       json=risk_assessment_data, headers=headers) as response:
                if response.status == 200:
                    risk_result = await response.json()
                    logger.info(f"✅ BFSI Risk Assessment: Score {risk_result.get('risk_score', 'N/A')}")
                    logger.info(f"   Recommendations: {len(risk_result.get('recommendations', []))}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ BFSI Risk Assessment failed: {response.status}")
                    test_results.append(False)
            
            # Test 2: Basel III Compliance Check
            compliance_check_data = {
                "framework": "Basel III",
                "business_unit": "capital_management",
                "current_ratios": {
                    "tier_1_capital_ratio": 12.5,
                    "total_capital_ratio": 15.2,
                    "leverage_ratio": 7.1,
                    "lcr": 125.0,
                    "nsfr": 110.0
                }
            }
            
            async with self.session.post(f"{self.ai_agents_url}/api/compliance-check", 
                                       json=compliance_check_data, headers=headers) as response:
                if response.status == 200:
                    comp_result = await response.json()
                    logger.info(f"✅ Basel III Compliance Check: Score {comp_result.get('compliance_score', 'N/A')}%")
                    logger.info(f"   Status: {comp_result.get('status', 'N/A')}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Basel III Compliance Check failed: {response.status}")
                    test_results.append(False)
            
            # Test 3: AML Transaction Monitoring
            aml_monitoring_data = {
                "transaction_data": {
                    "transaction_count": 15000,
                    "total_volume": 25000000,
                    "high_risk_countries": ["Country A", "Country B"],
                    "suspicious_patterns": ["round_amounts", "rapid_succession"]
                },
                "customer_data": {
                    "total_customers": 500,
                    "high_risk_customers": 25,
                    "pep_customers": 5,
                    "sanctions_matches": 0
                }
            }
            
            async with self.session.post(f"{self.ai_agents_url}/api/aml-monitoring", 
                                       json=aml_monitoring_data, headers=headers) as response:
                if response.status == 200:
                    aml_result = await response.json()
                    logger.info(f"✅ AML Monitoring: {aml_result.get('suspicious_transactions', 0)} suspicious transactions")
                    logger.info(f"   Risk Score: {aml_result.get('risk_score', 'N/A')}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ AML Monitoring failed: {response.status}")
                    test_results.append(False)
            
            # Test 4: Policy Analysis
            policy_analysis_data = {
                "policy_content": "Credit Risk Management Policy for Commercial Lending Operations",
                "analysis_type": "compliance_alignment",
                "frameworks": ["Basel III", "SOX", "FDIC"],
                "business_unit": "commercial_lending"
            }
            
            async with self.session.post(f"{self.ai_agents_url}/api/policy-analysis", 
                                       json=policy_analysis_data, headers=headers) as response:
                if response.status == 200:
                    policy_result = await response.json()
                    logger.info(f"✅ Policy Analysis: Alignment Score {policy_result.get('alignment_score', 'N/A')}%")
                    logger.info(f"   Gaps: {len(policy_result.get('gaps', []))}")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Policy Analysis failed: {response.status}")
                    test_results.append(False)
            
            return all(test_results)
            
        except Exception as e:
            logger.error(f"❌ AI Agent APIs error: {e}")
            return False
    
    async def test_dashboard_apis_with_real_data(self):
        """Test dashboard APIs with real aggregated data"""
        logger.info("📊 Testing Dashboard APIs with Real Aggregated Data")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        test_results = []
        
        try:
            # Test 1: Main dashboard
            async with self.session.get(f"{self.base_url}/api/dashboard", headers=headers) as response:
                if response.status == 200:
                    dashboard_result = await response.json()
                    logger.info("✅ Main dashboard data retrieved")
                    
                    # Verify dashboard components
                    data = dashboard_result.get('data', {})
                    logger.info(f"   Policies: {data.get('policies', {}).get('total_policies', 0)}")
                    logger.info(f"   Risks: {data.get('risks', {}).get('total_risks', 0)}")
                    logger.info(f"   Compliance Score: {data.get('compliance', {}).get('average_compliance_score', 0)}%")
                    logger.info(f"   Workflows: {data.get('workflows', {}).get('total_workflows', 0)}")
                    
                    test_results.append(True)
                else:
                    logger.error(f"❌ Main dashboard failed: {response.status}")
                    test_results.append(False)
            
            # Test 2: Risk dashboard
            async with self.session.get(f"{self.base_url}/api/dashboard/risks", headers=headers) as response:
                if response.status == 200:
                    risk_dashboard = await response.json()
                    logger.info("✅ Risk dashboard data retrieved")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Risk dashboard failed: {response.status}")
                    test_results.append(False)
            
            # Test 3: Compliance dashboard
            async with self.session.get(f"{self.base_url}/api/dashboard/compliance", headers=headers) as response:
                if response.status == 200:
                    comp_dashboard = await response.json()
                    logger.info("✅ Compliance dashboard data retrieved")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Compliance dashboard failed: {response.status}")
                    test_results.append(False)
            
            # Test 4: Analytics dashboard
            async with self.session.get(f"{self.base_url}/api/dashboard/analytics", headers=headers) as response:
                if response.status == 200:
                    analytics_dashboard = await response.json()
                    logger.info("✅ Analytics dashboard data retrieved")
                    test_results.append(True)
                else:
                    logger.error(f"❌ Analytics dashboard failed: {response.status}")
                    test_results.append(False)
            
            return all(test_results)
            
        except Exception as e:
            logger.error(f"❌ Dashboard APIs error: {e}")
            return False
    
    async def run_complete_api_test_suite(self):
        """Run the complete API test suite with real data"""
        logger.info("🧪 Starting Complete API Test Suite with Real Data")
        logger.info("=" * 80)
        
        test_suites = [
            ("Authentication APIs", self.test_authentication_apis),
            ("Risk APIs", self.test_risk_apis_with_real_data),
            ("Compliance APIs", self.test_compliance_apis_with_real_data),
            ("Policy APIs", self.test_policy_apis_with_real_data),
            ("Workflow APIs", self.test_workflow_apis_with_real_data),
            ("AI Agent APIs", self.test_ai_agent_apis_with_real_data),
            ("Dashboard APIs", self.test_dashboard_apis_with_real_data)
        ]
        
        for suite_name, suite_function in test_suites:
            logger.info(f"\n📋 Testing {suite_name}...")
            try:
                result = await suite_function()
                self.test_results[suite_name] = result
                if result:
                    logger.info(f"✅ {suite_name} completed successfully")
                else:
                    logger.error(f"❌ {suite_name} failed")
            except Exception as e:
                logger.error(f"❌ {suite_name} failed with error: {e}")
                self.test_results[suite_name] = False
        
        # Print test summary
        logger.info("\n" + "=" * 80)
        logger.info("📊 API Test Suite Results Summary")
        logger.info("=" * 80)
        
        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        logger.info(f"\n🎯 Test Results:")
        for suite_name, result in self.test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"   {suite_name}: {status}")
        
        logger.info(f"\n🏆 Overall Success Rate: {passed}/{total} test suites passed ({success_rate:.1f}%)")
        
        if success_rate >= 90:
            logger.info("🎉 Excellent! All APIs are working perfectly with real data!")
        elif success_rate >= 75:
            logger.info("✅ Good performance! Most APIs are working well.")
        elif success_rate >= 50:
            logger.info("⚠️ Some issues detected. Several APIs need attention.")
        else:
            logger.info("🚨 Significant issues detected. Major API problems need to be resolved.")
        
        return success_rate >= 75

async def main():
    """Main function to run complete API test suite"""
    logger.info("🧪 GRC Platform - Real Data API Testing Suite")
    logger.info("=" * 80)
    logger.info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async with RealDataAPITester() as tester:
        success = await tester.run_complete_api_test_suite()
    
    if success:
        logger.info("\n🎯 Next Steps:")
        logger.info("   1. Run end-to-end user journey tests")
        logger.info("   2. Run performance and load tests")
        logger.info("   3. Test with different user roles")
        logger.info("   4. Validate AI agent responses")
        sys.exit(0)
    else:
        logger.error("\n❌ API testing failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
