#!/usr/bin/env python3
"""
Security Configuration for BFSI API
Comprehensive security settings for BFSI compliance
"""

import os
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from cryptography.fernet import Fernet
import secrets
import hashlib
from passlib.hash import argon2

class SecurityConfig(BaseSettings):
    """Security configuration for BFSI compliance"""
    
    # JWT Configuration
    jwt_secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # Encryption Configuration
    encryption_key: str = Field(default_factory=lambda: Fernet.generate_key().decode())
    data_encryption_enabled: bool = True
    
    # Rate Limiting - Enhanced for BFSI security
    rate_limit_requests_per_minute: int = 60  # Reduced for security
    rate_limit_burst: int = 10  # Reduced burst capacity
    rate_limit_per_ip: bool = True
    rate_limit_per_user: bool = True
    rate_limit_per_api_key: bool = True
    
    # Login-specific rate limiting
    login_max_attempts: int = 5  # Maximum login attempts per window
    login_window_minutes: int = 15  # Time window for login attempts
    login_lockout_minutes: int = 30  # Account lockout duration
    login_exponential_backoff_base: int = 2  # Base for exponential backoff
    login_max_backoff_minutes: int = 60  # Maximum backoff time
    login_rate_limit_enabled: bool = True  # Enable login rate limiting
    
    # Database Security
    db_connection_pool_size: int = 10
    db_connection_timeout: int = 30
    db_encryption_enabled: bool = True
    
    # Audit Logging
    audit_log_enabled: bool = True
    audit_log_retention_days: int = 2555  # 7 years for BFSI compliance
    audit_log_encryption: bool = True
    
    # Data Retention
    data_retention_days: int = 2555  # 7 years
    auto_cleanup_enabled: bool = True
    
    # PCI-DSS Compliance
    pci_dss_enabled: bool = True
    card_data_encryption: bool = True
    transaction_signing: bool = True
    
    # GDPR Compliance
    gdpr_enabled: bool = True
    data_anonymization: bool = True
    consent_tracking: bool = True
    
    # Security Headers
    security_headers_enabled: bool = True
    
    # Environment detection
    environment: str = Field(default="development")
    
    # CORS origins from environment (comma-separated string)
    cors_origins_env: str = Field(default="", alias="BFSI_SECURITY_CORS_ORIGINS")
    
    # CORS Configuration - Environment-specific (computed property)
    @property
    def cors_origins(self) -> list:
        """Get CORS origins based on environment"""
        return self._get_cors_origins()
    
    def _get_cors_origins(self) -> list:
        """Get CORS origins based on environment"""
        env = self.environment.lower()
        
        if env == "production":
            # Production: Only allow explicitly configured domains
            if self.cors_origins_env:
                origins = [origin.strip() for origin in self.cors_origins_env.split(",") if origin.strip()]
                # Validate production origins (no localhost, must be HTTPS)
                validated_origins = []
                for origin in origins:
                    if SecurityConfig._validate_production_origin(origin):
                        validated_origins.append(origin)
                return validated_origins
            else:
                # No CORS origins configured for production - return empty list
                return []
        
        elif env == "staging":
            # Staging: Allow configured domains + limited localhost for testing
            origins = []
            if self.cors_origins_env:
                origins.extend([origin.strip() for origin in self.cors_origins_env.split(",") if origin.strip()])
            # Add staging-specific localhost for testing
            origins.extend([
                "https://localhost:3000",
                "https://localhost:8080"
            ])
            return origins
        
        else:
            # Development: Allow localhost and development URLs
            origins = []
            if self.cors_origins_env:
                origins.extend([origin.strip() for origin in self.cors_origins_env.split(",") if origin.strip()])
            # Add development defaults
            origins.extend([
                "https://localhost:3000",
                "https://localhost:8080",
                "https://127.0.0.1:3000",
                "https://127.0.0.1:8080",
                "http://localhost:3000",  # Allow HTTP in development
                "http://localhost:8080"
            ])
            return list(set(origins))  # Remove duplicates
    
    @staticmethod
    def _validate_production_origin(origin: str) -> bool:
        """Validate CORS origin for production environment"""
        if not origin:
            return False
        
        # Must be HTTPS in production
        if not origin.startswith("https://"):
            return False
        
        # Cannot contain localhost or local IPs in production
        forbidden_patterns = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "::1",
            "192.168.",
            "10.",
            "172.16.",
            "172.17.",
            "172.18.",
            "172.19.",
            "172.20.",
            "172.21.",
            "172.22.",
            "172.23.",
            "172.24.",
            "172.25.",
            "172.26.",
            "172.27.",
            "172.28.",
            "172.29.",
            "172.30.",
            "172.31."
        ]
        
        for pattern in forbidden_patterns:
            if pattern in origin:
                return False
        
        # Must be a valid domain format
        try:
            from urllib.parse import urlparse
            parsed = urlparse(origin)
            return bool(parsed.netloc and "." in parsed.netloc)
        except:
            return False
    
    # API Key Configuration
    api_key_enabled: bool = True
    api_key_header: str = "X-API-Key"
    
    # API Keys from environment variables
    # Format: BFSI_SECURITY_API_KEY_<CLIENT_NAME>=<API_KEY>
    # Example: BFSI_SECURITY_API_KEY_ADMIN_CLIENT=bfsi-admin-key-2024
    #          BFSI_SECURITY_API_KEY_COMPLIANCE_CLIENT=bfsi-compliance-key-2024
    #          BFSI_SECURITY_API_KEY_ANALYTICS_CLIENT=bfsi-analytics-key-2024
    
    @property
    def api_keys(self) -> Dict[str, str]:
        """Load API keys dynamically from environment variables"""
        return self._load_api_keys()
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables with validation"""
        api_keys = {}
        
        # Define expected client names and their environment variable names
        client_mappings = {
            "admin-client": "BFSI_SECURITY_API_KEY_ADMIN_CLIENT",
            "compliance-client": "BFSI_SECURITY_API_KEY_COMPLIANCE_CLIENT", 
            "analytics-client": "BFSI_SECURITY_API_KEY_ANALYTICS_CLIENT"
        }
        
        missing_keys = []
        
        for client_name, env_var in client_mappings.items():
            api_key = os.getenv(env_var)
            if api_key:
                # Validate API key format (basic validation)
                if self._validate_api_key(api_key):
                    api_keys[api_key] = client_name
                else:
                    raise ValueError(f"Invalid API key format for {client_name}: {env_var}")
            else:
                missing_keys.append(env_var)
        
        # In production, require all API keys to be set
        if self.environment.lower() == "production" and missing_keys:
            raise ValueError(
                f"Missing required API key environment variables in production: {', '.join(missing_keys)}. "
                f"Please set these environment variables with valid API keys."
            )
        
        # In development/staging, warn about missing keys but don't fail
        if missing_keys and self.environment.lower() != "production":
            import warnings
            warnings.warn(
                f"Missing API key environment variables: {', '.join(missing_keys)}. "
                f"Some API endpoints may not be accessible.",
                UserWarning
            )
        
        return api_keys
    
    def _validate_api_key(self, api_key: str) -> bool:
        """Validate API key format"""
        if not api_key or len(api_key) < 8:
            return False
        
        # Basic format validation - should contain alphanumeric characters and hyphens
        import re
        if not re.match(r'^[a-zA-Z0-9\-_]+$', api_key):
            return False
            
        return True
    
    # Session Security
    session_timeout_minutes: int = 30
    session_encryption: bool = True
    
    class Config:
        env_file = ".env"
        env_prefix = "BFSI_SECURITY_"

# Global security configuration
security_config = SecurityConfig()

# Encryption utilities
class EncryptionManager:
    """Manages encryption/decryption for sensitive data"""
    
    def __init__(self, key: str = None):
        self.key = key or security_config.encryption_key
        self.cipher = Fernet(self.key.encode() if isinstance(self.key, str) else self.key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        if not security_config.data_encryption_enabled:
            return data
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not security_config.data_encryption_enabled:
            return encrypted_data
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def hash_sensitive_data(self, data: str) -> str:
        """Create irreversible hash for sensitive data using salted argon2"""
        return argon2.hash(data)

# Global encryption manager
encryption_manager = EncryptionManager()

# Role definitions for RBAC
class Roles:
    """Role-based access control definitions"""
    
    ADMIN = "admin"
    COMPLIANCE_OFFICER = "compliance_officer"
    RISK_MANAGER = "risk_manager"
    DATA_ANALYST = "data_analyst"
    AUDITOR = "auditor"
    READONLY = "readonly"
    
    # Role permissions
    PERMISSIONS = {
        ADMIN: ["*"],  # All permissions
        COMPLIANCE_OFFICER: [
            "read:all", "write:compliance", "read:audit_logs"
        ],
        RISK_MANAGER: [
            "read:all", "write:risk_assessments", "read:transactions"
        ],
        DATA_ANALYST: [
            "read:all", "write:analytics", "read:metrics"
        ],
        AUDITOR: [
            "read:all", "read:audit_logs", "read:compliance"
        ],
        READONLY: [
            "read:all"
        ]
    }
    
    @classmethod
    def has_permission(cls, role: str, permission: str) -> bool:
        """Check if role has specific permission"""
        if role not in cls.PERMISSIONS:
            return False
        
        role_perms = cls.PERMISSIONS[role]
        return "*" in role_perms or permission in role_perms

# Security constants
class SecurityConstants:
    """Security-related constants"""
    
    # PCI-DSS Requirements
    PCI_DSS_VERSION = "4.0.1"
    PCI_DSS_REQUIREMENTS = [
        "Build and maintain secure networks",
        "Protect cardholder data",
        "Maintain vulnerability management program",
        "Implement strong access control measures",
        "Regularly monitor and test networks",
        "Maintain information security policy"
    ]
    
    # GDPR Requirements
    GDPR_ARTICLES = [
        "Article 5: Principles relating to processing",
        "Article 6: Lawfulness of processing",
        "Article 7: Conditions for consent",
        "Article 25: Data protection by design",
        "Article 32: Security of processing"
    ]
    
    # Data Classification Levels
    DATA_CLASSIFICATION = {
        "PUBLIC": 0,
        "INTERNAL": 1,
        "CONFIDENTIAL": 2,
        "RESTRICTED": 3,
        "TOP_SECRET": 4
    }
    
    # Encryption Standards
    ENCRYPTION_STANDARDS = {
        "AES_256": "AES-256-GCM",
        "RSA_4096": "RSA-4096",
        "ECDSA_P256": "ECDSA-P256"
    }
