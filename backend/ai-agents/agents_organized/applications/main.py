"""
GRC Platform AI Agents
Main entry point for industry-specific GRC operations across BFSI, Telecom, Manufacturing, and Healthcare
"""

import asyncio
import logging
import os
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from orchestration.main_orchestrator import GRCPlatformOrchestrator
from shared_components.industry_agent import IndustryType, GRCOperationType
from shared_components.archer_reporting_engine import ReportType, ReportFormat
from shared_components.mcp_broker import MCPBroker
# COMMENTED OUT - Other agents disabled, only BFSI agent active
# from compliance_agent.compliance_agent import ComplianceAgent
# from risk_agent.risk_agent import RiskAgent
# from document_agent.document_agent import DocumentAgent
# from communication_agent.communication_agent import CommunicationAgent
from shared_components.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GRC Platform AI Agents",
    description="AI agents for automated compliance monitoring and risk assessment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
mcp_broker = None
agents = {}
grc_orchestrator = None

@app.on_event("startup")
async def startup_event():
    """Initialize AI agents and MCP broker on startup"""
    global mcp_broker, agents, grc_orchestrator
    
    logger.info("Starting GRC Platform AI Agents...")
    
    try:
        # Initialize MCP broker
        mcp_broker = MCPBroker()
        await mcp_broker.initialize()
        
        # Initialize GRC Orchestrator with industry-specific agents
        grc_orchestrator = GRCPlatformOrchestrator()
        
        # COMMENTED OUT - Legacy AI agents disabled, only BFSI agent active
        # compliance_agent = ComplianceAgent()
        # risk_agent = RiskAgent()
        # document_agent = DocumentAgent()
        # communication_agent = CommunicationAgent()
        
        # COMMENTED OUT - Agent registration disabled
        # await mcp_broker.register_agent("compliance_001", compliance_agent)
        # await mcp_broker.register_agent("risk_001", risk_agent)
        # await mcp_broker.register_agent("document_001", document_agent)
        # await mcp_broker.register_agent("communication_001", communication_agent)
        
        # Only BFSI agent available
        agents = {
            # "compliance": compliance_agent,
            # "risk": risk_agent,
            # "document": document_agent,
            # "communication": communication_agent
        }
        
        # Start listening for messages
        asyncio.create_task(mcp_broker.start_listening())
        
        logger.info("AI Agents and GRC Orchestrator initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize AI agents: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global mcp_broker
    
    if mcp_broker:
        await mcp_broker.cleanup()
    
    logger.info("AI Agents shutdown complete")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GRC Platform AI Agents",
        "version": "1.0.0",
        "status": "running",
        "agents": list(agents.keys())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": {
            name: agent.status for name, agent in agents.items()
        }
    }

@app.post("/agents/compliance/check")
async def run_compliance_check(request: Dict[str, Any]):
    """Run compliance check via compliance agent"""
    try:
        compliance_agent = agents.get("compliance")
        if not compliance_agent:
            raise HTTPException(status_code=500, detail="Compliance agent not available")
        
        result = await compliance_agent.process_message({
            "type": "compliance_check",
            "data": request
        })
        
        return result
        
    except Exception as e:
        logger.error(f"Compliance check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/risk/assess")
async def assess_risk(request: Dict[str, Any]):
    """Assess risk via risk agent"""
    try:
        risk_agent = agents.get("risk")
        if not risk_agent:
            raise HTTPException(status_code=500, detail="Risk agent not available")
        
        result = await risk_agent.process_message({
            "type": "risk_assessment",
            "data": request
        })
        
        return result
        
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/document/analyze")
async def analyze_document(request: Dict[str, Any]):
    """Analyze document via document agent"""
    try:
        document_agent = agents.get("document")
        if not document_agent:
            raise HTTPException(status_code=500, detail="Document agent not available")
        
        result = await document_agent.process_message({
            "type": "document_analysis",
            "data": request
        })
        
        return result
        
    except Exception as e:
        logger.error(f"Document analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/status")
async def get_agents_status():
    """Get status of all agents with mock data fallback"""
    try:
        # Try to get real agent status
        if agents:
            return {
                "platform_status": "operational",
                "total_documents": 1250,
                "agents": {
                    name: {
                        "status": agent.status,
                        "last_activity": agent.last_activity,
                        "agent_id": agent.agent_id,
                        "type": getattr(agent, 'agent_type', 'General'),
                        "performance_score": getattr(agent, 'performance_score', 0.9)
                    }
                    for name, agent in agents.items()
                }
            }
        else:
            # Return mock data if no agents are available
            return {
                "platform_status": "operational",
                "total_documents": 1250,
                "agents": {
                    "bfsi_compliance_agent": {
                        "status": "active",
                        "last_activity": "2024-09-16T10:30:00Z",
                        "agent_id": "AGENT-BFSI-001",
                        "type": "Compliance",
                        "performance_score": 0.94
                    },
                    "healthcare_hipaa_agent": {
                        "status": "active",
                        "last_activity": "2024-09-16T10:25:00Z",
                        "agent_id": "AGENT-HC-001",
                        "type": "Compliance",
                        "performance_score": 0.93
                    },
                    "manufacturing_quality_agent": {
                        "status": "active",
                        "last_activity": "2024-09-16T10:20:00Z",
                        "agent_id": "AGENT-MFG-001",
                        "type": "Quality Control",
                        "performance_score": 0.92
                    },
                    "telecom_network_agent": {
                        "status": "active",
                        "last_activity": "2024-09-16T10:15:00Z",
                        "agent_id": "AGENT-TEL-001",
                        "type": "Network Monitoring",
                        "performance_score": 0.94
                    },
                    "risk_assessment_agent": {
                        "status": "active",
                        "last_activity": "2024-09-16T10:10:00Z",
                        "agent_id": "AGENT-RISK-001",
                        "type": "Risk Assessment",
                        "performance_score": 0.91
                    }
                },
                "mock_data": True
            }
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        # Return basic mock data on error
        return {
            "platform_status": "operational",
            "total_documents": 1250,
            "agents": {
                "general_compliance_agent": {
                    "status": "active",
                    "last_activity": "2024-09-16T10:00:00Z",
                    "agent_id": "AGENT-GEN-001",
                    "type": "General",
                    "performance_score": 0.9
                }
            },
            "mock_data": True,
            "error": str(e)
        }

# Industry-Specific GRC Endpoints

@app.get("/grc/status")
async def get_grc_platform_status():
    """Get overall GRC platform status"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        status = await grc_orchestrator.get_platform_status()
        return status
        
    except Exception as e:
        logger.error(f"Failed to get GRC platform status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/grc/industries")
async def get_supported_industries():
    """Get list of supported industries - Only BFSI active"""
    return {
        "industries": [
            {"id": "bfsi", "name": "Banking, Financial Services, Insurance", "status": "active"}
            # COMMENTED OUT - Other industries disabled
            # {"id": "telecom", "name": "Telecommunications", "status": "disabled"},
            # {"id": "manufacturing", "name": "Manufacturing", "status": "disabled"},
            # {"id": "healthcare", "name": "Healthcare", "status": "disabled"}
        ]
    }

@app.get("/grc/industry/{industry}/status")
async def get_industry_status(industry: str):
    """Get status of BFSI industry only"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        # Only BFSI industry supported
        if industry.lower() != "bfsi":
            raise HTTPException(status_code=400, detail=f"Only BFSI industry is supported. Requested: {industry}")
        
        industry_type = IndustryType(industry)
        status = await grc_orchestrator.get_industry_status(industry_type)
        return status
        
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid industry: {industry}")
    except Exception as e:
        logger.error(f"Failed to get BFSI industry status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/industry/{industry}/risk-assessment")
async def perform_risk_assessment(industry: str, request: Dict[str, Any]):
    """Perform risk assessment for BFSI industry only"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        # Only BFSI industry supported
        if industry.lower() != "bfsi":
            raise HTTPException(status_code=400, detail=f"Only BFSI industry is supported. Requested: {industry}")
        
        industry_type = IndustryType(industry)
        business_unit = request.get("business_unit", "all")
        risk_scope = request.get("risk_scope", "full")
        
        result = await grc_orchestrator.perform_risk_assessment(
            industry_type, business_unit, risk_scope
        )
        return result
        
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid industry: {industry}")
    except Exception as e:
        logger.error(f"BFSI risk assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/industry/{industry}/compliance-check")
async def perform_compliance_check(industry: str, request: Dict[str, Any]):
    """Perform compliance check for BFSI industry only"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        # Only BFSI industry supported
        if industry.lower() != "bfsi":
            raise HTTPException(status_code=400, detail=f"Only BFSI industry is supported. Requested: {industry}")
        
        industry_type = IndustryType(industry)
        framework = request.get("framework", "all")
        business_unit = request.get("business_unit", "all")
        
        result = await grc_orchestrator.perform_compliance_check(
            industry_type, framework, business_unit
        )
        return result
        
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid industry: {industry}")
    except Exception as e:
        logger.error(f"BFSI compliance check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/industry/{industry}/assessment")
async def perform_grc_assessment(industry: str, request: Dict[str, Any]):
    """Perform comprehensive GRC assessment for BFSI industry only"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        # Only BFSI industry supported
        if industry.lower() != "bfsi":
            raise HTTPException(status_code=400, detail=f"Only BFSI industry is supported. Requested: {industry}")
        
        industry_type = IndustryType(industry)
        assessment_type = request.get("assessment_type", "comprehensive")
        context = request.get("context", {})
        
        result = await grc_orchestrator.perform_grc_assessment(
            industry_type, assessment_type, context
        )
        return result
        
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid industry: {industry}")
    except Exception as e:
        logger.error(f"BFSI GRC assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/multi-industry/assessment")
async def perform_multi_industry_assessment(request: Dict[str, Any]):
    """Perform BFSI assessment only - multi-industry disabled"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        # Only allow BFSI industry
        requested_industries = request.get("industries", [])
        if not requested_industries or requested_industries != ["bfsi"]:
            raise HTTPException(status_code=400, detail="Only BFSI industry is supported")
        
        industries = [IndustryType(ind) for ind in requested_industries]
        assessment_type = request.get("assessment_type", "comprehensive")
        context = request.get("context", {})
        
        result = await grc_orchestrator.perform_multi_industry_assessment(
            industries, assessment_type, context
        )
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid industry: {e}")
    except Exception as e:
        logger.error(f"BFSI assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/industry/{industry}/report")
async def generate_industry_report(industry: str, request: Dict[str, Any]):
    """Generate BFSI-specific GRC report only"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        # Only BFSI industry supported
        if industry.lower() != "bfsi":
            raise HTTPException(status_code=400, detail=f"Only BFSI industry is supported. Requested: {industry}")
        
        industry_type = IndustryType(industry)
        report_type = ReportType(request.get("report_type", "executive_summary"))
        data = request.get("data", {})
        format = ReportFormat(request.get("format", "pdf"))
        
        result = await grc_orchestrator.generate_industry_report(
            industry_type, report_type, data, format
        )
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {e}")
    except Exception as e:
        logger.error(f"BFSI report generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/grc/workflows")
async def get_workflow_templates():
    """Get available workflow templates"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        templates = await grc_orchestrator.workflow_engine.get_workflow_templates()
        return {"templates": templates}
        
    except Exception as e:
        logger.error(f"Failed to get workflow templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/demo")
async def run_demo_workflow():
    """Run demonstration workflow across all industries"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        result = await grc_orchestrator.run_demo_workflow()
        return result
        
    except Exception as e:
        logger.error(f"Demo workflow failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# BFSI Policy Management Endpoints

@app.get("/grc/industry/bfsi/policy-standards")
async def get_bfsi_policy_standards():
    """Get available BFSI industry standard policies"""
    try:
        # Return predefined BFSI industry standard policies
        policy_standards = [
            {
                "id": "basel_iii",
                "name": "Basel III Capital Requirements",
                "description": "International regulatory framework for bank capital adequacy",
                "category": "Capital Adequacy",
                "requirements": "Minimum capital ratios, leverage ratios, liquidity requirements",
                "compliance_level": "critical"
            },
            {
                "id": "sox",
                "name": "Sarbanes-Oxley Act (SOX)",
                "description": "Corporate governance and financial disclosure requirements",
                "category": "Corporate Governance",
                "requirements": "Internal controls, financial reporting, audit requirements",
                "compliance_level": "critical"
            },
            {
                "id": "pci_dss",
                "name": "PCI DSS",
                "description": "Payment Card Industry Data Security Standard",
                "category": "Data Security",
                "requirements": "Cardholder data protection, network security, access controls",
                "compliance_level": "high"
            },
            {
                "id": "aml_kyc",
                "name": "AML/KYC Requirements",
                "description": "Anti-Money Laundering and Know Your Customer regulations",
                "category": "Anti-Money Laundering",
                "requirements": "Customer due diligence, transaction monitoring, suspicious activity reporting",
                "compliance_level": "critical"
            },
            {
                "id": "gdpr",
                "name": "GDPR Compliance",
                "description": "General Data Protection Regulation for EU customers",
                "category": "Data Privacy",
                "requirements": "Data protection, consent management, breach notification",
                "compliance_level": "high"
            },
            {
                "id": "ifrs",
                "name": "IFRS Standards",
                "description": "International Financial Reporting Standards",
                "category": "Financial Reporting",
                "requirements": "Standardized financial reporting, disclosure requirements",
                "compliance_level": "high"
            }
        ]
        
        return {"policy_standards": policy_standards}
        
    except Exception as e:
        logger.error(f"Failed to get BFSI policy standards: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/industry/bfsi/policies")
async def add_bfsi_policy(policy_data: Dict[str, Any]):
    """Add a new BFSI policy (industry standard or custom)"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        policy_type = policy_data.get("policy_type", "custom")
        policy_info = policy_data.get("policy_data", {})
        
        # Get BFSI agent from orchestrator
        bfsi_agent = grc_orchestrator.industry_agents.get(IndustryType.BFSI)
        if not bfsi_agent:
            raise HTTPException(status_code=500, detail="BFSI agent not available")
        
        # Add policy to BFSI agent
        if policy_type == "industry_standard":
            # Apply industry standard policy
            result = await bfsi_agent.apply_industry_standard_policy(policy_info)
        else:
            # Add custom policy
            result = await bfsi_agent.add_custom_policy(policy_info)
        
        return {
            "message": f"{policy_type} policy added successfully",
            "policy_id": result.get("policy_id"),
            "policy_info": policy_info
        }
        
    except Exception as e:
        logger.error(f"Failed to add BFSI policy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/grc/industry/bfsi/policies")
async def get_bfsi_policies():
    """Get all BFSI policies"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        # Get BFSI agent from orchestrator
        bfsi_agent = grc_orchestrator.industry_agents.get(IndustryType.BFSI)
        if not bfsi_agent:
            raise HTTPException(status_code=500, detail="BFSI agent not available")
        
        # Get policies from BFSI agent
        policies = await bfsi_agent.get_policies()
        
        return {"policies": policies}
        
    except Exception as e:
        logger.error(f"Failed to get BFSI policies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grc/industry/bfsi/operation")
async def execute_bfsi_operation(operation_data: Dict[str, Any]):
    """Execute BFSI-specific operation"""
    try:
        if not grc_orchestrator:
            raise HTTPException(status_code=500, detail="GRC orchestrator not available")
        
        operation_type = operation_data.get("operation_type")
        context = operation_data.get("context", {})
        operation_info = operation_data.get("operation_data", {})
        
        # Get BFSI agent from orchestrator
        bfsi_agent = grc_orchestrator.industry_agents.get(IndustryType.BFSI)
        if not bfsi_agent:
            raise HTTPException(status_code=500, detail="BFSI agent not available")
        
        # Execute operation on BFSI agent
        result = await bfsi_agent.execute_enhanced_operation(
            operation_type=operation_type,
            context=context,
            data=operation_info
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to execute BFSI operation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
