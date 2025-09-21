"""
Routing configuration for API Gateway

This module handles request routing to appropriate microservices.
It implements service discovery and load balancing logic.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import asyncio
from typing import Dict, Any
import logging

from src.core.config import settings

logger = logging.getLogger(__name__)

# Service registry mapping
SERVICE_REGISTRY = {
    "policies": settings.POLICY_SERVICE_URL,
    "risks": settings.RISK_SERVICE_URL,
    "compliance": settings.COMPLIANCE_SERVICE_URL,
    "workflows": settings.WORKFLOW_SERVICE_URL,
    "ai-agents": settings.AI_AGENTS_URL,
}

router = APIRouter()

@router.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_request(service_name: str, path: str, request: Request):
    """
    Route requests to appropriate microservices
    
    Args:
        service_name: Name of the target service
        path: Remaining path after service name
        request: Original request object
    """
    
    # Get service URL
    service_url = SERVICE_REGISTRY.get(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    # Construct target URL
    target_url = f"{service_url}/{path}"
    
    # Get request data
    body = await request.body()
    headers = dict(request.headers)
    
    # Remove host header to avoid conflicts
    headers.pop("host", None)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Forward request to target service
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=body
            )
            
            # Return response
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
    except httpx.TimeoutException:
        logger.error(f"Timeout when calling {service_name} service")
        raise HTTPException(status_code=504, detail="Service timeout")
    except httpx.ConnectError:
        logger.error(f"Connection error when calling {service_name} service")
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        logger.error(f"Error calling {service_name} service: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/services")
async def list_services():
    """List all available services"""
    return {
        "services": list(SERVICE_REGISTRY.keys()),
        "registry": SERVICE_REGISTRY
    }

@router.get("/services/{service_name}/health")
async def check_service_health(service_name: str):
    """Check health of a specific service"""
    service_url = SERVICE_REGISTRY.get(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{service_url}/health")
            return {
                "service": service_name,
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds()
            }
    except Exception as e:
        return {
            "service": service_name,
            "status": "unhealthy",
            "error": str(e)
        }
