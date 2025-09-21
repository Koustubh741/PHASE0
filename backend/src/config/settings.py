"""
Application settings and configuration.
"""

import os
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    host: str = Field(default="localhost", env="POSTGRES_HOST")
    port: int = Field(default=5432, env="POSTGRES_PORT")
    database: str = Field(default="grc_platform", env="POSTGRES_DB")
    user: str = Field(default="grc_user", env="POSTGRES_USER")
    password: str = Field(default="grc_password", env="POSTGRES_PASSWORD")
    
    @property
    def url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    db: int = Field(default=0, env="REDIS_DB")
    password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    @property
    def url(self) -> str:
        """Get Redis URL."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"

class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    token_expiry: int = Field(default=3600, env="TOKEN_EXPIRY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

class VectorStoreSettings(BaseSettings):
    """Vector store configuration settings."""
    persist_directory: str = Field(default="./vector_store", env="VECTOR_STORE_DIR")
    collection_name: str = Field(default="compliance-policies", env="VECTOR_COLLECTION")

class ServiceSettings(BaseSettings):
    """Service configuration settings."""
    compliance_port: int = Field(default=8003, env="COMPLIANCE_PORT")
    compliance_host: str = Field(default="0.0.0.0", env="COMPLIANCE_HOST")
    risk_port: int = Field(default=8002, env="RISK_PORT")
    risk_host: str = Field(default="0.0.0.0", env="RISK_HOST")
    policy_port: int = Field(default=8001, env="POLICY_PORT")
    policy_host: str = Field(default="0.0.0.0", env="POLICY_HOST")

class Settings(BaseSettings):
    """Main application settings."""
    app_name: str = Field(default="GRC Platform", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    version: str = Field(default="1.0.0", env="VERSION")
    
    # Security and CORS settings
    allowed_hosts: list = Field(default=["*"], env="ALLOWED_HOSTS")
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")
    
    # Sub-settings
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()
    vector_store: VectorStoreSettings = VectorStoreSettings()
    services: ServiceSettings = ServiceSettings()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()