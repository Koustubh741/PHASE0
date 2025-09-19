#!/usr/bin/env python3
"""
Hugging Face Transformers Client for GRC Platform
Provides interface to interact with the Hugging Face transformers service
"""

import os
import logging
import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class HuggingFaceClient:
    """Client for interacting with Hugging Face transformers service"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("HUGGINGFACE_SERVICE_URL", "http://localhost:8007")
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=300)  # 5 minutes for model loading
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check if the Hugging Face service is healthy"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Health check failed with status {response.status}")
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List all loaded models"""
        try:
            async with self.session.get(f"{self.base_url}/models") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("models", [])
                else:
                    raise Exception(f"Failed to list models: {response.status}")
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise
    
    async def chat(
        self,
        message: str,
        model_name: str = None,
        max_length: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Generate chat response"""
        try:
            payload = {
                "message": message,
                "max_length": max_length,
                "temperature": temperature,
                "top_p": top_p,
                "conversation_history": conversation_history or []
            }
            
            if model_name:
                payload["model_name"] = model_name
            
            async with self.session.post(
                f"{self.base_url}/chat",
                json=payload
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Chat request failed: {response.status} - {error_text}")
        except Exception as e:
            logger.error(f"Chat request failed: {e}")
            raise
    
    async def generate_embeddings(
        self,
        text: str,
        model_name: str = None
    ) -> Dict[str, Any]:
        """Generate embeddings for text"""
        try:
            payload = {"text": text}
            if model_name:
                payload["model_name"] = model_name
            
            async with self.session.post(
                f"{self.base_url}/embeddings",
                json=payload
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Embeddings request failed: {response.status} - {error_text}")
        except Exception as e:
            logger.error(f"Embeddings request failed: {e}")
            raise
    
    async def load_model(self, model_name: str) -> Dict[str, Any]:
        """Load a specific model"""
        try:
            async with self.session.post(f"{self.base_url}/models/{model_name}/load") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Model loading failed: {response.status} - {error_text}")
        except Exception as e:
            logger.error(f"Model loading failed: {e}")
            raise
    
    async def unload_model(self, model_name: str) -> Dict[str, Any]:
        """Unload a specific model"""
        try:
            async with self.session.delete(f"{self.base_url}/models/{model_name}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Model unloading failed: {response.status} - {error_text}")
        except Exception as e:
            logger.error(f"Model unloading failed: {e}")
            raise

class HuggingFaceAgent:
    """Enhanced agent that uses Hugging Face transformers for local LLM capabilities"""
    
    def __init__(self, client: HuggingFaceClient = None):
        self.client = client or HuggingFaceClient()
        self.conversation_history = []
        self.model_name = os.getenv("DEFAULT_MODEL_NAME", "microsoft/DialoGPT-medium")
        
    async def initialize(self):
        """Initialize the agent and check service health"""
        try:
            async with self.client as client:
                health = await client.health_check()
                logger.info(f"Hugging Face service is healthy: {health}")
                return True
        except Exception as e:
            logger.error(f"Failed to initialize Hugging Face agent: {e}")
            return False
    
    async def process_message(
        self,
        message: str,
        context: Dict[str, Any] = None,
        use_conversation_history: bool = True
    ) -> Dict[str, Any]:
        """Process a message using Hugging Face transformers"""
        try:
            # Prepare conversation history
            conversation_history = self.conversation_history if use_conversation_history else []
            
            # Add context to the message if provided
            if context:
                context_str = f"Context: {json.dumps(context, indent=2)}\n\nMessage: {message}"
            else:
                context_str = message
            
            async with self.client as client:
                # Generate response
                response = await client.chat(
                    message=context_str,
                    model_name=self.model_name,
                    max_length=150,
                    temperature=0.7,
                    conversation_history=conversation_history
                )
                
                # Update conversation history
                if use_conversation_history:
                    self.conversation_history.append({"role": "user", "content": message})
                    self.conversation_history.append({"role": "assistant", "content": response["response"]})
                    
                    # Keep only last 10 exchanges
                    if len(self.conversation_history) > 20:
                        self.conversation_history = self.conversation_history[-20:]
                
                return {
                    "response": response["response"],
                    "model_used": response["model_used"],
                    "processing_time": response["processing_time"],
                    "tokens_generated": response["tokens_generated"],
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return {
                "response": f"Error processing message: {str(e)}",
                "error": True,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        try:
            async with self.client as client:
                response = await client.generate_embeddings(text)
                return response["embedding"]
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    async def analyze_document(self, document_text: str) -> Dict[str, Any]:
        """Analyze a document using Hugging Face models"""
        try:
            # Generate embeddings for the document
            embeddings = await self.generate_embeddings(document_text)
            
            # Analyze the document content
            analysis_prompt = f"""
            Analyze the following document and provide insights on:
            1. Key topics and themes
            2. Compliance requirements mentioned
            3. Risk factors identified
            4. Recommendations
            
            Document: {document_text[:1000]}...
            """
            
            analysis = await self.process_message(analysis_prompt)
            
            return {
                "embeddings": embeddings,
                "analysis": analysis["response"],
                "model_used": analysis["model_used"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze document: {e}")
            raise
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def set_model(self, model_name: str):
        """Set the model to use for generation"""
        self.model_name = model_name

# Utility functions for easy integration
async def get_huggingface_response(message: str, model_name: str = None) -> str:
    """Quick function to get a response from Hugging Face service"""
    async with HuggingFaceClient() as client:
        response = await client.chat(message, model_name=model_name)
        return response["response"]

async def get_embeddings(text: str, model_name: str = None) -> List[float]:
    """Quick function to get embeddings from Hugging Face service"""
    async with HuggingFaceClient() as client:
        response = await client.generate_embeddings(text, model_name=model_name)
        return response["embedding"]

# Example usage
if __name__ == "__main__":
    async def test_huggingface_client():
        """Test the Hugging Face client"""
        async with HuggingFaceClient() as client:
            # Test health check
            health = await client.health_check()
            print(f"Health: {health}")
            
            # Test chat
            response = await client.chat("Hello, how are you?")
            print(f"Chat response: {response}")
            
            # Test embeddings
            embeddings = await client.generate_embeddings("This is a test sentence")
            print(f"Embeddings dimension: {len(embeddings['embedding'])}")
    
    # Run test
    asyncio.run(test_huggingface_client())


