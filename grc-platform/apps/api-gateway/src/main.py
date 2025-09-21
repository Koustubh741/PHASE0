"""
API Gateway Service

This is the main entry point for the GRC Platform API Gateway.
It serves as the central routing hub for all microservices.

Responsibilities:
- Request routing to appropriate services
- Authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- Service discovery and load balancing
- API versioning and documentation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn

from src.core.config import settings
from src.core.middleware import (
    SecurityMiddleware,
    RateLimitMiddleware,
    LoggingMiddleware,
    MetricsMiddleware
)
from src.core.routing import router
from src.core.database import init_db
from src.core.exceptions import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    await init_db()
    yield
    # Shutdown
    # Add any cleanup logic here if needed
    pass


# Initialize FastAPI application
app = FastAPI(
    title="GRC Platform API Gateway",
    description="Central API Gateway for GRC Platform microservices",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
app.add_middleware(SecurityMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)

# Include routers
app.include_router(router)

# Setup exception handlers
setup_exception_handlers(app)



@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
