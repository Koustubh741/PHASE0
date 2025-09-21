#!/usr/bin/env python3
"""
Local AI Services Client Library
Easy-to-use client for integrating with local Ollama and Hugging Face services
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from local_ai_config import ai_config, get_ollama_url, get_huggingface_url

@dataclass
class ChatResponse:
    """Chat response data class"""
    response: str
    model_used: str
    processing_time: float
    tokens_generated: int = 0

@dataclass
class EmbeddingResponse:
    """Embedding response data class"""
    embedding: List[float]
    model_used: str
    dimension: int
    processing_time: float = 0.0

class LocalAIClient:
    """Client for local AI services"""
    
    def __init__(self):
        self.ollama_config = ai_config.get_ollama_config()
        self.hf_config = ai_config.get_huggingface_config()
    
    def chat_with_ollama(self, message: str, model: str = None, **kwargs) -> ChatResponse:
        """Chat with Ollama service"""
        if not ai_config.is_service_enabled("ollama"):
            raise RuntimeError("Ollama service is not enabled")
        
        model = model or self.ollama_config["default_model"]
        
        payload = {
            "model": model,
            "prompt": message,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.ollama_config["temperature"]),
                "top_p": kwargs.get("top_p", self.ollama_config["top_p"]),
                "max_tokens": kwargs.get("max_tokens", self.ollama_config["max_tokens"])
            }
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                get_ollama_url("generate"),
                json=payload,
                timeout=self.ollama_config["timeout"]
            )
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return ChatResponse(
                    response=result.get("response", ""),
                    model_used=model,
                    processing_time=processing_time,
                    tokens_generated=len(result.get("response", "").split())
                )
            else:
                raise RuntimeError(f"Ollama API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to Ollama: {e}")
    
    def chat_with_huggingface(self, message: str, model: str = None, **kwargs) -> ChatResponse:
        """Chat with Hugging Face service"""
        if not ai_config.is_service_enabled("huggingface"):
            raise RuntimeError("Hugging Face service is not enabled")
        
        payload = {
            "message": message,
            "model_name": model or "simple",
            "max_length": kwargs.get("max_tokens", self.hf_config["max_tokens"]),
            "temperature": kwargs.get("temperature", self.hf_config["temperature"]),
            "top_p": kwargs.get("top_p", self.hf_config["top_p"])
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                get_huggingface_url("chat"),
                json=payload,
                timeout=self.hf_config["timeout"]
            )
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return ChatResponse(
                    response=result.get("response", ""),
                    model_used=result.get("model_used", "unknown"),
                    processing_time=processing_time,
                    tokens_generated=result.get("tokens_generated", 0)
                )
            else:
                raise RuntimeError(f"Hugging Face API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to Hugging Face: {e}")
    
    def get_embeddings(self, text: str, model: str = None) -> EmbeddingResponse:
        """Get embeddings from Hugging Face service"""
        if not ai_config.is_service_enabled("huggingface"):
            raise RuntimeError("Hugging Face service is not enabled")
        
        payload = {
            "text": text,
            "model_name": model or "simple"
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                get_huggingface_url("embeddings"),
                json=payload,
                timeout=self.hf_config["timeout"]
            )
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return EmbeddingResponse(
                    embedding=result.get("embedding", []),
                    model_used=result.get("model_used", "unknown"),
                    dimension=result.get("dimension", 0),
                    processing_time=processing_time
                )
            else:
                raise RuntimeError(f"Hugging Face API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to Hugging Face: {e}")
    
    def chat(self, message: str, service: str = "auto", **kwargs) -> ChatResponse:
        """Chat with available service (auto-select or specify)"""
        if service == "auto":
            # Try Ollama first, fallback to Hugging Face
            try:
                return self.chat_with_ollama(message, **kwargs)
            except Exception:
                try:
                    return self.chat_with_huggingface(message, **kwargs)
                except Exception:
                    raise RuntimeError("No AI services available")
        elif service == "ollama":
            return self.chat_with_ollama(message, **kwargs)
        elif service == "huggingface":
            return self.chat_with_huggingface(message, **kwargs)
        else:
            raise ValueError(f"Unknown service: {service}")
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all services"""
        health = {}
        
        # Check Ollama
        try:
            response = requests.get(get_ollama_url("tags"), timeout=5)
            health["ollama"] = response.status_code == 200
        except:
            health["ollama"] = False
        
        # Check Hugging Face
        try:
            response = requests.get(get_huggingface_url("health"), timeout=5)
            health["huggingface"] = response.status_code == 200
        except:
            health["huggingface"] = False
        
        return health
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get available models from all services"""
        models = {}
        
        # Get Ollama models
        try:
            response = requests.get(get_ollama_url("tags"), timeout=5)
            if response.status_code == 200:
                data = response.json()
                models["ollama"] = [m["name"] for m in data.get("models", [])]
            else:
                models["ollama"] = []
        except:
            models["ollama"] = []
        
        # Get Hugging Face models
        try:
            response = requests.get(get_huggingface_url("models"), timeout=5)
            if response.status_code == 200:
                data = response.json()
                models["huggingface"] = [m["model_name"] for m in data.get("models", [])]
            else:
                models["huggingface"] = []
        except:
            models["huggingface"] = []
        
        return models

# Global client instance
ai_client = LocalAIClient()

# Convenience functions
def chat(message: str, service: str = "auto", **kwargs) -> ChatResponse:
    """Quick chat function"""
    return ai_client.chat(message, service, **kwargs)

def get_embeddings(text: str, model: str = None) -> EmbeddingResponse:
    """Quick embedding function"""
    return ai_client.get_embeddings(text, model)

def health_check() -> Dict[str, bool]:
    """Quick health check"""
    return ai_client.health_check()

# Example usage and testing
if __name__ == "__main__":
    print("Local AI Client Test")
    print("=" * 30)
    
    # Health check
    health = health_check()
    print(f"Services health: {health}")
    
    # Available models
    models = ai_client.get_available_models()
    print(f"Available models: {models}")
    
    # Test chat
    if any(health.values()):
        try:
            response = chat("Hello, how are you?")
            print(f"Chat response: {response.response}")
            print(f"Model used: {response.model_used}")
            print(f"Processing time: {response.processing_time:.2f}s")
        except Exception as e:
            print(f"Chat test failed: {e}")
    
    # Test embeddings
    if health.get("huggingface", False):
        try:
            embeddings = get_embeddings("This is a test sentence")
            print(f"Embeddings dimension: {embeddings.dimension}")
            print(f"Embeddings preview: {embeddings.embedding[:5]}...")
        except Exception as e:
            print(f"Embeddings test failed: {e}")



