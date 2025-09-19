"""
AI Agents Service for GRC Platform
Handles AI agent operations and orchestrates multi-agent workflows
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
import logging
import sys
import os
from datetime import datetime

# Add the ai-agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ai-agents', 'agents_organized'))

# Import the orchestrator
from orchestration.main_orchestrator import GRCPlatformOrchestrator

logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI(
    title="GRC Platform AI Agents Service",
    description="AI Agents Service for GRC Platform",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator = None

# Pydantic models
class RiskAssessmentRequest(BaseModel):
    business_unit: str
    risk_scope: str
    industry_type: str
    context: Optional[Dict[str, Any]] = {}

class ComplianceCheckRequest(BaseModel):
    entity_id: str
    entity_type: str
    industry_type: str
    compliance_requirements: Optional[List[str]] = []

class PolicyReviewRequest(BaseModel):
    policy_id: str
    industry_type: str
    review_scope: str
    context: Optional[Dict[str, Any]] = {}

class AnalysisRequest(BaseModel):
    analysis_type: str
    industry_type: str
    data: Dict[str, Any]
    context: Optional[Dict[str, Any]] = {}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the orchestrator on startup"""
    global orchestrator
    try:
        orchestrator = GRCPlatformOrchestrator()
        logger.info("AI Agents Service started successfully")
    except Exception as e:
        logger.error(f"Failed to start AI Agents Service: {e}")
        raise

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-agents",
        "timestamp": datetime.now().isoformat(),
        "orchestrator_ready": orchestrator is not None
    }

# Agents status endpoint
@app.get("/agents/status")
async def get_agents_status():
    """Get status of all AI agents"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        status = {
            "orchestrator": "ready",
            "industry_agents": {},
            "specialized_agents": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Check industry agents
        for industry_type, agent in orchestrator.industry_agents.items():
            status["industry_agents"][industry_type.value] = {
                "status": "ready",
                "agent_id": agent.agent_id,
                "name": agent.name
            }
        
        # Check specialized agents
        if orchestrator.risk_agent:
            status["specialized_agents"]["risk_agent"] = {
                "status": "ready",
                "agent_id": orchestrator.risk_agent.agent_id,
                "name": orchestrator.risk_agent.name
            }
        
        if orchestrator.document_agent:
            status["specialized_agents"]["document_agent"] = {
                "status": "ready",
                "agent_id": orchestrator.document_agent.agent_id,
                "name": orchestrator.document_agent.name
            }
        
        if orchestrator.communication_agent:
            status["specialized_agents"]["communication_agent"] = {
                "status": "ready",
                "agent_id": orchestrator.communication_agent.agent_id,
                "name": orchestrator.communication_agent.name
            }
        
        if orchestrator.compliance_agent:
            status["specialized_agents"]["compliance_agent"] = {
                "status": "ready",
                "agent_id": orchestrator.compliance_agent.agent_id,
                "name": orchestrator.compliance_agent.name
            }
        
        return status
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Risk assessment endpoint
@app.post("/risk/assess")
async def assess_risk(request: RiskAssessmentRequest):
    """Perform risk assessment using AI agents"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Get the appropriate industry agent
        industry_agent = None
        for agent in orchestrator.industry_agents.values():
            if agent.industry_type.value == request.industry_type:
                industry_agent = agent
                break
        
        if not industry_agent:
            raise HTTPException(status_code=400, detail=f"No agent found for industry: {request.industry_type}")
        
        # Perform risk assessment
        context = {
            "business_unit": request.business_unit,
            "risk_scope": request.risk_scope,
            **request.context
        }
        
        result = await industry_agent.perform_grc_operation(
            "risk_assessment", context
        )
        
        return {
            "success": True,
            "industry_type": request.industry_type,
            "business_unit": request.business_unit,
            "risk_scope": request.risk_scope,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Compliance check endpoint
@app.post("/compliance/check")
async def check_compliance(request: ComplianceCheckRequest):
    """Perform compliance check using AI agents"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Use compliance agent
        if not orchestrator.compliance_agent:
            raise HTTPException(status_code=503, detail="Compliance agent not available")
        
        context = {
            "entity_id": request.entity_id,
            "entity_type": request.entity_type,
            "industry_type": request.industry_type,
            "compliance_requirements": request.compliance_requirements
        }
        
        result = await orchestrator.compliance_agent.execute_task({
            "task_type": "compliance_check",
            "context": context
        })
        
        return {
            "success": True,
            "entity_id": request.entity_id,
            "entity_type": request.entity_type,
            "industry_type": request.industry_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in compliance check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Policy review endpoint
@app.post("/policy/review")
async def review_policy(request: PolicyReviewRequest):
    """Perform policy review using AI agents"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Get the appropriate industry agent
        industry_agent = None
        for agent in orchestrator.industry_agents.values():
            if agent.industry_type.value == request.industry_type:
                industry_agent = agent
                break
        
        if not industry_agent:
            raise HTTPException(status_code=400, detail=f"No agent found for industry: {request.industry_type}")
        
        context = {
            "policy_id": request.policy_id,
            "review_scope": request.review_scope,
            **request.context
        }
        
        result = await industry_agent.perform_grc_operation(
            "policy_review", context
        )
        
        return {
            "success": True,
            "policy_id": request.policy_id,
            "industry_type": request.industry_type,
            "review_scope": request.review_scope,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in policy review: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Cross-domain analysis endpoint
@app.post("/analysis/cross-domain")
async def cross_domain_analysis(request: AnalysisRequest):
    """Perform cross-domain analysis using multiple AI agents"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        results = {}
        
        # Use risk agent for risk analysis
        if orchestrator.risk_agent:
            risk_result = await orchestrator.risk_agent.execute_task({
                "task_type": "risk_analysis",
                "context": request.data
            })
            results["risk_analysis"] = risk_result
        
        # Use document agent for document analysis
        if orchestrator.document_agent:
            doc_result = await orchestrator.document_agent.execute_task({
                "task_type": "document_analysis",
                "context": request.data
            })
            results["document_analysis"] = doc_result
        
        # Use compliance agent for compliance analysis
        if orchestrator.compliance_agent:
            compliance_result = await orchestrator.compliance_agent.execute_task({
                "task_type": "compliance_analysis",
                "context": request.data
            })
            results["compliance_analysis"] = compliance_result
        
        return {
            "success": True,
            "analysis_type": request.analysis_type,
            "industry_type": request.industry_type,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in cross-domain analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Industry-specific operations endpoint
@app.post("/industry/{industry_type}/operations")
async def industry_operations(industry_type: str, request: Dict[str, Any]):
    """Perform industry-specific operations"""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Get the appropriate industry agent
        industry_agent = None
        for agent in orchestrator.industry_agents.values():
            if agent.industry_type.value == industry_type:
                industry_agent = agent
                break
        
        if not industry_agent:
            raise HTTPException(status_code=400, detail=f"No agent found for industry: {industry_type}")
        
        operation_type = request.get("operation_type", "risk_assessment")
        context = request.get("context", {})
        
        result = await industry_agent.perform_grc_operation(operation_type, context)
        
        return {
            "success": True,
            "industry_type": industry_type,
            "operation_type": operation_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in industry operations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)



