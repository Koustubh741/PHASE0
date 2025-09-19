"""
GRC Platform AI Agents Main Orchestrator
Coordinates industry-specific GRC operations across BFSI, Telecom, Manufacturing, and Healthcare
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from core.industry_agent import IndustryType, GRCOperationType
from core.grc_workflow_engine import GRCWorkflowEngine
from core.archer_reporting_engine import ArcherReportingEngine, ReportType, ReportFormat
from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
from agents.telecom.telecom_grc_agent import TelecomGRCAgent
from agents.manufacturing.manufacturing_grc_agent import ManufacturingGRCAgent
from agents.healthcare.healthcare_grc_agent import HealthcareGRCAgent

class GRCPlatformOrchestrator:
    """
    Main orchestrator for GRC Platform AI Agents
    Manages industry-specific GRC operations and reporting
    """
    
    def __init__(self):
        self.workflow_engine = GRCWorkflowEngine()
        self.reporting_engine = ArcherReportingEngine()
        self.industry_agents = {}
        
        # Initialize industry agents
        self._initialize_industry_agents()
        
        # Register agents with workflow engine
        self._register_agents()
        
        logging.info("GRC Platform Orchestrator initialized")

    def _initialize_industry_agents(self):
        """Initialize all industry-specific GRC agents"""
        try:
            self.industry_agents[IndustryType.BFSI] = BFSIGRCAgent()
            self.industry_agents[IndustryType.TELECOM] = TelecomGRCAgent()
            self.industry_agents[IndustryType.MANUFACTURING] = ManufacturingGRCAgent()
            self.industry_agents[IndustryType.HEALTHCARE] = HealthcareGRCAgent()
            
            logging.info("All industry agents initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing industry agents: {str(e)}")
            raise

    def _register_agents(self):
        """Register agents with workflow engine"""
        for industry, agent in self.industry_agents.items():
            asyncio.create_task(self.workflow_engine.register_industry_agent(industry, agent))
        
        logging.info("All agents registered with workflow engine")

    async def perform_grc_assessment(self, industry: IndustryType, 
                                   assessment_type: str = "comprehensive",
                                   context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform comprehensive GRC assessment for a specific industry
        """
        if context is None:
            context = {}
        
        logging.info(f"Starting {assessment_type} GRC assessment for {industry.value}")
        
        try:
            # Create workflow based on assessment type
            workflow_id = await self.workflow_engine.create_workflow(
                assessment_type, industry, context
            )
            
            # Execute workflow
            result = await self.workflow_engine.execute_workflow(workflow_id)
            
            # Generate comprehensive report
            report = await self._generate_assessment_report(industry, result)
            
            return {
                "success": True,
                "industry": industry.value,
                "assessment_type": assessment_type,
                "workflow_id": workflow_id,
                "workflow_result": result,
                "assessment_report": report,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error in GRC assessment: {str(e)}")
            return {
                "success": False,
                "industry": industry.value,
                "assessment_type": assessment_type,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def perform_multi_industry_assessment(self, industries: List[IndustryType],
                                              assessment_type: str = "comprehensive",
                                              context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform GRC assessment across multiple industries
        """
        if context is None:
            context = {}
        
        logging.info(f"Starting multi-industry {assessment_type} assessment for {len(industries)} industries")
        
        results = {}
        
        # Execute assessments in parallel
        tasks = []
        for industry in industries:
            task = self.perform_grc_assessment(industry, assessment_type, context)
            tasks.append(task)
        
        # Wait for all assessments to complete
        assessment_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, industry in enumerate(industries):
            result = assessment_results[i]
            if isinstance(result, Exception):
                results[industry.value] = {
                    "success": False,
                    "error": str(result)
                }
            else:
                results[industry.value] = result
        
        # Generate consolidated report
        consolidated_report = await self._generate_consolidated_report(results)
        
        return {
            "success": True,
            "assessment_type": assessment_type,
            "industries_assessed": [ind.value for ind in industries],
            "individual_results": results,
            "consolidated_report": consolidated_report,
            "timestamp": datetime.now().isoformat()
        }

    async def generate_industry_report(self, industry: IndustryType,
                                     report_type: ReportType,
                                     data: Dict[str, Any] = None,
                                     format: ReportFormat = ReportFormat.PDF) -> Dict[str, Any]:
        """
        Generate industry-specific GRC report
        """
        if data is None:
            data = {}
        
        logging.info(f"Generating {report_type.value} report for {industry.value}")
        
        try:
            # Generate report using Archer reporting engine
            report = await self.reporting_engine.generate_report(
                report_type, industry.value, data, format
            )
            
            return {
                "success": True,
                "industry": industry.value,
                "report_type": report_type.value,
                "format": format.value,
                "report": report,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error generating report: {str(e)}")
            return {
                "success": False,
                "industry": industry.value,
                "report_type": report_type.value,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def perform_risk_assessment(self, industry: IndustryType,
                                    business_unit: str = "all",
                                    risk_scope: str = "full") -> Dict[str, Any]:
        """
        Perform industry-specific risk assessment
        """
        logging.info(f"Starting risk assessment for {industry.value} - {business_unit}")
        
        try:
            agent = self.industry_agents[industry]
            
            context = {
                "business_unit": business_unit,
                "risk_scope": risk_scope,
                "assessment_date": datetime.now().isoformat()
            }
            
            # Perform risk assessment
            result = await agent.perform_grc_operation(
                GRCOperationType.RISK_ASSESSMENT, context
            )
            
            return {
                "success": True,
                "industry": industry.value,
                "business_unit": business_unit,
                "risk_scope": risk_scope,
                "risk_assessment": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error in risk assessment: {str(e)}")
            return {
                "success": False,
                "industry": industry.value,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def perform_compliance_check(self, industry: IndustryType,
                                     framework: str = "all",
                                     business_unit: str = "all") -> Dict[str, Any]:
        """
        Perform industry-specific compliance check
        """
        logging.info(f"Starting compliance check for {industry.value} - {framework}")
        
        try:
            agent = self.industry_agents[industry]
            
            context = {
                "framework": framework,
                "business_unit": business_unit,
                "check_scope": "full",
                "check_date": datetime.now().isoformat()
            }
            
            # Perform compliance check
            result = await agent.perform_grc_operation(
                GRCOperationType.COMPLIANCE_CHECK, context
            )
            
            return {
                "success": True,
                "industry": industry.value,
                "framework": framework,
                "business_unit": business_unit,
                "compliance_check": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error in compliance check: {str(e)}")
            return {
                "success": False,
                "industry": industry.value,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def get_industry_status(self, industry: IndustryType) -> Dict[str, Any]:
        """
        Get current status of GRC operations for an industry
        """
        try:
            agent = self.industry_agents[industry]
            
            # Get industry KPIs
            kpis = agent._get_industry_kpis()
            
            # Get recent workflow status
            workflows = await self.workflow_engine.list_workflows(industry=industry.value)
            
            return {
                "success": True,
                "industry": industry.value,
                "status": "operational",
                "kpis": kpis,
                "recent_workflows": workflows,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error getting industry status: {str(e)}")
            return {
                "success": False,
                "industry": industry.value,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def get_platform_status(self) -> Dict[str, Any]:
        """
        Get overall platform status across all industries
        """
        try:
            industry_status = {}
            
            # Get status for all industries
            for industry in IndustryType:
                status = await self.get_industry_status(industry)
                industry_status[industry.value] = status
            
            # Get overall workflow statistics
            all_workflows = await self.workflow_engine.list_workflows()
            
            # Calculate platform metrics
            total_workflows = len(all_workflows)
            completed_workflows = len([w for w in all_workflows if w["status"] == "completed"])
            running_workflows = len([w for w in all_workflows if w["status"] == "running"])
            
            return {
                "success": True,
                "platform_status": "operational",
                "industries": industry_status,
                "workflow_statistics": {
                    "total_workflows": total_workflows,
                    "completed_workflows": completed_workflows,
                    "running_workflows": running_workflows,
                    "success_rate": (completed_workflows / total_workflows * 100) if total_workflows > 0 else 0
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error getting platform status: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _generate_assessment_report(self, industry: IndustryType, 
                                        workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive assessment report"""
        try:
            # Extract data from workflow result
            data = {
                "workflow_results": workflow_result.get("results", {}),
                "workflow_status": workflow_result.get("status", "unknown"),
                "workflow_duration": workflow_result.get("duration", "unknown")
            }
            
            # Generate executive summary report
            report = await self.reporting_engine.generate_report(
                ReportType.EXECUTIVE_SUMMARY, industry.value, data, ReportFormat.PDF
            )
            
            return report
            
        except Exception as e:
            logging.error(f"Error generating assessment report: {str(e)}")
            return {"error": str(e)}

    async def _generate_consolidated_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate consolidated report across multiple industries"""
        try:
            consolidated_data = {
                "multi_industry_results": results,
                "summary": {
                    "total_industries": len(results),
                    "successful_assessments": len([r for r in results.values() if r.get("success", False)]),
                    "failed_assessments": len([r for r in results.values() if not r.get("success", False)])
                }
            }
            
            # Generate trend analysis report
            report = await self.reporting_engine.generate_report(
                ReportType.TREND_ANALYSIS, "multi_industry", consolidated_data, ReportFormat.PDF
            )
            
            return report
            
        except Exception as e:
            logging.error(f"Error generating consolidated report: {str(e)}")
            return {"error": str(e)}

    async def run_demo_workflow(self) -> Dict[str, Any]:
        """
        Run a demonstration workflow across all industries
        """
        logging.info("Running demo workflow across all industries")
        
        try:
            # Run comprehensive assessment for all industries
            industries = [IndustryType.BFSI, IndustryType.TELECOM, 
                         IndustryType.MANUFACTURING, IndustryType.HEALTHCARE]
            
            result = await self.perform_multi_industry_assessment(
                industries, "comprehensive_grc_assessment"
            )
            
            # Generate demo reports
            demo_reports = {}
            for industry in industries:
                industry_result = result["individual_results"].get(industry.value, {})
                if industry_result.get("success", False):
                    report = await self.generate_industry_report(
                        industry, ReportType.EXECUTIVE_SUMMARY
                    )
                    demo_reports[industry.value] = report
            
            return {
                "success": True,
                "demo_type": "comprehensive_grc_assessment",
                "industries": [ind.value for ind in industries],
                "assessment_result": result,
                "demo_reports": demo_reports,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error in demo workflow: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Main execution function
async def main():
    """Main function to demonstrate GRC Platform capabilities"""
    print("🤖 GRC Platform AI Agents - Starting Demo")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = GRCPlatformOrchestrator()
    
    # Get platform status
    print("\n📊 Getting Platform Status...")
    platform_status = await orchestrator.get_platform_status()
    print(f"Platform Status: {platform_status.get('platform_status', 'Unknown')}")
    print(f"Industries: {list(platform_status.get('industries', {}).keys())}")
    
    # Run demo workflow
    print("\n🚀 Running Demo Workflow...")
    demo_result = await orchestrator.run_demo_workflow()
    
    if demo_result.get("success", False):
        print("✅ Demo workflow completed successfully!")
        print(f"Industries assessed: {demo_result.get('industries', [])}")
        
        # Show sample results
        individual_results = demo_result.get("assessment_result", {}).get("individual_results", {})
        for industry, result in individual_results.items():
            if result.get("success", False):
                workflow_result = result.get("workflow_result", {})
                print(f"\n{industry.upper()} Results:")
                print(f"  Status: {workflow_result.get('status', 'Unknown')}")
                print(f"  Duration: {workflow_result.get('duration', 'Unknown')}")
    else:
        print("❌ Demo workflow failed!")
        print(f"Error: {demo_result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("🎉 GRC Platform AI Agents Demo Complete!")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run main function
    asyncio.run(main())
