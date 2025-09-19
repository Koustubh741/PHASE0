#!/usr/bin/env python3
"""
GRC Platform AI Agents - Live Demo
Demonstrates industry-specific GRC operations across BFSI, Telecom, Manufacturing, and Healthcare
"""

import sys
import os
import asyncio
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def demo_bfsi_agent():
    """Demo BFSI GRC Agent"""
    print("\n🏦 BFSI (Banking, Financial Services, Insurance) Agent Demo")
    print("=" * 60)
    
    try:
        # Import BFSI agent
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        from core.industry_agent import GRCOperationType
        
        # Initialize agent
        bfsi_agent = BFSIGRCAgent()
        print(f"✅ Agent Initialized: {bfsi_agent.name}")
        print(f"📊 Industry: {bfsi_agent.industry.value}")
        print(f"🏛️ Regulatory Bodies: {len(bfsi_agent.regulatory_bodies)}")
        
        # Demo Risk Assessment
        print("\n⚠️ Performing Credit Risk Assessment...")
        risk_context = {
            "business_unit": "investment_banking",
            "risk_scope": "credit"
        }
        
        risk_result = await bfsi_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, risk_context
        )
        
        if risk_result.get("success", False):
            print(f"✅ Risk Assessment Completed")
            print(f"   📊 Risks Identified: {risk_result.get('risks_identified', 0)}")
            print(f"   📋 Risk Categories: {len(risk_result.get('risk_details', []))}")
            print(f"   💡 Recommendations: {len(risk_result.get('recommendations', []))}")
            
            # Show sample risk
            risks = risk_result.get('risk_details', [])
            if risks:
                sample_risk = risks[0]
                print(f"   🔍 Sample Risk: {sample_risk.get('subcategory', 'N/A')}")
                print(f"      Likelihood: {sample_risk.get('likelihood', 'N/A')}")
                print(f"      Impact: {sample_risk.get('impact', 'N/A')}")
        else:
            print(f"❌ Risk Assessment Failed: {risk_result.get('error', 'Unknown')}")
        
        # Demo Compliance Check
        print("\n✅ Performing Basel III Compliance Check...")
        compliance_context = {
            "framework": "basel iii",
            "business_unit": "all",
            "check_scope": "full"
        }
        
        compliance_result = await bfsi_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, compliance_context
        )
        
        if compliance_result.get("success", False):
            print(f"✅ Compliance Check Completed")
            print(f"   📊 Compliance Score: {compliance_result.get('compliance_score', 0):.1f}%")
            print(f"   📋 Requirements Checked: {compliance_result.get('requirements_checked', 0)}")
        else:
            print(f"❌ Compliance Check Failed: {compliance_result.get('error', 'Unknown')}")
        
        # Show KPIs
        print("\n📈 BFSI KPIs:")
        kpis = bfsi_agent._get_industry_kpis()
        for category, metrics in kpis.items():
            print(f"   {category.title()}:")
            for metric, data in metrics.items():
                print(f"     {metric}: {data.get('current', 'N/A')} (target: {data.get('target', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"❌ BFSI Agent Demo Failed: {e}")
        return False

async def demo_telecom_agent():
    """Demo Telecom GRC Agent"""
    print("\n📡 Telecom Agent Demo")
    print("=" * 60)
    
    try:
        # Import Telecom agent
        from agents.telecom.telecom_grc_agent import TelecomGRCAgent
        from core.industry_agent import GRCOperationType
        
        # Initialize agent
        telecom_agent = TelecomGRCAgent()
        print(f"✅ Agent Initialized: {telecom_agent.name}")
        print(f"📊 Industry: {telecom_agent.industry.value}")
        print(f"🏛️ Regulatory Bodies: {len(telecom_agent.regulatory_bodies)}")
        
        # Demo Network Security Risk Assessment
        print("\n🔒 Performing Network Security Risk Assessment...")
        security_context = {
            "business_unit": "network_operations",
            "risk_scope": "security"
        }
        
        security_result = await telecom_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, security_context
        )
        
        if security_result.get("success", False):
            print(f"✅ Security Risk Assessment Completed")
            print(f"   📊 Risks Identified: {security_result.get('risks_identified', 0)}")
            
            # Show sample security risk
            risks = security_result.get('risk_details', [])
            if risks:
                for risk in risks[:2]:  # Show first 2 risks
                    print(f"   🔍 {risk.get('subcategory', 'N/A')}: {risk.get('description', 'N/A')[:50]}...")
        else:
            print(f"❌ Security Risk Assessment Failed: {security_result.get('error', 'Unknown')}")
        
        # Demo FCC Compliance Check
        print("\n📋 Performing FCC Compliance Check...")
        fcc_context = {
            "framework": "fcc",
            "business_unit": "all",
            "check_scope": "full"
        }
        
        fcc_result = await telecom_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, fcc_context
        )
        
        if fcc_result.get("success", False):
            print(f"✅ FCC Compliance Check Completed")
            print(f"   📊 Compliance Score: {fcc_result.get('compliance_score', 0):.1f}%")
        else:
            print(f"❌ FCC Compliance Check Failed: {fcc_result.get('error', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Telecom Agent Demo Failed: {e}")
        return False

async def demo_manufacturing_agent():
    """Demo Manufacturing GRC Agent"""
    print("\n🏭 Manufacturing Agent Demo")
    print("=" * 60)
    
    try:
        # Import Manufacturing agent
        from agents.manufacturing.manufacturing_grc_agent import ManufacturingGRCAgent
        from core.industry_agent import GRCOperationType
        
        # Initialize agent
        mfg_agent = ManufacturingGRCAgent()
        print(f"✅ Agent Initialized: {mfg_agent.name}")
        print(f"📊 Industry: {mfg_agent.industry.value}")
        print(f"🏛️ Regulatory Bodies: {len(mfg_agent.regulatory_bodies)}")
        
        # Demo Safety Risk Assessment
        print("\n🛡️ Performing Safety Risk Assessment...")
        safety_context = {
            "business_unit": "production",
            "risk_scope": "safety"
        }
        
        safety_result = await mfg_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, safety_context
        )
        
        if safety_result.get("success", False):
            print(f"✅ Safety Risk Assessment Completed")
            print(f"   📊 Risks Identified: {safety_result.get('risks_identified', 0)}")
            
            # Show safety risks
            risks = safety_result.get('risk_details', [])
            if risks:
                for risk in risks[:2]:
                    print(f"   🔍 {risk.get('subcategory', 'N/A')}: {risk.get('description', 'N/A')[:50]}...")
        else:
            print(f"❌ Safety Risk Assessment Failed: {safety_result.get('error', 'Unknown')}")
        
        # Demo ISO 9001 Compliance Check
        print("\n📋 Performing ISO 9001 Compliance Check...")
        iso_context = {
            "framework": "iso_9001",
            "business_unit": "all",
            "check_scope": "full"
        }
        
        iso_result = await mfg_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, iso_context
        )
        
        if iso_result.get("success", False):
            print(f"✅ ISO 9001 Compliance Check Completed")
            print(f"   📊 Compliance Score: {iso_result.get('compliance_score', 0):.1f}%")
        else:
            print(f"❌ ISO 9001 Compliance Check Failed: {iso_result.get('error', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Manufacturing Agent Demo Failed: {e}")
        return False

async def demo_healthcare_agent():
    """Demo Healthcare GRC Agent"""
    print("\n🏥 Healthcare Agent Demo")
    print("=" * 60)
    
    try:
        # Import Healthcare agent
        from agents.healthcare.healthcare_grc_agent import HealthcareGRCAgent
        from core.industry_agent import GRCOperationType
        
        # Initialize agent
        healthcare_agent = HealthcareGRCAgent()
        print(f"✅ Agent Initialized: {healthcare_agent.name}")
        print(f"📊 Industry: {healthcare_agent.industry.value}")
        print(f"🏛️ Regulatory Bodies: {len(healthcare_agent.regulatory_bodies)}")
        
        # Demo Patient Safety Risk Assessment
        print("\n👥 Performing Patient Safety Risk Assessment...")
        safety_context = {
            "business_unit": "patient_care",
            "risk_scope": "patient_safety"
        }
        
        safety_result = await healthcare_agent.perform_grc_operation(
            GRCOperationType.RISK_ASSESSMENT, safety_context
        )
        
        if safety_result.get("success", False):
            print(f"✅ Patient Safety Risk Assessment Completed")
            print(f"   📊 Risks Identified: {safety_result.get('risks_identified', 0)}")
            
            # Show patient safety risks
            risks = safety_result.get('risk_details', [])
            if risks:
                for risk in risks[:2]:
                    print(f"   🔍 {risk.get('subcategory', 'N/A')}: {risk.get('description', 'N/A')[:50]}...")
        else:
            print(f"❌ Patient Safety Risk Assessment Failed: {safety_result.get('error', 'Unknown')}")
        
        # Demo HIPAA Compliance Check
        print("\n📋 Performing HIPAA Compliance Check...")
        hipaa_context = {
            "framework": "hipaa",
            "business_unit": "all",
            "check_scope": "full"
        }
        
        hipaa_result = await healthcare_agent.perform_grc_operation(
            GRCOperationType.COMPLIANCE_CHECK, hipaa_context
        )
        
        if hipaa_result.get("success", False):
            print(f"✅ HIPAA Compliance Check Completed")
            print(f"   📊 Compliance Score: {hipaa_result.get('compliance_score', 0):.1f}%")
        else:
            print(f"❌ HIPAA Compliance Check Failed: {hipaa_result.get('error', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Healthcare Agent Demo Failed: {e}")
        return False

async def demo_reporting_engine():
    """Demo Archer-style Reporting Engine"""
    print("\n📊 Archer-Style Reporting Engine Demo")
    print("=" * 60)
    
    try:
        from core.archer_reporting_engine import ArcherReportingEngine, ReportType, ReportFormat
        
        # Initialize reporting engine
        reporting_engine = ArcherReportingEngine()
        print("✅ Reporting Engine Initialized")
        
        # Demo Executive Summary Report
        print("\n📄 Generating Executive Summary Report for BFSI...")
        mock_data = {
            "risk_score": 75,
            "compliance_score": 85,
            "audit_score": 90,
            "total_risks": 25,
            "high_risks": 3,
            "regulatory_violations": 0,
            "customer_satisfaction": 4.2
        }
        
        report = await reporting_engine.generate_report(
            ReportType.EXECUTIVE_SUMMARY, "bfsi", mock_data, ReportFormat.JSON
        )
        
        if report:
            print("✅ Executive Summary Report Generated")
            report_data = report.get("report_data", {})
            print(f"   📊 Report Type: {report_data.get('report_type', 'Unknown')}")
            print(f"   🏭 Industry: {report_data.get('industry', 'Unknown')}")
            print(f"   📁 Format: {report.get('format', 'Unknown')}")
            print(f"   📏 File Size: {report.get('file_size', 0)} bytes")
            
            # Show summary
            summary = report_data.get("executive_summary", {})
            if summary:
                print(f"   🎯 Overall Status: {summary.get('overall_status', 'Unknown')}")
                print(f"   🏆 Key Achievements: {len(summary.get('key_achievements', []))}")
                print(f"   ⚠️ Critical Issues: {len(summary.get('critical_issues', []))}")
        else:
            print("❌ Report Generation Failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Reporting Engine Demo Failed: {e}")
        return False

async def demo_workflow_engine():
    """Demo GRC Workflow Engine"""
    print("\n⚙️ GRC Workflow Engine Demo")
    print("=" * 60)
    
    try:
        from core.grc_workflow_engine import GRCWorkflowEngine
        from core.industry_agent import IndustryType
        from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
        
        # Initialize workflow engine
        workflow_engine = GRCWorkflowEngine()
        print("✅ Workflow Engine Initialized")
        
        # Register BFSI agent
        bfsi_agent = BFSIGRCAgent()
        await workflow_engine.register_industry_agent(IndustryType.BFSI, bfsi_agent)
        print("✅ BFSI Agent Registered with Workflow Engine")
        
        # Get workflow templates
        templates = await workflow_engine.get_workflow_templates()
        print(f"✅ Workflow Templates Loaded: {len(templates)} templates")
        
        # Show available templates
        for template_name, template_info in templates.items():
            print(f"   📋 {template_name}: {template_info['name']}")
            print(f"      Description: {template_info['description']}")
            print(f"      Industries: {', '.join(template_info['industries'])}")
            print(f"      Operations: {', '.join(template_info['operations'])}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow Engine Demo Failed: {e}")
        return False

async def main():
    """Main demo function"""
    print("🤖 GRC Platform AI Agents - Live Demo")
    print("=" * 70)
    print("Demonstrating industry-specific GRC operations across 4 sectors:")
    print("🏦 BFSI (Banking, Financial Services, Insurance)")
    print("📡 Telecom (Telecommunications)")
    print("🏭 Manufacturing (Industrial Manufacturing)")
    print("🏥 Healthcare (Healthcare & Life Sciences)")
    print("=" * 70)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Track demo results
    demo_results = []
    
    # Run demos
    demo_results.append(("BFSI Agent", await demo_bfsi_agent()))
    demo_results.append(("Telecom Agent", await demo_telecom_agent()))
    demo_results.append(("Manufacturing Agent", await demo_manufacturing_agent()))
    demo_results.append(("Healthcare Agent", await demo_healthcare_agent()))
    demo_results.append(("Reporting Engine", await demo_reporting_engine()))
    demo_results.append(("Workflow Engine", await demo_workflow_engine()))
    
    # Print results summary
    print("\n" + "=" * 70)
    print("📊 Demo Results Summary")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for demo_name, result in demo_results:
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{demo_name:.<40} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Demos: {len(demo_results)}")
    print(f"Successful: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(demo_results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All demos successful! AI Agents system is fully operational!")
        print("🚀 Ready for production deployment!")
    else:
        print(f"\n⚠️ {failed} demo(s) failed. Please check the errors above.")
    
    print(f"\nDemo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
