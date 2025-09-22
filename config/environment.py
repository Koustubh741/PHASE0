"""
Environment Configuration Management
Centralized configuration for different environments
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class Environment(Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    name: str = "grc_platform"
    user: str = "grc_user"
    password: str = "grc_password"
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600
    pool_pre_ping: bool = True
    
    @property
    def url(self) -> str:
        """Get database URL"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

@dataclass
class RedisConfig:
    """Redis configuration"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    max_connections: int = 20
    
    @property
    def url(self) -> str:
        """Get Redis URL"""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"

@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str = "demo-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    password_min_length: int = 8
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 15

@dataclass
class APIConfig:
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    reload: bool = True
    workers: int = 1
    log_level: str = "INFO"
    cors_origins: list = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:3000", "http://localhost:8080"]

@dataclass
class FrontendConfig:
    """Frontend configuration"""
    api_url: str = "http://localhost:8000/api/v1"
    environment: str = "development"
    debug: bool = True

@dataclass
class BFSIAIConfig:
    """BFSI AI configuration"""
    host: str = "localhost"
    port: int = 8001
    model_path: str = "./models"
    max_workers: int = 4
    timeout: int = 300
    cache_ttl: int = 3600

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5

class EnvironmentManager:
    """Environment configuration manager"""
    
    def __init__(self, environment: Environment = None):
        self.environment = environment or self._detect_environment()
        self.config = self._load_configuration()
    
    def _detect_environment(self) -> Environment:
        """Detect current environment"""
        env = os.getenv("ENVIRONMENT", "development").lower()
        
        if env in ["dev", "development"]:
            return Environment.DEVELOPMENT
        elif env in ["test", "testing"]:
            return Environment.TESTING
        elif env in ["stage", "staging"]:
            return Environment.STAGING
        elif env in ["prod", "production"]:
            return Environment.PRODUCTION
        else:
            return Environment.DEVELOPMENT
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration for current environment"""
        config = {
            "environment": self.environment.value,
            "database": self._get_database_config(),
            "redis": self._get_redis_config(),
            "security": self._get_security_config(),
            "api": self._get_api_config(),
            "frontend": self._get_frontend_config(),
            "bfsi_ai": self._get_bfsi_ai_config(),
            "logging": self._get_logging_config(),
        }
        
        return config
    
    def _get_database_config(self) -> DatabaseConfig:
        """Get database configuration"""
        return DatabaseConfig(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            name=os.getenv("POSTGRES_DB", "grc_platform"),
            user=os.getenv("POSTGRES_USER", "grc_user"),
            password=os.getenv("POSTGRES_PASSWORD", "grc_password"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
            pool_pre_ping=os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
        )
    
    def _get_redis_config(self) -> RedisConfig:
        """Get Redis configuration"""
        return RedisConfig(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            password=os.getenv("REDIS_PASSWORD"),
            max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "20"))
        )
    
    def _get_security_config(self) -> SecurityConfig:
        """Get security configuration"""
        return SecurityConfig(
            secret_key=os.getenv("SECRET_KEY", "demo-secret-key-change-in-production"),
            algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
            password_min_length=int(os.getenv("PASSWORD_MIN_LENGTH", "8")),
            max_login_attempts=int(os.getenv("MAX_LOGIN_ATTEMPTS", "5")),
            lockout_duration_minutes=int(os.getenv("LOCKOUT_DURATION_MINUTES", "15"))
        )
    
    def _get_api_config(self) -> APIConfig:
        """Get API configuration"""
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
        
        return APIConfig(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "8000")),
            debug=os.getenv("DEBUG", "true").lower() == "true",
            reload=os.getenv("RELOAD", "true").lower() == "true",
            workers=int(os.getenv("WORKERS", "1")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            cors_origins=cors_origins
        )
    
    def _get_frontend_config(self) -> FrontendConfig:
        """Get frontend configuration"""
        return FrontendConfig(
            api_url=os.getenv("REACT_APP_API_URL", "http://localhost:8000/api/v1"),
            environment=os.getenv("REACT_APP_ENVIRONMENT", "development"),
            debug=os.getenv("REACT_APP_DEBUG", "true").lower() == "true"
        )
    
    def _get_bfsi_ai_config(self) -> BFSIAIConfig:
        """Get BFSI AI configuration"""
        return BFSIAIConfig(
            host=os.getenv("BFSI_AI_HOST", "localhost"),
            port=int(os.getenv("BFSI_AI_PORT", "8001")),
            model_path=os.getenv("BFSI_AI_MODEL_PATH", "./models"),
            max_workers=int(os.getenv("BFSI_AI_MAX_WORKERS", "4")),
            timeout=int(os.getenv("BFSI_AI_TIMEOUT", "300")),
            cache_ttl=int(os.getenv("BFSI_AI_CACHE_TTL", "3600"))
        )
    
    def _get_logging_config(self) -> LoggingConfig:
        """Get logging configuration"""
        return LoggingConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            file_path=os.getenv("LOG_FILE_PATH"),
            max_file_size=int(os.getenv("LOG_MAX_FILE_SIZE", "10485760")),
            backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5"))
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_database_url(self) -> str:
        """Get database URL"""
        return self.get("database.url")
    
    def get_redis_url(self) -> str:
        """Get Redis URL"""
        return self.get("redis.url")
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == Environment.PRODUCTION
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == Environment.DEVELOPMENT
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate configuration and return issues"""
        issues = []
        
        # Validate database configuration
        db_config = self.get("database")
        if not db_config.password or db_config.password == "demo-secret-key-change-in-production":
            if self.is_production():
                issues.append("Production database password not set")
        
        # Validate security configuration
        security_config = self.get("security")
        if not security_config.secret_key or security_config.secret_key == "demo-secret-key-change-in-production":
            if self.is_production():
                issues.append("Production secret key not set")
        
        # Validate required environment variables
        required_vars = {
            "development": ["DATABASE_URL"],
            "production": ["DATABASE_URL", "SECRET_KEY", "POSTGRES_PASSWORD"]
        }
        
        for var in required_vars.get(self.environment.value, []):
            if not os.getenv(var):
                issues.append(f"Required environment variable {var} not set")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "environment": self.environment.value
        }

# Global environment manager instance
env_manager = EnvironmentManager()

def get_environment_manager() -> EnvironmentManager:
    """Get the global environment manager"""
    return env_manager

def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value"""
    return env_manager.get(key, default)

def get_database_url() -> str:
    """Get database URL"""
    return env_manager.get_database_url()

def get_redis_url() -> str:
    """Get Redis URL"""
    return env_manager.get_redis_url()

def is_production() -> bool:
    """Check if running in production"""
    return env_manager.is_production()

def is_development() -> bool:
    """Check if running in development"""
    return env_manager.is_development()
