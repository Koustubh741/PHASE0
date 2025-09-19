"""
Configuration settings for AI agents
"""

import os
from typing import Optional

# Try to import BaseSettings from pydantic_settings, fallback to pydantic
try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        # Fallback to a simple class if pydantic is not available
        class BaseSettings:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    
    # ChromaDB Configuration
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "compliance-policies"
    
    # Database
    redis_url: str = "redis://localhost:6379"
    postgres_url: Optional[str] = None
    
    # AI Model Settings
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.1
    openai_max_tokens: int = 1000
    
    # Vector Store Settings
    chroma_collection_name: str = "compliance-policies"
    vector_dimension: int = 1536
    
    # Agent Settings
    agent_timeout: int = 30
    max_retries: int = 3
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
