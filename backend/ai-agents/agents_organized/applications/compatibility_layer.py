#!/usr/bin/env python3
"""
Compatibility Layer for Enhanced Multi-LLM Service
Ensures backward compatibility with existing API calls
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class CompatibilityAdapter:
    """Adapter to make enhanced service compatible with original API calls"""
    
    def __init__(self, enhanced_service_url: str = "http://localhost:8007"):
        self.enhanced_service_url = enhanced_service_url
        self.model_mapping = {
            # Map original model names to enhanced service model IDs
            "microsoft/DialoGPT-medium": "tiny-llama",
            "sentence-transformers/all-MiniLM-L6-v2": "all-minilm",
            "ProsusAI/finbert": "phi-2",
            "gpt2": "tiny-llama",
            "gpt2-medium": "phi-2",
            "gpt2-large": "gemma-2b",
            "gpt2-xl": "llama2-7b"
        }
    
    def map_model_name(self, original_name: str) -> str:
        """Map original model name to enhanced service model ID"""
        return self.model_mapping.get(original_name, "tiny-llama")
    
    def adapt_chat_request(self, original_request: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt original chat request to enhanced service format"""
        enhanced_request = {
            "message": original_request.get("message", ""),
            "max_length": original_request.get("max_length", 100),
            "temperature": original_request.get("temperature", 0.7),
            "top_p": original_request.get("top_p", 0.9),
            "conversation_history": original_request.get("conversation_history", []),
            "auto_model_selection": True
        }
        
        # Map model name if provided
        if "model_name" in original_request:
            enhanced_request["model_id"] = self.map_model_name(original_request["model_name"])
        
        return enhanced_request
    
    def adapt_embedding_request(self, original_request: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt original embedding request to enhanced service format"""
        enhanced_request = {
            "text": original_request.get("text", ""),
            "auto_model_selection": True
        }
        
        # Map model name if provided
        if "model_name" in original_request:
            enhanced_request["model_id"] = self.map_model_name(original_request["model_name"])
        
        return enhanced_request
    
    def adapt_response(self, enhanced_response: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt enhanced service response to original format"""
        # Extract model_used and map back to original name if possible
        model_used = enhanced_response.get("model_used", "")
        
        # Find original name if it exists in mapping
        original_model_name = None
        for orig_name, enhanced_id in self.model_mapping.items():
            if enhanced_id == model_used:
                original_model_name = orig_name
                break
        
        # Create response in original format
        original_response = {
            "response": enhanced_response.get("response", ""),
            "model_used": original_model_name or model_used,
            "tokens_generated": enhanced_response.get("tokens_generated", 0),
            "processing_time": enhanced_response.get("processing_time", 0.0)
        }
        
        # Add optional fields if present
        if "conversation_id" in enhanced_response:
            original_response["conversation_id"] = enhanced_response["conversation_id"]
        
        return original_response

class BackwardCompatibleService:
    """Service wrapper that provides backward compatibility"""
    
    def __init__(self):
        self.adapter = CompatibilityAdapter()
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check compatible with original service"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.adapter.enhanced_service_url}/health") as response:
                    if response.status == 200:
                        health_data = await response.json()
                        return {
                            "status": "healthy",
                            "service": "huggingface-transformers",
                            "loaded_models": health_data.get("loaded_models", []),
                            "timestamp": health_data.get("timestamp", "")
                        }
                    else:
                        raise HTTPException(status_code=response.status, detail="Service unavailable")
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(status_code=503, detail="Service unavailable")
    
    async def list_models(self) -> Dict[str, Any]:
        """List models compatible with original service"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.adapter.enhanced_service_url}/models") as response:
                    if response.status == 200:
                        models_data = await response.json()
                        
                        # Convert enhanced format to original format
                        original_models = []
                        for model_id, model_info in models_data.get("models", {}).items():
                            original_models.append({
                                "model_name": model_id,
                                "model_type": model_info.get("model_info", {}).get("model_type", "chat"),
                                "loaded": model_info.get("status") == "loaded",
                                "memory_usage": "Unknown"
                            })
                        
                        return {"models": original_models}
                    else:
                        raise HTTPException(status_code=response.status, detail="Failed to list models")
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise HTTPException(status_code=500, detail="Failed to list models")
    
    async def chat(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Chat endpoint compatible with original service"""
        try:
            import aiohttp
            
            # Adapt request to enhanced service format
            enhanced_request = self.adapter.adapt_chat_request(request_data)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.adapter.enhanced_service_url}/chat",
                    json=enhanced_request
                ) as response:
                    if response.status == 200:
                        enhanced_response = await response.json()
                        return self.adapter.adapt_response(enhanced_response)
                    else:
                        error_text = await response.text()
                        raise HTTPException(status_code=response.status, detail=error_text)
        except Exception as e:
            logger.error(f"Chat request failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def generate_embeddings(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Embeddings endpoint compatible with original service"""
        try:
            import aiohttp
            
            # Adapt request to enhanced service format
            enhanced_request = self.adapter.adapt_embedding_request(request_data)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.adapter.enhanced_service_url}/embeddings",
                    json=enhanced_request
                ) as response:
                    if response.status == 200:
                        enhanced_response = await response.json()
                        
                        # Adapt response to original format
                        return {
                            "embedding": enhanced_response.get("embedding", []),
                            "model_used": enhanced_response.get("model_used", ""),
                            "dimension": enhanced_response.get("dimension", 0)
                        }
                    else:
                        error_text = await response.text()
                        raise HTTPException(status_code=response.status, detail=error_text)
        except Exception as e:
            logger.error(f"Embeddings request failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# Global compatibility service instance
compatibility_service = BackwardCompatibleService()

# Pydantic models for backward compatibility
class CompatibleChatRequest(BaseModel):
    message: str
    model_name: Optional[str] = None
    max_length: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    conversation_history: Optional[List[Dict[str, str]]] = []

class CompatibleEmbeddingRequest(BaseModel):
    text: str
    model_name: Optional[str] = None

class CompatibleChatResponse(BaseModel):
    response: str
    model_used: str
    tokens_generated: int
    processing_time: float
    conversation_id: Optional[str] = None

class CompatibleEmbeddingResponse(BaseModel):
    embedding: List[float]
    model_used: str
    dimension: int

class CompatibleModelInfo(BaseModel):
    model_name: str
    model_type: str
    loaded: bool
    memory_usage: Optional[str] = None

# Utility functions for easy integration
async def get_compatible_response(message: str, model_name: str = None) -> str:
    """Quick function to get a response using compatibility layer"""
    request_data = {"message": message}
    if model_name:
        request_data["model_name"] = model_name
    
    response = await compatibility_service.chat(request_data)
    return response["response"]

async def get_compatible_embeddings(text: str, model_name: str = None) -> List[float]:
    """Quick function to get embeddings using compatibility layer"""
    request_data = {"text": text}
    if model_name:
        request_data["model_name"] = model_name
    
    response = await compatibility_service.generate_embeddings(request_data)
    return response["embedding"]

# Example usage
if __name__ == "__main__":
    async def test_compatibility():
        """Test the compatibility layer"""
        try:
            # Test health check
            health = await compatibility_service.health_check()
            print(f"Health: {health}")
            
            # Test chat with original model name
            chat_response = await compatibility_service.chat({
                "message": "Hello, how are you?",
                "model_name": "microsoft/DialoGPT-medium"
            })
            print(f"Chat response: {chat_response}")
            
            # Test embeddings with original model name
            embeddings_response = await compatibility_service.generate_embeddings({
                "text": "This is a test sentence",
                "model_name": "sentence-transformers/all-MiniLM-L6-v2"
            })
            print(f"Embeddings dimension: {embeddings_response['dimension']}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Run test
    asyncio.run(test_compatibility())
