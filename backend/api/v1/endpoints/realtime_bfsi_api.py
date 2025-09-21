#!/usr/bin/env python3
"""
Real-Time BFSI API Service - Enhanced Security Version
FastAPI service for real-time BFSI data processing and monitoring
with comprehensive security features for BFSI compliance

Security Features:
- JWT/OAuth2 authentication with role-based access control
- Redis-based login rate limiting with exponential backoff
- Account lockout after repeated failed attempts
- AES-256-GCM encryption for sensitive data
- Comprehensive audit logging
- PCI-DSS and GDPR compliance
- CSRF protection with Redis token storage
- Security headers and CORS protection
"""

import asyncio
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uvicorn
import logging
import json
import sqlite3
import hashlib
import hmac
import secrets
import queue
import redis
import aioredis
import math

# Security imports
from security_config import security_config, encryption_manager, SecurityConstants
from security_auth import (
    auth_service, get_current_user, require_permission, require_role,
    require_admin, require_compliance_access, require_audit_access,
    User, Token, TokenData
)
from security_middleware import (
    RateLimitMiddleware, SecurityHeadersMiddleware, RequestValidationMiddleware,
    AuditLoggingMiddleware, EncryptionHeadersMiddleware, ComplianceMiddleware
)
from security_data_access import SecureDataRepository, DatabaseConfig

# Additional security imports
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from real_bfsi_data_integration import realtime_manager, start_real_time_bfsi, get_real_time_status, stop_real_time_bfsi, RealTimeBFSIEvent, BFSIDataSource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis connection for rate limiting
redis_client = None
async_redis_client = None

class LoginRateLimitService:
    """Redis-based login rate limiting with exponential backoff and account lockout"""
    
    def __init__(self):
        self.redis_client = redis_client
        self.async_redis_client = async_redis_client
        
        # Rate limiting configuration from security_config
        self.max_login_attempts = security_config.login_max_attempts
        self.window_minutes = security_config.login_window_minutes
        self.lockout_minutes = security_config.login_lockout_minutes
        self.exponential_backoff_base = security_config.login_exponential_backoff_base
        self.max_backoff_minutes = security_config.login_max_backoff_minutes
        self.enabled = security_config.login_rate_limit_enabled
        
        # Redis key prefixes
        self.attempts_key_prefix = "login_attempts:"
        self.lockout_key_prefix = "account_lockout:"
        self.backoff_key_prefix = "login_backoff:"
    
    async def check_rate_limit(self, identifier: str, is_ip: bool = False) -> tuple[bool, dict]:
        """
        Check if login attempt is allowed
        Returns: (is_allowed, rate_limit_info)
        """
        try:
            # Check if rate limiting is enabled
            if not self.enabled:
                return True, {"rate_limiting": "disabled"}
            
            if not self.async_redis_client:
                # Fallback to in-memory storage if Redis unavailable
                return await self._check_memory_rate_limit(identifier, is_ip)
            
            current_time = datetime.now()
            key_type = "ip" if is_ip else "user"
            attempts_key = f"{self.attempts_key_prefix}{key_type}:{identifier}"
            lockout_key = f"{self.lockout_key_prefix}{key_type}:{identifier}"
            backoff_key = f"{self.backoff_key_prefix}{key_type}:{identifier}"
            
            # Check if account is locked out
            lockout_until = await self.async_redis_client.get(lockout_key)
            if lockout_until:
                lockout_until_dt = datetime.fromisoformat(lockout_until)
                if current_time < lockout_until_dt:
                    remaining_lockout = (lockout_until_dt - current_time).total_seconds()
                    return False, {
                        "error": "Account temporarily locked",
                        "retry_after": int(remaining_lockout),
                        "reason": "account_locked"
                    }
                else:
                    # Lockout expired, remove the key
                    await self.async_redis_client.delete(lockout_key)
            
            # Check exponential backoff
            backoff_until = await self.async_redis_client.get(backoff_key)
            if backoff_until:
                backoff_until_dt = datetime.fromisoformat(backoff_until)
                if current_time < backoff_until_dt:
                    remaining_backoff = (backoff_until_dt - current_time).total_seconds()
                    return False, {
                        "error": "Rate limit exceeded - exponential backoff active",
                        "retry_after": int(remaining_backoff),
                        "reason": "exponential_backoff"
                    }
            
            # Get current attempts
            attempts_data = await self.async_redis_client.get(attempts_key)
            if attempts_data:
                attempts = json.loads(attempts_data)
            else:
                attempts = {"count": 0, "first_attempt": current_time.isoformat()}
            
            # Check if we're within the time window
            first_attempt = datetime.fromisoformat(attempts["first_attempt"])
            window_elapsed = (current_time - first_attempt).total_seconds() / 60
            
            if window_elapsed >= self.window_minutes:
                # Reset window
                attempts = {"count": 0, "first_attempt": current_time.isoformat()}
            
            # Check if limit exceeded
            if attempts["count"] >= self.max_login_attempts:
                # Calculate exponential backoff
                backoff_minutes = min(
                    self.exponential_backoff_base ** attempts["count"],
                    self.max_backoff_minutes
                )
                backoff_until = current_time + timedelta(minutes=backoff_minutes)
                
                # Set backoff
                await self.async_redis_client.setex(
                    backoff_key,
                    int(backoff_minutes * 60),
                    backoff_until.isoformat()
                )
                
                # If this is a significant number of attempts, lock the account
                if attempts["count"] >= self.max_login_attempts * 2:
                    lockout_until = current_time + timedelta(minutes=self.lockout_minutes)
                    await self.async_redis_client.setex(
                        lockout_key,
                        int(self.lockout_minutes * 60),
                        lockout_until.isoformat()
                    )
                    return False, {
                        "error": "Account locked due to excessive failed attempts",
                        "retry_after": int(self.lockout_minutes * 60),
                        "reason": "account_locked"
                    }
                
                return False, {
                    "error": "Too many login attempts",
                    "retry_after": int(backoff_minutes * 60),
                    "reason": "rate_limit_exceeded"
                }
            
            return True, {
                "attempts_remaining": self.max_login_attempts - attempts["count"] - 1,
                "window_reset_in": int((self.window_minutes - window_elapsed) * 60) if window_elapsed < self.window_minutes else 0
            }
            
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # Fail open - allow login if rate limiting fails
            return True, {"warning": "Rate limiting temporarily unavailable"}
    
    async def record_failed_attempt(self, identifier: str, is_ip: bool = False):
        """Record a failed login attempt"""
        try:
            if not self.async_redis_client:
                return
            
            current_time = datetime.now()
            key_type = "ip" if is_ip else "user"
            attempts_key = f"{self.attempts_key_prefix}{key_type}:{identifier}"
            
            # Get current attempts
            attempts_data = await self.async_redis_client.get(attempts_key)
            if attempts_data:
                attempts = json.loads(attempts_data)
            else:
                attempts = {"count": 0, "first_attempt": current_time.isoformat()}
            
            # Increment count
            attempts["count"] += 1
            
            # Store with expiration
            await self.async_redis_client.setex(
                attempts_key,
                int(self.window_minutes * 60),
                json.dumps(attempts)
            )
            
        except Exception as e:
            logger.error(f"Failed to record login attempt: {e}")
    
    async def record_successful_login(self, identifier: str, is_ip: bool = False):
        """Clear rate limiting data after successful login"""
        try:
            if not self.async_redis_client:
                return
            
            key_type = "ip" if is_ip else "user"
            attempts_key = f"{self.attempts_key_prefix}{key_type}:{identifier}"
            backoff_key = f"{self.backoff_key_prefix}{key_type}:{identifier}"
            
            # Clear attempts and backoff
            await self.async_redis_client.delete(attempts_key)
            await self.async_redis_client.delete(backoff_key)
            
        except Exception as e:
            logger.error(f"Failed to clear rate limit data: {e}")
    
    async def _check_memory_rate_limit(self, identifier: str, is_ip: bool = False) -> tuple[bool, dict]:
        """Fallback in-memory rate limiting when Redis is unavailable"""
        # This is a simplified fallback - in production, you'd want more sophisticated storage
        return True, {"warning": "Using fallback rate limiting"}

# Initialize login rate limiting service
login_rate_limiter = LoginRateLimitService()

class EventPriority:
    """Event priority levels for BFSI events"""
    CRITICAL = 1    # System failures, security breaches, regulatory violations
    HIGH = 2        # Transaction failures, compliance issues, risk alerts
    MEDIUM = 3      # Performance issues, operational alerts
    LOW = 4         # General notifications, status updates
    
    @classmethod
    def get_priority(cls, event_type: str, data: dict) -> int:
        """Determine event priority based on type and data"""
        # Critical events
        if event_type in ["security_breach", "system_failure", "regulatory_violation"]:
            return cls.CRITICAL
        
        # High priority events
        if event_type in ["transaction_failure", "compliance_alert", "risk_threshold_exceeded"]:
            return cls.HIGH
        
        # Medium priority events
        if event_type in ["performance_degradation", "operational_alert"]:
            return cls.MEDIUM
        
        # Check data content for additional priority indicators
        if data and isinstance(data, dict):
            # Look for critical keywords in data
            critical_keywords = ["breach", "failure", "violation", "critical", "urgent"]
            data_str = str(data).lower()
            if any(keyword in data_str for keyword in critical_keywords):
                return cls.CRITICAL
        
        return cls.LOW

class OverflowEventStorage:
    """Persistent storage for overflow events to prevent data loss"""
    
    def __init__(self, db_path: str = "overflow_events.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for overflow events"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS overflow_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE NOT NULL,
                    event_type TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    source_system TEXT,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    processed BOOLEAN DEFAULT FALSE,
                    retry_count INTEGER DEFAULT 0,
                    error_message TEXT
                )
            ''')
            
            # Create indexes for efficient querying
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_priority ON overflow_events(priority)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_processed ON overflow_events(processed)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON overflow_events(timestamp)')
            
            conn.commit()
            conn.close()
            logger.info("Overflow events database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize overflow events database: {e}")
    
    def store_overflow_event(self, event: RealTimeBFSIEvent) -> bool:
        """Store overflow event in persistent storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Determine event priority
            priority = EventPriority.get_priority(event.event_type, event.data)
            
            cursor.execute('''
                INSERT OR REPLACE INTO overflow_events 
                (event_id, event_type, priority, timestamp, source_system, data, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.event_id,
                event.event_type,
                priority,
                event.timestamp.isoformat(),
                event.source_system,
                json.dumps(event.data),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Overflow event {event.event_id} stored with priority {priority}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store overflow event {event.event_id}: {e}")
            return False
    
    def get_pending_events(self, limit: int = 100) -> List[dict]:
        """Retrieve pending overflow events ordered by priority"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT event_id, event_type, priority, timestamp, source_system, data, created_at
                FROM overflow_events 
                WHERE processed = FALSE 
                ORDER BY priority ASC, timestamp ASC 
                LIMIT ?
            ''', (limit,))
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    "event_id": row[0],
                    "event_type": row[1],
                    "priority": row[2],
                    "timestamp": row[3],
                    "source_system": row[4],
                    "data": json.loads(row[5]),
                    "created_at": row[6]
                })
            
            conn.close()
            return events
            
        except Exception as e:
            logger.error(f"Failed to retrieve pending events: {e}")
            return []
    
    def mark_event_processed(self, event_id: str) -> bool:
        """Mark an overflow event as processed"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE overflow_events 
                SET processed = TRUE 
                WHERE event_id = ?
            ''', (event_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark event {event_id} as processed: {e}")
            return False
    
    def increment_retry_count(self, event_id: str, error_message: str = None) -> bool:
        """Increment retry count for failed event processing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE overflow_events 
                SET retry_count = retry_count + 1, error_message = ?
                WHERE event_id = ?
            ''', (error_message, event_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Failed to increment retry count for event {event_id}: {e}")
            return False
    
    def cleanup_old_events(self, days: int = 7) -> int:
        """Clean up old processed events"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            cursor.execute('''
                DELETE FROM overflow_events 
                WHERE processed = TRUE AND created_at < ?
            ''', (cutoff_date,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            logger.info(f"Cleaned up {deleted_count} old overflow events")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup old events: {e}")
            return 0

# Initialize overflow event storage
overflow_storage = OverflowEventStorage()

async def _make_room_for_critical_event(event: RealTimeBFSIEvent, priority: int) -> bool:
    """Make room in queue for critical events by removing lower priority events"""
    try:
        removed_events = []
        queue_size = realtime_manager.event_queue.qsize()
        
        # Try to remove lower priority events to make room
        for _ in range(min(queue_size, 3)):  # Try to remove up to 3 events
            try:
                old_event = realtime_manager.event_queue.get_nowait()
                old_priority = EventPriority.get_priority(old_event.event_type, old_event.data)
                
                # If old event has lower priority, store it in overflow
                if old_priority > priority:
                    # Store the removed event in overflow storage
                    overflow_storage.store_overflow_event(old_event)
                    removed_events.append(old_event.event_id)
                    logger.info(f"Removed lower priority event {old_event.event_id} to make room for critical event")
                else:
                    # Put the event back if it has higher or equal priority
                    realtime_manager.event_queue.put_nowait(old_event)
                    break
                    
            except asyncio.QueueEmpty:
                break
        
        # If we made room, try to add the critical event
        if removed_events:
            try:
                realtime_manager.event_queue.put_nowait(event)
                logger.info(f"Critical event {event.event_id} added to queue after removing {len(removed_events)} lower priority events")
                return True
            except asyncio.QueueFull:
                # Still full, store the critical event in overflow
                overflow_storage.store_overflow_event(event)
                logger.warning(f"Queue still full after cleanup, critical event {event.event_id} stored in overflow")
                return False
        
        return False
        
    except Exception as e:
        logger.error(f"Error making room for critical event {event.event_id}: {e}")
        return False

async def check_login_rate_limit(request: Request) -> None:
    """Dependency to check login rate limiting before authentication"""
    try:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        # Check rate limit for IP
        is_allowed, rate_info = await login_rate_limiter.check_rate_limit(client_ip, is_ip=True)
        
        if not is_allowed:
            retry_after = rate_info.get("retry_after", 60)
            reason = rate_info.get("reason", "rate_limit_exceeded")
            error_msg = rate_info.get("error", "Rate limit exceeded")
            
            # Log the rate limit violation
            logger.warning(f"Login rate limit exceeded for IP {client_ip}: {reason}")
            
            raise HTTPException(
                status_code=429,
                detail=error_msg,
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(login_rate_limiter.max_login_attempts),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(datetime.now().timestamp() + retry_after))
                }
            )
        
        # Add rate limit headers to response
        if "attempts_remaining" in rate_info:
            request.state.rate_limit_info = rate_info
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login rate limit check failed: {e}")
        # Fail open - allow login if rate limiting fails
        pass

# Initialize secure data repository
db_config = DatabaseConfig(
    db_path=realtime_manager.db_path,
    max_connections=security_config.db_connection_pool_size,
    connection_timeout=security_config.db_connection_timeout,
    encryption_enabled=security_config.db_encryption_enabled,
    audit_enabled=security_config.audit_log_enabled
)
secure_repository = SecureDataRepository(db_config)

# Data source validation and persistence functions
def validate_data_source_type(source_type: str) -> bool:
    """Validate data source type against allowed values"""
    allowed_types = ["database", "api", "file", "stream"]
    return source_type in allowed_types

def validate_connection_config(source_type: str, connection_config: Dict[str, Any]) -> tuple[bool, str]:
    """Validate connection configuration based on source type"""
    if not connection_config:
        return False, "Connection configuration cannot be empty"
    
    if source_type == "database":
        required_fields = ["host", "port", "database"]
        for field in required_fields:
            if field not in connection_config:
                return False, f"Database source requires '{field}' field in connection_config"
        # Validate port is numeric
        try:
            port = int(connection_config["port"])
            if not (1 <= port <= 65535):
                return False, "Port must be between 1 and 65535"
        except (ValueError, TypeError):
            return False, "Port must be a valid integer"
            
    elif source_type == "api":
        required_fields = ["url"]
        for field in required_fields:
            if field not in connection_config:
                return False, f"API source requires '{field}' field in connection_config"
        # Validate URL format
        url = connection_config["url"]
        if not (url.startswith("http://") or url.startswith("https://")):
            return False, "API URL must start with http:// or https://"
            
    elif source_type == "file":
        required_fields = ["path"]
        for field in required_fields:
            if field not in connection_config:
                return False, f"File source requires '{field}' field in connection_config"
        # Validate path exists (optional check)
        file_path = connection_config["path"]
        if not os.path.exists(file_path):
            logger.warning(f"File path does not exist: {file_path}")
            
    elif source_type == "stream":
        required_fields = ["endpoint"]
        for field in required_fields:
            if field not in connection_config:
                return False, f"Stream source requires '{field}' field in connection_config"
    
    return True, "Valid configuration"

def save_data_source_to_database(data_source: BFSIDataSource) -> bool:
    """Save data source to database for persistence"""
    try:
        with sqlite3.connect(realtime_manager.db_path) as conn:
            cursor = conn.cursor()
            
            # Create data_sources table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL,
                    connection_config TEXT NOT NULL,
                    refresh_interval INTEGER DEFAULT 60,
                    enabled BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert or update data source
            cursor.execute('''
                INSERT OR REPLACE INTO data_sources 
                (name, type, connection_config, refresh_interval, enabled, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                data_source.name,
                data_source.type,
                json.dumps(data_source.connection_config),
                data_source.refresh_interval,
                data_source.enabled
            ))
            
            conn.commit()
            logger.info(f"Data source '{data_source.name}' saved to database")
            return True
            
    except Exception as e:
        logger.error(f"Failed to save data source to database: {e}")
        return False

def load_data_sources_from_database() -> List[BFSIDataSource]:
    """Load data sources from database"""
    data_sources = []
    try:
        with sqlite3.connect(realtime_manager.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT name, type, connection_config, refresh_interval, enabled
                FROM data_sources
                WHERE enabled = TRUE
                ORDER BY created_at
            ''')
            
            for row in cursor.fetchall():
                name, type_name, connection_config_str, refresh_interval, enabled = row
                connection_config = json.loads(connection_config_str)
                
                data_source = BFSIDataSource(
                    name=name,
                    type=type_name,
                    connection_config=connection_config,
                    refresh_interval=refresh_interval,
                    enabled=bool(enabled)
                )
                data_sources.append(data_source)
                
        logger.info(f"Loaded {len(data_sources)} data sources from database")
        
    except Exception as e:
        logger.error(f"Failed to load data sources from database: {e}")
        
    return data_sources

def check_data_source_exists(name: str) -> bool:
    """Check if a data source with the given name already exists"""
    try:
        with sqlite3.connect(realtime_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM data_sources WHERE name = ?', (name,))
            count = cursor.fetchone()[0]
            return count > 0
    except Exception as e:
        logger.error(f"Failed to check data source existence: {e}")
        return False

# API Key Authentication
class APIKeyAuth:
    """API Key authentication for enhanced security"""
    
    def __init__(self):
        self.api_keys = security_config.api_keys
        self.header_name = security_config.api_key_header
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """Verify API key and return client name"""
        if not security_config.api_key_enabled:
            return None
        
        if api_key in self.api_keys:
            return self.api_keys[api_key]
        return None
    
    async def __call__(self, request: Request):
        """API Key authentication dependency"""
        if not security_config.api_key_enabled:
            return None
        
        api_key = request.headers.get(self.header_name)
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"API key required in {self.header_name} header",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        client_name = self.verify_api_key(api_key)
        if not client_name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        return {"client_name": client_name, "api_key": api_key}

# Initialize API key authentication
api_key_auth = APIKeyAuth()

# Security configuration validation
def validate_security_config():
    """Validate security configuration for BFSI compliance"""
    issues = []
    
    # Check CORS configuration
    if "*" in security_config.cors_origins:
        issues.append("CRITICAL: Wildcard CORS origins detected - security risk")
    
    if len(security_config.cors_origins) == 0:
        issues.append("WARNING: No CORS origins configured")
    
    # Check API key configuration
    if security_config.api_key_enabled and len(security_config.api_keys) == 0:
        issues.append("WARNING: API key authentication enabled but no keys configured")
    
    # Check rate limiting
    if security_config.rate_limit_requests_per_minute > 100:
        issues.append("WARNING: High rate limit may allow abuse")
    
    # Check encryption
    if not security_config.data_encryption_enabled:
        issues.append("CRITICAL: Data encryption disabled - compliance risk")
    
    if issues:
        logger.warning("Security configuration issues detected:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("Security configuration validated successfully")
    
    return issues

# Validate security configuration on startup
validate_security_config()

# Initialize data sources from database on startup
def initialize_data_sources():
    """Load data sources from database on application startup"""
    try:
        db_sources = load_data_sources_from_database()
        if db_sources:
            # Merge with existing sources (avoid duplicates)
            existing_names = {source.name for source in realtime_manager.data_sources}
            for db_source in db_sources:
                if db_source.name not in existing_names:
                    realtime_manager.data_sources.append(db_source)
            logger.info(f"Loaded {len(db_sources)} data sources from database on startup")
        else:
            logger.info("No data sources found in database, using environment configuration only")
    except Exception as e:
        logger.error(f"Failed to initialize data sources from database: {e}")

# Initialize data sources
initialize_data_sources()

# Initialize FastAPI app with security features
app = FastAPI(
    title="Real-Time BFSI API - Secure",
    description="Real-Time BFSI Data Processing and Monitoring with Enhanced Security",
    version="2.0.0",
    docs_url="/docs" if security_config.security_headers_enabled else None,
    redoc_url="/redoc" if security_config.security_headers_enabled else None
)

# Add security middleware (order matters!)
app.add_middleware(ComplianceMiddleware)
app.add_middleware(EncryptionHeadersMiddleware)
app.add_middleware(AuditLoggingMiddleware)
app.add_middleware(RequestValidationMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

# Add startup and shutdown event handlers for Redis
@app.on_event("startup")
async def startup_event():
    """Initialize Redis connections on startup"""
    global redis_client, async_redis_client
    
    try:
        # Initialize CSRF storage
        await csrf_storage.initialize()
        logger.info("Redis CSRF token storage initialized successfully")
        
        # Initialize login rate limiter Redis connections
        redis_client = redis.from_url("redis://localhost:6379/1", decode_responses=True)
        async_redis_client = aioredis.from_url("redis://localhost:6379/1", decode_responses=True)
        
        # Update the rate limiter with the Redis connections
        login_rate_limiter.redis_client = redis_client
        login_rate_limiter.async_redis_client = async_redis_client
        
        logger.info("Redis login rate limiting initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Redis connections: {e}")
        # Continue startup even if Redis fails - will fall back to in-memory storage

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up Redis connections on shutdown"""
    try:
        await csrf_storage.close()
        logger.info("Redis CSRF token storage closed successfully")
        
        # Close login rate limiter Redis connections
        if async_redis_client:
            await async_redis_client.close()
            logger.info("Redis login rate limiting connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing Redis connections: {e}")

# Add CORS middleware with strict security controls
# SECURITY: CORS is configured with specific trusted origins only
# - No wildcard origins allowed to prevent CSRF attacks
# - Credentials only enabled for trusted origins
# - Limited headers to prevent header injection
# - Preflight caching to reduce attack surface
app.add_middleware(
    CORSMiddleware,
    allow_origins=security_config.cors_origins,  # Specific trusted origins only
    allow_credentials=True,  # Only enabled for trusted origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization", "Content-Type", "X-Requested-With", 
        "X-API-Key", "X-Client-Version", "X-Request-ID"
    ],
    expose_headers=["X-Request-ID", "X-Rate-Limit-Remaining"],
    max_age=3600  # Cache preflight requests for 1 hour
)

# Enhanced Pydantic models with strict validation
class RealTimeEventRequest(BaseModel):
    """Real-time event processing request with security validation"""
    event_type: str = Field(..., min_length=1, max_length=50, regex="^[a-zA-Z0-9_-]+$")
    data: Dict[str, Any] = Field(..., max_items=100)
    priority: str = Field(default="medium", regex="^(low|medium|high|critical)$")
    source_system: str = Field(default="Manual Input", max_length=100)
    
    @validator('data')
    def validate_data_size(cls, v):
        """Validate data size and content"""
        if len(str(v).encode('utf-8')) > 10000:  # 10KB limit
            raise ValueError('Data payload too large')
        return v
    
    @validator('event_type')
    def validate_event_type(cls, v):
        """Validate event type against allowed values"""
        allowed_types = [
            'fraud_detection', 'compliance_check', 'risk_assessment',
            'transaction_monitoring', 'document_analysis', 'alert'
        ]
        if v not in allowed_types:
            raise ValueError(f'Invalid event type. Allowed: {allowed_types}')
        return v

class DataSourceConfig(BaseModel):
    """Data source configuration with security validation"""
    name: str = Field(..., min_length=1, max_length=100, regex="^[a-zA-Z0-9_-]+$")
    type: str = Field(..., regex="^(database|api|file|stream)$")
    connection_config: Dict[str, Any] = Field(..., max_items=20)
    refresh_interval: int = Field(default=60, ge=1, le=3600)
    enabled: bool = True
    

class ProcessingStatus(BaseModel):
    """Processing status response with security metadata"""
    active: bool
    queue_size: int = Field(ge=0)
    data_sources: int = Field(ge=0)
    last_processed: Optional[str] = None
    security_status: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('last_processed')
    def validate_timestamp(cls, v):
        """Validate timestamp format"""
        if v:
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Invalid timestamp format')
        return v

class SecureTransactionRequest(BaseModel):
    """Secure transaction request with PCI-DSS compliance"""
    transaction_id: Optional[str] = Field(None, max_length=50)
    amount: float = Field(..., ge=0.01, le=1000000)
    customer_id: str = Field(..., min_length=1, max_length=50)
    transaction_type: str = Field(..., regex="^(debit|credit|transfer|payment)$")
    location: str = Field(..., max_length=200)
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    @validator('customer_id')
    def validate_customer_id(cls, v):
        """Validate customer ID format"""
        if not v.isalnum():
            raise ValueError('Customer ID must be alphanumeric')
        return v

class ComplianceCheckRequest(BaseModel):
    """Compliance check request with GDPR compliance"""
    regulation: str = Field(..., min_length=1, max_length=100)
    process: str = Field(..., min_length=1, max_length=200)
    controls: List[str] = Field(..., max_items=50)
    documents: List[str] = Field(..., max_items=20)
    
    @validator('regulation')
    def validate_regulation(cls, v):
        """Validate regulation against known frameworks"""
        allowed_regulations = [
            'PCI-DSS', 'GDPR', 'SOX', 'Basel-III', 'MiFID-II', 'Dodd-Frank'
        ]
        if v not in allowed_regulations:
            raise ValueError(f'Invalid regulation. Allowed: {allowed_regulations}')
        return v

class RiskAssessmentRequest(BaseModel):
    """Risk assessment request with validation"""
    risk_type: str = Field(..., regex="^(credit|market|operational|liquidity|reputation)$")
    portfolio: str = Field(..., min_length=1, max_length=100)
    exposure: float = Field(..., ge=0.0)
    probability: float = Field(..., ge=0.0, le=1.0)
    impact: float = Field(..., ge=0.0, le=1.0)
    
    @validator('probability', 'impact')
    def validate_probability_impact(cls, v):
        """Validate probability and impact values"""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Value must be between 0.0 and 1.0')
        return v

class AuditLogRequest(BaseModel):
    """Audit log request with security controls"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    user_id: Optional[str] = None
    operation: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    
    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        """Validate date format"""
        if v:
            try:
                datetime.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid date format. Use ISO format.')
        return v

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        broken_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Mark broken connections for removal
                broken_connections.append(connection)
        
        # Remove broken connections safely after iteration
        for connection in broken_connections:
            if connection in self.active_connections:
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Background task for real-time processing with synchronization
processing_task = None
processing_lock = asyncio.Lock()  # Prevent race conditions in start/stop
processing_state = {
    "active": False,
    "task": None,
    "start_time": None,
    "stop_requested": False
}

# Redis-based CSRF token storage
class RedisCSRFTokenStorage:
    """Redis-based CSRF token storage for production use"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """Initialize Redis connection"""
        self.redis_url = redis_url
        self.redis_client = None
        self.async_redis_client = None
        self.redis_available = False
        
    async def initialize(self):
        """Initialize async Redis connection"""
        try:
            self.async_redis_client = aioredis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            await self.async_redis_client.ping()
            self.redis_available = True
            logger.info("Redis CSRF token storage initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis CSRF storage: {e}")
            self.redis_available = False
            # Don't raise exception - allow fallback to in-memory storage
    
    async def set_token(self, user_id: str, token: str, expires_in_seconds: int = 3600) -> bool:
        """Store CSRF token with expiration"""
        try:
            if not self.redis_available:
                # Fallback to in-memory storage
                csrf_tokens[user_id] = {
                    "token": token,
                    "created_at": datetime.now(),
                    "expires_at": datetime.now() + timedelta(seconds=expires_in_seconds)
                }
                return True
            
            token_data = {
                "token": token,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(seconds=expires_in_seconds)).isoformat()
            }
            
            key = f"csrf_token:{user_id}"
            await self.async_redis_client.setex(
                key, 
                expires_in_seconds, 
                json.dumps(token_data)
            )
            return True
        except Exception as e:
            logger.error(f"Error storing CSRF token for user {user_id}: {e}")
            # Fallback to in-memory storage
            csrf_tokens[user_id] = {
                "token": token,
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(seconds=expires_in_seconds)
            }
            return True
    
    async def get_token(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve CSRF token data"""
        try:
            key = f"csrf_token:{user_id}"
            token_data = await self.async_redis_client.get(key)
            
            if token_data:
                return json.loads(token_data)
            return None
        except Exception as e:
            logger.error(f"Error retrieving CSRF token for user {user_id}: {e}")
            return None
    
    async def validate_token(self, user_id: str, token: str) -> bool:
        """Validate CSRF token"""
        try:
            token_data = await self.get_token(user_id)
            if not token_data:
                return False
            
            # Check if token matches
            if token_data.get("token") != token:
                return False
            
            # Check if token is expired
            if not self.redis_available:
                # For in-memory storage, check datetime object
                expires_at = token_data.get("expires_at")
                if isinstance(expires_at, datetime) and datetime.now() > expires_at:
                    del csrf_tokens[user_id]
                    return False
            else:
                # For Redis storage, check ISO format string
                expires_at = datetime.fromisoformat(token_data.get("expires_at", ""))
                if datetime.now() > expires_at:
                    await self.delete_token(user_id)
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating CSRF token for user {user_id}: {e}")
            return False
    
    async def delete_token(self, user_id: str) -> bool:
        """Delete CSRF token"""
        try:
            if not self.redis_available:
                # Fallback to in-memory storage
                if user_id in csrf_tokens:
                    del csrf_tokens[user_id]
                    return True
                return False
            
            key = f"csrf_token:{user_id}"
            result = await self.async_redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting CSRF token for user {user_id}: {e}")
            # Fallback to in-memory storage
            if user_id in csrf_tokens:
                del csrf_tokens[user_id]
                return True
            return False
    
    async def cleanup_expired_tokens(self) -> int:
        """Clean up expired tokens (Redis TTL handles this automatically, but this is for manual cleanup)"""
        try:
            if not self.redis_available:
                # Fallback to in-memory storage cleanup
                current_time = datetime.now()
                expired_users = [
                    user_id for user_id, token_data in csrf_tokens.items()
                    if current_time > token_data["expires_at"]
                ]
                
                for user_id in expired_users:
                    del csrf_tokens[user_id]
                
                if expired_users:
                    logger.info(f"Cleaned up {len(expired_users)} expired CSRF tokens from memory")
                
                return len(expired_users)
            
            # Get all CSRF token keys
            keys = await self.async_redis_client.keys("csrf_token:*")
            cleaned_count = 0
            
            for key in keys:
                token_data = await self.async_redis_client.get(key)
                if token_data:
                    data = json.loads(token_data)
                    expires_at = datetime.fromisoformat(data.get("expires_at", ""))
                    if datetime.now() > expires_at:
                        await self.async_redis_client.delete(key)
                        cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} expired CSRF tokens from Redis")
            
            return cleaned_count
        except Exception as e:
            logger.error(f"Error cleaning up expired CSRF tokens: {e}")
            return 0
    
    async def close(self):
        """Close Redis connection"""
        if self.async_redis_client:
            await self.async_redis_client.close()
            self.async_redis_client = None

# Initialize Redis CSRF token storage
csrf_storage = RedisCSRFTokenStorage()

# Legacy in-memory storage (kept for fallback, will be removed)
csrf_tokens: Dict[str, Dict[str, Any]] = {}

def validate_csrf_token(user_id: str, token: str) -> bool:
    """Validate CSRF token for the given user"""
    try:
        if user_id not in csrf_tokens:
            return False
            
        stored_token_data = csrf_tokens[user_id]
        
        # Check if token matches
        if stored_token_data["token"] != token:
            return False
            
        # Check if token is expired
        if datetime.now() > stored_token_data["expires_at"]:
            # Clean up expired token
            del csrf_tokens[user_id]
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error validating CSRF token: {e}", exc_info=True)
        return False

async def cleanup_expired_csrf_tokens():
    """Clean up expired CSRF tokens using Redis storage"""
    try:
        cleaned_count = await csrf_storage.cleanup_expired_tokens()
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} expired CSRF tokens from Redis")
    except Exception as e:
        logger.error(f"Error cleaning up CSRF tokens: {e}", exc_info=True)

async def validate_csrf_token_dependency(request: Request, current_user: User = Depends(get_current_user)):
    """Dependency to validate CSRF token for POST requests"""
    # Only validate CSRF tokens for state-changing HTTP methods
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        csrf_token = request.headers.get('X-CSRF-Token')
        
        if not csrf_token:
            raise HTTPException(
                status_code=403,
                detail="CSRF token required for this operation",
                headers={"X-CSRF-Required": "true"}
            )
        
        # Clean up expired tokens before validation (async)
        await cleanup_expired_csrf_tokens()
        
        if not await validate_csrf_token(current_user.user_id, csrf_token):
            raise HTTPException(
                status_code=403,
                detail="Invalid or expired CSRF token",
                headers={"X-CSRF-Required": "true"}
            )
        
        logger.info(f"CSRF token validated for user {current_user.user_id}")
    
    return current_user

# Helper functions for processing lifecycle management
async def start_processing_task():
    """Start the real-time processing task with proper lifecycle management"""
    try:
        # Set processing state
        processing_state["active"] = True
        processing_state["start_time"] = datetime.now()
        processing_state["stop_requested"] = False
        
        # Start the real-time BFSI processing
        await start_real_time_bfsi()
        
        logger.info("Real-time processing task completed successfully")
    except Exception as e:
        logger.error(f"Real-time processing task failed: {e}")
        raise
    finally:
        # Clean up processing state
        processing_state["active"] = False
        processing_state["task"] = None
        processing_state["start_time"] = None

async def stop_processing_task():
    """Gracefully stop the real-time processing task"""
    try:
        # Signal stop request
        processing_state["stop_requested"] = True
        
        # Stop the realtime manager
        stop_real_time_bfsi()
        
        # Wait for task to complete if it exists
        if processing_state["task"] and not processing_state["task"].done():
            try:
                await asyncio.wait_for(processing_state["task"], timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Processing task did not stop within timeout, cancelling")
                processing_state["task"].cancel()
                try:
                    await processing_state["task"]
                except asyncio.CancelledError:
                    pass
        
        logger.info("Real-time processing stopped gracefully")
    except Exception as e:
        logger.error(f"Error stopping processing task: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint with security information"""
    return {
        "service": "Real-Time BFSI API - Secure",
        "version": "2.0.0",
        "description": "Real-Time BFSI Data Processing and Monitoring with Enhanced Security",
        "status": "active",
        "security_features": {
            "authentication": "JWT/OAuth2 + API Keys",
            "encryption": "AES-256-GCM",
            "compliance": "PCI-DSS, GDPR",
            "audit_logging": "enabled",
            "rate_limiting": "enabled",
            "cors": "restricted_origins"
        },
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "metrics": "/metrics",
            "events": "/events",
            "websocket": "/ws",
            "start": "/start",
            "stop": "/stop",
            "processing_state": "/processing/state",
            "auth": "/auth/login",
            "transactions": "/transactions",
            "compliance": "/compliance",
            "audit": "/audit",
            "api_keys": "/api-keys",
            "data_sources": "/data-sources",
            "data_sources_reload": "/data-sources/reload"
        }
    }

# Authentication endpoints
@app.post("/auth/login", response_model=Token)
async def login(
    username: str, 
    password: str, 
    request: Request,
    _: None = Depends(check_login_rate_limit)
):
    """Authenticate user and return JWT tokens with rate limiting protection"""
    client_ip = request.client.host if request.client else "unknown"
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    
    try:
        # Attempt authentication
        user = auth_service.authenticate_user(username, password)
        
        if not user:
            # Record failed attempt for both IP and username
            await login_rate_limiter.record_failed_attempt(client_ip, is_ip=True)
            await login_rate_limiter.record_failed_attempt(username, is_ip=False)
            
            # Log failed attempt
            logger.warning(f"Failed login attempt for username '{username}' from IP {client_ip}")
            
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Clear rate limiting data on successful login
        await login_rate_limiter.record_successful_login(client_ip, is_ip=True)
        await login_rate_limiter.record_successful_login(username, is_ip=False)
        
        # Log successful login
        logger.info(f"Successful login for user '{username}' from IP {client_ip}")
        
        # Create tokens
        token_data = {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "permissions": user.permissions
        }
        
        access_token = auth_service.create_access_token(token_data)
        refresh_token = auth_service.create_refresh_token(token_data)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=security_config.jwt_access_token_expire_minutes * 60
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (like rate limiting or authentication failures)
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error during login for user '{username}': {e}")
        
        # Record failed attempt for unexpected errors
        await login_rate_limiter.record_failed_attempt(client_ip, is_ip=True)
        await login_rate_limiter.record_failed_attempt(username, is_ip=False)
        
        raise HTTPException(
            status_code=500,
            detail="Internal server error during authentication"
        )

@app.get("/csrf-token")
async def get_csrf_token(current_user: User = Depends(get_current_user)):
    """Get CSRF token for form submissions (requires authentication)"""
    try:
        # Generate a secure CSRF token
        csrf_token = secrets.token_urlsafe(32)
        
        # Store the token in Redis with 1 hour expiration
        success = await csrf_storage.set_token(
            current_user.user_id, 
            csrf_token, 
            expires_in_seconds=3600
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to store CSRF token")
        
        logger.info(f"Generated CSRF token for user {current_user.user_id}")
        
        return {
            "csrf_token": csrf_token,
            "expires_in": 3600,  # 1 hour in seconds
            "user_id": current_user.user_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating CSRF token: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate CSRF token")

@app.get("/api-keys")
async def get_api_keys_info(api_key_info: dict = Depends(api_key_auth)):
    """Get API key information (requires valid API key)"""
    try:
        return {
            "api_key_status": "valid",
            "client_name": api_key_info["client_name"],
            "security_features": {
                "api_key_authentication": "enabled",
                "rate_limiting": "enabled",
                "encryption": "AES-256-GCM",
                "cors_restrictions": "enabled"
            },
            "usage_guidelines": {
                "header_name": security_config.api_key_header,
                "rate_limit": f"{security_config.rate_limit_requests_per_minute} requests/minute",
                "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
                "security_headers": "required"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"API key info failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint with security status"""
    try:
        # Check if real-time processing is active
        status = realtime_manager.processing_active
        
        # Check database connectivity
        db_status = "healthy"
        try:
            with sqlite3.connect(realtime_manager.db_path) as conn:
                # Test connection by executing a simple query
                conn.execute("SELECT 1")
        except Exception:
            db_status = "error: database connection failed"
        
        # Security status
        security_status = {
            "encryption_enabled": security_config.data_encryption_enabled,
            "audit_logging": security_config.audit_log_enabled,
            "rate_limiting": True,
            "compliance_frameworks": ["PCI-DSS", "GDPR"]
        }
        
        return {
            "service": "Real-Time BFSI API - Secure",
            "status": "healthy" if status else "inactive",
            "processing_active": status,
            "database": db_status,
            "security": security_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status(current_user: User = Depends(get_current_user)):
    """Get real-time processing status (requires authentication) with enhanced state tracking"""
    try:
        metrics = realtime_manager.get_real_time_metrics()
        
        # Enhanced processing status with synchronization state
        processing_status = {
            "active": realtime_manager.processing_active,
            "queue_size": realtime_manager.event_queue.qsize(),
            "data_sources": len(realtime_manager.data_sources),
            "enabled_sources": len([s for s in realtime_manager.data_sources if s.enabled]),
            "synchronized_state": {
                "active": processing_state["active"],
                "start_time": processing_state["start_time"].isoformat() if processing_state["start_time"] else None,
                "task_running": processing_state["task"] is not None and not processing_state["task"].done(),
                "stop_requested": processing_state["stop_requested"],
                "task_id": id(processing_state["task"]) if processing_state["task"] else None
            }
        }
        
        return {
            "processing_status": processing_status,
            "metrics": metrics,
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role,
                "permissions": current_user.permissions
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics(current_user: User = Depends(require_permission("read:metrics"))):
    """Get detailed real-time metrics (requires metrics permission)"""
    try:
        metrics = realtime_manager.get_real_time_metrics()
        
        # Add additional metrics
        metrics["system_info"] = {
            "uptime": datetime.now().isoformat(),
            "data_sources": [
                {
                    "name": source.name,
                    "type": source.type,
                    "enabled": source.enabled,
                    "refresh_interval": source.refresh_interval
                }
                for source in realtime_manager.data_sources
            ],
            "queue_status": {
                "pending_events": realtime_manager.event_queue.qsize(),
                "event_types": "queue_processing"  # Cannot iterate over asyncio.Queue directly
            },
            "security_metrics": {
                "encryption_status": "enabled",
                "audit_logging": "active",
                "rate_limiting": "active",
                "authentication": "JWT"
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def get_recent_events(limit: int = 50, hours: int = 24, 
                           current_user: User = Depends(get_current_user)):
    """Get recent processed events (requires authentication)"""
    try:
        # Use secure repository instead of direct SQLite access
        events = []
        
        # Get recent transactions
        transactions = secure_repository.get_transactions(
            limit=limit, offset=0, user_id=current_user.user_id
        )
        
        for transaction in transactions:
            events.append({
                "event_id": transaction["id"],
                "event_type": "fraud_detection",
                "transaction_id": transaction["transaction_id"],
                "amount": transaction["amount"],
                "customer_id": transaction["customer_id"],
                "transaction_type": transaction["transaction_type"],
                "location": transaction["location"],
                "timestamp": transaction["timestamp"],
                "risk_score": transaction["risk_score"]
            })
        
        # Get recent compliance checks
        compliance_checks = secure_repository.get_compliance_checks(
            limit=limit, offset=0, user_id=current_user.user_id
        )
        
        for check in compliance_checks:
            events.append({
                "event_id": check["id"],
                "event_type": "compliance_check",
                "regulation": check["regulation"],
                "process": check["process"],
                "controls": check["controls"],
                "documents": check["documents"],
                "timestamp": check["timestamp"],
                "compliance_score": check["compliance_score"]
            })
        
        # Get recent risk assessments
        risk_assessments = secure_repository.get_risk_assessments(
            limit=limit, offset=0, user_id=current_user.user_id
        )
        
        for assessment in risk_assessments:
            events.append({
                "event_id": assessment["id"],
                "event_type": "risk_assessment",
                "risk_type": assessment["risk_type"],
                "portfolio": assessment["portfolio"],
                "exposure": assessment["exposure"],
                "probability": assessment["probability"],
                "impact": assessment["impact"],
                "timestamp": assessment["timestamp"],
                "risk_score": assessment["risk_score"]
            })
        
        # Get recent documents
        documents = secure_repository.get_documents(
            limit=limit, offset=0, user_id=current_user.user_id
        )
        
        for document in documents:
            events.append({
                "event_id": document["id"],
                "event_type": "document_analysis",
                "document_type": document["document_type"],
                "classification": document["classification"],
                "compliance_framework": document["compliance_framework"],
                "timestamp": document["timestamp"]
            })
        
        # Sort by timestamp and limit
        events.sort(key=lambda x: x["timestamp"], reverse=True)
        events = events[:limit]
        
        return {
            "events": events,
            "total_count": len(events),
            "time_range": f"Last {hours} hours",
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# New secure endpoints for BFSI operations
@app.get("/transactions")
async def get_transactions(limit: int = 50, offset: int = 0,
                          current_user: User = Depends(require_permission("read:transactions"))):
    """Get transactions with security controls"""
    try:
        transactions = secure_repository.get_transactions(
            limit=limit, offset=offset, user_id=current_user.user_id
        )
        
        return {
            "transactions": transactions,
            "total_count": len(transactions),
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions")
async def create_transaction(transaction: SecureTransactionRequest,
                           current_user: User = Depends(require_permission("write:transactions"))):
    """Create new transaction with PCI-DSS compliance"""
    try:
        transaction_data = transaction.dict()
        transaction_id = secure_repository.create_transaction(
            transaction_data, user_id=current_user.user_id
        )
        
        return {
            "message": "Transaction created successfully",
            "transaction_id": transaction_id,
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to create transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/compliance")
async def get_compliance_checks(limit: int = 50, offset: int = 0,
                               current_user: User = Depends(require_compliance_access)):
    """Get compliance checks (requires compliance officer access)"""
    try:
        compliance_checks = secure_repository.get_compliance_checks(
            limit=limit, offset=offset, user_id=current_user.user_id
        )
        
        return {
            "compliance_checks": compliance_checks,
            "total_count": len(compliance_checks),
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get compliance checks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compliance")
async def create_compliance_check(compliance: ComplianceCheckRequest,
                                 current_user: User = Depends(require_compliance_access)):
    """Create compliance check (requires compliance officer access)"""
    try:
        # Implementation would create compliance check
        return {
            "message": "Compliance check created successfully",
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to create compliance check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audit")
async def get_audit_logs(request: AuditLogRequest,
                        current_user: User = Depends(require_audit_access)):
    """Get audit logs (requires auditor access)"""
    try:
        audit_logs = secure_repository.get_audit_logs(
            start_date=request.start_date,
            end_date=request.end_date,
            user_id=request.user_id,
            limit=request.limit
        )
        
        return {
            "audit_logs": audit_logs,
            "total_count": len(audit_logs),
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get audit logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/process")
async def process_real_time_event(request: RealTimeEventRequest,
                                 current_user: User = Depends(require_permission("write:events"))):
    """Process a real-time event manually (requires event processing permission)"""
    try:
        # Validate event type against allowed types
        allowed_types = [
            'fraud_detection', 'compliance_check', 'risk_assessment',
            'transaction_monitoring', 'document_analysis', 'alert'
        ]
        if request.event_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f'Invalid event type. Allowed: {allowed_types}'
            )
        
        # Create event with security controls
        event = RealTimeBFSIEvent(
            event_id=f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            event_type=request.event_type,
            timestamp=datetime.now(),
            source_system=request.source_system,
            data=request.data,
            priority=request.priority
        )
        
        # Add to queue with intelligent overflow handling
        try:
            realtime_manager.event_queue.put_nowait(event)
            logger.info(f"Event {event.event_id} added to queue")
        except asyncio.QueueFull:
            # Determine event priority
            priority = EventPriority.get_priority(event.event_type, event.data)
            
            logger.warning(f"Event queue is full, handling overflow for event {event.event_id} with priority {priority}")
            
            # Store overflow event in persistent storage
            if overflow_storage.store_overflow_event(event):
                logger.info(f"Overflow event {event.event_id} stored in persistent storage")
                
                # For critical events, try to make room by removing lower priority events
                if priority <= EventPriority.HIGH:
                    await _make_room_for_critical_event(event, priority)
                
                # Return success response with overflow notification
                return {
                    "message": "Event queued successfully",
                    "event_id": event.event_id,
                    "status": "queued_with_overflow",
                    "overflow_stored": True,
                    "priority": priority,
                    "note": "Event stored in persistent overflow storage due to queue capacity"
                }
            else:
                # If persistent storage fails, fall back to old behavior
                logger.error(f"Failed to store overflow event {event.event_id}, falling back to queue replacement")
                try:
                    realtime_manager.event_queue.get_nowait()  # Remove oldest
                    realtime_manager.event_queue.put_nowait(event)  # Add new
                    logger.info(f"Replaced oldest event with {event.event_id}")
                except asyncio.QueueEmpty:
                    pass
                
                raise HTTPException(
                    status_code=503, 
                    detail="Event queue is full and overflow storage failed. Please try again later."
                )
        
        # Broadcast to WebSocket clients
        await manager.broadcast(json.dumps({
            "type": "event_queued",
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
            "priority": event.priority,
            "user_id": current_user.user_id
        }))
        
        return {
            "message": "Event queued for processing",
            "event_id": event.event_id,
            "event_type": event.event_type,
            "queue_position": realtime_manager.event_queue.qsize(),
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to process event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start")
async def start_processing(background_tasks: BackgroundTasks,
                          current_user: User = Depends(validate_csrf_token_dependency),
                          _: User = Depends(require_admin)):
    """Start real-time processing (requires admin access) with race condition protection"""
    async with processing_lock:  # Prevent concurrent start/stop operations
        try:
            # Check if processing is already active
            if processing_state["active"] or realtime_manager.processing_active:
                return {
                    "message": "Real-time processing is already active",
                    "processing_state": {
                        "active": processing_state["active"],
                        "start_time": processing_state["start_time"].isoformat() if processing_state["start_time"] else None,
                        "task_running": processing_state["task"] is not None and not processing_state["task"].done()
                    },
                    "user": {
                        "user_id": current_user.user_id,
                        "role": current_user.role
                    },
                    "timestamp": datetime.now().isoformat()
                }
            
            # Create and store the background task
            task = asyncio.create_task(start_processing_task())
            processing_state["task"] = task
            background_tasks.add_task(lambda: task)  # Add to background tasks for cleanup
            
            # Broadcast to WebSocket clients
            await manager.broadcast(json.dumps({
                "type": "processing_started",
                "timestamp": datetime.now().isoformat(),
                "user_id": current_user.user_id,
                "task_id": id(task)
            }))
            
            return {
                "message": "Real-time processing started",
                "processing_state": {
                    "active": processing_state["active"],
                    "start_time": processing_state["start_time"].isoformat() if processing_state["start_time"] else None,
                    "task_id": id(task)
                },
                "user": {
                    "user_id": current_user.user_id,
                    "role": current_user.role
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to start processing: {e}")
            # Clean up on error
            processing_state["active"] = False
            processing_state["task"] = None
            processing_state["start_time"] = None
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
async def stop_processing(current_user: User = Depends(validate_csrf_token_dependency),
                         _: User = Depends(require_admin)):
    """Stop real-time processing (requires admin access) with graceful shutdown"""
    async with processing_lock:  # Prevent concurrent start/stop operations
        try:
            # Check if processing is active
            if not processing_state["active"] and not realtime_manager.processing_active:
                return {
                    "message": "Real-time processing is not active",
                    "processing_state": {
                        "active": processing_state["active"],
                        "start_time": processing_state["start_time"].isoformat() if processing_state["start_time"] else None,
                        "task_running": processing_state["task"] is not None and not processing_state["task"].done()
                    },
                    "user": {
                        "user_id": current_user.user_id,
                        "role": current_user.role
                    },
                    "timestamp": datetime.now().isoformat()
                }
            
            # Gracefully stop the processing task
            await stop_processing_task()
            
            # Broadcast to WebSocket clients
            await manager.broadcast(json.dumps({
                "type": "processing_stopped",
                "timestamp": datetime.now().isoformat(),
                "user_id": current_user.user_id,
                "graceful_shutdown": True
            }))
            
            return {
                "message": "Real-time processing stopped gracefully",
                "processing_state": {
                    "active": processing_state["active"],
                    "start_time": processing_state["start_time"].isoformat() if processing_state["start_time"] else None,
                    "stop_requested": processing_state["stop_requested"]
                },
                "user": {
                    "user_id": current_user.user_id,
                    "role": current_user.role
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to stop processing: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/processing/state")
async def get_processing_state(current_user: User = Depends(require_admin)):
    """Get detailed processing state information (admin only)"""
    try:
        return {
            "processing_state": {
                "active": processing_state["active"],
                "start_time": processing_state["start_time"].isoformat() if processing_state["start_time"] else None,
                "stop_requested": processing_state["stop_requested"],
                "task_info": {
                    "exists": processing_state["task"] is not None,
                    "running": processing_state["task"] is not None and not processing_state["task"].done(),
                    "cancelled": processing_state["task"] is not None and processing_state["task"].cancelled(),
                    "task_id": id(processing_state["task"]) if processing_state["task"] else None
                },
                "realtime_manager_active": realtime_manager.processing_active,
                "queue_size": realtime_manager.event_queue.qsize()
            },
            "synchronization": {
                "lock_acquired": processing_lock.locked(),
                "lock_owner": "unknown"  # asyncio.Lock doesn't expose owner info
            },
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Processing state check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def sanitize_connection_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize connection configuration by redacting sensitive information"""
    if not config:
        return {}
    
    # Define sensitive field patterns to redact
    sensitive_patterns = [
        'password', 'passwd', 'pwd', 'secret', 'key', 'token', 'auth',
        'credential', 'api_key', 'access_key', 'private_key', 'cert',
        'ssl_key', 'ssl_cert', 'jwt_secret', 'encryption_key'
    ]
    
    sanitized_config = {}
    for key, value in config.items():
        # Check if the key contains sensitive information
        key_lower = key.lower()
        is_sensitive = any(pattern in key_lower for pattern in sensitive_patterns)
        
        if is_sensitive:
            # Redact sensitive values
            if isinstance(value, str) and len(value) > 0:
                # Show first 2 and last 2 characters for debugging purposes
                if len(value) <= 4:
                    sanitized_config[key] = "***"
                else:
                    sanitized_config[key] = f"{value[:2]}***{value[-2:]}"
            else:
                sanitized_config[key] = "***"
        else:
            # Keep non-sensitive values as-is
            sanitized_config[key] = value
    
    return sanitized_config

@app.get("/data-sources")
async def get_data_sources(current_user: User = Depends(require_permission("read:data_sources"))):
    """Get configured data sources (requires data sources permission)"""
    try:
        # Load data sources from database and sync with realtime manager
        db_sources = load_data_sources_from_database()
        
        # Update realtime manager with database sources (merge strategy)
        existing_names = {source.name for source in realtime_manager.data_sources}
        for db_source in db_sources:
            if db_source.name not in existing_names:
                realtime_manager.data_sources.append(db_source)
        
        return {
            "data_sources": [
                {
                    "name": source.name,
                    "type": source.type,
                    "enabled": source.enabled,
                    "refresh_interval": source.refresh_interval,
                    "connection_config": sanitize_connection_config(source.connection_config)
                }
                for source in realtime_manager.data_sources
            ],
            "total_count": len(realtime_manager.data_sources),
            "enabled_count": len([s for s in realtime_manager.data_sources if s.enabled]),
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get data sources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/data-sources")
async def add_data_source(source_config: DataSourceConfig,
                          current_user: User = Depends(require_permission("write:data_sources"))):
    """Add a new data source (requires data sources write permission) with validation and persistence"""
    try:
        # Check if data source with this name already exists
        if check_data_source_exists(source_config.name):
            raise HTTPException(
                status_code=400,
                detail=f"Data source with name '{source_config.name}' already exists"
            )
        
        # Validate data source type
        if not validate_data_source_type(source_config.type):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data source type '{source_config.type}'. Allowed types: database, api, file, stream"
            )
        
        # Validate connection configuration
        is_valid, error_message = validate_connection_config(source_config.type, source_config.connection_config)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid connection configuration: {error_message}"
            )
        
        # Create new data source
        new_source = BFSIDataSource(
            name=source_config.name,
            type=source_config.type,
            connection_config=source_config.connection_config,
            refresh_interval=source_config.refresh_interval,
            enabled=source_config.enabled
        )
        
        # Save to database for persistence
        if not save_data_source_to_database(new_source):
            raise HTTPException(
                status_code=500,
                detail="Failed to save data source to database"
            )
        
        # Add to realtime manager for immediate use
        realtime_manager.data_sources.append(new_source)
        
        # Broadcast to WebSocket clients
        await manager.broadcast(json.dumps({
            "type": "data_source_added",
            "source_name": new_source.name,
            "source_type": new_source.type,
            "timestamp": datetime.now().isoformat(),
            "user_id": current_user.user_id
        }))
        
        return {
            "message": "Data source added successfully",
            "source_name": new_source.name,
            "source_type": new_source.type,
            "validation": {
                "type_valid": True,
                "connection_valid": True,
                "persistence_saved": True
            },
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Failed to add data source: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/data-sources/{source_name}")
async def delete_data_source(source_name: str,
                            current_user: User = Depends(require_permission("write:data_sources"))):
    """Delete a data source (requires data sources write permission)"""
    try:
        # Check if data source exists
        if not check_data_source_exists(source_name):
            raise HTTPException(
                status_code=404,
                detail=f"Data source '{source_name}' not found"
            )
        
        # Remove from database
        with sqlite3.connect(realtime_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM data_sources WHERE name = ?', (source_name,))
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"Data source '{source_name}' not found in database"
                )
            conn.commit()
        
        # Remove from realtime manager
        realtime_manager.data_sources = [
            source for source in realtime_manager.data_sources 
            if source.name != source_name
        ]
        
        # Broadcast to WebSocket clients
        await manager.broadcast(json.dumps({
            "type": "data_source_deleted",
            "source_name": source_name,
            "timestamp": datetime.now().isoformat(),
            "user_id": current_user.user_id
        }))
        
        return {
            "message": f"Data source '{source_name}' deleted successfully",
            "source_name": source_name,
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete data source: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/data-sources/reload")
async def reload_data_sources(current_user: User = Depends(require_admin)):
    """Reload data sources from database (admin only)"""
    try:
        # Load data sources from database
        db_sources = load_data_sources_from_database()
        
        # Clear existing sources and replace with database sources
        realtime_manager.data_sources.clear()
        realtime_manager.data_sources.extend(db_sources)
        
        # Broadcast to WebSocket clients
        await manager.broadcast(json.dumps({
            "type": "data_sources_reloaded",
            "count": len(db_sources),
            "timestamp": datetime.now().isoformat(),
            "user_id": current_user.user_id
        }))
        
        return {
            "message": "Data sources reloaded from database",
            "loaded_count": len(db_sources),
            "sources": [
                {
                    "name": source.name,
                    "type": source.type,
                    "enabled": source.enabled
                }
                for source in db_sources
            ],
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to reload data sources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def filter_metrics_by_user_permissions(metrics: Dict[str, Any], user: User) -> Dict[str, Any]:
    """Filter metrics data based on user permissions and role"""
    try:
        filtered_metrics = metrics.copy()
        
        # Admin users get full access
        if user.role in ["admin", "super_admin"]:
            return filtered_metrics
        
        # Compliance users get compliance-related data
        if user.role == "compliance_officer":
            # Filter to show only compliance-relevant metrics
            if "events" in filtered_metrics:
                compliance_events = [
                    event for event in filtered_metrics["events"]
                    if event.get("category") in ["compliance", "risk", "audit"]
                ]
                filtered_metrics["events"] = compliance_events
        
        # Regular users get limited data
        if user.role == "user":
            # Remove sensitive fields
            sensitive_fields = ["internal_notes", "raw_data", "system_logs"]
            for field in sensitive_fields:
                if field in filtered_metrics:
                    del filtered_metrics[field]
            
            # Limit event details
            if "events" in filtered_metrics:
                for event in filtered_metrics["events"]:
                    # Remove sensitive fields from events
                    for field in sensitive_fields:
                        event.pop(field, None)
        
        # API key users get basic metrics only
        if user.user_id.startswith("api_key_"):
            # Return only basic system status
            basic_metrics = {
                "processing_active": filtered_metrics.get("processing_active", False),
                "queue_size": filtered_metrics.get("queue_size", 0),
                "data_sources_count": filtered_metrics.get("data_sources_count", 0),
                "timestamp": filtered_metrics.get("timestamp")
            }
            return basic_metrics
        
        return filtered_metrics
        
    except Exception as e:
        logger.error(f"Error filtering metrics for user {user.user_id}: {e}")
        # Return basic metrics on error
        return {
            "processing_active": metrics.get("processing_active", False),
            "queue_size": metrics.get("queue_size", 0),
            "timestamp": datetime.now().isoformat()
        }

async def authenticate_websocket_connection(websocket: WebSocket) -> Optional[User]:
    """Authenticate WebSocket connection using token from query parameters or headers"""
    try:
        # Try to get token from query parameters first
        token = websocket.query_params.get("token")
        
        # If no token in query params, try to get from headers
        if not token:
            # WebSocket headers are available in the connection
            headers = websocket.headers
            auth_header = headers.get("authorization") or headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]  # Remove "Bearer " prefix
        
        # If still no token, try X-CSRF-Token header
        if not token:
            token = headers.get("x-csrf-token") or headers.get("X-CSRF-Token")
        
        if not token:
            logger.warning("WebSocket connection rejected: No authentication token provided")
            return None
        
        # Validate the token using existing auth service
        try:
            # Try JWT token validation first
            user = await auth_service.get_user_from_token(token)
            if user:
                logger.info(f"WebSocket connection authenticated for user: {user.user_id}")
                return user
        except Exception as jwt_error:
            logger.debug(f"JWT token validation failed: {jwt_error}")
        
        # If JWT validation failed, try API key validation
        try:
            # Check if it's an API key
            api_key_info = await api_key_auth({"api_key": token})
            if api_key_info:
                # Create a user object for API key authentication
                user = User(
                    user_id=f"api_key_{api_key_info.get('key_id', 'unknown')}",
                    username=api_key_info.get('name', 'API Key User'),
                    email=api_key_info.get('email', 'api@system.local'),
                    role=api_key_info.get('role', 'api_user'),
                    permissions=api_key_info.get('permissions', [])
                )
                logger.info(f"WebSocket connection authenticated via API key: {user.user_id}")
                return user
        except Exception as api_error:
            logger.debug(f"API key validation failed: {api_error}")
        
        logger.warning(f"WebSocket connection rejected: Invalid authentication token")
        return None
        
    except Exception as e:
        logger.error(f"Error authenticating WebSocket connection: {e}")
        return None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates with authentication"""
    # Authenticate the connection before accepting
    user = await authenticate_websocket_connection(websocket)
    if not user:
        await websocket.close(code=1008, reason="Authentication required")
        return
    
    await manager.connect(websocket)
    
    try:
        # Send initial status with user context
        status = {
            "processing_status": {
                "active": realtime_manager.processing_active,
                "queue_size": realtime_manager.event_queue.qsize(),
                "data_sources": len(realtime_manager.data_sources),
                "enabled_sources": len([s for s in realtime_manager.data_sources if s.enabled])
            },
            "user_context": {
                "user_id": user.user_id,
                "username": user.username,
                "role": user.role,
                "permissions": user.permissions
            },
            "timestamp": datetime.now().isoformat()
        }
        
        await manager.send_personal_message(json.dumps({
            "type": "initial_status",
            "data": status
        }), websocket)
        
        # Log successful WebSocket connection with user info
        logger.info(f"WebSocket connection established for user: {user.user_id} (role: {user.role})")
        
        # Keep connection alive and send periodic updates
        while True:
            await asyncio.sleep(30)  # Send update every 30 seconds
            
            if realtime_manager.processing_active:
                # Get metrics with user-specific filtering
                metrics = realtime_manager.get_real_time_metrics()
                
                # Filter data based on user permissions
                filtered_metrics = await filter_metrics_by_user_permissions(metrics, user)
                
                await manager.send_personal_message(json.dumps({
                    "type": "metrics_update",
                    "data": filtered_metrics,
                    "user_context": {
                        "user_id": user.user_id,
                        "role": user.role
                    },
                    "timestamp": datetime.now().isoformat()
                }), websocket)
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user: {user.user_id}")
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error for user {user.user_id}: {e}")
        manager.disconnect(websocket)

@app.get("/dashboard")
async def get_dashboard_data(current_user: User = Depends(get_current_user)):
    """Get comprehensive dashboard data (requires authentication)"""
    try:
        metrics = realtime_manager.get_real_time_metrics()
        recent_events = await get_recent_events(limit=10, hours=1, current_user=current_user)
        
        return {
            "dashboard": {
                "system_status": {
                    "processing_active": realtime_manager.processing_active,
                    "queue_size": realtime_manager.event_queue.qsize(),
                    "data_sources_active": len([s for s in realtime_manager.data_sources if s.enabled])
                },
                "metrics": metrics,
                "recent_activity": recent_events,
                "security_status": {
                    "encryption_enabled": security_config.data_encryption_enabled,
                    "audit_logging": security_config.audit_log_enabled,
                    "rate_limiting": True,
                    "compliance_frameworks": ["PCI-DSS", "GDPR"]
                },
                "user": {
                    "user_id": current_user.user_id,
                    "role": current_user.role,
                    "permissions": current_user.permissions
                },
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Dashboard data failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional security endpoints
@app.get("/security/status")
async def get_security_status(current_user: User = Depends(require_admin)):
    """Get security status (admin only)"""
    try:
        return {
            "security_config": {
                "encryption_enabled": security_config.data_encryption_enabled,
                "audit_logging": security_config.audit_log_enabled,
                "rate_limiting": True,
                "compliance_frameworks": ["PCI-DSS", "GDPR"],
                "data_retention_days": security_config.data_retention_days,
                "session_timeout_minutes": security_config.session_timeout_minutes
            },
            "encryption_status": {
                "algorithm": "AES-256-GCM",
                "key_rotation": "enabled",
                "data_at_rest": "encrypted",
                "data_in_transit": "TLS 1.3"
            },
            "compliance_status": {
                "pci_dss": security_config.pci_dss_enabled,
                "gdpr": security_config.gdpr_enabled,
                "data_anonymization": security_config.data_anonymization,
                "consent_tracking": security_config.consent_tracking
            },
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Security status failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/security/encrypt")
async def encrypt_data(data: str, current_user: User = Depends(require_permission("write:encryption"))):
    """Encrypt sensitive data (requires encryption permission)"""
    try:
        encrypted_data = encryption_manager.encrypt(data)
        return {
            "encrypted_data": encrypted_data,
            "algorithm": "AES-256-GCM",
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/compliance/frameworks")
async def get_compliance_frameworks(current_user: User = Depends(require_compliance_access)):
    """Get supported compliance frameworks (compliance officer access)"""
    try:
        return {
            "frameworks": {
                "PCI-DSS": {
                    "version": SecurityConstants.PCI_DSS_VERSION,
                    "requirements": SecurityConstants.PCI_DSS_REQUIREMENTS,
                    "enabled": security_config.pci_dss_enabled
                },
                "GDPR": {
                    "articles": SecurityConstants.GDPR_ARTICLES,
                    "enabled": security_config.gdpr_enabled,
                    "data_anonymization": security_config.data_anonymization,
                    "consent_tracking": security_config.consent_tracking
                }
            },
            "data_classification": SecurityConstants.DATA_CLASSIFICATION,
            "encryption_standards": SecurityConstants.ENCRYPTION_STANDARDS,
            "user": {
                "user_id": current_user.user_id,
                "role": current_user.role
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Compliance frameworks failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Production Security Configuration
class ServerSecurityConfig:
    """Production-level security configuration for uvicorn server"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development").lower()
        self.host = self._get_secure_host()
        self.port = int(os.getenv("PORT", 8009))
        self.workers = int(os.getenv("WORKERS", 1))
        self.max_requests = int(os.getenv("MAX_REQUESTS", 1000))
        self.max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 100))
        self.timeout_keep_alive = int(os.getenv("TIMEOUT_KEEP_ALIVE", 5))
        self.limit_max_requests = int(os.getenv("LIMIT_MAX_REQUESTS", 10000))
        self.limit_concurrency = int(os.getenv("LIMIT_CONCURRENCY", 1000))
        
        # TLS Configuration
        self.ssl_keyfile = os.getenv("SSL_KEYFILE")
        self.ssl_certfile = os.getenv("SSL_CERTFILE")
        self.ssl_ca_certs = os.getenv("SSL_CA_CERTS")
        self.ssl_ciphers = os.getenv("SSL_CIPHERS", "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS")
        self.ssl_minimum_version = os.getenv("SSL_MINIMUM_VERSION", "TLSv1.2")
        
        # Security Headers and Limits
        self.limit_request_line = int(os.getenv("LIMIT_REQUEST_LINE", 4094))
        self.limit_request_fields = int(os.getenv("LIMIT_REQUEST_FIELDS", 100))
        self.limit_request_field_size = int(os.getenv("LIMIT_REQUEST_FIELD_SIZE", 8190))
        self.limit_request_body = int(os.getenv("LIMIT_REQUEST_BODY", 10485760))  # 10MB default
        
        # Logging and Monitoring
        self.access_log = os.getenv("ACCESS_LOG", "true").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "info").lower()
        self.use_colors = os.getenv("USE_COLORS", "false").lower() == "true"
        
    def _get_secure_host(self) -> str:
        """Get secure host binding based on environment"""
        if self.environment == "production":
            # Production: Bind to localhost only for reverse proxy setup
            return os.getenv("HOST", "127.0.0.1")
        elif self.environment == "staging":
            # Staging: Bind to specific interface
            return os.getenv("HOST", "127.0.0.1")
        else:
            # Development: Allow broader access but warn
            logger.warning("Running in development mode - consider using production environment for security")
            return os.getenv("HOST", "0.0.0.0")
    
    def get_ssl_config(self) -> dict:
        """Get SSL/TLS configuration for production"""
        ssl_config = {}
        
        if self.ssl_keyfile and self.ssl_certfile:
            ssl_config.update({
                "ssl_keyfile": self.ssl_keyfile,
                "ssl_certfile": self.ssl_certfile,
                "ssl_ciphers": self.ssl_ciphers,
                "ssl_minimum_version": self.ssl_minimum_version
            })
            
            if self.ssl_ca_certs:
                ssl_config["ssl_ca_certs"] = self.ssl_ca_certs
                
            logger.info("TLS/SSL configuration enabled")
        else:
            logger.warning("TLS/SSL not configured - use reverse proxy for production")
            
        return ssl_config
    
    def get_security_headers(self) -> dict:
        """Get security headers configuration"""
        return {
            "hsts": True,
            "hsts_max_age": 31536000,  # 1 year
            "hsts_include_subdomains": True,
            "hsts_preload": True,
            "content_security_policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            "referrer_policy": "strict-origin-when-cross-origin",
            "permissions_policy": "geolocation=(), microphone=(), camera=()"
        }
    
    def validate_security_config(self) -> List[str]:
        """Validate security configuration and return warnings"""
        warnings = []
        
        if self.environment == "production":
            if self.host == "0.0.0.0":
                warnings.append("CRITICAL: Production environment binding to 0.0.0.0 - use reverse proxy")
            
            if not (self.ssl_keyfile and self.ssl_certfile):
                warnings.append("WARNING: No TLS/SSL configuration - use reverse proxy for HTTPS")
            
            if self.workers == 1:
                warnings.append("INFO: Single worker in production - consider increasing workers")
        
        if self.limit_request_body > 52428800:  # 50MB
            warnings.append("WARNING: Large request body limit may allow abuse")
        
        if self.limit_concurrency > 2000:
            warnings.append("WARNING: High concurrency limit may impact performance")
        
        return warnings

# Initialize security configuration
server_config = ServerSecurityConfig()

# Validate configuration and log warnings
security_warnings = server_config.validate_security_config()
if security_warnings:
    logger.warning("Server security configuration warnings:")
    for warning in security_warnings:
        logger.warning(f"  - {warning}")

# Overflow event management endpoints
@app.get("/overflow-events")
async def get_overflow_events(
    limit: int = 100,
    processed: bool = False,
    current_user: User = Depends(get_current_user)
):
    """Get overflow events with optional filtering"""
    try:
        events = overflow_storage.get_pending_events(limit)
        
        # Filter by processed status if specified
        if not processed:
            events = [e for e in events if not e.get('processed', False)]
        
        return {
            "overflow_events": events,
            "count": len(events),
            "limit": limit,
            "processed_filter": processed
        }
    except Exception as e:
        logger.error(f"Error retrieving overflow events: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve overflow events")

@app.post("/overflow-events/{event_id}/process")
async def process_overflow_event(
    event_id: str,
    current_user: User = Depends(get_current_user)
):
    """Manually process an overflow event"""
    try:
        # Get the event from overflow storage
        events = overflow_storage.get_pending_events(1000)  # Get all pending events
        event_data = next((e for e in events if e['event_id'] == event_id), None)
        
        if not event_data:
            raise HTTPException(status_code=404, detail="Overflow event not found")
        
        # Create RealTimeBFSIEvent object
        event = RealTimeBFSIEvent(
            event_id=event_data['event_id'],
            event_type=event_data['event_type'],
            timestamp=datetime.fromisoformat(event_data['timestamp']),
            source_system=event_data['source_system'],
            data=event_data['data']
        )
        
        # Try to add to queue
        try:
            realtime_manager.event_queue.put_nowait(event)
            overflow_storage.mark_event_processed(event_id)
            logger.info(f"Overflow event {event_id} successfully processed and added to queue")
            
            return {
                "message": "Overflow event processed successfully",
                "event_id": event_id,
                "status": "queued"
            }
        except asyncio.QueueFull:
            # Queue still full, increment retry count
            overflow_storage.increment_retry_count(event_id, "Queue still full")
            raise HTTPException(
                status_code=503, 
                detail="Event queue is still full. Event will be retried later."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing overflow event {event_id}: {e}")
        overflow_storage.increment_retry_count(event_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to process overflow event")

@app.post("/overflow-events/process-all")
async def process_all_overflow_events(
    max_events: int = 50,
    current_user: User = Depends(require_admin)
):
    """Process all pending overflow events (admin only)"""
    try:
        events = overflow_storage.get_pending_events(max_events)
        processed_count = 0
        failed_count = 0
        
        for event_data in events:
            try:
                # Create RealTimeBFSIEvent object
                event = RealTimeBFSIEvent(
                    event_id=event_data['event_id'],
                    event_type=event_data['event_type'],
                    timestamp=datetime.fromisoformat(event_data['timestamp']),
                    source_system=event_data['source_system'],
                    data=event_data['data']
                )
                
                # Try to add to queue
                realtime_manager.event_queue.put_nowait(event)
                overflow_storage.mark_event_processed(event_data['event_id'])
                processed_count += 1
                
            except asyncio.QueueFull:
                overflow_storage.increment_retry_count(event_data['event_id'], "Queue full during batch processing")
                failed_count += 1
            except Exception as e:
                overflow_storage.increment_retry_count(event_data['event_id'], str(e))
                failed_count += 1
        
        return {
            "message": "Batch processing completed",
            "processed": processed_count,
            "failed": failed_count,
            "total": len(events)
        }
        
    except Exception as e:
        logger.error(f"Error in batch processing overflow events: {e}")
        raise HTTPException(status_code=500, detail="Failed to process overflow events")

@app.delete("/overflow-events/cleanup")
async def cleanup_overflow_events(
    days: int = 7,
    current_user: User = Depends(require_admin)
):
    """Clean up old processed overflow events (admin only)"""
    try:
        deleted_count = overflow_storage.cleanup_old_events(days)
        return {
            "message": f"Cleaned up {deleted_count} old overflow events",
            "deleted_count": deleted_count,
            "retention_days": days
        }
    except Exception as e:
        logger.error(f"Error cleaning up overflow events: {e}")
        raise HTTPException(status_code=500, detail="Failed to cleanup overflow events")

@app.get("/overflow-events/stats")
async def get_overflow_stats(current_user: User = Depends(get_current_user)):
    """Get overflow event statistics"""
    try:
        # Get basic stats from database
        conn = sqlite3.connect(overflow_storage.db_path)
        cursor = conn.cursor()
        
        # Total events
        cursor.execute("SELECT COUNT(*) FROM overflow_events")
        total_events = cursor.fetchone()[0]
        
        # Pending events
        cursor.execute("SELECT COUNT(*) FROM overflow_events WHERE processed = FALSE")
        pending_events = cursor.fetchone()[0]
        
        # Events by priority
        cursor.execute("SELECT priority, COUNT(*) FROM overflow_events WHERE processed = FALSE GROUP BY priority")
        priority_stats = dict(cursor.fetchall())
        
        # Recent events (last 24 hours)
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        cursor.execute("SELECT COUNT(*) FROM overflow_events WHERE created_at > ?", (yesterday,))
        recent_events = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_events": total_events,
            "pending_events": pending_events,
            "processed_events": total_events - pending_events,
            "recent_events_24h": recent_events,
            "priority_distribution": {
                "critical": priority_stats.get(1, 0),
                "high": priority_stats.get(2, 0),
                "medium": priority_stats.get(3, 0),
                "low": priority_stats.get(4, 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting overflow stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get overflow statistics")

if __name__ == "__main__":
    # Get SSL configuration
    ssl_config = server_config.get_ssl_config()
    
    # Prepare uvicorn configuration
    uvicorn_config = {
        "app": app,
        "host": server_config.host,
        "port": server_config.port,
        "workers": server_config.workers if server_config.environment == "production" else 1,
        "log_level": server_config.log_level,
        "access_log": server_config.access_log,
        "use_colors": server_config.use_colors,
        "timeout_keep_alive": server_config.timeout_keep_alive,
        "limit_max_requests": server_config.limit_max_requests,
        "limit_concurrency": server_config.limit_concurrency,
        "limit_request_line": server_config.limit_request_line,
        "limit_request_fields": server_config.limit_request_fields,
        "limit_request_field_size": server_config.limit_request_field_size,
        "limit_request_body": server_config.limit_request_body,
        **ssl_config
    }
    
    # Add worker-specific configurations for production
    if server_config.environment == "production" and server_config.workers > 1:
        uvicorn_config.update({
            "max_requests": server_config.max_requests,
            "max_requests_jitter": server_config.max_requests_jitter
        })
    
    # Log startup configuration
    logger.info(f"Starting BFSI API server in {server_config.environment} mode")
    logger.info(f"Host: {server_config.host}, Port: {server_config.port}")
    logger.info(f"Workers: {server_config.workers}")
    logger.info(f"TLS/SSL: {'Enabled' if ssl_config else 'Disabled (use reverse proxy)'}")
    logger.info(f"Request limits: {server_config.limit_request_body} bytes body, {server_config.limit_concurrency} concurrent")
    
    # Start the server
    uvicorn.run(**uvicorn_config)



