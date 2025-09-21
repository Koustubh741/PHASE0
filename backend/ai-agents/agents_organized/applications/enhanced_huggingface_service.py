#!/usr/bin/env python3
"""
Enhanced Hugging Face Transformers Service for GRC Platform
Multi-LLM service with user-selectable large and small models
"""

import os
import logging
import asyncio
import psutil
import time
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
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
from enum import Enum

# Import our model catalog
from model_catalog import ModelCatalog, ModelInfo, ModelType, ModelCategory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced Hugging Face Multi-LLM Service",
    description="Advanced LLM service with user-selectable models for GRC Platform",
    version="2.0.0"
)

# Global variables for loaded models
loaded_models: Dict[str, Dict[str, Any]] = {}
model_pipelines: Dict[str, Any] = {}
model_usage_stats: Dict[str, Dict[str, Any]] = {}

# System configuration
ENABLE_GPU = os.getenv("ENABLE_GPU", "false").lower() == "true"
MAX_CONCURRENT_MODELS = int(os.getenv("MAX_CONCURRENT_MODELS", "3"))
AUTO_UNLOAD_INACTIVE_MODELS = os.getenv("AUTO_UNLOAD_INACTIVE_MODELS", "true").lower() == "true"
INACTIVE_THRESHOLD_MINUTES = int(os.getenv("INACTIVE_THRESHOLD_MINUTES", "30"))

# Pydantic models for API
class ModelSelectionRequest(BaseModel):
    """Request for model selection with validation"""
    model_id: str = Field(..., description="Model ID from catalog")
    task_description: Optional[str] = Field(None, description="Description of the task to help with recommendations")
    force_load: bool = Field(False, description="Force load even if resources are limited")

class ChatRequest(BaseModel):
    """Enhanced chat request with model selection"""
    message: str = Field(..., description="User message")
    model_id: Optional[str] = Field(None, description="Specific model to use")
    max_length: Optional[int] = Field(100, description="Maximum response length")
    temperature: Optional[float] = Field(0.7, description="Temperature for generation")
    top_p: Optional[float] = Field(0.9, description="Top-p for generation")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    auto_model_selection: bool = Field(True, description="Automatically select best model if model_id not specified")

class EmbeddingRequest(BaseModel):
    """Enhanced embedding request"""
    text: str = Field(..., description="Text to embed")
    model_id: Optional[str] = Field(None, description="Specific embedding model to use")
    auto_model_selection: bool = Field(True, description="Automatically select best embedding model")

class ModelRecommendationRequest(BaseModel):
    """Request for model recommendations"""
    task_description: str = Field(..., description="Description of the task")
    preferred_speed: Optional[str] = Field(None, description="Speed preference: fast, balanced, quality")
    memory_limit_gb: Optional[float] = Field(None, description="Memory limit in GB")
    category: Optional[str] = Field(None, description="Task category filter")

class ChatResponse(BaseModel):
    """Enhanced chat response"""
    response: str = Field(..., description="Generated response")
    model_used: str = Field(..., description="Model used for generation")
    model_info: Dict[str, Any] = Field(..., description="Model information")
    tokens_generated: int = Field(..., description="Approximate tokens generated")
    processing_time: float = Field(..., description="Processing time in seconds")
    conversation_id: Optional[str] = Field(None)
    confidence_score: Optional[float] = Field(None, description="Confidence score for the response")

class EmbeddingResponse(BaseModel):
    """Enhanced embedding response"""
    embedding: List[float] = Field(..., description="Generated embedding vector")
    model_used: str = Field(..., description="Model used for embedding")
    model_info: Dict[str, Any] = Field(..., description="Model information")
    dimension: int = Field(..., description="Embedding dimension")
    processing_time: float = Field(..., description="Processing time in seconds")

class ModelRecommendationResponse(BaseModel):
    """Model recommendation response"""
    recommended_models: List[Dict[str, Any]] = Field(..., description="List of recommended models")
    primary_recommendation: Dict[str, Any] = Field(..., description="Primary model recommendation")
    reasoning: str = Field(..., description="Reasoning for the recommendation")

class ModelStatusResponse(BaseModel):
    """Model status response"""
    loaded_models: Dict[str, Dict[str, Any]] = Field(..., description="Currently loaded models")
    system_resources: Dict[str, Any] = Field(..., description="System resource usage")
    recommendations: Dict[str, Any] = Field(..., description="System recommendations")

# Utility functions
def get_system_resources() -> Dict[str, Any]:
    """Get current system resource usage"""
    memory = psutil.virtual_memory()
    return {
        "total_memory_gb": round(memory.total / (1024**3), 2),
        "available_memory_gb": round(memory.available / (1024**3), 2),
        "memory_usage_percent": memory.percent,
        "cpu_count": psutil.cpu_count(),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "has_gpu": torch.cuda.is_available() if ENABLE_GPU else False,
        "gpu_count": torch.cuda.device_count() if ENABLE_GPU and torch.cuda.is_available() else 0
    }

def get_model_performance_metrics(model_id: str, processing_time: float, response_length: int) -> Dict[str, Any]:
    """Calculate performance metrics for a model"""
    model_info = ModelCatalog.get_model_info(model_id)
    if not model_info:
        return {}
    
    # Calculate tokens per second
    tokens_per_second = response_length / processing_time if processing_time > 0 else 0
    
    return {
        "tokens_per_second": round(tokens_per_second, 2),
        "processing_time": processing_time,
        "response_length": response_length,
        "model_size": model_info.performance.parameters,
        "memory_efficiency": round(model_info.performance.speed / model_info.memory_requirement_gb, 2)
    }

async def auto_select_model_for_task(task_description: str, model_type: ModelType = ModelType.SMALL_LLM) -> Optional[str]:
    """Automatically select the best model for a given task"""
    system_resources = get_system_resources()
    
    # Get recommended model from catalog
    recommended_model = ModelCatalog.get_recommended_model_for_task(task_description)
    if recommended_model:
        # Validate if the recommended model can be loaded
        validation = ModelCatalog.validate_model_selection(
            recommended_model.id,
            system_resources["available_memory_gb"],
            system_resources["has_gpu"]
        )
        if validation["valid"]:
            return recommended_model.id
    
    # Fallback to default models
    default_models = ModelCatalog.get_default_models()
    for model_id, model_info in default_models.items():
        if model_info.model_type == model_type:
            validation = ModelCatalog.validate_model_selection(
                model_id,
                system_resources["available_memory_gb"],
                system_resources["has_gpu"]
            )
            if validation["valid"]:
                return model_id
    
    return None

async def unload_inactive_models():
    """Unload models that haven't been used recently"""
    if not AUTO_UNLOAD_INACTIVE_MODELS:
        return
    
    current_time = time.time()
    models_to_unload = []
    
    for model_id, stats in model_usage_stats.items():
        if model_id not in loaded_models:
            continue
            
        last_used = stats.get("last_used", 0)
        if current_time - last_used > (INACTIVE_THRESHOLD_MINUTES * 60):
            models_to_unload.append(model_id)
    
    for model_id in models_to_unload:
        await unload_model(model_id)
        logger.info(f"Auto-unloaded inactive model: {model_id}")

# Model loading functions
async def load_model_from_catalog(model_id: str) -> bool:
    """Load a model from the catalog"""
    try:
        model_info = ModelCatalog.get_model_info(model_id)
        if not model_info:
            raise ValueError(f"Model {model_id} not found in catalog")
        
        # Validate system resources
        system_resources = get_system_resources()
        validation = ModelCatalog.validate_model_selection(
            model_id,
            system_resources["available_memory_gb"],
            system_resources["has_gpu"]
        )
        
        if not validation["valid"]:
            raise ValueError(f"Cannot load model: {validation['reason']}")
        
        # Check if already loaded
        if model_id in loaded_models:
            logger.info(f"Model {model_id} already loaded")
            return True
        
        # Unload inactive models if we're at the limit
        if len(loaded_models) >= MAX_CONCURRENT_MODELS:
            await unload_inactive_models()
            if len(loaded_models) >= MAX_CONCURRENT_MODELS:
                raise ValueError(f"Maximum concurrent models limit reached ({MAX_CONCURRENT_MODELS})")
        
        logger.info(f"Loading model: {model_info.name}")
        
        # Load based on model type
        if model_info.model_type in [ModelType.SMALL_LLM, ModelType.LARGE_LLM, ModelType.SPECIALIZED]:
            await load_chat_model(model_id, model_info)
        elif model_info.model_type == ModelType.EMBEDDING:
            await load_embedding_model(model_id, model_info)
        else:
            raise ValueError(f"Unsupported model type: {model_info.model_type}")
        
        # Initialize usage stats
        model_usage_stats[model_id] = {
            "loaded_at": time.time(),
            "last_used": time.time(),
            "usage_count": 0,
            "total_processing_time": 0.0
        }
        
        logger.info(f"Successfully loaded model: {model_info.name}")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model {model_id}: {e}")
        raise

async def load_chat_model(model_id: str, model_info: ModelInfo):
    """Load a chat model"""
    tokenizer = AutoTokenizer.from_pretrained(
        model_info.huggingface_id,
        trust_remote_code=False,
        local_files_only=False,
        use_fast=True
    )
    
    # Ensure pad_token is defined
    if tokenizer.pad_token is None:
        if tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token
        else:
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    
    model = AutoModelForCausalLM.from_pretrained(
        model_info.huggingface_id,
        torch_dtype=torch.float16 if ENABLE_GPU else torch.float32,
        device_map="auto" if ENABLE_GPU else None,
        trust_remote_code=False,
        local_files_only=False
    )
    
    # Create pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if ENABLE_GPU else -1
    )
    
    # Store in global variables
    loaded_models[model_id] = {
        "model": model,
        "tokenizer": tokenizer,
        "type": "chat",
        "model_info": model_info.dict()
    }
    model_pipelines[model_id] = pipe

async def load_embedding_model(model_id: str, model_info: ModelInfo):
    """Load an embedding model"""
    tokenizer = AutoTokenizer.from_pretrained(
        model_info.huggingface_id,
        trust_remote_code=False,
        local_files_only=False,
        use_fast=True
    )
    
    model = AutoModel.from_pretrained(
        model_info.huggingface_id,
        torch_dtype=torch.float16 if ENABLE_GPU else torch.float32,
        device_map="auto" if ENABLE_GPU else None,
        trust_remote_code=False,
        local_files_only=False
    )
    
    # Create pipeline
    pipe = pipeline(
        "feature-extraction",
        model=model,
        tokenizer=tokenizer,
        device=0 if ENABLE_GPU else -1
    )
    
    # Store in global variables
    loaded_models[model_id] = {
        "model": model,
        "tokenizer": tokenizer,
        "type": "embedding",
        "model_info": model_info.dict()
    }
    model_pipelines[model_id] = pipe

async def unload_model(model_id: str):
    """Unload a model to free memory"""
    try:
        if model_id not in loaded_models:
            logger.warning(f"Model {model_id} not loaded")
            return
        
        # Remove from loaded models
        del loaded_models[model_id]
        if model_id in model_pipelines:
            del model_pipelines[model_id]
        
        # Remove usage stats
        if model_id in model_usage_stats:
            del model_usage_stats[model_id]
        
        # Force garbage collection
        import gc
        gc.collect()
        
        if ENABLE_GPU and torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info(f"Successfully unloaded model: {model_id}")
        
    except Exception as e:
        logger.error(f"Error unloading model {model_id}: {e}")
        raise

# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize the service"""
    logger.info("Starting Enhanced Hugging Face Multi-LLM Service...")
    
    # Set random seed for reproducibility
    set_seed(42)
    
    # Load default models
    default_models = ModelCatalog.get_default_models()
    for model_id in default_models.keys():
        try:
            await load_model_from_catalog(model_id)
        except Exception as e:
            logger.warning(f"Could not load default model {model_id}: {e}")
    
    logger.info("Enhanced service startup completed")

@app.get("/health")
async def health_check():
    """Health check endpoint with enhanced information"""
    system_resources = get_system_resources()
    return {
        "status": "healthy",
        "service": "enhanced-huggingface-multi-llm",
        "version": "2.0.0",
        "loaded_models": list(loaded_models.keys()),
        "system_resources": system_resources,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/models", response_model=Dict[str, Any])
async def list_available_models(
    model_type: Optional[str] = Query(None, description="Filter by model type"),
    category: Optional[str] = Query(None, description="Filter by category"),
    loaded_only: bool = Query(False, description="Show only loaded models")
):
    """List all available models with filtering options"""
    if loaded_only:
        loaded_model_info = {}
        for model_id in loaded_models.keys():
            model_info = ModelCatalog.get_model_info(model_id)
            if model_info:
                loaded_model_info[model_id] = {
                    "model_info": model_info.dict(),
                    "usage_stats": model_usage_stats.get(model_id, {}),
                    "status": "loaded"
                }
        return {"models": loaded_model_info}
    
    all_models = ModelCatalog.get_available_models()
    
    # Apply filters
    if model_type:
        all_models = {k: v for k, v in all_models.items() if v.model_type.value == model_type}
    
    if category:
        all_models = {k: v for k, v in all_models.items() if v.category.value == category}
    
    # Add status information
    models_with_status = {}
    for model_id, model_info in all_models.items():
        models_with_status[model_id] = {
            "model_info": model_info.dict(),
            "status": "loaded" if model_id in loaded_models else "available",
            "usage_stats": model_usage_stats.get(model_id, {})
        }
    
    return {"models": models_with_status}

@app.post("/models/recommend", response_model=ModelRecommendationResponse)
async def recommend_models(request: ModelRecommendationRequest):
    """Get model recommendations based on task description"""
    all_models = ModelCatalog.get_available_models()
    system_resources = get_system_resources()
    
    # Filter models based on criteria
    candidate_models = []
    
    for model_id, model_info in all_models.items():
        # Check resource requirements
        validation = ModelCatalog.validate_model_selection(
            model_id,
            system_resources["available_memory_gb"],
            system_resources["has_gpu"]
        )
        
        if not validation["valid"]:
            continue
        
        # Apply category filter if specified
        if request.category and model_info.category.value != request.category:
            continue
        
        # Apply speed preference
        if request.preferred_speed:
            if request.preferred_speed == "fast" and model_info.performance.speed < 8.0:
                continue
            elif request.preferred_speed == "quality" and model_info.performance.quality < 8.0:
                continue
        
        candidate_models.append((model_id, model_info))
    
    # Sort by relevance (simple scoring)
    def calculate_score(model_info: ModelInfo, task: str) -> float:
        score = 0.0
        task_lower = task.lower()
        
        # Speed preference
        if request.preferred_speed == "fast":
            score += model_info.performance.speed * 0.4
        elif request.preferred_speed == "quality":
            score += model_info.performance.quality * 0.4
        else:
            score += (model_info.performance.speed + model_info.performance.quality) * 0.2
        
        # Category matching
        if any(keyword in task_lower for keyword in model_info.use_cases):
            score += 2.0
        
        # Memory efficiency
        score += (10.0 / model_info.memory_requirement_gb) * 0.2
        
        return score
    
    candidate_models.sort(key=lambda x: calculate_score(x[1], request.task_description), reverse=True)
    
    # Prepare response
    recommended_models = []
    for model_id, model_info in candidate_models[:5]:  # Top 5 recommendations
        recommended_models.append({
            "model_id": model_id,
            "model_info": model_info.dict(),
            "score": calculate_score(model_info, request.task_description)
        })
    
    primary_recommendation = recommended_models[0] if recommended_models else {}
    
    reasoning = f"Recommended {primary_recommendation.get('model_info', {}).get('name', 'model')} based on your task requirements"
    
    return ModelRecommendationResponse(
        recommended_models=recommended_models,
        primary_recommendation=primary_recommendation,
        reasoning=reasoning
    )

@app.post("/models/{model_id}/load")
async def load_model_endpoint(model_id: str, background_tasks: BackgroundTasks):
    """Load a specific model"""
    try:
        if model_id in loaded_models:
            return {"message": f"Model {model_id} already loaded", "status": "already_loaded"}
        
        # Load model in background
        background_tasks.add_task(load_model_from_catalog, model_id)
        
        return {"message": f"Loading model {model_id} in background", "status": "loading"}
        
    except Exception as e:
        logger.error(f"Error loading model {model_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/models/{model_id}")
async def unload_model_endpoint(model_id: str):
    """Unload a specific model"""
    try:
        if model_id not in loaded_models:
            raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
        
        await unload_model(model_id)
        
        return {"message": f"Model {model_id} unloaded successfully", "status": "unloaded"}
        
    except Exception as e:
        logger.error(f"Error unloading model {model_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/{model_id}/status")
async def get_model_status(model_id: str):
    """Get status and usage statistics for a specific model"""
    model_info = ModelCatalog.get_model_info(model_id)
    if not model_info:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
    
    is_loaded = model_id in loaded_models
    usage_stats = model_usage_stats.get(model_id, {})
    
    return {
        "model_id": model_id,
        "model_info": model_info.dict(),
        "status": "loaded" if is_loaded else "available",
        "usage_stats": usage_stats,
        "system_validation": ModelCatalog.validate_model_selection(
            model_id,
            get_system_resources()["available_memory_gb"],
            get_system_resources()["has_gpu"]
        )
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Enhanced chat endpoint with automatic model selection"""
    try:
        start_time = time.time()
        
        # Determine which model to use
        model_id = request.model_id
        
        if not model_id and request.auto_model_selection:
            model_id = await auto_select_model_for_task(request.message)
        
        if not model_id:
            # Fallback to any available model
            available_models = [mid for mid in loaded_models.keys() if loaded_models[mid]["type"] == "chat"]
            if not available_models:
                raise HTTPException(status_code=503, detail="No chat models available")
            model_id = available_models[0]
        
        # Ensure model is loaded
        if model_id not in loaded_models:
            await load_model_from_catalog(model_id)
        
        # Get model pipeline
        pipe = model_pipelines.get(model_id)
        if not pipe:
            raise HTTPException(status_code=500, detail=f"Model {model_id} not properly loaded")
        
        # Security: Validate and sanitize input
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if len(request.message) > 10000:
            raise HTTPException(status_code=400, detail="Message too long (max 10KB)")
        
        # Sanitize input text
        import re
        sanitized_message = re.sub(r'[<>"\']', '', request.message.strip())
        
        # Prepare input text
        input_text = sanitized_message
        if request.conversation_history:
            context = ""
            for msg in request.conversation_history[-5:]:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                sanitized_role = re.sub(r'[<>"\']', '', str(role))
                sanitized_content = re.sub(r'[<>"\']', '', str(content))
                context += f"{sanitized_role}: {sanitized_content}\n"
            input_text = context + f"user: {sanitized_message}\nassistant:"
        
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
        processing_time = time.time() - start_time
        
        # Update usage stats
        if model_id in model_usage_stats:
            model_usage_stats[model_id]["last_used"] = time.time()
            model_usage_stats[model_id]["usage_count"] += 1
            model_usage_stats[model_id]["total_processing_time"] += processing_time
        
        # Calculate metrics
        tokens_generated = len(response.split())
        model_info = ModelCatalog.get_model_info(model_id)
        performance_metrics = get_model_performance_metrics(model_id, processing_time, tokens_generated)
        
        # Calculate confidence score (simple heuristic)
        confidence_score = min(1.0, len(response) / 50.0) if response else 0.0
        
        return ChatResponse(
            response=response,
            model_used=model_id,
            model_info=model_info.dict() if model_info else {},
            tokens_generated=tokens_generated,
            processing_time=processing_time,
            confidence_score=confidence_score,
            **performance_metrics
        )
        
    except Exception as e:
        logger.error(f"Error in chat generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embeddings", response_model=EmbeddingResponse)
async def generate_embeddings(request: EmbeddingRequest):
    """Enhanced embeddings endpoint with automatic model selection"""
    try:
        start_time = time.time()
        
        # Determine which model to use
        model_id = request.model_id
        
        if not model_id and request.auto_model_selection:
            model_id = await auto_select_model_for_task(request.text, ModelType.EMBEDDING)
        
        if not model_id:
            # Fallback to any available embedding model
            available_models = [mid for mid in loaded_models.keys() if loaded_models[mid]["type"] == "embedding"]
            if not available_models:
                raise HTTPException(status_code=503, detail="No embedding models available")
            model_id = available_models[0]
        
        # Ensure model is loaded
        if model_id not in loaded_models:
            await load_model_from_catalog(model_id)
        
        # Get model pipeline
        pipe = model_pipelines.get(model_id)
        if not pipe:
            raise HTTPException(status_code=500, detail=f"Model {model_id} not properly loaded")
        
        # Security: Validate and sanitize input
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(request.text) > 50000:
            raise HTTPException(status_code=400, detail="Text too long (max 50KB)")
        
        # Sanitize input text
        import re
        sanitized_text = re.sub(r'[<>"\']', '', request.text.strip())
        
        # Generate embeddings
        embeddings = pipe(sanitized_text)
        
        # Extract the embedding vector
        if isinstance(embeddings, list) and len(embeddings) > 0:
            result = embeddings[0]
            if isinstance(result, list):
                import torch
                tensor_result = torch.tensor(result)
                embedding_vector = tensor_result.mean(dim=0).tolist()
            else:
                embedding_vector = result.mean(dim=0).tolist() if hasattr(result, 'mean') else list(result)
        else:
            embedding_vector = embeddings.mean(dim=0).tolist() if hasattr(embeddings, 'mean') else list(embeddings)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update usage stats
        if model_id in model_usage_stats:
            model_usage_stats[model_id]["last_used"] = time.time()
            model_usage_stats[model_id]["usage_count"] += 1
            model_usage_stats[model_id]["total_processing_time"] += processing_time
        
        # Get model info
        model_info = ModelCatalog.get_model_info(model_id)
        
        return EmbeddingResponse(
            embedding=embedding_vector,
            model_used=model_id,
            model_info=model_info.dict() if model_info else {},
            dimension=len(embedding_vector),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/status", response_model=ModelStatusResponse)
async def get_system_status():
    """Get comprehensive system status"""
    system_resources = get_system_resources()
    
    # Prepare loaded models info
    loaded_models_info = {}
    for model_id, model_data in loaded_models.items():
        model_info = ModelCatalog.get_model_info(model_id)
        loaded_models_info[model_id] = {
            "model_info": model_info.dict() if model_info else {},
            "usage_stats": model_usage_stats.get(model_id, {}),
            "memory_usage": "Unknown"  # Could add actual memory tracking
        }
    
    # Generate recommendations
    recommendations = {
        "can_load_more_models": len(loaded_models) < MAX_CONCURRENT_MODELS,
        "suggested_models": [],
        "resource_warnings": []
    }
    
    if system_resources["memory_usage_percent"] > 80:
        recommendations["resource_warnings"].append("High memory usage detected")
    
    if not system_resources["has_gpu"] and ENABLE_GPU:
        recommendations["resource_warnings"].append("GPU not available but expected")
    
    return ModelStatusResponse(
        loaded_models=loaded_models_info,
        system_resources=system_resources,
        recommendations=recommendations
    )

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Enhanced Hugging Face Multi-LLM Service",
        "version": "2.0.0",
        "description": "Advanced LLM service with user-selectable models for GRC Platform",
        "features": [
            "Multi-LLM support",
            "Automatic model selection",
            "Resource management",
            "Usage analytics",
            "Model recommendations"
        ],
        "endpoints": {
            "health": "/health",
            "models": "/models",
            "recommendations": "/models/recommend",
            "chat": "/chat",
            "embeddings": "/embeddings",
            "system_status": "/system/status"
        },
        "available_models": len(ModelCatalog.get_available_models()),
        "loaded_models": len(loaded_models)
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8007))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
