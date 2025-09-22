"""
API Gateway for GRC Platform Microservices
Handles routing, load balancing, authentication, and service discovery
"""

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, List, Optional, Any
import httpx
import asyncio
import logging
import time
import json
from datetime import datetime, timedelta
from collections import defaultdict
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from ...config.settings import settings
except ImportError:
    # Fallback for direct execution
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    from config.settings import settings

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """Service registry for microservices discovery"""
    
    def __init__(self):
        self.services: Dict[str, List[Dict[str, Any]]] = {
            "policy": [
                {"host": "localhost", "port": 8001, "healthy": True, "last_check": datetime.now()},
            ],
            "risk": [
                {"host": "localhost", "port": 8002, "healthy": True, "last_check": datetime.now()},
            ],
            "compliance": [
                {"host": "localhost", "port": 8003, "healthy": True, "last_check": datetime.now()},
            ],
            "workflow": [
                {"host": "localhost", "port": 8004, "healthy": True, "last_check": datetime.now()},
            ],
            "ai-agents": [
                {"host": "localhost", "port": 8005, "healthy": True, "last_check": datetime.now()},
            ],
        }
        self.circuit_breakers: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "failures": 0,
            "last_failure": None,
            "state": "closed"  # closed, open, half-open
        })
    
    def get_service_url(self, service_name: str, path: str = "") -> Optional[str]:
        """Get the URL for a service instance"""
        if service_name not in self.services:
            return None
        
        # Check circuit breaker
        cb = self.circuit_breakers[service_name]
        if cb["state"] == "open":
            if datetime.now() - cb["last_failure"] < timedelta(minutes=5):
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Service {service_name} is temporarily unavailable"
                )
            else:
                cb["state"] = "half-open"
        
        # Get healthy service instances
        healthy_services = [s for s in self.services[service_name] if s["healthy"]]
        if not healthy_services:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"No healthy instances available for service {service_name}"
            )
        
        # Simple round-robin selection
        service = healthy_services[0]  # For demo, just use first available
        return f"http://{service['host']}:{service['port']}{path}"
    
    def record_success(self, service_name: str):
        """Record successful request"""
        cb = self.circuit_breakers[service_name]
        cb["failures"] = 0
        cb["state"] = "closed"
    
    def record_failure(self, service_name: str):
        """Record failed request"""
        cb = self.circuit_breakers[service_name]
        cb["failures"] += 1
        cb["last_failure"] = datetime.now()
        
        if cb["failures"] >= 5:  # Threshold for circuit breaker
            cb["state"] = "open"
            logger.warning(f"Circuit breaker opened for service {service_name}")


class APIGateway:
    """API Gateway for routing requests to microservices"""
    
    def __init__(self):
        self.service_registry = ServiceRegistry()
        self.route_mappings = {
            "/api/v1/policies": "policy",
            "/api/v1/risks": "risk", 
            "/api/v1/compliance": "compliance",
            "/api/v1/workflows": "workflow",
            "/api/v1/ai-agents": "ai-agents",
        }
        self.auth_required_paths = {
            "/api/v1/policies": True,
            "/api/v1/risks": True,
            "/api/v1/compliance": True,
            "/api/v1/workflows": True,
            "/api/v1/ai-agents": False,  # AI agents might be public
        }
    
    def get_service_name(self, path: str) -> Optional[str]:
        """Determine which service should handle the request"""
        for route_prefix, service_name in self.route_mappings.items():
            if path.startswith(route_prefix):
                return service_name
        return None
    
    def is_auth_required(self, path: str) -> bool:
        """Check if authentication is required for this path"""
        for route_prefix, auth_required in self.auth_required_paths.items():
            if path.startswith(route_prefix):
                return auth_required
        return False
    
    async def proxy_request(
        self,
        request: Request,
        service_name: str,
        target_path: str
    ) -> JSONResponse:
        """Proxy request to the appropriate microservice"""
        
        try:
            # Get service URL
            service_url = self.service_registry.get_service_url(service_name, target_path)
            if not service_url:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Service {service_name} not found"
                )
            
            # Prepare headers
            headers = dict(request.headers)
            # Remove host header to avoid conflicts
            headers.pop("host", None)
            
            # Prepare query parameters
            query_params = dict(request.query_params)
            
            # Prepare body for non-GET requests
            body = None
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
            
            # Make request to microservice
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method=request.method,
                    url=service_url,
                    headers=headers,
                    params=query_params,
                    content=body
                )
                
                # Record success
                self.service_registry.record_success(service_name)
                
                # Return response
                return JSONResponse(
                    content=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text},
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
                
        except httpx.TimeoutException:
            self.service_registry.record_failure(service_name)
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"Request to {service_name} service timed out"
            )
        except httpx.ConnectError:
            self.service_registry.record_failure(service_name)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Cannot connect to {service_name} service"
            )
        except Exception as e:
            self.service_registry.record_failure(service_name)
            logger.error(f"Error proxying request to {service_name}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal gateway error"
            )


# Global API Gateway instance
api_gateway = APIGateway()


def get_api_gateway() -> APIGateway:
    """Get API Gateway instance"""
    return api_gateway


async def authenticate_request(request: Request) -> Optional[Dict[str, Any]]:
    """Authenticate the request and return user info"""
    # For demo purposes, we'll implement basic token validation
    # In production, this would validate JWT tokens with the auth service
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    
    # TODO: Implement actual JWT validation with auth service
    # For now, return a mock user for demo
    if token == "demo-token":
        return {
            "user_id": "demo-user-id",
            "email": "demo@example.com",
            "role": "admin",
            "organization_id": "demo-org-id"
        }
    
    return None


async def health_check_service(service_name: str, service_config: Dict[str, Any]) -> bool:
    """Check if a service is healthy"""
    try:
        service_url = f"http://{service_config['host']}:{service_config['port']}/health"
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(service_url)
            return response.status_code == 200
    except:
        return False


async def periodic_health_check():
    """Periodic health check for all services"""
    while True:
        try:
            for service_name, service_instances in api_gateway.service_registry.services.items():
                for instance in service_instances:
                    is_healthy = await health_check_service(service_name, instance)
                    instance["healthy"] = is_healthy
                    instance["last_check"] = datetime.now()
                    
                    if is_healthy:
                        api_gateway.service_registry.record_success(service_name)
                    else:
                        api_gateway.service_registry.record_failure(service_name)
            
            await asyncio.sleep(30)  # Check every 30 seconds
        except Exception as e:
            logger.error(f"Error in health check: {str(e)}")
            await asyncio.sleep(30)
