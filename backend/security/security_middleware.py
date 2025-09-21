#!/usr/bin/env python3
"""
Security Middleware for BFSI API
Rate limiting, security headers, and request validation
"""

import time
import hashlib
import asyncio
import re
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict, deque
import json

from security_config import security_config

logger = logging.getLogger(__name__)


def get_client_ip_from_request(request: Request, trust_proxy: bool = False) -> str:
    """
    Get client IP address with configurable proxy trust validation.
    
    This utility function provides secure IP detection that prevents IP spoofing
    attacks by only trusting forwarded headers when explicitly configured to do so.
    
    Args:
        request: FastAPI Request object
        trust_proxy: Whether to trust X-Forwarded-For and X-Real-IP headers (default: False)
                    Set to True only when behind a trusted reverse proxy/load balancer
    
    Returns:
        str: Client IP address
        
    Security Note:
        Only set trust_proxy=True when your application is deployed behind a trusted
        reverse proxy (nginx, Apache, CloudFlare, etc.) that you control. Never trust
        these headers from untrusted sources as they can be easily spoofed by attackers.
    """
    # Only trust forwarded headers if we're behind a trusted proxy
    if trust_proxy:
        # Check for forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
    
    # Fallback to direct connection IP when not trusting proxy or no forwarded headers
    return request.client.host if request.client else "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window with secure IP detection.
    
    Security Features:
    - Configurable proxy trust to prevent IP spoofing attacks
    - When trust_proxy=False (default): Only uses direct connection IP, ignoring X-Forwarded-For and X-Real-IP headers
    - When trust_proxy=True: Trusts forwarded headers from trusted proxy/load balancer
    
    Args:
        app: ASGI application
        requests_per_minute: Maximum requests per minute per IP (default: from security_config)
        burst_limit: Maximum burst requests per IP (default: from security_config)
        trust_proxy: Whether to trust X-Forwarded-For and X-Real-IP headers (default: False)
                    Set to True only when behind a trusted reverse proxy/load balancer
                    
    Security Note:
        Only set trust_proxy=True when your application is deployed behind a trusted
        reverse proxy (nginx, Apache, CloudFlare, etc.) that you control. Never trust
        these headers from untrusted sources as they can be easily spoofed by attackers.
    """
    
    def __init__(self, app: ASGIApp, requests_per_minute: int = None, burst_limit: int = None, trust_proxy: bool = False):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute or security_config.rate_limit_requests_per_minute
        self.burst_limit = burst_limit or security_config.rate_limit_burst
        self.trust_proxy = trust_proxy
        self.requests = defaultdict(deque)
        self.burst_requests = defaultdict(deque)
        self.last_activity = {}  # Track last activity time for each IP
        self.cleanup_threshold = 300  # 5 minutes of inactivity before cleanup
        self.last_cleanup = time.time()  # Track when we last performed cleanup
        self.cleanup_interval = 60  # Perform cleanup every 60 seconds
        self.lock = asyncio.Lock()  # Thread safety for deque operations
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting"""
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        async with self.lock:
            # Update last activity for this IP
            self.last_activity[client_ip] = current_time
            
            # Perform periodic cleanup of inactive IPs
            if current_time - self.last_cleanup > self.cleanup_interval:
                await self.cleanup_inactive_ips(current_time)
                self.last_cleanup = current_time
            
            # Clean old requests
            await self.clean_old_requests(client_ip, current_time)
            
            # Check rate limits
            if not await self.check_rate_limit(client_ip, current_time):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )
            
            # Check burst limit
            if not await self.check_burst_limit(client_ip, current_time):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Burst limit exceeded"
                )
            
            # Record request
            self.requests[client_ip].append(current_time)
            self.burst_requests[client_ip].append(current_time)
            
            # Calculate remaining requests for headers
            remaining_requests = self.requests_per_minute - len(self.requests[client_ip])
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining_requests)
        
        return response
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address with proxy trust validation"""
        return get_client_ip_from_request(request, self.trust_proxy)
    
    async def clean_old_requests(self, client_ip: str, current_time: float):
        """Remove old requests outside the time window"""
        # Remove requests older than 1 minute
        while self.requests[client_ip] and current_time - self.requests[client_ip][0] > 60:
            self.requests[client_ip].popleft()
        
        # Remove burst requests older than 1 second
        while self.burst_requests[client_ip] and current_time - self.burst_requests[client_ip][0] > 1:
            self.burst_requests[client_ip].popleft()
    
    async def cleanup_inactive_ips(self, current_time: float):
        """Remove IP entries that have been inactive for too long"""
        inactive_ips = []
        
        # Find IPs that have been inactive for longer than the threshold
        for ip, last_activity_time in self.last_activity.items():
            if current_time - last_activity_time > self.cleanup_threshold:
                inactive_ips.append(ip)
        
        # Remove inactive IPs from all tracking dictionaries
        for ip in inactive_ips:
            # Remove from defaultdicts (this will remove the key entirely)
            if ip in self.requests:
                del self.requests[ip]
            if ip in self.burst_requests:
                del self.burst_requests[ip]
            # Remove from last_activity tracking
            del self.last_activity[ip]
        
        if inactive_ips:
            logger.info(f"Cleaned up {len(inactive_ips)} inactive IPs: {inactive_ips}")
            logger.debug(f"Current active IPs: {len(self.last_activity)}")
    
    async def check_rate_limit(self, client_ip: str, current_time: float) -> bool:
        """Check if client is within rate limit"""
        return len(self.requests[client_ip]) < self.requests_per_minute
    
    async def check_burst_limit(self, client_ip: str, current_time: float) -> bool:
        """Check if client is within burst limit"""
        return len(self.burst_requests[client_ip]) < self.burst_limit

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }
    
    async def dispatch(self, request: Request, call_next):
        """Add security headers to response"""
        response = await call_next(request)
        
        for header, value in self.security_headers.items():
            response.headers[header] = value
        
        return response

class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate and sanitize incoming requests"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.max_request_size = 10 * 1024 * 1024  # 10MB
        self.blocked_patterns = [
            r"<script.*?>.*?</script>",  # XSS attempts
            r"javascript:",  # JavaScript injection
            r"vbscript:",  # VBScript injection
            r"onload\s*=",  # Event handler injection
            r"onerror\s*=",  # Event handler injection
            r"union\s+select",  # SQL injection
            r"drop\s+table",  # SQL injection
            r"delete\s+from",  # SQL injection
        ]
    
    async def dispatch(self, request: Request, call_next):
        """Validate request before processing"""
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_request_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Request too large"
            )
        
        # Validate request body for malicious content
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            if body:
                body_str = body.decode("utf-8", errors="ignore")
                if self.contains_malicious_content(body_str):
                    client_ip = request.client.host if request.client and hasattr(request.client, 'host') else "unknown"
                    logger.warning(f"Malicious content detected from {client_ip}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Malicious content detected"
                    )
                
                # Restore the request body for downstream middleware/handlers
                async def receive():
                    return {
                        "type": "http.request",
                        "body": body,
                        "more_body": False
                    }
                request._receive = receive
        
        response = await call_next(request)
        return response
    
    def contains_malicious_content(self, content: str) -> bool:
        """Check if content contains malicious patterns"""
        content_lower = content.lower()
        
        for pattern in self.blocked_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return True
        
        return False

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log all requests for audit purposes with secure IP detection.
    
    Args:
        app: ASGI application
        trust_proxy: Whether to trust X-Forwarded-For and X-Real-IP headers (default: False)
                    Set to True only when behind a trusted reverse proxy/load balancer
                    
    Security Note:
        Only set trust_proxy=True when your application is deployed behind a trusted
        reverse proxy (nginx, Apache, CloudFlare, etc.) that you control. Never trust
        these headers from untrusted sources as they can be easily spoofed by attackers.
    """
    
    def __init__(self, app: ASGIApp, trust_proxy: bool = False):
        super().__init__(app)
        self.trust_proxy = trust_proxy
        self.audit_logger = logging.getLogger("audit")
        self.audit_logger.setLevel(logging.INFO)
        
        # Create audit log handler with rotation
        handler = RotatingFileHandler(
            "audit.log",
            maxBytes=10*1024*1024,  # 10MB per file
            backupCount=5  # Keep 5 backup files
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.audit_logger.addHandler(handler)
    
    async def dispatch(self, request: Request, call_next):
        """Log request for audit purposes"""
        start_time = time.time()
        
        # Extract request details
        client_ip = self.get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")
        method = request.method
        url = str(request.url)
        
        # Log request
        self.audit_logger.info(
            f"REQUEST: {method} {url} from {client_ip} - User-Agent: {user_agent}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log response
        self.audit_logger.info(
            f"RESPONSE: {response.status_code} for {method} {url} "
            f"from {client_ip} - Processing time: {processing_time:.3f}s"
        )
        
        return response
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address with proxy trust validation"""
        return get_client_ip_from_request(request, self.trust_proxy)

class EncryptionHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add encryption-related headers to responses.
    
    This middleware only adds headers indicating encryption capabilities and key IDs.
    Actual encryption is handled at the TLS/SSL level or by infrastructure components.
    The headers serve as indicators to clients about the encryption standards in use.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        from security_config import encryption_manager
        self.encryption_manager = encryption_manager
    
    async def dispatch(self, request: Request, call_next):
        """Process request and add encryption headers to response"""
        # This middleware only adds headers - actual encryption is handled
        # at the TLS/SSL level or by infrastructure components like load balancers
        # and reverse proxies that terminate SSL/TLS connections
        
        response = await call_next(request)
        
        # Add encryption headers
        response.headers["X-Content-Encryption"] = "AES-256-GCM"
        response.headers["X-Encryption-Key-ID"] = "bfsi-key-001"
        
        return response

class ComplianceMiddleware(BaseHTTPMiddleware):
    """Ensure BFSI compliance requirements"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.compliance_headers = {
            "X-Compliance-Framework": "PCI-DSS,GDPR",
            "X-Data-Classification": "CONFIDENTIAL",
            "X-Encryption-Standard": "AES-256-GCM",
            "X-Audit-Required": "true"
        }
    
    async def dispatch(self, request: Request, call_next):
        """Add compliance headers and validate requests"""
        # Check for required compliance headers
        if not request.headers.get("X-Request-ID"):
            # Generate request ID for tracking - safely check client host
            client_ip = request.client.host if request.client and hasattr(request.client, 'host') else "unknown"
            request_id = hashlib.sha256(
                f"{client_ip}{time.time()}".encode()
            ).hexdigest()[:16]
            # Set the generated request_id in the request headers for downstream use
            request.headers["X-Request-ID"] = request_id
        else:
            request_id = request.headers.get("X-Request-ID")
        
        response = await call_next(request)
        
        # Add compliance headers
        for header, value in self.compliance_headers.items():
            response.headers[header] = value
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = str(int(time.time() * 1000))
        
        return response
