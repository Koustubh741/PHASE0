"""
Database Configuration Module
Centralized configuration management for database connections with security best practices
"""

import os
import logging
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration with environment variable support and validation"""
    
    def __init__(self):
        self._database_url: Optional[str] = None
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate database configuration and set up connection string"""
        # Try to get full DATABASE_URL first (recommended for production)
        self._database_url = os.getenv("DATABASE_URL")
        
        if self._database_url:
            self._validate_database_url()
            logger.info("Using DATABASE_URL from environment variables")
            return
        
        # Fallback to individual components for development
        self._construct_from_components()
    
    def _validate_database_url(self) -> None:
        """Validate the DATABASE_URL format"""
        try:
            parsed = urlparse(self._database_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid DATABASE_URL format")
            logger.debug("DATABASE_URL validation successful")
        except Exception as e:
            raise ValueError(f"Invalid DATABASE_URL format: {e}")
    
    def _construct_from_components(self) -> None:
        """Construct database URL from individual environment variables"""
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "grc_platform")
        db_user = os.getenv("DB_USER", "grc_user")
        db_password = os.getenv("DB_PASSWORD", "grc_password")
        
        # Validate required variables for production
        if os.getenv("ENVIRONMENT") == "production":
            required_vars = {
                "DB_HOST": db_host,
                "DB_NAME": db_name,
                "DB_USER": db_user,
                "DB_PASSWORD": db_password
            }
            missing_vars = [var for var, value in required_vars.items() 
                          if not value or value in ["grc_user", "grc_password", "localhost"]]
            
            if missing_vars:
                raise ValueError(f"Missing or default values for required environment variables: {', '.join(missing_vars)}")
        
        self._database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Log warnings for development
        logger.warning("DATABASE_URL not found in environment variables. Using individual DB_* variables.")
        logger.warning("For production deployment, set DATABASE_URL environment variable for better security.")
    
    @property
    def database_url(self) -> str:
        """Get the database URL"""
        if not self._database_url:
            raise RuntimeError("Database configuration not initialized")
        return self._database_url
    
    @property
    def is_secure_config(self) -> bool:
        """Check if configuration uses secure environment variables"""
        return bool(os.getenv("DATABASE_URL"))
    
    def get_connection_params(self) -> dict:
        """Get connection parameters for advanced configuration"""
        parsed = urlparse(self.database_url)
        return {
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.lstrip('/'),
            "username": parsed.username,
            "password": parsed.password,
            "scheme": parsed.scheme
        }

# Global configuration instance
db_config = DatabaseConfig()

def get_database_url() -> str:
    """Get database URL from configuration"""
    return db_config.database_url

def is_secure_config() -> bool:
    """Check if using secure configuration"""
    return db_config.is_secure_config
