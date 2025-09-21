"""
GRC Platform AI Agents
Main entry point for industry-specific GRC operations across BFSI, Telecom, Manufacturing, and Healthcare
"""

import asyncio
import logging
import os
import uuid
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from orchestration.legacy_main_orchestrator import GRCPlatformOrchestrator
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
        
        # Initialize MCP-enabled BFSI agents
        from bfsi_agent.bfsi_mcp_subagents import (
            initialize_all_bfsi_mcp_agents, 
            register_agents_with_mcp_broker,
            BFSIMCPAgentFactory
        )
        
        # Create and initialize all BFSI MCP agents
        bfsi_agents = await initialize_all_bfsi_mcp_agents()
        
        # Register BFSI agents with MCP broker
        registration_results = await register_agents_with_mcp_broker(bfsi_agents, mcp_broker)
        
        # Log registration results
        for agent_id, success in registration_results.items():
            if success:
                logger.info(f"✅ BFSI Agent {agent_id} registered successfully")
            else:
                logger.error(f"❌ Failed to register BFSI Agent {agent_id}")
        
        # Store agents for API access
        agents = bfsi_agents
        
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
    """Get status of all agents including MCP-enabled BFSI agents"""
    try:
        # Try to get real agent status
        if agents:
            agent_statuses = {}
            for agent_id, agent in agents.items():
                if hasattr(agent, 'get_health_status'):
                    # MCP-enabled BFSI agents
                    agent_statuses[agent_id] = agent.get_health_status()
                else:
                    # Legacy agents or fallback
                    agent_statuses[agent_id] = {
                        "agent_id": agent_id,
                        "name": getattr(agent, 'name', 'Unknown'),
                        "status": getattr(agent, 'status', 'unknown'),
                        "last_activity": getattr(agent, 'last_activity', None),
                        "agent_type": getattr(agent, 'agent_type', 'General'),
                        "performance_metrics": getattr(agent, 'performance_metrics', {})
                    }
            
            # Get MCP broker status
            mcp_status = {
                "status": "active" if mcp_broker else "inactive",
                "registered_agents": mcp_broker.get_registered_agents() if mcp_broker else [],
                "is_listening": mcp_broker.is_running if mcp_broker else False
            }
            
            return {
                "platform_status": "operational",
                "total_documents": 1250,
                "agents": agent_statuses,
                "mcp_broker": mcp_status,
                "bfsi_mcp_enabled": True,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Return empty data if no agents are available
            return {
                "platform_status": "operational",
                "total_documents": 0,
                "agents": {},
                "mcp_broker": {"status": "inactive"},
                "bfsi_mcp_enabled": False
            }
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        # Return error response
        return {
            "platform_status": "error",
            "total_documents": 0,
            "agents": {},
            "mcp_broker": {"status": "error"},
            "error": str(e)
        }

# MCP-Specific Endpoints

@app.get("/mcp/status")
async def get_mcp_status():
    """Get MCP broker and agent communication status"""
    try:
        if not mcp_broker:
            raise HTTPException(status_code=500, detail="MCP broker not available")
        
        return {
            "mcp_broker_status": "active",
            "registered_agents": mcp_broker.get_registered_agents(),
            "is_listening": mcp_broker.is_running,
            "total_agents": len(mcp_broker.get_registered_agents()),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting MCP status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/agents")
async def get_mcp_agents():
    """Get detailed information about all MCP-enabled agents"""
    try:
        if not agents:
            return {"agents": [], "total": 0}
        
        agent_details = []
        for agent_id, agent in agents.items():
            if hasattr(agent, 'get_health_status'):
                agent_info = agent.get_health_status()
                agent_details.append(agent_info)
        
        return {
            "agents": agent_details,
            "total": len(agent_details),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting MCP agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/message")
async def send_mcp_message(request: Dict[str, Any]):
    """Send a message via MCP protocol"""
    try:
        if not mcp_broker:
            raise HTTPException(status_code=500, detail="MCP broker not available")
        
        # Validate message structure
        required_fields = ["message_id", "timestamp", "source_agent", "message_type"]
        for field in required_fields:
            if field not in request:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Send message via MCP broker
        await mcp_broker.send_message(request)
        
        return {
            "status": "sent",
            "message_id": request.get("message_id"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error sending MCP message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/broadcast")
async def broadcast_mcp_message(request: Dict[str, Any]):
    """Broadcast a message to all MCP agents"""
    try:
        if not mcp_broker:
            raise HTTPException(status_code=500, detail="MCP broker not available")
        
        # Create broadcast message
        broadcast_message = {
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "source_agent": "api_endpoint",
            "destination_agent": None,  # Broadcast to all
            "message_type": request.get("message_type", "broadcast"),
            "priority": request.get("priority", "medium"),
            "payload": request.get("payload", {}),
            "metadata": request.get("metadata", {})
        }
        
        # Broadcast message
        await mcp_broker.broadcast_message(broadcast_message)
        
        return {
            "status": "broadcasted",
            "message_id": broadcast_message["message_id"],
            "timestamp": broadcast_message["timestamp"],
            "target_agents": mcp_broker.get_registered_agents()
        }
        
    except Exception as e:
        logger.error(f"Error broadcasting MCP message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/agent/{agent_id}/health")
async def get_agent_health(agent_id: str):
    """Get detailed health status of a specific MCP agent"""
    try:
        if agent_id not in agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        agent = agents[agent_id]
        if hasattr(agent, 'get_health_status'):
            return agent.get_health_status()
        else:
            return {
                "agent_id": agent_id,
                "name": getattr(agent, 'name', 'Unknown'),
                "status": getattr(agent, 'status', 'unknown'),
                "error": "Agent does not support health status reporting"
            }
        
    except Exception as e:
        logger.error(f"Error getting agent health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/agent/{agent_id}/task")
async def delegate_task_to_agent(agent_id: str, request: Dict[str, Any]):
    """Delegate a task to a specific MCP agent"""
    try:
        if agent_id not in agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        agent = agents[agent_id]
        if not hasattr(agent, 'execute_task'):
            raise HTTPException(status_code=400, detail=f"Agent {agent_id} does not support task execution")
        
        # Execute task
        result = await agent.execute_task(request)
        
        return {
            "status": "completed",
            "agent_id": agent_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error delegating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
