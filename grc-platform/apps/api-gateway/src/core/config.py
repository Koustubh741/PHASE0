"""
Configuration management for API Gateway

This module handles all configuration settings for the API Gateway service.
It uses Pydantic Settings for type-safe configuration management.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import sys
import logging

class Settings(BaseSettings):
    """Application settings"""
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://grc_user:grc_password@localhost:5432/grc_platform"
    REDIS_URL: str = "redis://localhost:6379"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_production_config()
    
    def _validate_production_config(self):
        """Validate configuration for production environment"""
        # Check if we're in production environment
        env = os.getenv("ENV") or os.getenv("FASTAPI_ENV") or self.ENVIRONMENT
        is_production = env.lower() == "production"
        
        # Define unsafe default values
        unsafe_database_url = "postgresql://grc_user:grc_password@localhost:5432/grc_platform"
        unsafe_redis_url = "redis://localhost:6379"
        unsafe_jwt_secret = "your-secret-key-here"
        
        # Check for unsafe defaults
        database_unsafe = self.DATABASE_URL == unsafe_database_url
        redis_unsafe = self.REDIS_URL == unsafe_redis_url
        jwt_unsafe = not self.JWT_SECRET_KEY or self.JWT_SECRET_KEY == unsafe_jwt_secret or len(self.JWT_SECRET_KEY) < 32
        
        if database_unsafe or redis_unsafe or jwt_unsafe:
            error_message = self._get_validation_error_message(database_unsafe, redis_unsafe, jwt_unsafe)
            
            if is_production:
                # In production, fail hard with clear error message
                logging.error(f"PRODUCTION CONFIGURATION ERROR: {error_message}")
                print(f"ERROR: {error_message}", file=sys.stderr)
                sys.exit(1)
            else:
                # In non-production, log warning but continue
                logging.warning(f"CONFIGURATION WARNING: {error_message}")
    
    def _get_validation_error_message(self, database_unsafe: bool, redis_unsafe: bool, jwt_unsafe: bool) -> str:
        """Generate actionable error message for configuration issues"""
        issues = []
        
        if database_unsafe:
            issues.append("DATABASE_URL is using the default/test value")
        
        if redis_unsafe:
            issues.append("REDIS_URL is using the default/test value")
        
        if jwt_unsafe:
            if not self.JWT_SECRET_KEY:
                issues.append("JWT_SECRET_KEY is missing")
            elif self.JWT_SECRET_KEY == "your-secret-key-here":
                issues.append("JWT_SECRET_KEY is using the insecure placeholder")
            elif len(self.JWT_SECRET_KEY) < 32:
                issues.append("JWT_SECRET_KEY is too short (minimum 32 characters)")
            else:
                issues.append("JWT_SECRET_KEY is invalid")
        
        message = f"Unsafe configuration detected: {', '.join(issues)}. "
        message += "Please set proper environment variables: "
        
        if database_unsafe:
            message += "DATABASE_URL=<your-production-database-url> "
        
        if redis_unsafe:
            message += "REDIS_URL=<your-production-redis-url> "
        
        if jwt_unsafe:
            message += "JWT_SECRET_KEY=<your-secure-jwt-secret-at-least-32-chars>"
        
        message += " or update your .env file with production values."
        
        return message
    
    # Security
    JWT_SECRET_KEY: str  # No default - must be provided via environment
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Service URLs
    POLICY_SERVICE_URL: str = "http://localhost:8001"
    RISK_SERVICE_URL: str = "http://localhost:8002"
    COMPLIANCE_SERVICE_URL: str = "http://localhost:8003"
    WORKFLOW_SERVICE_URL: str = "http://localhost:8004"
    AI_AGENTS_URL: str = "http://localhost:8005"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
