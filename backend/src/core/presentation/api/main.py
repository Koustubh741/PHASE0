"""
API Gateway for GRC Platform
Central entry point for all GRC services
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import logging
from typing import Dict, Any, Optional
import os
import sys

# Add services directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
from mock_data_service import mock_data_service
from datetime import datetime

logger = logging.getLogger(__name__)

# Service URLs
POLICY_SERVICE_URL = os.getenv("POLICY_SERVICE_URL", "http://localhost:8001")
RISK_SERVICE_URL = os.getenv("RISK_SERVICE_URL", "http://localhost:8002")
COMPLIANCE_SERVICE_URL = os.getenv("COMPLIANCE_SERVICE_URL", "http://localhost:8003")
WORKFLOW_SERVICE_URL = os.getenv("WORKFLOW_SERVICE_URL", "http://localhost:8004")
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL", "http://localhost:8005")

# FastAPI App
app = FastAPI(
    title="GRC Platform API Gateway",
    description="Central API Gateway for GRC Platform Services",
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

# Security
security = HTTPBearer()

# HTTP Client
http_client = httpx.AsyncClient(timeout=30.0)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Simplified authentication - in production, implement proper JWT validation
    return {
        "id": "user-123",
        "organization_id": "org-123",
        "role": "ADMIN"
    }

def get_current_user_optional():
    # Optional authentication for development
    return {
        "id": "user-123",
        "organization_id": "org-123",
        "role": "ADMIN"
    }

async def forward_request(service_url: str, path: str, method: str, 
                         headers: Dict[str, str], body: Any = None) -> Dict[str, Any]:
    """Forward request to appropriate service"""
    try:
        url = f"{service_url}{path}"
        
        # Prepare headers
        forward_headers = {k: v for k, v in headers.items() 
                          if k.lower() not in ['host', 'content-length']}
        
        # Make request
        if method.upper() == "GET":
            response = await http_client.get(url, headers=forward_headers)
        elif method.upper() == "POST":
            response = await http_client.post(url, headers=forward_headers, json=body)
        elif method.upper() == "PUT":
            response = await http_client.put(url, headers=forward_headers, json=body)
        elif method.upper() == "DELETE":
            response = await http_client.delete(url, headers=forward_headers)
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")
        
        return {
            "status_code": response.status_code,
            "content": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            "headers": dict(response.headers)
        }
        
    except httpx.RequestError as e:
        logger.error(f"Request error to {service_url}: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        logger.error(f"Error forwarding request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "policy": POLICY_SERVICE_URL,
            "risk": RISK_SERVICE_URL,
            "compliance": COMPLIANCE_SERVICE_URL,
            "workflow": WORKFLOW_SERVICE_URL,
            "ai-agents": AI_AGENTS_URL
        }
    }

# Policy Service Routes
@app.api_route("/policies/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def policy_routes(path: str, request: Request, current_user: dict = Depends(get_current_user)):
    """Route requests to Policy Service"""
    body = None
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except:
            body = None
    
    return await forward_request(
        POLICY_SERVICE_URL,
        f"/policies/{path}",
        request.method,
        dict(request.headers),
        body
    )

# Risk Service Routes
@app.api_route("/risks/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def risk_routes(path: str, request: Request, current_user: dict = Depends(get_current_user)):
    """Route requests to Risk Service"""
    body = None
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except:
            body = None
    
    return await forward_request(
        RISK_SERVICE_URL,
        f"/risks/{path}",
        request.method,
        dict(request.headers),
        body
    )

# Compliance Service Routes
@app.api_route("/compliance/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def compliance_routes(path: str, request: Request, current_user: dict = Depends(get_current_user)):
    """Route requests to Compliance Service"""
    body = None
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except:
            body = None
    
    return await forward_request(
        COMPLIANCE_SERVICE_URL,
        f"/{path}",
        request.method,
        dict(request.headers),
        body
    )

# Workflow Service Routes
@app.api_route("/workflows/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def workflow_routes(path: str, request: Request, current_user: dict = Depends(get_current_user)):
    """Route requests to Workflow Service"""
    body = None
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except:
            body = None
    
    return await forward_request(
        WORKFLOW_SERVICE_URL,
        f"/{path}",
        request.method,
        dict(request.headers),
        body
    )

# AI Agents Routes
@app.api_route("/ai-agents/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def ai_agents_routes(path: str, request: Request, current_user: dict = Depends(get_current_user)):
    """Route requests to AI Agents Service"""
    body = None
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except:
            body = None
    
    return await forward_request(
        AI_AGENTS_URL,
        f"/{path}",
        request.method,
        dict(request.headers),
        body
    )

# Unified GRC Endpoints
@app.get("/grc/dashboard")
async def get_grc_dashboard(current_user: dict = Depends(get_current_user_optional)):
    """Get unified GRC dashboard data"""
    try:
        # Collect data from all services
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "organization_id": current_user["organization_id"],
            "services": {}
        }
        
        # Get policy stats
        try:
            policy_response = await http_client.get(f"{POLICY_SERVICE_URL}/policies/stats")
            if policy_response.status_code == 200:
                dashboard_data["services"]["policies"] = policy_response.json()
        except Exception as e:
            logger.warning(f"Failed to get policy stats: {e}")
        
        # Get risk stats
        try:
            risk_response = await http_client.get(f"{RISK_SERVICE_URL}/risks/stats")
            if risk_response.status_code == 200:
                dashboard_data["services"]["risks"] = risk_response.json()
        except Exception as e:
            logger.warning(f"Failed to get risk stats: {e}")
        
        # Get compliance stats
        try:
            compliance_response = await http_client.get(f"{COMPLIANCE_SERVICE_URL}/compliance/stats")
            if compliance_response.status_code == 200:
                dashboard_data["services"]["compliance"] = compliance_response.json()
        except Exception as e:
            logger.warning(f"Failed to get compliance stats: {e}")
        
        # Get workflow stats
        try:
            workflow_response = await http_client.get(f"{WORKFLOW_SERVICE_URL}/workflows/stats")
            if workflow_response.status_code == 200:
                dashboard_data["services"]["workflows"] = workflow_response.json()
        except Exception as e:
            logger.warning(f"Failed to get workflow stats: {e}")
        
        # Get AI agents status
        try:
            ai_response = await http_client.get(f"{AI_AGENTS_URL}/agents/status")
            if ai_response.status_code == 200:
                dashboard_data["services"]["ai_agents"] = ai_response.json()
        except Exception as e:
            logger.warning(f"Failed to get AI agents status: {e}")
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error getting GRC dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard data")

@app.post("/grc/search")
async def unified_search(request: Dict[str, Any], current_user: dict = Depends(get_current_user)):
    """Unified search across all GRC services"""
    try:
        query = request.get("query", "")
        search_type = request.get("type", "all")
        
        search_results = {
            "query": query,
            "type": search_type,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        # Search policies
        if search_type in ["all", "policies"]:
            try:
                policy_response = await http_client.post(
                    f"{POLICY_SERVICE_URL}/policies/search",
                    json={"query": query, "organization_id": current_user["organization_id"]}
                )
                if policy_response.status_code == 200:
                    search_results["results"]["policies"] = policy_response.json()
            except Exception as e:
                logger.warning(f"Failed to search policies: {e}")
        
        # Search risks
        if search_type in ["all", "risks"]:
            try:
                risk_response = await http_client.post(
                    f"{RISK_SERVICE_URL}/risks/search",
                    json={"query": query, "organization_id": current_user["organization_id"]}
                )
                if risk_response.status_code == 200:
                    search_results["results"]["risks"] = risk_response.json()
            except Exception as e:
                logger.warning(f"Failed to search risks: {e}")
        
        # Search compliance
        if search_type in ["all", "compliance"]:
            try:
                compliance_response = await http_client.post(
                    f"{COMPLIANCE_SERVICE_URL}/compliance/search",
                    json={"query": query, "organization_id": current_user["organization_id"]}
                )
                if compliance_response.status_code == 200:
                    search_results["results"]["compliance"] = compliance_response.json()
            except Exception as e:
                logger.warning(f"Failed to search compliance: {e}")
        
        return search_results
        
    except Exception as e:
        logger.error(f"Error performing unified search: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform search")

@app.post("/grc/analysis")
async def perform_grc_analysis(request: Dict[str, Any], current_user: dict = Depends(get_current_user)):
    """Perform comprehensive GRC analysis"""
    try:
        analysis_type = request.get("analysis_type", "comprehensive")
        organization_id = current_user["organization_id"]
        
        # Use AI agents for analysis
        analysis_response = await http_client.post(
            f"{AI_AGENTS_URL}/analysis/cross-domain",
            json={
                "organization_id": organization_id,
                "analysis_type": analysis_type
            }
        )
        
        if analysis_response.status_code == 200:
            return analysis_response.json()
        else:
            raise HTTPException(status_code=500, detail="Analysis failed")
        
    except Exception as e:
        logger.error(f"Error performing GRC analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform analysis")

# Service Status Endpoint
@app.get("/services/status")
async def get_services_status():
    """Get status of all services"""
    try:
        services_status = {
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }
        
        # Check each service
        services = {
            "policy": POLICY_SERVICE_URL,
            "risk": RISK_SERVICE_URL,
            "compliance": COMPLIANCE_SERVICE_URL,
            "workflow": WORKFLOW_SERVICE_URL,
            "ai-agents": AI_AGENTS_URL
        }
        
        for service_name, service_url in services.items():
            try:
                response = await http_client.get(f"{service_url}/health", timeout=5.0)
                services_status["services"][service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_url,
                    "response_time": response.elapsed.total_seconds()
                }
            except Exception as e:
                services_status["services"][service_name] = {
                    "status": "unhealthy",
                    "url": service_url,
                    "error": str(e)
                }
        
        return services_status
        
    except Exception as e:
        logger.error(f"Error getting services status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get services status")

# Startup and Shutdown Events
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("GRC Platform API Gateway started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await http_client.aclose()
    logger.info("GRC Platform API Gateway stopped")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
