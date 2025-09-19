#!/usr/bin/env python3
"""
Test Script for GRC Platform AI Agents
Tests the industry-specific AI agents without full dependencies
"""

import sys
import os
import asyncio
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all AI agent modules can be imported"""
    print("🔍 Testing AI Agent Imports...")
    
    try:
        # Test core modules
        from core.industry_agent import IndustryType, GRCOperationType
        print("  ✅ Core industry agent imports successful")
        
        from core.grc_workflow_engine import GRCWorkflowEngine
        print("  ✅ GRC workflow engine import successful")
        
        from core.archer_reporting_engine import ArcherReportingEngine, ReportType, ReportFormat
        print("  ✅ Archer reporting engine import successful")
        
        # Test industry-specific agents
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        print("  ✅ BFSI GRC Agent import successful")
        
        from agents.telecom.telecom_grc_agent import TelecomGRCAgent
        print("  ✅ Telecom GRC Agent import successful")
        
        from agents.manufacturing.manufacturing_grc_agent import ManufacturingGRCAgent
        print("  ✅ Manufacturing GRC Agent import successful")
        
        from agents.healthcare.healthcare_grc_agent import HealthcareGRCAgent
        print("  ✅ Healthcare GRC Agent import successful")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False

def test_industry_agents():
    """Test industry-specific agent initialization"""
    print("\n🏭 Testing Industry Agent Initialization...")
    
    try:
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        from agents.telecom.telecom_grc_agent import TelecomGRCAgent
        from agents.manufacturing.manufacturing_grc_agent import ManufacturingGRCAgent
        from agents.healthcare.healthcare_grc_agent import HealthcareGRCAgent
        from core.industry_agent import IndustryType
        
        # Test BFSI Agent
        bfsi_agent = BFSIGRCAgent()
        print(f"  ✅ BFSI Agent initialized: {bfsi_agent.name}")
        print(f"     Industry: {bfsi_agent.industry.value}")
        print(f"     Risk Categories: {len(bfsi_agent.risk_categories)}")
        print(f"     Compliance Requirements: {len(bfsi_agent.compliance_requirements)}")
        
        # Test Telecom Agent
        telecom_agent = TelecomGRCAgent()
        print(f"  ✅ Telecom Agent initialized: {telecom_agent.name}")
        print(f"     Industry: {telecom_agent.industry.value}")
        print(f"     Risk Categories: {len(telecom_agent.risk_categories)}")
        
        # Test Manufacturing Agent
        mfg_agent = ManufacturingGRCAgent()
        print(f"  ✅ Manufacturing Agent initialized: {mfg_agent.name}")
        print(f"     Industry: {mfg_agent.industry.value}")
        print(f"     Risk Categories: {len(mfg_agent.risk_categories)}")
        
        # Test Healthcare Agent
        healthcare_agent = HealthcareGRCAgent()
        print(f"  ✅ Healthcare Agent initialized: {healthcare_agent.name}")
        print(f"     Industry: {healthcare_agent.industry.value}")
        print(f"     Risk Categories: {len(healthcare_agent.risk_categories)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent initialization error: {e}")
        return False

async def test_workflow_engine():
    """Test GRC workflow engine"""
    print("\n⚙️ Testing GRC Workflow Engine...")
    
    try:
        from core.grc_workflow_engine import GRCWorkflowEngine
        from core.industry_agent import IndustryType
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        
        # Initialize workflow engine
        workflow_engine = GRCWorkflowEngine()
        print("  ✅ Workflow engine initialized")
        
        # Register BFSI agent
        bfsi_agent = BFSIGRCAgent()
        await workflow_engine.register_industry_agent(IndustryType.BFSI, bfsi_agent)
        print("  ✅ BFSI agent registered with workflow engine")
        
        # Get workflow templates
        templates = await workflow_engine.get_workflow_templates()
        print(f"  ✅ Workflow templates loaded: {len(templates)} templates")
        
        # List available templates
        for template_name, template_info in templates.items():
            print(f"     - {template_name}: {template_info['name']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Workflow engine error: {e}")
        return False

async def test_reporting_engine():
    """Test Archer reporting engine"""
    print("\n📊 Testing Archer Reporting Engine...")
    
    try:
        from core.archer_reporting_engine import ArcherReportingEngine, ReportType, ReportFormat
        
        # Initialize reporting engine
        reporting_engine = ArcherReportingEngine()
        print("  ✅ Reporting engine initialized")
        
        # Test report generation (mock data)
        mock_data = {
            "risk_score": 75,
            "compliance_score": 85,
            "audit_score": 90,
            "total_risks": 25,
            "high_risks": 3
        }
        
        # Generate executive summary report
        report = await reporting_engine.generate_report(
            ReportType.EXECUTIVE_SUMMARY, "bfsi", mock_data, ReportFormat.JSON
        )
        print("  ✅ Executive summary report generated")
        print(f"     Report type: {report.get('report_data', {}).get('report_type', 'Unknown')}")
        print(f"     Format: {report.get('format', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Reporting engine error: {e}")
        return False

async def test_risk_assessment():
    """Test risk assessment functionality"""
    print("\n⚠️ Testing Risk Assessment...")
    
    try:
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        from core.industry_agent import GRCOperationType
        
        # Initialize BFSI agent
        bfsi_agent = BFSIGRCAgent()
        
        # Test risk assessment
        context = {
            "business_unit": "investment_banking",
            "risk_scope": "credit"
        }
        
        result = await bfsi_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, context
        )
        
        if result.get("success", False):
            print("  ✅ Risk assessment completed successfully")
            print(f"     Risks identified: {result.get('risks_identified', 0)}")
            print(f"     Risk categories: {len(result.get('risk_details', []))}")
            print(f"     Recommendations: {len(result.get('recommendations', []))}")
        else:
            print(f"  ❌ Risk assessment failed: {result.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Risk assessment error: {e}")
        return False

async def test_compliance_check():
    """Test compliance check functionality"""
    print("\n✅ Testing Compliance Check...")
    
    try:
        from agents.telecom.telecom_grc_agent import TelecomGRCAgent
        from core.industry_agent import GRCOperationType
        
        # Initialize Telecom agent
        telecom_agent = TelecomGRCAgent()
        
        # Test compliance check
        context = {
            "framework": "fcc",
            "business_unit": "network_operations",
            "check_scope": "full"
        }
        
        result = await telecom_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, context
        )
        
        if result.get("success", False):
            print("  ✅ Compliance check completed successfully")
            print(f"     Compliance score: {result.get('compliance_score', 0):.1f}%")
            print(f"     Requirements checked: {result.get('requirements_checked', 0)}")
        else:
            print(f"  ❌ Compliance check failed: {result.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Compliance check error: {e}")
        return False

async def main():
    """Main test function"""
    print("🤖 GRC Platform AI Agents - System Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track test results
    test_results = []
    
    # Run tests
    test_results.append(("Import Test", test_imports()))
    test_results.append(("Agent Initialization", test_industry_agents()))
    test_results.append(("Workflow Engine", await test_workflow_engine()))
    test_results.append(("Reporting Engine", await test_reporting_engine()))
    test_results.append(("Risk Assessment", await test_risk_assessment()))
    test_results.append(("Compliance Check", await test_compliance_check()))
    
    # Print results summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! AI Agents system is ready!")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please check the errors above.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
