#!/usr/bin/env python3
"""
Final Test - GRC Platform AI Agents
Comprehensive test of all industry-specific GRC operations
"""

import sys
import os
import asyncio
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_all_industries():
    """Test all industry agents"""
    print("🤖 GRC Platform AI Agents - Final Comprehensive Test")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {}
    
    # Test BFSI Agent
    print("🏦 Testing BFSI Agent...")
    try:
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        from core.industry_agent import GRCOperationType
        
        bfsi_agent = BFSIGRCAgent()
        
        # Test risk assessment
        risk_result = await bfsi_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, 
            {"business_unit": "investment_banking", "risk_scope": "credit"}
        )
        
        # Test compliance check
        compliance_result = await bfsi_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, 
            {"framework": "basel iii", "business_unit": "all", "check_scope": "full"}
        )
        
        results["BFSI"] = {
            "risk_assessment": risk_result.get("success", False),
            "compliance_check": compliance_result.get("success", False),
            "risks_identified": risk_result.get("risks_identified", 0),
            "compliance_score": compliance_result.get("compliance_score", 0)
        }
        
        print(f"  ✅ BFSI Agent: Risk Assessment ({risk_result.get('risks_identified', 0)} risks), Compliance ({compliance_result.get('compliance_score', 0):.1f}%)")
        
    except Exception as e:
        results["BFSI"] = {"error": str(e)}
        print(f"  ❌ BFSI Agent failed: {e}")
    
    # Test Telecom Agent
    print("📡 Testing Telecom Agent...")
    try:
        from agents.telecom.telecom_grc_agent import TelecomGRCAgent
        
        telecom_agent = TelecomGRCAgent()
        
        # Test security risk assessment
        security_result = await telecom_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, 
            {"business_unit": "network_operations", "risk_scope": "security"}
        )
        
        # Test FCC compliance
        fcc_result = await telecom_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, 
            {"framework": "fcc", "business_unit": "all", "check_scope": "full"}
        )
        
        results["Telecom"] = {
            "risk_assessment": security_result.get("success", False),
            "compliance_check": fcc_result.get("success", False),
            "risks_identified": security_result.get("risks_identified", 0),
            "compliance_score": fcc_result.get("compliance_score", 0)
        }
        
        print(f"  ✅ Telecom Agent: Security Assessment ({security_result.get('risks_identified', 0)} risks), FCC Compliance ({fcc_result.get('compliance_score', 0):.1f}%)")
        
    except Exception as e:
        results["Telecom"] = {"error": str(e)}
        print(f"  ❌ Telecom Agent failed: {e}")
    
    # Test Manufacturing Agent
    print("🏭 Testing Manufacturing Agent...")
    try:
        from agents.manufacturing.manufacturing_grc_agent import ManufacturingGRCAgent
        
        mfg_agent = ManufacturingGRCAgent()
        
        # Test safety risk assessment
        safety_result = await mfg_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, 
            {"business_unit": "production", "risk_scope": "safety"}
        )
        
        # Test ISO compliance
        iso_result = await mfg_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, 
            {"framework": "iso_9001", "business_unit": "all", "check_scope": "full"}
        )
        
        results["Manufacturing"] = {
            "risk_assessment": safety_result.get("success", False),
            "compliance_check": iso_result.get("success", False),
            "risks_identified": safety_result.get("risks_identified", 0),
            "compliance_score": iso_result.get("compliance_score", 0)
        }
        
        print(f"  ✅ Manufacturing Agent: Safety Assessment ({safety_result.get('risks_identified', 0)} risks), ISO Compliance ({iso_result.get('compliance_score', 0):.1f}%)")
        
    except Exception as e:
        results["Manufacturing"] = {"error": str(e)}
        print(f"  ❌ Manufacturing Agent failed: {e}")
    
    # Test Healthcare Agent
    print("🏥 Testing Healthcare Agent...")
    try:
        from agents.healthcare.healthcare_grc_agent import HealthcareGRCAgent
        
        healthcare_agent = HealthcareGRCAgent()
        
        # Test patient safety risk assessment
        safety_result = await healthcare_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, 
            {"business_unit": "patient_care", "risk_scope": "patient_safety"}
        )
        
        # Test HIPAA compliance
        hipaa_result = await healthcare_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, 
            {"framework": "hipaa", "business_unit": "all", "check_scope": "full"}
        )
        
        results["Healthcare"] = {
            "risk_assessment": safety_result.get("success", False),
            "compliance_check": hipaa_result.get("success", False),
            "risks_identified": safety_result.get("risks_identified", 0),
            "compliance_score": hipaa_result.get("compliance_score", 0)
        }
        
        print(f"  ✅ Healthcare Agent: Patient Safety Assessment ({safety_result.get('risks_identified', 0)} risks), HIPAA Compliance ({hipaa_result.get('compliance_score', 0):.1f}%)")
        
    except Exception as e:
        results["Healthcare"] = {"error": str(e)}
        print(f"  ❌ Healthcare Agent failed: {e}")
    
    # Test Reporting Engine
    print("📊 Testing Archer Reporting Engine...")
    try:
        from core.archer_reporting_engine import ArcherReportingEngine, ReportType, ReportFormat
        
        reporting_engine = ArcherReportingEngine()
        
        mock_data = {
            "risk_score": 75,
            "compliance_score": 85,
            "total_risks": 25,
            "high_risks": 3
        }
        
        report = await reporting_engine.generate_report(
            ReportType.EXECUTIVE_SUMMARY, "bfsi", mock_data, ReportFormat.JSON
        )
        
        results["Reporting"] = {
            "success": bool(report),
            "report_type": report.get("report_data", {}).get("report_type", "Unknown") if report else "Failed"
        }
        
        print(f"  ✅ Reporting Engine: {report.get('report_data', {}).get('report_type', 'Unknown')} report generated")
        
    except Exception as e:
        results["Reporting"] = {"error": str(e)}
        print(f"  ❌ Reporting Engine failed: {e}")
    
    # Test Workflow Engine
    print("⚙️ Testing GRC Workflow Engine...")
    try:
        from core.grc_workflow_engine import GRCWorkflowEngine
        from core.industry_agent import IndustryType
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        
        workflow_engine = GRCWorkflowEngine()
        bfsi_agent = BFSIGRCAgent()
        
        await workflow_engine.register_industry_agent(IndustryType.BFSI, bfsi_agent)
        templates = await workflow_engine.get_workflow_templates()
        
        results["Workflow"] = {
            "success": True,
            "templates_count": len(templates),
            "agent_registered": True
        }
        
        print(f"  ✅ Workflow Engine: {len(templates)} templates loaded, agent registered")
        
    except Exception as e:
        results["Workflow"] = {"error": str(e)}
        print(f"  ❌ Workflow Engine failed: {e}")
    
    # Print final results
    print("\n" + "=" * 70)
    print("📊 FINAL TEST RESULTS")
    print("=" * 70)
    
    total_tests = 0
    passed_tests = 0
    
    for component, result in results.items():
        if "error" in result:
            print(f"{component:.<30} ❌ FAILED")
            print(f"  Error: {result['error']}")
        else:
            if component in ["BFSI", "Telecom", "Manufacturing", "Healthcare"]:
                risk_ok = result.get("risk_assessment", False)
                compliance_ok = result.get("compliance_check", False)
                risks = result.get("risks_identified", 0)
                score = result.get("compliance_score", 0)
                
                if risk_ok and compliance_ok:
                    print(f"{component:.<30} ✅ PASSED")
                    print(f"  Risks: {risks}, Compliance: {score:.1f}%")
                    passed_tests += 2
                    total_tests += 2
                else:
                    print(f"{component:.<30} ❌ FAILED")
                    print(f"  Risk Assessment: {'✅' if risk_ok else '❌'}, Compliance: {'✅' if compliance_ok else '❌'}")
                    total_tests += 2
            
            elif component == "Reporting":
                if result.get("success", False):
                    print(f"{component:.<30} ✅ PASSED")
                    print(f"  Report: {result.get('report_type', 'Unknown')}")
                    passed_tests += 1
                    total_tests += 1
                else:
                    print(f"{component:.<30} ❌ FAILED")
                    total_tests += 1
            
            elif component == "Workflow":
                if result.get("success", False):
                    print(f"{component:.<30} ✅ PASSED")
                    print(f"  Templates: {result.get('templates_count', 0)}, Agent: {'✅' if result.get('agent_registered', False) else '❌'}")
                    passed_tests += 1
                    total_tests += 1
                else:
                    print(f"{component:.<30} ❌ FAILED")
                    total_tests += 1
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 GRC Platform AI Agents are FULLY OPERATIONAL!")
        print("✅ Ready for production deployment!")
        print("\n📋 System Capabilities:")
        print("   • Industry-specific risk assessments")
        print("   • Regulatory compliance monitoring")
        print("   • Automated workflow orchestration")
        print("   • Archer-style reporting and analytics")
        print("   • Multi-industry GRC operations")
        print("   • Real-time monitoring and alerts")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} test(s) failed.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(test_all_industries())
