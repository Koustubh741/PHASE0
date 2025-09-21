#!/usr/bin/env python3
"""
Simple Hugging Face Transformers Service for GRC Platform
Lightweight version that doesn't require large model downloads
"""

import os
import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Simple Hugging Face Transformers Service",
    description="Lightweight LLM service for GRC Platform",
    version="1.0.0"
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    model_name: Optional[str] = "simple"
    max_length: Optional[int] = 100
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    model_used: str
    tokens_generated: int
    processing_time: float

class EmbeddingRequest(BaseModel):
    text: str
    model_name: Optional[str] = "simple"

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    model_used: str
    dimension: int

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "simple-huggingface-transformers",
        "models": ["simple"],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/models")
async def list_models():
    """List available models"""
    return {
        "models": [
            {
                "model_name": "simple",
                "model_type": "chat",
                "loaded": True,
                "description": "Simple rule-based response generator"
            }
        ]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate chat response using simple logic"""
    try:
        start_time = datetime.utcnow()
        
        # Simple response generation based on keywords
        message_lower = request.message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            response = "Hello! I'm a simple AI assistant. How can I help you today?"
        elif any(word in message_lower for word in ["how", "what", "who", "when", "where", "why"]):
            response = "That's an interesting question. I'm a simple AI that can help with basic conversations."
        elif any(word in message_lower for word in ["help", "assist", "support"]):
            response = "I'm here to help! I can answer basic questions and have simple conversations."
        elif any(word in message_lower for word in ["thank", "thanks"]):
            response = "You're welcome! I'm happy to help."
        else:
            response = f"I understand you said: '{request.message}'. I'm a simple AI assistant ready to help with your questions."
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Estimate tokens
        tokens_generated = len(response.split())
        
        return ChatResponse(
            response=response,
            model_used="simple",
            tokens_generated=tokens_generated,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in chat generation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/embeddings", response_model=EmbeddingResponse)
async def generate_embeddings(request: EmbeddingRequest):
    """Generate simple embeddings based on text length and keywords"""
    try:
        # Simple embedding generation based on text characteristics
        text = request.text.lower()
        
        # Create a simple embedding based on text features
        embedding = []
        
        # Add features based on text length
        embedding.append(len(text) / 100.0)  # Normalized length
        
        # Add features based on word count
        word_count = len(text.split())
        embedding.append(word_count / 50.0)  # Normalized word count
        
        # Add features based on character types
        embedding.append(len([c for c in text if c.isalpha()]) / len(text) if text else 0)
        embedding.append(len([c for c in text if c.isdigit()]) / len(text) if text else 0)
        
        # Add keyword-based features
        keywords = ["hello", "help", "question", "thank", "good", "bad", "yes", "no"]
        for keyword in keywords:
            embedding.append(1.0 if keyword in text else 0.0)
        
        # Pad to make it a consistent size
        while len(embedding) < 20:
            embedding.append(0.0)
        
        # Truncate if too long
        embedding = embedding[:20]
        
        return EmbeddingResponse(
            embedding=embedding,
            model_used="simple",
            dimension=len(embedding)
        )
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Simple Hugging Face Transformers Service",
        "version": "1.0.0",
        "description": "Lightweight LLM service for GRC Platform",
        "endpoints": {
            "health": "/health",
            "models": "/models",
            "chat": "/chat",
            "embeddings": "/embeddings"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8007))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )



