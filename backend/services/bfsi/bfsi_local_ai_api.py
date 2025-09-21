#!/usr/bin/env python3
"""
BFSI Local AI API Service
FastAPI service that exposes BFSI Local AI Agent functionality
"""

import asyncio
import copy
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
import logging

from bfsi_local_ai_integration import (
    bfsi_agent, 
    process_bfsi_compliance_check,
    process_bfsi_risk_assessment, 
    process_bfsi_fraud_detection,
    process_bfsi_document_analysis
)
from security_auth import auth_service, get_current_user
from security_config import security_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BFSI Local AI API",
    description="BFSI GRC Agent with Local AI Integration",
    version="1.0.0"
)

# Security configuration
security_scheme = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """
    Verify the provided JWT token for authentication
    
    Args:
        credentials: HTTP authorization credentials containing the bearer token
        
    Returns:
        str: The verified token
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    try:
        # Verify JWT token using the existing auth service
        token_data = auth_service.verify_token(token)
        logger.info(f"Authentication successful for user: {token_data.username} (role: {token_data.role})")
        return token
    except HTTPException as e:
        # Re-raise HTTP exceptions from auth service
        raise e
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Pydantic models
class BFSIRequest(BaseModel):
    """BFSI analysis request"""
    task_type: str
    data: Dict[str, Any]
    priority: str = "medium"

class ComplianceCheckRequest(BaseModel):
    """Compliance check request"""
    regulation: str
    process: str
    controls: List[str]
    documents: Optional[List[str]] = None
    priority: str = "medium"

class RiskAssessmentRequest(BaseModel):
    """Risk assessment request"""
    risk_type: str
    portfolio: str
    exposure: float
    probability: str
    impact: str = "medium"
    controls: Optional[List[str]] = None

class FraudDetectionRequest(BaseModel):
    """Fraud detection request"""
    transaction_id: str
    amount: float
    customer_id: str
    transaction_type: str
    location: str
    timestamp: str

class DocumentAnalysisRequest(BaseModel):
    """Document analysis request"""
    document_type: str
    content: str
    classification: Optional[str] = None
    compliance_framework: Optional[str] = None

class BFSIResponse(BaseModel):
    """BFSI analysis response"""
    task_id: str
    analysis_id: str
    findings: List[str]
    risk_score: float
    compliance_score: float
    recommendations: List[str]
    ai_insights: str
    timestamp: str
    status: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "BFSI Local AI API",
        "version": "1.0.0",
        "description": "BFSI GRC Agent with Local AI Integration",
        "endpoints": {
            "health": "/health",
            "compliance": "/compliance/check",
            "risk": "/risk/assess",
            "fraud": "/fraud/detect",
            "documents": "/documents/analyze"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        health = await bfsi_agent.health_check()
        return health
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Health check failed due to internal error")

@app.get("/status")
async def get_status():
    """Get BFSI agent status"""
    try:
        summary = await bfsi_agent.get_analysis_summary()
        return {
            "status": "active",
            "agent_id": bfsi_agent.agent_id,
            "name": bfsi_agent.name,
            "analysis_summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status check failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Status check failed due to internal error")

@app.post("/compliance/check", response_model=BFSIResponse)
async def compliance_check(request: ComplianceCheckRequest, token: str = Depends(verify_token)):
    """Perform BFSI compliance check"""
    try:
        data = {
            "regulation": request.regulation,
            "process": request.process,
            "controls": request.controls,
            "documents": request.documents or [],
            "priority": request.priority
        }
        
        result = await process_bfsi_compliance_check(data)
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Compliance check failed"))
        
        return BFSIResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Compliance check failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Compliance check failed due to internal error")

@app.post("/risk/assess", response_model=BFSIResponse)
async def risk_assessment(request: RiskAssessmentRequest, token: str = Depends(verify_token)):
    """Perform BFSI risk assessment"""
    try:
        data = {
            "risk_type": request.risk_type,
            "portfolio": request.portfolio,
            "exposure": request.exposure,
            "probability": request.probability,
            "impact": request.impact,
            "controls": request.controls or []
        }
        
        result = await process_bfsi_risk_assessment(data)
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Risk assessment failed"))
        
        return BFSIResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Risk assessment failed due to internal error")

@app.post("/fraud/detect", response_model=BFSIResponse)
async def fraud_detection(request: FraudDetectionRequest, token: str = Depends(verify_token)):
    """Perform BFSI fraud detection"""
    try:
        data = {
            "transaction_id": request.transaction_id,
            "amount": request.amount,
            "customer_id": request.customer_id,
            "transaction_type": request.transaction_type,
            "location": request.location,
            "timestamp": request.timestamp
        }
        
        result = await process_bfsi_fraud_detection(data)
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Fraud detection failed"))
        
        return BFSIResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fraud detection failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Fraud detection failed due to internal error")

@app.post("/documents/analyze", response_model=BFSIResponse)
async def document_analysis(request: DocumentAnalysisRequest, token: str = Depends(verify_token)):
    """Perform BFSI document analysis"""
    try:
        data = {
            "document_type": request.document_type,
            "content": request.content,
            "classification": request.classification,
            "compliance_framework": request.compliance_framework
        }
        
        result = await process_bfsi_document_analysis(data)
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Document analysis failed"))
        
        return BFSIResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Document analysis failed due to internal error")

@app.post("/analyze", response_model=BFSIResponse)
async def general_analysis(request: BFSIRequest, token: str = Depends(verify_token)):
    """Perform general BFSI analysis"""
    try:
        data = request.data.copy()
        data["priority"] = request.priority
        
        result = await bfsi_agent.process_bfsi_request(request.task_type, data)
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))
        
        return BFSIResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"General analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="General analysis failed due to internal error")

@app.get("/analyses")
async def get_analyses(limit: int = 10, offset: int = 0, token: str = Depends(verify_token)):
    """Get recent analyses"""
    try:
        # Validate pagination parameters
        if limit <= 0:
            raise HTTPException(status_code=400, detail="Limit must be positive")
        if limit > 1000:  # Cap limit to prevent excessive memory usage
            raise HTTPException(status_code=400, detail="Limit cannot exceed 1000")
        if offset < 0:
            raise HTTPException(status_code=400, detail="Offset must be non-negative")
        
        # Create thread-safe copy to prevent concurrent modification issues
        analyses_copy = copy.copy(bfsi_agent.analysis_results)
        total = len(analyses_copy)
        
        # Paginate results
        start = offset
        end = min(offset + limit, total)
        paginated_analyses = analyses_copy[start:end]
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "analyses": [
                {
                    "analysis_id": a.analysis_id,
                    "task_id": a.task_id,
                    "findings": a.findings,
                    "risk_score": a.risk_score,
                    "compliance_score": a.compliance_score,
                    "recommendations": a.recommendations,
                    "timestamp": a.timestamp.isoformat()
                }
                for a in reversed(paginated_analyses)  # Most recent first
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analyses: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve analyses due to internal error")

@app.get("/analyses/{analysis_id}")
async def get_analysis(analysis_id: str, token: str = Depends(verify_token)):
    """Get specific analysis by ID"""
    try:
        analysis = next(
            (a for a in bfsi_agent.analysis_results if a.analysis_id == analysis_id),
            None
        )
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {
            "analysis_id": analysis.analysis_id,
            "task_id": analysis.task_id,
            "findings": analysis.findings,
            "risk_score": analysis.risk_score,
            "compliance_score": analysis.compliance_score,
            "recommendations": analysis.recommendations,
            "ai_insights": analysis.ai_insights,
            "timestamp": analysis.timestamp.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analysis {analysis_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve analysis due to internal error")

@app.get("/metrics")
async def get_metrics(token: str = Depends(verify_token)):
    """Get BFSI agent metrics"""
    try:
        summary = await bfsi_agent.get_analysis_summary()
        health = await bfsi_agent.health_check()
        
        return {
            "agent_metrics": summary,
            "health_status": health,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics due to internal error")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8008))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
