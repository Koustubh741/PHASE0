"""
GRC Platform AI Agents Main Orchestrator
Coordinates industry-specific GRC operations across BFSI, Telecom, Manufacturing, and Healthcare
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from shared_components.industry_agent import IndustryType, GRCOperationType
from bfsi_agent.bfsi_grc_agent import BFSIGRCAgent
# COMMENTED OUT - Other industry agents disabled, only BFSI agent active
# from telecom_agent.telecom_grc_agent import TelecomGRCAgent
# from manufacturing_agent.manufacturing_grc_agent import ManufacturingGRCAgent
# from healthcare_agent.healthcare_grc_agent import HealthcareGRCAgent
# from compliance_agent.compliance_agent import ComplianceAgent
# from risk_agent.risk_agent import RiskAgent
# from document_agent.document_agent import DocumentAgent
# from communication_agent.communication_agent import CommunicationAgent

class GRCPlatformOrchestrator:
    """
    Main orchestrator for GRC Platform AI Agents
    Manages industry-specific GRC operations and reporting
    """
    
    def __init__(self):
        self.workflow_engine = None  # GRCWorkflowEngine()
        self.reporting_engine = None  # ArcherReportingEngine()
        self.industry_agents = {}
        self.compliance_agent = None
        self.risk_agent = None
        self.document_agent = None
        self.communication_agent = None
        
        # Initialize industry agents
        self._initialize_industry_agents()
        
        # Initialize specialized agents
        self._initialize_specialized_agents()
        
        # Register agents with workflow engine
        self._register_agents()
        
        logging.info("GRC Platform Orchestrator initialized")

    def _initialize_industry_agents(self):
        """Initialize BFSI industry-specific GRC agents only"""
        try:
            # Only initialize BFSI agent - other agents commented out
            self.industry_agents[IndustryType.BFSI] = BFSIGRCAgent()
            
            # COMMENTED OUT - Other industry agents disabled
            # self.industry_agents[IndustryType.TELECOM] = TelecomGRCAgent()
            # self.industry_agents[IndustryType.MANUFACTURING] = ManufacturingGRCAgent()
            # self.industry_agents[IndustryType.HEALTHCARE] = HealthcareGRCAgent()
            # self.compliance_agent = ComplianceAgent()
            
            logging.info("BFSI industry agent initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing BFSI industry agent: {str(e)}")
            raise

    def _initialize_specialized_agents(self):
        """Initialize specialized agents (Risk, Document, Communication) - COMMENTED OUT"""
        try:
            # COMMENTED OUT - Specialized agents disabled, only BFSI agent active
            # self.risk_agent = RiskAgent()
            # self.document_agent = DocumentAgent()
            # self.communication_agent = CommunicationAgent()
            
            logging.info("Specialized agents initialization skipped - only BFSI agent active")
        except Exception as e:
            logging.error(f"Error in specialized agents initialization: {str(e)}")
            # Don't raise - just log the error since agents are commented out

    def _register_agents(self):
        """Register BFSI agent with workflow engine only"""
        try:
            if self.workflow_engine:
                # Only register BFSI agent
                for industry_type, agent in self.industry_agents.items():
                    self.workflow_engine.register_agent(agent)
                
                # COMMENTED OUT - Other agents disabled
                # self.workflow_engine.register_agent(self.compliance_agent)
                # self.workflow_engine.register_agent(self.risk_agent)
                # self.workflow_engine.register_agent(self.document_agent)
                # self.workflow_engine.register_agent(self.communication_agent)
                logging.info("BFSI agent registered with workflow engine")
        except Exception as e:
            logging.error(f"Error registering BFSI agent: {str(e)}")

    async def perform_industry_operation(self, industry: str, operation_type: str, 
                                       context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform GRC operation for specific industry"""
        try:
            # Map string to IndustryType enum - Only BFSI supported
            industry_mapping = {
                "bfsi": IndustryType.BFSI,
                # COMMENTED OUT - Other industries disabled
                # "telecom": IndustryType.TELECOM,
                # "manufacturing": IndustryType.MANUFACTURING,
                # "healthcare": IndustryType.HEALTHCARE
            }
            
            industry_type = industry_mapping.get(industry.lower())
            if not industry_type:
                return {
                    "success": False,
                    "error": f"Unsupported industry: {industry}",
                    "supported_industries": list(industry_mapping.keys())
                }
            
            # Get the appropriate agent
            agent = self.industry_agents.get(industry_type)
            if not agent:
                return {
                    "success": False,
                    "error": f"Agent not found for industry: {industry}"
                }
            
            # Map string to GRCOperationType enum
            operation_mapping = {
                "risk_assessment": GRCOperationType.RISK_ASSESSMENT,
                "compliance_check": GRCOperationType.COMPLIANCE_CHECK,
                "policy_review": GRCOperationType.POLICY_REVIEW,
                "audit_planning": GRCOperationType.AUDIT_PLANNING,
                "incident_response": GRCOperationType.INCIDENT_RESPONSE,
                "regulatory_reporting": GRCOperationType.REGULATORY_REPORTING
            }
            
            grc_operation = operation_mapping.get(operation_type.lower())
            if not grc_operation:
                return {
                    "success": False,
                    "error": f"Unsupported operation type: {operation_type}",
                    "supported_operations": list(operation_mapping.keys())
                }
            
            # Perform the operation
            result = await agent.perform_grc_operation(grc_operation, context)
            
            # Add orchestrator metadata
            result["orchestrator"] = {
                "name": "GRC Platform Orchestrator",
                "timestamp": datetime.now().isoformat(),
                "industry": industry,
                "operation_type": operation_type
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Error performing industry operation: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "orchestrator": "GRC Platform Orchestrator"
            }

    async def perform_cross_industry_operation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform GRC operation across multiple industries"""
        try:
            industries = context.get("industries", [])
            operation_type = context.get("operation_type")
            operation_context = context.get("context", {})
            
            if not industries:
                return {
                    "success": False,
                    "error": "No industries specified for cross-industry operation"
                }
            
            if not operation_type:
                return {
                    "success": False,
                    "error": "No operation type specified"
                }
            
            # Perform operation for each industry
            results = {}
            for industry in industries:
                result = await self.perform_industry_operation(
                    industry, operation_type, operation_context
                )
                results[industry] = result
            
            # Aggregate results
            aggregated_result = {
                "success": True,
                "operation": "cross_industry_operation",
                "operation_type": operation_type,
                "industries": industries,
                "individual_results": results,
                "summary": self._generate_cross_industry_summary(results),
                "executed_at": datetime.now().isoformat(),
                "orchestrator": "GRC Platform Orchestrator"
            }
            
            return aggregated_result
            
        except Exception as e:
            logging.error(f"Error performing cross-industry operation: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "orchestrator": "GRC Platform Orchestrator"
            }

    def _generate_cross_industry_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of cross-industry operation results"""
        summary = {
            "total_industries": len(results),
            "successful_operations": 0,
            "failed_operations": 0,
            "common_risks": [],
            "common_compliance_issues": [],
            "recommendations": []
        }
        
        for industry, result in results.items():
            if result.get("success", False):
                summary["successful_operations"] += 1
            else:
                summary["failed_operations"] += 1
        
        return summary

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        try:
            status = {
                "orchestrator": "GRC Platform Orchestrator",
                "timestamp": datetime.now().isoformat(),
                "agents": {}
            }
            
            # Check industry agents
            for industry_type, agent in self.industry_agents.items():
                status["agents"][industry_type.value] = {
                    "name": agent.name,
                    "agent_id": agent.agent_id,
                    "status": "active",
                    "industry": industry_type.value,
                    "regulatory_bodies": agent.regulatory_bodies
                }
            
            # COMMENTED OUT - Compliance agent disabled
            # if self.compliance_agent:
            #     status["agents"]["compliance"] = {
            #         "name": self.compliance_agent.name,
            #         "agent_id": self.compliance_agent.agent_id,
            #         "status": "active",
            #         "type": "general_compliance"
            #     }
            
            return status
            
        except Exception as e:
            logging.error(f"Error getting agent status: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "orchestrator": "GRC Platform Orchestrator"
            }

    async def perform_compliance_check(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform compliance check using BFSI agent only - compliance agent disabled"""
        try:
            # Use BFSI agent for compliance checks instead of dedicated compliance agent
            bfsi_agent = self.industry_agents.get(IndustryType.BFSI)
            if not bfsi_agent:
                return {
                    "success": False,
                    "error": "BFSI agent not available"
                }
            
            # Perform compliance check using BFSI agent
            result = await bfsi_agent.execute_enhanced_operation("compliance_check", context)
            
            # Add orchestrator metadata
            result["orchestrator"] = {
                "name": "GRC Platform Orchestrator (BFSI Only)",
                "timestamp": datetime.now().isoformat(),
                "agent_type": "bfsi_compliance"
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Error performing BFSI compliance check: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "orchestrator": "GRC Platform Orchestrator (BFSI Only)"
            }

    async def shutdown(self):
        """Shutdown BFSI orchestrator and agents only"""
        try:
            logging.info("Shutting down GRC Platform Orchestrator (BFSI Only)...")
            
            # Shutdown BFSI agent only
            for industry_type, agent in self.industry_agents.items():
                if hasattr(agent, 'shutdown'):
                    await agent.shutdown()
            
            # COMMENTED OUT - Specialized agents disabled
            # if self.compliance_agent and hasattr(self.compliance_agent, 'shutdown'):
            #     await self.compliance_agent.shutdown()
            
            logging.info("GRC Platform Orchestrator (BFSI Only) shutdown complete")
            
        except Exception as e:
            logging.error(f"Error during BFSI shutdown: {str(e)}")

# Global orchestrator instance
orchestrator = GRCPlatformOrchestrator()
