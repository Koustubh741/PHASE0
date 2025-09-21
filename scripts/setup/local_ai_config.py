#!/usr/bin/env python3
"""
Local AI Services Configuration for GRC Platform
Configuration file to integrate local Ollama and Hugging Face services
"""

import os
from typing import Dict, Any
from copy import deepcopy

# Local AI Services Configuration
LOCAL_AI_CONFIG = {
    "ollama": {
        "enabled": True,
        "base_url": "http://localhost:11434",
        "default_model": "llama2",
        "api_endpoints": {
            "generate": "/api/generate",
            "tags": "/api/tags",
            "pull": "/api/pull",
            "delete": "/api/delete"
        },
        "timeout": 60,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    },
    "huggingface": {
        "enabled": True,
        "base_url": "http://localhost:8007",
        "api_endpoints": {
            "chat": "/chat",
            "embeddings": "/embeddings",
            "health": "/health",
            "models": "/models"
        },
        "timeout": 30,
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9
    }
}

# Environment-specific configurations
class LocalAIConfig:
    """Configuration class for local AI services"""
    
    def __init__(self):
        self.config = deepcopy(LOCAL_AI_CONFIG)
        
        # Override with environment variables if present
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Ollama configuration
        if os.getenv("OLLAMA_BASE_URL"):
            self.config["ollama"]["base_url"] = os.getenv("OLLAMA_BASE_URL")
        
        if os.getenv("OLLAMA_DEFAULT_MODEL"):
            self.config["ollama"]["default_model"] = os.getenv("OLLAMA_DEFAULT_MODEL")
        
        # Hugging Face configuration
        if os.getenv("HUGGINGFACE_BASE_URL"):
            self.config["huggingface"]["base_url"] = os.getenv("HUGGINGFACE_BASE_URL")
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """Get Ollama configuration"""
        return self.config["ollama"]
    
    def get_huggingface_config(self) -> Dict[str, Any]:
        """Get Hugging Face configuration"""
        return self.config["huggingface"]
    
    def get_service_url(self, service: str, endpoint: str = None) -> str:
        """Get full URL for a service endpoint"""
        if service not in self.config:
            raise ValueError(f"Unknown service: {service}")
        
        base_url = self.config[service]["base_url"]
        if endpoint:
            if endpoint in self.config[service]["api_endpoints"]:
                return f"{base_url}{self.config[service]['api_endpoints'][endpoint]}"
            else:
                raise ValueError(f"Unknown endpoint for {service}: {endpoint}")
        
        return base_url
    
    def is_service_enabled(self, service: str) -> bool:
        """Check if a service is enabled"""
        return self.config.get(service, {}).get("enabled", False)

# Global configuration instance
ai_config = LocalAIConfig()

# Convenience functions
def get_ollama_url(endpoint: str = None) -> str:
    """Get Ollama service URL"""
    return ai_config.get_service_url("ollama", endpoint)

def get_huggingface_url(endpoint: str = None) -> str:
    """Get Hugging Face service URL"""
    return ai_config.get_service_url("huggingface", endpoint)

def is_ollama_enabled() -> bool:
    """Check if Ollama is enabled"""
    return ai_config.is_service_enabled("ollama")

def is_huggingface_enabled() -> bool:
    """Check if Hugging Face is enabled"""
    return ai_config.is_service_enabled("huggingface")

# Service integration helpers
def get_chat_service_config() -> Dict[str, Any]:
    """Get configuration for chat services"""
    return {
        "ollama": ai_config.get_ollama_config() if is_ollama_enabled() else None,
        "huggingface": ai_config.get_huggingface_config() if is_huggingface_enabled() else None
    }

def get_embedding_service_config() -> Dict[str, Any]:
    """Get configuration for embedding services"""
    return {
        "huggingface": ai_config.get_huggingface_config() if is_huggingface_enabled() else None
    }

# Example usage and testing
if __name__ == "__main__":
    print("Local AI Services Configuration")
    print("=" * 40)
    
    config = LocalAIConfig()
    
    print(f"Ollama enabled: {is_ollama_enabled()}")
    print(f"Ollama URL: {get_ollama_url()}")
    print(f"Ollama generate URL: {get_ollama_url('generate')}")
    
    print(f"\nHugging Face enabled: {is_huggingface_enabled()}")
    print(f"Hugging Face URL: {get_huggingface_url()}")
    print(f"Hugging Face chat URL: {get_huggingface_url('chat')}")
    
    print(f"\nChat services: {get_chat_service_config()}")
    print(f"Embedding services: {get_embedding_service_config()}")



