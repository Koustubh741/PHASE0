"""
Main FastAPI Application for GRC Platform
Production-ready GRC backend with comprehensive security and audit features
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from ...config.settings import settings

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
    logger.info("Starting GRC Platform API...")
    yield
    # Shutdown
    logger.info("Shutting down GRC Platform API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="GRC Platform API - Governance, Risk, and Compliance platform",
    version=settings.version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan
)

# Security Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{client_ip} - {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Time: {process_time:.3f}s"
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
        "service": "grc-platform-api",
        "version": settings.version,
        "timestamp": time.time()
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "docs": "/docs" if settings.debug else "Documentation not available in production"
    }


# Include API routes
from fastapi import APIRouter
from ..api.v1.endpoints import auth, users, policies, workflows, bfsi_ai, analytics, monitoring, workflow_automation

# API v1 router
api_v1_router = APIRouter(prefix="/api/v1")

# Include endpoint routers
api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(policies.router)
api_v1_router.include_router(workflows.router)
api_v1_router.include_router(bfsi_ai.router)
api_v1_router.include_router(analytics.router) # Added analytics router
api_v1_router.include_router(monitoring.router) # Added monitoring router
api_v1_router.include_router(workflow_automation.router) # Added workflow automation router

# Include the main API router
app.include_router(api_v1_router)

# API Gateway Integration
# Note: The API Gateway is available as a separate service at backend/src/core/infrastructure/api_gateway/
# It can be run independently to route requests to microservices
# To use the API Gateway instead of direct routes, comment out the above router inclusion
# and use the gateway service instead


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )