#!/usr/bin/env python3
"""
Content Security Policy (CSP) Middleware
Generates nonces for secure inline script and style execution
"""

import secrets
import hashlib
from typing import Dict, Any
from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware


class CSPNonceMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate and inject CSP nonces for secure inline content
    """
    
    def __init__(self, app, csp_policy: str = None):
        super().__init__(app)
        self.csp_policy = csp_policy or self._get_default_csp()
    
    def _get_default_csp(self) -> str:
        """Get default CSP policy"""
        return (
            "default-src 'self'; "
            "script-src 'self' 'nonce-{NONCE}'; "
            "style-src 'self' 'nonce-{NONCE}'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self' ws: wss:; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
    
    def _generate_nonce(self) -> str:
        """Generate a cryptographically secure nonce"""
        return secrets.token_urlsafe(32)
    
    def _inject_nonce(self, content: str, nonce: str) -> str:
        """Inject nonce into HTML content for inline scripts and styles"""
        # Add nonce to existing script tags
        content = content.replace(
            '<script>',
            f'<script nonce="{nonce}">'
        )
        content = content.replace(
            '<style>',
            f'<style nonce="{nonce}">'
        )
        return content
    
    async def dispatch(self, request: Request, call_next):
        """Process request and inject CSP headers"""
        # Generate nonce for this request
        nonce = self._generate_nonce()
        
        # Process the request
        response = await call_next(request)
        
        # Set CSP header with nonce
        csp_with_nonce = self.csp_policy.replace('{NONCE}', nonce)
        response.headers['Content-Security-Policy'] = csp_with_nonce
        
        # If it's an HTML response, inject nonce into content
        if isinstance(response, HTMLResponse):
            if hasattr(response, 'body'):
                content = response.body.decode('utf-8')
                content = self._inject_nonce(content, nonce)
                response.body = content.encode('utf-8')
        
        return response


class CSPHashMiddleware(BaseHTTPMiddleware):
    """
    Alternative CSP middleware using SHA hashes for inline content
    """
    
    def __init__(self, app, allowed_hashes: Dict[str, list] = None):
        super().__init__(app)
        self.allowed_hashes = allowed_hashes or {}
    
    def _calculate_sha256_hash(self, content: str) -> str:
        """Calculate SHA256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _get_csp_with_hashes(self) -> str:
        """Generate CSP with SHA hashes"""
        script_hashes = self.allowed_hashes.get('script', [])
        style_hashes = self.allowed_hashes.get('style', [])
        
        script_src = "'self'"
        if script_hashes:
            script_src += " " + " ".join([f"'sha256-{h}'" for h in script_hashes])
        
        style_src = "'self'"
        if style_hashes:
            style_src += " " + " ".join([f"'sha256-{h}'" for h in style_hashes])
        
        return (
            f"default-src 'self'; "
            f"script-src {script_src}; "
            f"style-src {style_src}; "
            f"img-src 'self' data:; "
            f"font-src 'self'; "
            f"connect-src 'self' ws: wss:; "
            f"frame-ancestors 'none'; "
            f"base-uri 'self'; "
            f"form-action 'self'"
        )
    
    async def dispatch(self, request: Request, call_next):
        """Process request with hash-based CSP"""
        response = await call_next(request)
        
        # Set CSP header with hashes
        csp_with_hashes = self._get_csp_with_hashes()
        response.headers['Content-Security-Policy'] = csp_with_hashes
        
        return response


def create_csp_middleware(app, mode: str = "nonce", **kwargs):
    """
    Factory function to create appropriate CSP middleware
    
    Args:
        app: FastAPI application
        mode: "nonce" or "hash"
        **kwargs: Additional arguments for middleware
    
    Returns:
        Configured CSP middleware
    """
    if mode == "nonce":
        return CSPNonceMiddleware(app, **kwargs)
    elif mode == "hash":
        return CSPHashMiddleware(app, **kwargs)
    else:
        raise ValueError("Mode must be 'nonce' or 'hash'")


# Example usage for API-only endpoints
def create_api_only_csp() -> str:
    """Create strict CSP for API-only endpoints"""
    return (
        "default-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'none'; "
        "form-action 'none'"
    )


# Example usage for mixed application
def create_mixed_csp() -> str:
    """Create CSP for mixed API and HTML application"""
    return (
        "default-src 'self'; "
        "script-src 'self' 'nonce-{NONCE}'; "
        "style-src 'self' 'nonce-{NONCE}'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
