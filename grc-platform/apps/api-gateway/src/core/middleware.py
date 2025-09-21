"""
Middleware components for API Gateway

This module contains all middleware components used by the API Gateway service.
Each middleware handles a specific concern like security, rate limiting, logging, etc.
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from typing import Callable
import asyncio
from collections import deque
import json
import redis.asyncio as redis
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for handling security headers and protection"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Thread-safe rate limiting middleware to prevent abuse"""
    
    def __init__(self, app, requests_per_minute: int = 100, use_redis: bool = False, redis_url: str = "redis://localhost:6379"):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self.use_redis = use_redis
        self.redis_url = redis_url
        
        if self.use_redis:
            self.redis_client = None
            self._cleanup_task = None
        else:
            # In-memory storage with thread safety
            self._lock = asyncio.Lock()
            self.requests = {}  # IP -> deque of timestamps
            self._cleanup_task = None
            self._last_cleanup = time.time()
    
    async def _init_redis(self):
        """Initialize Redis connection if using Redis backend"""
        if self.use_redis and self.redis_client is None:
            try:
                self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
                await self.redis_client.ping()
                logger.info("Redis connection established for rate limiting")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                logger.warning("Falling back to in-memory rate limiting")
                self.use_redis = False
    
    async def _redis_rate_limit(self, client_ip: str) -> bool:
        """Redis-based rate limiting using sliding window with Lua script"""
        if not self.redis_client:
            await self._init_redis()
            if not self.redis_client:
                return False
        
        try:
            # Lua script for atomic sliding window rate limiting
            lua_script = """
            local key = KEYS[1]
            local window = tonumber(ARGV[1])
            local limit = tonumber(ARGV[2])
            local now = tonumber(ARGV[3])
            
            -- Remove old entries
            redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
            
            -- Count current requests
            local current = redis.call('ZCARD', key)
            
            if current < limit then
                -- Add new request
                redis.call('ZADD', key, now, now)
                redis.call('EXPIRE', key, window)
                return 0  -- Allowed
            else
                return 1  -- Rate limited
            end
            """
            
            key = f"rate_limit:{client_ip}"
            result = await self.redis_client.eval(
                lua_script, 1, key, 
                self.window_seconds, self.requests_per_minute, int(time.time())
            )
            
            return result == 1  # True if rate limited
            
        except Exception as e:
            logger.error(f"Redis rate limiting error: {e}")
            return False  # Allow on error
    
    async def _memory_rate_limit(self, client_ip: str) -> bool:
        """In-memory rate limiting with thread safety and lazy cleanup"""
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds
        
        async with self._lock:
            # Lazy cleanup - only when accessing this IP
            if client_ip in self.requests:
                # Remove old timestamps from deque
                while self.requests[client_ip] and self.requests[client_ip][0] < cutoff_time:
                    self.requests[client_ip].popleft()
                
                # Check if limit exceeded
                if len(self.requests[client_ip]) >= self.requests_per_minute:
                    return True  # Rate limited
                
                # Add current request
                self.requests[client_ip].append(current_time)
            else:
                # New IP - create new deque
                self.requests[client_ip] = deque([current_time])
            
            return False  # Not rate limited
    
    async def _periodic_cleanup(self):
        """Background task to periodically clean up stale IP entries"""
        while True:
            try:
                await asyncio.sleep(300)  # Clean every 5 minutes
                current_time = time.time()
                cutoff_time = current_time - self.window_seconds
                
                async with self._lock:
                    # Remove IPs with no recent requests
                    stale_ips = [
                        ip for ip, timestamps in self.requests.items()
                        if not timestamps or timestamps[-1] < cutoff_time
                    ]
                    for ip in stale_ips:
                        del self.requests[ip]
                    
                    if stale_ips:
                        logger.info(f"Cleaned up {len(stale_ips)} stale IP entries from rate limiter")
                        
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")
    
    async def _start_cleanup_task(self):
        """Start the background cleanup task"""
        if self._cleanup_task is None and not self.use_redis:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
            logger.info("Started periodic cleanup task for rate limiter")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host
        
        # Start cleanup task if not already started
        if not self._cleanup_task:
            await self._start_cleanup_task()
        
        # Check rate limit
        if self.use_redis:
            is_rate_limited = await self._redis_rate_limit(client_ip)
        else:
            is_rate_limited = await self._memory_rate_limit(client_ip)
        
        if is_rate_limited:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "limit": self.requests_per_minute,
                    "window_seconds": self.window_seconds
                }
            )
        
        response = await call_next(request)
        return response
    
    async def cleanup(self):
        """Cleanup resources when middleware is destroyed"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        if self.use_redis and self.redis_client:
            await self.redis_client.close()

class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging middleware for request/response logging"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - "
            f"Process time: {process_time:.4f}s"
        )
        
        return response

class MetricsMiddleware(BaseHTTPMiddleware):
    """Metrics collection middleware for monitoring"""
    
    def __init__(self, app):
        super().__init__(app)
        self.request_count = 0
        self.response_times = []
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        self.request_count += 1
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        self.response_times.append(process_time)
        
        # Keep only last 1000 response times
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        return response
    
    def get_metrics(self) -> dict:
        """Get current metrics"""
        if not self.response_times:
            return {
                "request_count": self.request_count,
                "avg_response_time": 0,
                "max_response_time": 0
            }
        
        return {
            "request_count": self.request_count,
            "avg_response_time": sum(self.response_times) / len(self.response_times),
            "max_response_time": max(self.response_times)
        }
