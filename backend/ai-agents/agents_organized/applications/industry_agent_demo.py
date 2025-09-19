"""
Industry Multi-Agent Strategy Demo
Demonstrates the enhanced capabilities with Ollama and Chroma
"""

import asyncio
import logging
from datetime import datetime
import json

from industry_orchestrator_manager import IndustryOrchestratorManager
from industry_multi_agent_strategy import IndustryMultiAgentOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def demo_bfsi_industry_agents():
    """Demo BFSI industry multi-agent strategy"""
    print("\n" + "="*80)
    print("🏦 BFSI INDUSTRY MULTI-AGENT STRATEGY DEMO")
    print("="*80)
    
    try:
        # Initialize BFSI orchestrator
        bfsi_orchestrator = IndustryMultiAgentOrchestrator("bfsi")
        await bfsi_orchestrator.initialize()
        
        print(f"✅ BFSI Orchestrator initialized with {len(bfsi_orchestrator.agents)} specialized agents")
        print(f"🤖 Using Ollama model: {bfsi_orchestrator.industry_specific_models}")
        print(f"📚 Chroma collections: {bfsi_orchestrator.chroma_collections}")
        
        # List BFSI agents
        print("\n📋 BFSI Specialized Agents:")
        for agent_id, agent in bfsi_orchestrator.agents.items():
            capability = bfsi_orchestrator.agent_capabilities.get(agent_id)
            print(f"  • {agent_id}: {capability.specialization if capability else 'General'}")
        
        # Execute BFSI analysis
        print("\n🔍 Executing BFSI Industry Analysis...")
        start_time = datetime.now()
        
        result = await bfsi_orchestrator.execute_industry_analysis(
            organization_id="demo-bfsi-bank",
            analysis_type="comprehensive"
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"✅ BFSI Analysis completed in {execution_time:.2f} seconds")
        print(f"📊 Analysis Results:")
        print(f"  • Industry: {result.get('industry')}")
        print(f"  • Agents Used: {result.get('performance_metrics', {}).get('agents_used', 0)}")
        print(f"  • Tasks Completed: {result.get('performance_metrics', {}).get('tasks_completed', 0)}")
        print(f"  • Ollama Model: {result.get('performance_metrics', {}).get('ollama_model', 'N/A')}")
        
        # Show analysis results
        analysis_results = result.get('analysis_results', {})
        if analysis_results:
            print(f"  • Overall Assessment: {analysis_results.get('overall_assessment', 'N/A')}")
            print(f"  • Compliance Status: {analysis_results.get('compliance_status', 'N/A')}")
            print(f"  • Risk Level: {analysis_results.get('risk_level', 'N/A')}")
            print(f"  • Confidence Score: {analysis_results.get('confidence_score', 0.0):.2f}")
        
        await bfsi_orchestrator.cleanup()
        return result
        
    except Exception as e:
        print(f"❌ BFSI Demo failed: {e}")
        return None

async def demo_telecom_industry_agents():
    """Demo Telecom industry multi-agent strategy"""
    print("\n" + "="*80)
    print("📡 TELECOM INDUSTRY MULTI-AGENT STRATEGY DEMO")
    print("="*80)
    
    try:
        # Initialize Telecom orchestrator
        telecom_orchestrator = IndustryMultiAgentOrchestrator("telecom")
        await telecom_orchestrator.initialize()
        
        print(f"✅ Telecom Orchestrator initialized with {len(telecom_orchestrator.agents)} specialized agents")
        print(f"🤖 Using Ollama model: {telecom_orchestrator.industry_specific_models}")
        print(f"📚 Chroma collections: {telecom_orchestrator.chroma_collections}")
        
        # List Telecom agents
        print("\n📋 Telecom Specialized Agents:")
        for agent_id, agent in telecom_orchestrator.agents.items():
            capability = telecom_orchestrator.agent_capabilities.get(agent_id)
            print(f"  • {agent_id}: {capability.specialization if capability else 'General'}")
        
        # Execute Telecom analysis
        print("\n🔍 Executing Telecom Industry Analysis...")
        start_time = datetime.now()
        
        result = await telecom_orchestrator.execute_industry_analysis(
            organization_id="demo-telecom-provider",
            analysis_type="comprehensive"
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Telecom Analysis completed in {execution_time:.2f} seconds")
        print(f"📊 Analysis Results:")
        print(f"  • Industry: {result.get('industry')}")
        print(f"  • Agents Used: {result.get('performance_metrics', {}).get('agents_used', 0)}")
        print(f"  • Tasks Completed: {result.get('performance_metrics', {}).get('tasks_completed', 0)}")
        print(f"  • Ollama Model: {result.get('performance_metrics', {}).get('ollama_model', 'N/A')}")
        
        # Show analysis results
        analysis_results = result.get('analysis_results', {})
        if analysis_results:
            print(f"  • Overall Assessment: {analysis_results.get('overall_assessment', 'N/A')}")
            print(f"  • Compliance Status: {analysis_results.get('compliance_status', 'N/A')}")
            print(f"  • Risk Level: {analysis_results.get('risk_level', 'N/A')}")
            print(f"  • Confidence Score: {analysis_results.get('confidence_score', 0.0):.2f}")
        
        await telecom_orchestrator.cleanup()
        return result
        
    except Exception as e:
        print(f"❌ Telecom Demo failed: {e}")
        return None

async def demo_manufacturing_industry_agents():
    """Demo Manufacturing industry multi-agent strategy"""
    print("\n" + "="*80)
    print("🏭 MANUFACTURING INDUSTRY MULTI-AGENT STRATEGY DEMO")
    print("="*80)
    
    try:
        # Initialize Manufacturing orchestrator
        manufacturing_orchestrator = IndustryMultiAgentOrchestrator("manufacturing")
        await manufacturing_orchestrator.initialize()
        
        print(f"✅ Manufacturing Orchestrator initialized with {len(manufacturing_orchestrator.agents)} specialized agents")
        print(f"🤖 Using Ollama model: {manufacturing_orchestrator.industry_specific_models}")
        print(f"📚 Chroma collections: {manufacturing_orchestrator.chroma_collections}")
        
        # List Manufacturing agents
        print("\n📋 Manufacturing Specialized Agents:")
        for agent_id, agent in manufacturing_orchestrator.agents.items():
            capability = manufacturing_orchestrator.agent_capabilities.get(agent_id)
            print(f"  • {agent_id}: {capability.specialization if capability else 'General'}")
        
        # Execute Manufacturing analysis
        print("\n🔍 Executing Manufacturing Industry Analysis...")
        start_time = datetime.now()
        
        result = await manufacturing_orchestrator.execute_industry_analysis(
            organization_id="demo-manufacturing-plant",
            analysis_type="comprehensive"
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Manufacturing Analysis completed in {execution_time:.2f} seconds")
        print(f"📊 Analysis Results:")
        print(f"  • Industry: {result.get('industry')}")
        print(f"  • Agents Used: {result.get('performance_metrics', {}).get('agents_used', 0)}")
        print(f"  • Tasks Completed: {result.get('performance_metrics', {}).get('tasks_completed', 0)}")
        print(f"  • Ollama Model: {result.get('performance_metrics', {}).get('ollama_model', 'N/A')}")
        
        # Show analysis results
        analysis_results = result.get('analysis_results', {})
        if analysis_results:
            print(f"  • Overall Assessment: {analysis_results.get('overall_assessment', 'N/A')}")
            print(f"  • Compliance Status: {analysis_results.get('compliance_status', 'N/A')}")
            print(f"  • Risk Level: {analysis_results.get('risk_level', 'N/A')}")
            print(f"  • Confidence Score: {analysis_results.get('confidence_score', 0.0):.2f}")
        
        await manufacturing_orchestrator.cleanup()
        return result
        
    except Exception as e:
        print(f"❌ Manufacturing Demo failed: {e}")
        return None

async def demo_healthcare_industry_agents():
    """Demo Healthcare industry multi-agent strategy"""
    print("\n" + "="*80)
    print("🏥 HEALTHCARE INDUSTRY MULTI-AGENT STRATEGY DEMO")
    print("="*80)
    
    try:
        # Initialize Healthcare orchestrator
        healthcare_orchestrator = IndustryMultiAgentOrchestrator("healthcare")
        await healthcare_orchestrator.initialize()
        
        print(f"✅ Healthcare Orchestrator initialized with {len(healthcare_orchestrator.agents)} specialized agents")
        print(f"🤖 Using Ollama model: {healthcare_orchestrator.industry_specific_models}")
        print(f"📚 Chroma collections: {healthcare_orchestrator.chroma_collections}")
        
        # List Healthcare agents
        print("\n📋 Healthcare Specialized Agents:")
        for agent_id, agent in healthcare_orchestrator.agents.items():
            capability = healthcare_orchestrator.agent_capabilities.get(agent_id)
            print(f"  • {agent_id}: {capability.specialization if capability else 'General'}")
        
        # Execute Healthcare analysis
        print("\n🔍 Executing Healthcare Industry Analysis...")
        start_time = datetime.now()
        
        result = await healthcare_orchestrator.execute_industry_analysis(
            organization_id="demo-healthcare-system",
            analysis_type="comprehensive"
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Healthcare Analysis completed in {execution_time:.2f} seconds")
        print(f"📊 Analysis Results:")
        print(f"  • Industry: {result.get('industry')}")
        print(f"  • Agents Used: {result.get('performance_metrics', {}).get('agents_used', 0)}")
        print(f"  • Tasks Completed: {result.get('performance_metrics', {}).get('tasks_completed', 0)}")
        print(f"  • Ollama Model: {result.get('performance_metrics', {}).get('ollama_model', 'N/A')}")
        
        # Show analysis results
        analysis_results = result.get('analysis_results', {})
        if analysis_results:
            print(f"  • Overall Assessment: {analysis_results.get('overall_assessment', 'N/A')}")
            print(f"  • Compliance Status: {analysis_results.get('compliance_status', 'N/A')}")
            print(f"  • Risk Level: {analysis_results.get('risk_level', 'N/A')}")
            print(f"  • Confidence Score: {analysis_results.get('confidence_score', 0.0):.2f}")
        
        await healthcare_orchestrator.cleanup()
        return result
        
    except Exception as e:
        print(f"❌ Healthcare Demo failed: {e}")
        return None

async def demo_cross_industry_analysis():
    """Demo cross-industry analysis"""
    print("\n" + "="*80)
    print("🌐 CROSS-INDUSTRY MULTI-AGENT STRATEGY DEMO")
    print("="*80)
    
    try:
        # Initialize industry manager
        industry_manager = IndustryOrchestratorManager()
        await industry_manager.initialize()
        
        print(f"✅ Industry Manager initialized with {len(industry_manager.industry_orchestrators)} industry orchestrators")
        print(f"🏭 Supported Industries: {', '.join(industry_manager.supported_industries)}")
        
        # Execute cross-industry analysis
        print("\n🔍 Executing Cross-Industry Analysis...")
        start_time = datetime.now()
        
        result = await industry_manager.execute_cross_industry_analysis(
            organization_id="demo-multi-industry-corp",
            industries=["bfsi", "telecom", "manufacturing", "healthcare"],
            analysis_type="comprehensive"
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Cross-Industry Analysis completed in {execution_time:.2f} seconds")
        
        # Show cross-industry results
        cross_industry_analysis = result.get('cross_industry_analysis', {})
        if cross_industry_analysis:
            print(f"📊 Cross-Industry Results:")
            print(f"  • Overall Status: {cross_industry_analysis.get('overall_status', 'N/A')}")
            print(f"  • Overall Compliance Score: {cross_industry_analysis.get('overall_compliance_score', 0.0):.2f}")
            print(f"  • Overall Risk Score: {cross_industry_analysis.get('overall_risk_score', 0.0):.2f}")
            
            analysis_summary = cross_industry_analysis.get('analysis_summary', {})
            print(f"  • Total Industries: {analysis_summary.get('total_industries', 0)}")
            print(f"  • Successful Analyses: {analysis_summary.get('successful_analyses', 0)}")
            print(f"  • Total Issues: {analysis_summary.get('total_issues', 0)}")
            print(f"  • Total Recommendations: {analysis_summary.get('total_recommendations', 0)}")
        
        # Show industry-specific results
        industry_results = result.get('industry_results', {})
        print(f"\n📋 Industry-Specific Results:")
        for industry, industry_result in industry_results.items():
            if "error" not in industry_result:
                performance_metrics = industry_result.get('performance_metrics', {})
                print(f"  • {industry.upper()}: {performance_metrics.get('execution_time', 0):.2f}s, {performance_metrics.get('agents_used', 0)} agents")
            else:
                print(f"  • {industry.upper()}: Failed - {industry_result.get('error', 'Unknown error')}")
        
        await industry_manager.cleanup()
        return result
        
    except Exception as e:
        print(f"❌ Cross-Industry Demo failed: {e}")
        return None

async def demo_comprehensive_industry_report():
    """Demo comprehensive industry report"""
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE INDUSTRY REPORT DEMO")
    print("="*80)
    
    try:
        # Initialize industry manager
        industry_manager = IndustryOrchestratorManager()
        await industry_manager.initialize()
        
        print("✅ Industry Manager initialized")
        
        # Generate comprehensive report
        print("\n🔍 Generating Comprehensive Industry Report...")
        start_time = datetime.now()
        
        result = await industry_manager.get_comprehensive_industry_report(
            organization_id="demo-comprehensive-corp"
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Comprehensive Report generated in {execution_time:.2f} seconds")
        
        # Show report summary
        report_summary = result.get('report_summary', {})
        print(f"📊 Report Summary:")
        print(f"  • Total Industries Analyzed: {report_summary.get('total_industries_analyzed', 0)}")
        print(f"  • Analysis Timestamp: {report_summary.get('analysis_timestamp', 'N/A')}")
        print(f"  • Technologies Used: {', '.join(report_summary.get('technologies_used', []))}")
        
        # Show recommendations
        recommendations = result.get('recommendations', {})
        priority_actions = recommendations.get('priority_actions', [])
        industry_focus = recommendations.get('industry_focus', [])
        
        print(f"\n🎯 Priority Actions:")
        for i, action in enumerate(priority_actions[:3], 1):
            print(f"  {i}. {action}")
        
        print(f"\n🏭 Industry Focus Recommendations:")
        for i, focus in enumerate(industry_focus[:3], 1):
            print(f"  {i}. {focus}")
        
        await industry_manager.cleanup()
        return result
        
    except Exception as e:
        print(f"❌ Comprehensive Report Demo failed: {e}")
        return None

async def main():
    """Main demo function"""
    print("🚀 INDUSTRY MULTI-AGENT STRATEGY DEMO")
    print("Enhanced with Ollama LLM and Chroma Vector Database")
    print("="*80)
    
    demos = [
        ("BFSI Industry Agents", demo_bfsi_industry_agents),
        ("Telecom Industry Agents", demo_telecom_industry_agents),
        ("Manufacturing Industry Agents", demo_manufacturing_industry_agents),
        ("Healthcare Industry Agents", demo_healthcare_industry_agents),
        ("Cross-Industry Analysis", demo_cross_industry_analysis),
        ("Comprehensive Industry Report", demo_comprehensive_industry_report)
    ]
    
    results = {}
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n🎬 Starting {demo_name} Demo...")
            result = await demo_func()
            results[demo_name] = result
            print(f"✅ {demo_name} Demo completed successfully")
        except Exception as e:
            print(f"❌ {demo_name} Demo failed: {e}")
            results[demo_name] = None
    
    # Summary
    print("\n" + "="*80)
    print("📊 DEMO SUMMARY")
    print("="*80)
    
    successful_demos = [name for name, result in results.items() if result is not None]
    failed_demos = [name for name, result in results.items() if result is None]
    
    print(f"✅ Successful Demos: {len(successful_demos)}")
    for demo in successful_demos:
        print(f"  • {demo}")
    
    if failed_demos:
        print(f"\n❌ Failed Demos: {len(failed_demos)}")
        for demo in failed_demos:
            print(f"  • {demo}")
    
    print(f"\n🎉 Industry Multi-Agent Strategy Demo completed!")
    print(f"📈 Success Rate: {len(successful_demos)}/{len(demos)} ({len(successful_demos)/len(demos)*100:.1f}%)")

if __name__ == "__main__":
    asyncio.run(main())
