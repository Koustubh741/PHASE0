"""
Exception handling for API Gateway

This module defines custom exceptions and exception handlers
for the API Gateway service.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

class ServiceUnavailableException(Exception):
    """Raised when a microservice is unavailable"""
    pass

class RateLimitExceededException(Exception):
    """Raised when rate limit is exceeded"""
    pass

class AuthenticationException(Exception):
    """Raised when authentication fails"""
    pass

class AuthorizationException(Exception):
    """Raised when authorization fails"""
    pass

def setup_exception_handlers(app: FastAPI):
    """Setup global exception handlers"""
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors"""
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation error",
                "details": exc.errors(),
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(ServiceUnavailableException)
    async def service_unavailable_handler(request: Request, exc: ServiceUnavailableException):
        """Handle service unavailable errors"""
        logger.error(f"Service unavailable: {exc}")
        return JSONResponse(
            status_code=503,
            content={
                "error": "Service unavailable",
                "message": str(exc),
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(RateLimitExceededException)
    async def rate_limit_handler(request: Request, exc: RateLimitExceededException):
        """Handle rate limit exceeded errors"""
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "message": str(exc),
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(AuthenticationException)
    async def authentication_handler(request: Request, exc: AuthenticationException):
        """Handle authentication errors"""
        return JSONResponse(
            status_code=401,
            content={
                "error": "Authentication failed",
                "message": str(exc),
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(AuthorizationException)
    async def authorization_handler(request: Request, exc: AuthorizationException):
        """Handle authorization errors"""
        return JSONResponse(
            status_code=403,
            content={
                "error": "Authorization failed",
                "message": str(exc),
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "path": str(request.url)
            }
        )
