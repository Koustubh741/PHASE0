#!/usr/bin/env python3
"""
Real Bank Employee End-to-End Journey Test
Simulates a complete bank employee workflow through the GRC platform
Following the system architecture diagram from frontend to AI agents
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

class RealBankEmployeeTester:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'http://localhost:3001')
        self.frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        self.ai_agents_url = os.getenv('AI_AGENTS_URL', 'http://localhost:8000')
        self.session = None
        self.auth_token = None
        self.user_id = None
        self.organization_id = "org-123"
        
        # Test data
        self.test_scenarios = {
            "cfo": {
                "email": "cfo@testbank.com",
                "role": "Chief Risk Officer",
                "workflows": ["executive_dashboard", "risk_oversight", "compliance_reporting"]
            },
            "compliance_manager": {
                "email": "compliance@testbank.com", 
                "role": "Compliance Manager",
                "workflows": ["compliance_monitoring", "policy_management", "audit_preparation"]
            },
            "risk_analyst": {
                "email": "risk@testbank.com",
                "role": "Risk Analyst", 
                "workflows": ["risk_assessment", "portfolio_analysis", "stress_testing"]
            },
            "operations_manager": {
                "email": "ops@testbank.com",
                "role": "Operations Manager",
                "workflows": ["workflow_management", "task_assignment", "process_optimization"]
            }
        }
        
        self.test_results = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_system_health(self):
        """Test 1: System Health Check - All Services"""
        logger.info("🏥 Testing System Health - All Services")
        
        health_checks = {
            "Backend API": f"{self.base_url}/health",
            "Frontend": f"{self.frontend_url}",
            "AI Agents": f"{self.ai_agents_url}/health"
        }
        
        results = {}
        for service, url in health_checks.items():
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        results[service] = True
                        logger.info(f"  ✅ {service}: Healthy")
                    else:
                        results[service] = False
                        logger.warning(f"  ❌ {service}: Unhealthy (Status: {response.status})")
            except Exception as e:
                results[service] = False
                logger.error(f"  ❌ {service}: Connection failed - {e}")
        
        self.test_results["system_health"] = all(results.values())
        return all(results.values())
    
    async def test_user_authentication(self, user_type: str):
        """Test 2: User Authentication Flow"""
        logger.info(f"🔐 Testing User Authentication - {user_type.title()}")
        
        user_data = self.test_scenarios[user_type]
        
        # Step 1: Login
        login_data = {
            "email": user_data["email"],
            "password": "password123"  # Default test password
        }
        
        try:
            async with self.session.post(f"{self.base_url}/api/auth/login", 
                                       json=login_data) as response:
                if response.status == 200:
                    login_result = await response.json()
                    self.auth_token = login_result.get("data", {}).get("token")
                    self.user_id = login_result.get("data", {}).get("user", {}).get("id")
                    
                    logger.info(f"  ✅ Login successful for {user_data['role']}")
                    logger.info(f"     User ID: {self.user_id}")
                    logger.info(f"     Token received: {'Yes' if self.auth_token else 'No'}")
                    
                    return True
                else:
                    logger.error(f"  ❌ Login failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Authentication error: {e}")
            return False
    
    async def test_dashboard_access(self):
        """Test 3: Dashboard Access and Data Loading"""
        logger.info("📊 Testing Dashboard Access and Data Loading")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        try:
            # Test dashboard endpoint
            async with self.session.get(f"{self.base_url}/api/dashboard", 
                                      headers=headers) as response:
                if response.status == 200:
                    dashboard_data = await response.json()
                    
                    # Verify dashboard components
                    required_components = ["policies", "risks", "compliance", "workflows", "ai_agents"]
                    missing_components = []
                    
                    for component in required_components:
                        if component not in dashboard_data.get("data", {}):
                            missing_components.append(component)
                    
                    if not missing_components:
                        logger.info("  ✅ Dashboard data loaded successfully")
                        logger.info(f"     Policies: {dashboard_data['data']['policies'].get('total_policies', 0)}")
                        logger.info(f"     Risks: {dashboard_data['data']['risks'].get('total_risks', 0)}")
                        logger.info(f"     Compliance Score: {dashboard_data['data']['compliance'].get('average_compliance_score', 0)}%")
                        logger.info(f"     Workflows: {dashboard_data['data']['workflows'].get('total_workflows', 0)}")
                        
                        return True
                    else:
                        logger.error(f"  ❌ Missing dashboard components: {missing_components}")
                        return False
                else:
                    logger.error(f"  ❌ Dashboard access failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Dashboard error: {e}")
            return False
    
    async def test_risk_management_workflow(self):
        """Test 4: Risk Management Workflow - Real Bank Scenario"""
        logger.info("⚠️ Testing Risk Management Workflow - Real Bank Scenario")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Step 1: Create a real bank risk scenario
        risk_scenario = {
            "title": "Commercial Real Estate Portfolio Concentration Risk",
            "description": "High concentration in commercial real estate loans (35% of total portfolio) with potential for significant losses in economic downturn",
            "category": "Credit Risk",
            "risk_level": "High",
            "probability": 0.4,
            "impact": 0.8,
            "mitigation_plan": "Diversify portfolio, increase capital reserves, implement stress testing",
            "owner_id": self.user_id,
            "organization_id": self.organization_id
        }
        
        try:
            # Create risk
            async with self.session.post(f"{self.base_url}/api/risks", 
                                       json=risk_scenario, headers=headers) as response:
                if response.status == 201:
                    risk_result = await response.json()
                    risk_id = risk_result["data"]["id"]
                    logger.info(f"  ✅ Risk created successfully: {risk_id}")
                    
                    # Step 2: Test risk assessment with AI agents
                    assessment_data = {
                        "risk_id": risk_id,
                        "assessment_type": "credit_risk",
                        "business_unit": "commercial_lending",
                        "portfolio_data": {
                            "total_exposure": 500000000,
                            "cre_exposure": 175000000,
                            "concentration_ratio": 0.35,
                            "average_ltv": 0.75,
                            "geographic_concentration": 0.6
                        }
                    }
                    
                    # Call AI agent for risk assessment
                    async with self.session.post(f"{self.ai_agents_url}/api/risk-assessment", 
                                               json=assessment_data, headers=headers) as ai_response:
                        if ai_response.status == 200:
                            ai_result = await ai_response.json()
                            logger.info("  ✅ AI Risk Assessment completed")
                            logger.info(f"     Risk Score: {ai_result.get('risk_score', 'N/A')}")
                            logger.info(f"     Recommendations: {len(ai_result.get('recommendations', []))}")
                            
                            # Step 3: Update risk with AI assessment
                            update_data = {
                                "risk_score": ai_result.get('risk_score', 75),
                                "ai_recommendations": ai_result.get('recommendations', []),
                                "status": "assessed"
                            }
                            
                            async with self.session.put(f"{self.base_url}/api/risks/{risk_id}", 
                                                      json=update_data, headers=headers) as update_response:
                                if update_response.status == 200:
                                    logger.info("  ✅ Risk updated with AI assessment")
                                    return True
                                else:
                                    logger.error(f"  ❌ Risk update failed: {update_response.status}")
                                    return False
                        else:
                            logger.error(f"  ❌ AI Risk Assessment failed: {ai_response.status}")
                            return False
                else:
                    logger.error(f"  ❌ Risk creation failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Risk management workflow error: {e}")
            return False
    
    async def test_compliance_monitoring_workflow(self):
        """Test 5: Compliance Monitoring Workflow - Basel III Scenario"""
        logger.info("✅ Testing Compliance Monitoring Workflow - Basel III Scenario")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Step 1: Create Basel III compliance assessment
        compliance_scenario = {
            "title": "Basel III Capital Adequacy Assessment Q4 2024",
            "description": "Quarterly assessment of capital adequacy ratios and Basel III compliance requirements",
            "framework": "Basel III",
            "requirements": [
                "Tier 1 Capital Ratio ≥ 6%",
                "Total Capital Ratio ≥ 8%", 
                "Leverage Ratio ≥ 3%",
                "LCR ≥ 100%",
                "NSFR ≥ 100%"
            ],
            "due_date": (datetime.now() + timedelta(days=15)).isoformat(),
            "assessor_id": self.user_id,
            "organization_id": self.organization_id
        }
        
        try:
            # Create compliance assessment
            async with self.session.post(f"{self.base_url}/api/compliance", 
                                       json=compliance_scenario, headers=headers) as response:
                if response.status == 201:
                    compliance_result = await response.json()
                    compliance_id = compliance_result["data"]["id"]
                    logger.info(f"  ✅ Compliance assessment created: {compliance_id}")
                    
                    # Step 2: Test compliance checking with AI agents
                    compliance_data = {
                        "compliance_id": compliance_id,
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
                    
                    # Call AI agent for compliance check
                    async with self.session.post(f"{self.ai_agents_url}/api/compliance-check", 
                                               json=compliance_data, headers=headers) as ai_response:
                        if ai_response.status == 200:
                            ai_result = await ai_response.json()
                            logger.info("  ✅ AI Compliance Check completed")
                            logger.info(f"     Compliance Score: {ai_result.get('compliance_score', 'N/A')}%")
                            logger.info(f"     Status: {ai_result.get('status', 'N/A')}")
                            
                            # Step 3: Update compliance with AI results
                            update_data = {
                                "score": ai_result.get('compliance_score', 85),
                                "status": ai_result.get('status', 'compliant'),
                                "ai_analysis": ai_result.get('analysis', {}),
                                "recommendations": ai_result.get('recommendations', [])
                            }
                            
                            async with self.session.put(f"{self.base_url}/api/compliance/{compliance_id}", 
                                                      json=update_data, headers=headers) as update_response:
                                if update_response.status == 200:
                                    logger.info("  ✅ Compliance updated with AI analysis")
                                    return True
                                else:
                                    logger.error(f"  ❌ Compliance update failed: {update_response.status}")
                                    return False
                        else:
                            logger.error(f"  ❌ AI Compliance Check failed: {ai_response.status}")
                            return False
                else:
                    logger.error(f"  ❌ Compliance creation failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Compliance monitoring workflow error: {e}")
            return False
    
    async def test_policy_management_workflow(self):
        """Test 6: Policy Management Workflow - Real Bank Policy"""
        logger.info("📋 Testing Policy Management Workflow - Real Bank Policy")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Step 1: Create a real bank policy
        policy_scenario = {
            "title": "Credit Risk Management Policy 2024",
            "description": "Comprehensive policy for credit risk assessment, monitoring, and mitigation in commercial lending operations",
            "category": "Risk Management",
            "content": """
            This policy establishes the framework for credit risk management in our commercial lending operations.
            
            Key Requirements:
            1. Credit limits based on borrower financial strength
            2. Regular portfolio monitoring and stress testing
            3. Diversification requirements by sector and geography
            4. Collateral valuation and monitoring procedures
            5. Early warning indicators and escalation procedures
            
            Compliance Requirements:
            - Basel III credit risk framework
            - SOX internal controls
            - Regulatory reporting requirements
            """,
            "owner_id": self.user_id,
            "organization_id": self.organization_id,
            "effective_date": datetime.now().isoformat(),
            "review_date": (datetime.now() + timedelta(days=365)).isoformat()
        }
        
        try:
            # Create policy
            async with self.session.post(f"{self.base_url}/api/policies", 
                                       json=policy_scenario, headers=headers) as response:
                if response.status == 201:
                    policy_result = await response.json()
                    policy_id = policy_result["data"]["id"]
                    logger.info(f"  ✅ Policy created successfully: {policy_id}")
                    
                    # Step 2: Test policy analysis with AI agents
                    analysis_data = {
                        "policy_id": policy_id,
                        "analysis_type": "compliance_alignment",
                        "frameworks": ["Basel III", "SOX", "FDIC"],
                        "business_unit": "commercial_lending"
                    }
                    
                    # Call AI agent for policy analysis
                    async with self.session.post(f"{self.ai_agents_url}/api/policy-analysis", 
                                               json=analysis_data, headers=headers) as ai_response:
                        if ai_response.status == 200:
                            ai_result = await ai_response.json()
                            logger.info("  ✅ AI Policy Analysis completed")
                            logger.info(f"     Alignment Score: {ai_result.get('alignment_score', 'N/A')}%")
                            logger.info(f"     Compliance Gaps: {len(ai_result.get('gaps', []))}")
                            
                            # Step 3: Update policy with AI analysis
                            update_data = {
                                "alignment_score": ai_result.get('alignment_score', 85),
                                "compliance_gaps": ai_result.get('gaps', []),
                                "recommendations": ai_result.get('recommendations', []),
                                "status": "analyzed"
                            }
                            
                            async with self.session.put(f"{self.base_url}/api/policies/{policy_id}", 
                                                      json=update_data, headers=headers) as update_response:
                                if update_response.status == 200:
                                    logger.info("  ✅ Policy updated with AI analysis")
                                    return True
                                else:
                                    logger.error(f"  ❌ Policy update failed: {update_response.status}")
                                    return False
                        else:
                            logger.error(f"  ❌ AI Policy Analysis failed: {ai_response.status}")
                            return False
                else:
                    logger.error(f"  ❌ Policy creation failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Policy management workflow error: {e}")
            return False
    
    async def test_workflow_management(self):
        """Test 7: Workflow Management - Real Bank Process"""
        logger.info("⚙️ Testing Workflow Management - Real Bank Process")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Step 1: Create a real bank workflow
        workflow_scenario = {
            "name": "Monthly Risk Committee Review Process",
            "description": "Monthly workflow for risk committee review of portfolio risks and compliance status",
            "steps": [
                {
                    "step_name": "Data Collection",
                    "description": "Collect risk metrics, compliance scores, and portfolio data",
                    "assignee_id": self.user_id,
                    "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
                    "priority": "high"
                },
                {
                    "step_name": "Risk Analysis",
                    "description": "Analyze risk trends and identify emerging risks",
                    "assignee_id": self.user_id,
                    "due_date": (datetime.now() + timedelta(days=10)).isoformat(),
                    "priority": "high"
                },
                {
                    "step_name": "Committee Review",
                    "description": "Present findings to risk committee",
                    "assignee_id": self.user_id,
                    "due_date": (datetime.now() + timedelta(days=15)).isoformat(),
                    "priority": "critical"
                }
            ],
            "organization_id": self.organization_id
        }
        
        try:
            # Create workflow
            async with self.session.post(f"{self.base_url}/api/workflows", 
                                       json=workflow_scenario, headers=headers) as response:
                if response.status == 201:
                    workflow_result = await response.json()
                    workflow_id = workflow_result["data"]["id"]
                    logger.info(f"  ✅ Workflow created successfully: {workflow_id}")
                    
                    # Step 2: Test workflow execution
                    execution_data = {
                        "workflow_id": workflow_id,
                        "execution_type": "automated",
                        "trigger_conditions": {
                            "schedule": "monthly",
                            "data_ready": True,
                            "approvals_complete": True
                        }
                    }
                    
                    # Call workflow engine
                    async with self.session.post(f"{self.base_url}/api/workflows/{workflow_id}/execute", 
                                               json=execution_data, headers=headers) as exec_response:
                        if exec_response.status == 200:
                            exec_result = await exec_response.json()
                            logger.info("  ✅ Workflow execution initiated")
                            logger.info(f"     Execution ID: {exec_result.get('execution_id', 'N/A')}")
                            logger.info(f"     Status: {exec_result.get('status', 'N/A')}")
                            
                            return True
                        else:
                            logger.error(f"  ❌ Workflow execution failed: {exec_response.status}")
                            return False
                else:
                    logger.error(f"  ❌ Workflow creation failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Workflow management error: {e}")
            return False
    
    async def test_ai_agent_integration(self):
        """Test 8: AI Agent Integration - Multi-Agent Coordination"""
        logger.info("🤖 Testing AI Agent Integration - Multi-Agent Coordination")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test multi-agent scenario
        multi_agent_scenario = {
            "scenario_type": "comprehensive_risk_assessment",
            "business_unit": "commercial_lending",
            "agents_required": [
                "bfsi_compliance_agent",
                "bfsi_risk_agent", 
                "bfsi_fraud_agent",
                "bfsi_aml_agent"
            ],
            "input_data": {
                "portfolio_size": 500000000,
                "customer_count": 1500,
                "transaction_volume": 25000000,
                "risk_metrics": {
                    "default_rate": 0.025,
                    "concentration_ratio": 0.35,
                    "geographic_spread": 0.6
                }
            }
        }
        
        try:
            # Call multi-agent orchestrator
            async with self.session.post(f"{self.ai_agents_url}/api/multi-agent/coordinate", 
                                       json=multi_agent_scenario, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("  ✅ Multi-agent coordination successful")
                    logger.info(f"     Agents activated: {len(result.get('agents_activated', []))}")
                    logger.info(f"     Analysis completed: {result.get('analysis_complete', False)}")
                    logger.info(f"     Recommendations: {len(result.get('recommendations', []))}")
                    
                    # Verify individual agent responses
                    for agent_id, agent_result in result.get('agent_results', {}).items():
                        logger.info(f"     {agent_id}: {agent_result.get('status', 'unknown')}")
                    
                    return True
                else:
                    logger.error(f"  ❌ Multi-agent coordination failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ AI agent integration error: {e}")
            return False
    
    async def test_reporting_and_analytics(self):
        """Test 9: Reporting and Analytics - Executive Dashboard"""
        logger.info("📊 Testing Reporting and Analytics - Executive Dashboard")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test executive report generation
        report_scenario = {
            "report_type": "executive_summary",
            "time_period": "quarterly",
            "business_units": ["commercial_lending", "retail_banking", "investment_banking"],
            "metrics": [
                "risk_score",
                "compliance_score", 
                "capital_adequacy",
                "operational_efficiency"
            ],
            "format": "pdf"
        }
        
        try:
            # Generate executive report
            async with self.session.post(f"{self.base_url}/api/reports/generate", 
                                       json=report_scenario, headers=headers) as response:
                if response.status == 200:
                    report_result = await response.json()
                    logger.info("  ✅ Executive report generated successfully")
                    logger.info(f"     Report ID: {report_result.get('report_id', 'N/A')}")
                    logger.info(f"     Format: {report_result.get('format', 'N/A')}")
                    logger.info(f"     Size: {report_result.get('file_size', 'N/A')} bytes")
                    
                    return True
                else:
                    logger.error(f"  ❌ Report generation failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Reporting and analytics error: {e}")
            return False
    
    async def test_real_time_monitoring(self):
        """Test 10: Real-time Monitoring and Alerts"""
        logger.info("🔔 Testing Real-time Monitoring and Alerts")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test real-time monitoring setup
        monitoring_scenario = {
            "monitoring_type": "risk_threshold_breach",
            "thresholds": {
                "credit_risk_score": 80,
                "compliance_score": 70,
                "capital_ratio": 8.0
            },
            "alert_channels": ["email", "dashboard", "api"],
            "business_units": ["commercial_lending", "retail_banking"]
        }
        
        try:
            # Set up monitoring
            async with self.session.post(f"{self.base_url}/api/monitoring/setup", 
                                       json=monitoring_scenario, headers=headers) as response:
                if response.status == 200:
                    monitoring_result = await response.json()
                    logger.info("  ✅ Real-time monitoring setup successful")
                    logger.info(f"     Monitoring ID: {monitoring_result.get('monitoring_id', 'N/A')}")
                    logger.info(f"     Thresholds configured: {len(monitoring_result.get('thresholds', []))}")
                    
                    # Test alert generation
                    alert_data = {
                        "monitoring_id": monitoring_result.get('monitoring_id'),
                        "trigger_type": "threshold_breach",
                        "metric": "credit_risk_score",
                        "current_value": 85,
                        "threshold_value": 80
                    }
                    
                    async with self.session.post(f"{self.base_url}/api/alerts/generate", 
                                               json=alert_data, headers=headers) as alert_response:
                        if alert_response.status == 200:
                            alert_result = await alert_response.json()
                            logger.info("  ✅ Alert generated successfully")
                            logger.info(f"     Alert ID: {alert_result.get('alert_id', 'N/A')}")
                            logger.info(f"     Severity: {alert_result.get('severity', 'N/A')}")
                            
                            return True
                        else:
                            logger.error(f"  ❌ Alert generation failed: {alert_response.status}")
                            return False
                else:
                    logger.error(f"  ❌ Monitoring setup failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"  ❌ Real-time monitoring error: {e}")
            return False
    
    async def run_complete_journey(self, user_type: str):
        """Run the complete bank employee journey"""
        logger.info(f"🏦 Starting Complete Bank Employee Journey - {user_type.title()}")
        logger.info("=" * 80)
        
        journey_steps = [
            ("System Health Check", self.test_system_health),
            ("User Authentication", lambda: self.test_user_authentication(user_type)),
            ("Dashboard Access", self.test_dashboard_access),
            ("Risk Management Workflow", self.test_risk_management_workflow),
            ("Compliance Monitoring", self.test_compliance_monitoring_workflow),
            ("Policy Management", self.test_policy_management_workflow),
            ("Workflow Management", self.test_workflow_management),
            ("AI Agent Integration", self.test_ai_agent_integration),
            ("Reporting and Analytics", self.test_reporting_and_analytics),
            ("Real-time Monitoring", self.test_real_time_monitoring)
        ]
        
        for step_name, step_function in journey_steps:
            logger.info(f"\n📋 Step: {step_name}")
            try:
                result = await step_function()
                self.test_results[step_name] = result
                if result:
                    logger.info(f"✅ {step_name} completed successfully")
                else:
                    logger.error(f"❌ {step_name} failed")
            except Exception as e:
                logger.error(f"❌ {step_name} failed with error: {e}")
                self.test_results[step_name] = False
        
        # Print journey summary
        logger.info("\n" + "=" * 80)
        logger.info(f"🎯 Complete Journey Summary - {user_type.title()}")
        logger.info("=" * 80)
        
        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        logger.info(f"\n📊 Journey Results:")
        for step_name, result in self.test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"   {step_name}: {status}")
        
        logger.info(f"\n🎉 Journey Completion: {passed}/{total} steps passed ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            logger.info("🏆 Excellent! The platform is working well for this user type.")
        elif success_rate >= 60:
            logger.info("⚠️ Good performance with some issues to address.")
        else:
            logger.info("🚨 Significant issues detected. Platform needs attention.")
        
        return success_rate >= 80

async def main():
    """Main function to run complete bank employee journey tests"""
    logger.info("🏦 GRC Platform - Real Bank Employee Journey Testing")
    logger.info("=" * 80)
    logger.info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test all user types
    user_types = ["cfo", "compliance_manager", "risk_analyst", "operations_manager"]
    overall_results = {}
    
    for user_type in user_types:
        logger.info(f"\n{'='*20} Testing {user_type.replace('_', ' ').title()} {'='*20}")
        
        async with RealBankEmployeeTester() as tester:
            success = await tester.run_complete_journey(user_type)
            overall_results[user_type] = success
        
        # Wait between user tests
        await asyncio.sleep(5)
    
    # Print overall summary
    logger.info("\n" + "=" * 80)
    logger.info("🏆 OVERALL TESTING SUMMARY")
    logger.info("=" * 80)
    
    successful_users = sum(1 for success in overall_results.values() if success)
    total_users = len(overall_results)
    
    logger.info(f"\n👥 User Type Results:")
    for user_type, success in overall_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"   {user_type.replace('_', ' ').title()}: {status}")
    
    logger.info(f"\n🎯 Overall Success Rate: {successful_users}/{total_users} user types ({successful_users/total_users*100:.1f}%)")
    
    if successful_users == total_users:
        logger.info("🎉 ALL USER JOURNEYS PASSED! Platform is ready for production!")
    elif successful_users >= total_users * 0.75:
        logger.info("✅ Most user journeys passed. Platform is mostly ready.")
    else:
        logger.info("⚠️ Multiple user journey failures. Platform needs significant work.")
    
    logger.info(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
