"""
Standalone API Gateway Main Application
Entry point for the GRC Platform API Gateway (no external dependencies)
"""

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import asyncio
import sys
import os

from gateway_standalone import api_gateway, authenticate_request, periodic_health_check

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting GRC Platform API Gateway...")
    
    # Start health check task
    health_check_task = asyncio.create_task(periodic_health_check())
    
    yield
    
    # Shutdown
    logger.info("Shutting down GRC Platform API Gateway...")
    health_check_task.cancel()
    try:
        await health_check_task
    except asyncio.CancelledError:
        pass


# Create FastAPI application
app = FastAPI(
    title="GRC Platform API Gateway",
    description="API Gateway for GRC Platform Microservices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"]
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    start_time = time.time()
    client_ip = request.headers.get("X-Forwarded-For", request.client.host if request.client else "unknown")
    
    # Determine service
    service_name = api_gateway.get_service_name(request.url.path)
    
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{client_ip} - {request.method} {request.url.path} -> "
        f"{service_name or 'gateway'} - Status: {response.status_code} - Time: {process_time:.3f}s"
    )
    
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "grc-platform-api-gateway",
        "version": "1.0.0",
        "timestamp": time.time(),
        "services": {
            service: len([s for s in instances if s["healthy"]])
            for service, instances in api_gateway.service_registry.services.items()
        }
    }


# Service status endpoint
@app.get("/services/status")
async def services_status():
    """Get status of all microservices"""
    services_status = {}
    
    for service_name, instances in api_gateway.service_registry.services.items():
        healthy_instances = [s for s in instances if s["healthy"]]
        circuit_breaker = api_gateway.service_registry.circuit_breakers[service_name]
        
        services_status[service_name] = {
            "total_instances": len(instances),
            "healthy_instances": len(healthy_instances),
            "circuit_breaker_state": circuit_breaker["state"],
            "last_failure": circuit_breaker["last_failure"].isoformat() if circuit_breaker["last_failure"] else None,
            "instances": [
                {
                    "host": instance["host"],
                    "port": instance["port"],
                    "healthy": instance["healthy"],
                    "last_check": instance["last_check"].isoformat()
                }
                for instance in instances
            ]
        }
    
    return services_status


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GRC Platform API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "services": list(api_gateway.service_registry.services.keys())
    }


# Main proxy route handler
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_request(request: Request, path: str):
    """Proxy requests to appropriate microservices"""
    
    # Skip gateway's own endpoints
    if path in ["health", "services/status", "docs", "redoc", "openapi.json", ""]:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Determine target service
    full_path = f"/{path}"
    service_name = api_gateway.get_service_name(full_path)
    
    if not service_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Check authentication if required
    if api_gateway.is_auth_required(full_path):
        user = await authenticate_request(request)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Add user info to request headers for downstream services
        request.headers = request.headers.mutablecopy()
        request.headers["X-User-ID"] = user["user_id"]
        request.headers["X-User-Email"] = user["email"]
        request.headers["X-User-Role"] = user["role"]
        request.headers["X-Organization-ID"] = user["organization_id"]
    
    # Proxy to microservice
    try:
        return await api_gateway.proxy_request(request, service_name, full_path)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error proxying request to {service_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gateway error"
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main_standalone:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
