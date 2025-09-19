#!/usr/bin/env python3
"""
Hugging Face Transformers Service for GRC Platform
Provides local LLM capabilities using Hugging Face transformers
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
from transformers import (
    AutoTokenizer, 
    AutoModel, 
    AutoModelForCausalLM,
    pipeline,
    set_seed
)
import torch
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Hugging Face Transformers Service",
    description="Local LLM service using Hugging Face transformers for GRC Platform",
    version="1.0.0"
)

# Global variables for loaded models
loaded_models = {}
model_pipelines = {}

# Configuration
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL_NAME", "microsoft/DialoGPT-medium")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
MAX_MODEL_SIZE = os.getenv("MAX_MODEL_SIZE", "2GB")
ENABLE_GPU = os.getenv("ENABLE_GPU", "false").lower() == "true"

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    model_name: Optional[str] = DEFAULT_MODEL
    max_length: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    conversation_history: Optional[List[Dict[str, str]]] = []

class EmbeddingRequest(BaseModel):
    text: str
    model_name: Optional[str] = EMBEDDING_MODEL

class ModelInfo(BaseModel):
    model_name: str
    model_type: str
    loaded: bool
    memory_usage: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    model_used: str
    tokens_generated: int
    processing_time: float
    conversation_id: Optional[str] = None

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    model_used: str
    dimension: int

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    logger.info("Starting Hugging Face Transformers Service...")
    
    # Set random seed for reproducibility
    set_seed(42)
    
    # Load default models
    await load_default_models()
    
    logger.info("Service startup completed")

async def load_default_models():
    """Load default models for the service"""
    try:
        logger.info(f"Loading default chat model: {DEFAULT_MODEL}")
        await load_chat_model(DEFAULT_MODEL)
        
        logger.info(f"Loading default embedding model: {EMBEDDING_MODEL}")
        await load_embedding_model(EMBEDDING_MODEL)
        
    except Exception as e:
        logger.error(f"Error loading default models: {e}")

async def load_chat_model(model_name: str):
    """Load a chat model"""
    try:
        if model_name in loaded_models:
            logger.info(f"Model {model_name} already loaded")
            return
        
        logger.info(f"Loading chat model: {model_name}")
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if ENABLE_GPU else torch.float32,
            device_map="auto" if ENABLE_GPU else None
        )
        
        # Create pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if ENABLE_GPU else -1
        )
        
        # Store in global variables
        loaded_models[model_name] = {
            "model": model,
            "tokenizer": tokenizer,
            "type": "chat"
        }
        model_pipelines[model_name] = pipe
        
        logger.info(f"Successfully loaded model: {model_name}")
        
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {e}")
        raise

async def load_embedding_model(model_name: str):
    """Load an embedding model"""
    try:
        if model_name in loaded_models:
            logger.info(f"Model {model_name} already loaded")
            return
        
        logger.info(f"Loading embedding model: {model_name}")
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if ENABLE_GPU else torch.float32,
            device_map="auto" if ENABLE_GPU else None
        )
        
        # Create pipeline
        pipe = pipeline(
            "feature-extraction",
            model=model,
            tokenizer=tokenizer,
            device=0 if ENABLE_GPU else -1
        )
        
        # Store in global variables
        loaded_models[model_name] = {
            "model": model,
            "tokenizer": tokenizer,
            "type": "embedding"
        }
        model_pipelines[model_name] = pipe
        
        logger.info(f"Successfully loaded embedding model: {model_name}")
        
    except Exception as e:
        logger.error(f"Error loading embedding model {model_name}: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "huggingface-transformers",
        "loaded_models": list(loaded_models.keys()),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/models")
async def list_models():
    """List all loaded models"""
    models_info = []
    for model_name, model_data in loaded_models.items():
        models_info.append(ModelInfo(
            model_name=model_name,
            model_type=model_data["type"],
            loaded=True,
            memory_usage="Unknown"  # Could add memory tracking here
        ))
    
    return {"models": models_info}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate chat response using loaded model"""
    try:
        start_time = datetime.utcnow()
        
        # Ensure model is loaded
        if request.model_name not in loaded_models:
            await load_chat_model(request.model_name)
        
        # Get the pipeline
        pipe = model_pipelines.get(request.model_name)
        if not pipe:
            raise HTTPException(status_code=500, detail=f"Model {request.model_name} not properly loaded")
        
        # Prepare input text
        input_text = request.message
        if request.conversation_history:
            # Build conversation context
            context = ""
            for msg in request.conversation_history[-5:]:  # Last 5 messages
                context += f"{msg.get('role', 'user')}: {msg.get('content', '')}\n"
            input_text = context + f"user: {request.message}\nassistant:"
        
        # Generate response
        result = pipe(
            input_text,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            do_sample=True,
            pad_token_id=pipe.tokenizer.eos_token_id
        )
        
        # Extract response
        generated_text = result[0]["generated_text"]
        response = generated_text[len(input_text):].strip()
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Estimate tokens (rough approximation)
        tokens_generated = len(response.split())
        
        return ChatResponse(
            response=response,
            model_used=request.model_name,
            tokens_generated=tokens_generated,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in chat generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embeddings", response_model=EmbeddingResponse)
async def generate_embeddings(request: EmbeddingRequest):
    """Generate embeddings for text"""
    try:
        # Ensure model is loaded
        if request.model_name not in loaded_models:
            await load_embedding_model(request.model_name)
        
        # Get the pipeline
        pipe = model_pipelines.get(request.model_name)
        if not pipe:
            raise HTTPException(status_code=500, detail=f"Model {request.model_name} not properly loaded")
        
        # Generate embeddings
        embeddings = pipe(request.text)
        
        # Extract the embedding vector
        # The embeddings are returned as a list of lists (tokens)
        # We need to convert to tensor first, then take mean pooling
        if isinstance(embeddings, list) and len(embeddings) > 0:
            # Get the first (and usually only) result
            result = embeddings[0]
            if isinstance(result, list):
                # Convert list to tensor for mean pooling
                import torch
                tensor_result = torch.tensor(result)
                # Take mean across all tokens to get sentence embedding
                embedding_vector = tensor_result.mean(dim=0).tolist()
            else:
                # Already a tensor
                embedding_vector = result.mean(dim=0).tolist() if hasattr(result, 'mean') else list(result)
        else:
            # Direct tensor format
            embedding_vector = embeddings.mean(dim=0).tolist() if hasattr(embeddings, 'mean') else list(embeddings)
        
        return EmbeddingResponse(
            embedding=embedding_vector,
            model_used=request.model_name,
            dimension=len(embedding_vector)
        )
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/models/{model_name}/load")
async def load_model(model_name: str, background_tasks: BackgroundTasks):
    """Load a specific model"""
    try:
        if model_name in loaded_models:
            return {"message": f"Model {model_name} already loaded"}
        
        # Determine model type and load accordingly
        if "embedding" in model_name.lower() or "sentence" in model_name.lower():
            background_tasks.add_task(load_embedding_model, model_name)
        else:
            background_tasks.add_task(load_chat_model, model_name)
        
        return {"message": f"Loading model {model_name} in background"}
        
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/models/{model_name}")
async def unload_model(model_name: str):
    """Unload a specific model to free memory"""
    try:
        if model_name not in loaded_models:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        # Remove from loaded models
        del loaded_models[model_name]
        if model_name in model_pipelines:
            del model_pipelines[model_name]
        
        # Force garbage collection
        import gc
        gc.collect()
        
        if ENABLE_GPU:
            torch.cuda.empty_cache()
        
        return {"message": f"Model {model_name} unloaded successfully"}
        
    except Exception as e:
        logger.error(f"Error unloading model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Hugging Face Transformers Service",
        "version": "1.0.0",
        "description": "Local LLM service for GRC Platform",
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

