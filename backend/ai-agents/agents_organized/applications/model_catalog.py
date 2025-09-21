#!/usr/bin/env python3
"""
Model Catalog for Multi-LLM Service
Defines available large and small language models with metadata
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class ModelType(str, Enum):
    """Model type enumeration"""
    LARGE_LLM = "large_llm"
    SMALL_LLM = "small_llm"
    EMBEDDING = "embedding"
    SPECIALIZED = "specialized"

class ModelCategory(str, Enum):
    """Model category enumeration"""
    GENERAL = "general"
    CODE = "code"
    FINANCE = "finance"
    LEGAL = "legal"
    SECURITY = "security"
    COMPLIANCE = "compliance"

class ModelPerformance(BaseModel):
    """Model performance characteristics"""
    speed: float = Field(..., description="Speed score (1-10, 10 being fastest)")
    quality: float = Field(..., description="Quality score (1-10, 10 being highest)")
    memory_usage: str = Field(..., description="Memory usage description")
    context_length: int = Field(..., description="Maximum context length in tokens")
    parameters: str = Field(..., description="Number of parameters")
    
class ModelInfo(BaseModel):
    """Complete model information"""
    id: str = Field(..., description="Unique model identifier")
    name: str = Field(..., description="User-friendly model name")
    description: str = Field(..., description="Model description")
    model_type: ModelType = Field(..., description="Type of model")
    category: ModelCategory = Field(..., description="Model category")
    huggingface_id: str = Field(..., description="Hugging Face model ID")
    performance: ModelPerformance = Field(..., description="Performance characteristics")
    use_cases: List[str] = Field(..., description="Recommended use cases")
    limitations: List[str] = Field(..., description="Model limitations")
    recommended_for: List[str] = Field(..., description="Recommended for specific tasks")
    memory_requirement_gb: float = Field(..., description="Minimum memory requirement in GB")
    gpu_required: bool = Field(False, description="Whether GPU is required for optimal performance")
    is_default: bool = Field(False, description="Whether this is a default model")
    tags: List[str] = Field(default_factory=list, description="Model tags for filtering")

class ModelCatalog:
    """Centralized model catalog with predefined models"""
    
    @staticmethod
    def get_available_models() -> Dict[str, ModelInfo]:
        """Get all available models"""
        return {
            # Small LLMs (Fast, Low Memory)
            "tiny-llama": ModelInfo(
                id="tiny-llama",
                name="TinyLlama (1.1B)",
                description="Ultra-fast small language model optimized for speed and efficiency",
                model_type=ModelType.SMALL_LLM,
                category=ModelCategory.GENERAL,
                huggingface_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                performance=ModelPerformance(
                    speed=9.5,
                    quality=6.5,
                    memory_usage="~2GB RAM",
                    context_length=2048,
                    parameters="1.1B"
                ),
                use_cases=[
                    "Quick responses",
                    "Simple Q&A",
                    "Basic text generation",
                    "Real-time chat"
                ],
                limitations=[
                    "Limited reasoning capability",
                    "Shorter context understanding",
                    "Basic language tasks only"
                ],
                recommended_for=[
                    "Fast responses",
                    "Low-resource environments",
                    "Simple conversations"
                ],
                memory_requirement_gb=2.0,
                gpu_required=False,
                is_default=True,
                tags=["fast", "lightweight", "chat"]
            ),
            
            "phi-2": ModelInfo(
                id="phi-2",
                name="Microsoft Phi-2 (2.7B)",
                description="High-quality small language model with excellent reasoning capabilities",
                model_type=ModelType.SMALL_LLM,
                category=ModelCategory.GENERAL,
                huggingface_id="microsoft/Phi-2",
                performance=ModelPerformance(
                    speed=8.0,
                    quality=8.5,
                    memory_usage="~6GB RAM",
                    context_length=2048,
                    parameters="2.7B"
                ),
                use_cases=[
                    "Code generation",
                    "Mathematical reasoning",
                    "General conversation",
                    "Question answering"
                ],
                limitations=[
                    "Limited to 2K context",
                    "May struggle with very complex tasks"
                ],
                recommended_for=[
                    "Balanced performance",
                    "Code assistance",
                    "Educational content"
                ],
                memory_requirement_gb=6.0,
                gpu_required=False,
                tags=["reasoning", "code", "balanced"]
            ),
            
            "gemma-2b": ModelInfo(
                id="gemma-2b",
                name="Google Gemma 2B",
                description="Efficient small model with strong performance for its size",
                model_type=ModelType.SMALL_LLM,
                category=ModelCategory.GENERAL,
                huggingface_id="google/gemma-2b-it",
                performance=ModelPerformance(
                    speed=8.5,
                    quality=7.5,
                    memory_usage="~4GB RAM",
                    context_length=8192,
                    parameters="2B"
                ),
                use_cases=[
                    "Instruction following",
                    "Text generation",
                    "Dialogue systems",
                    "Content creation"
                ],
                limitations=[
                    "Limited complex reasoning",
                    "May need fine-tuning for specific domains"
                ],
                recommended_for=[
                    "Instruction-based tasks",
                    "Content generation",
                    "Dialogue systems"
                ],
                memory_requirement_gb=4.0,
                gpu_required=False,
                tags=["instruction", "dialogue", "google"]
            ),
            
            # Large LLMs (High Quality, More Resources)
            "llama2-7b": ModelInfo(
                id="llama2-7b",
                name="Llama 2 7B Chat",
                description="High-quality large language model with excellent conversational abilities",
                model_type=ModelType.LARGE_LLM,
                category=ModelCategory.GENERAL,
                huggingface_id="meta-llama/Llama-2-7b-chat-hf",
                performance=ModelPerformance(
                    speed=6.0,
                    quality=9.0,
                    memory_usage="~14GB RAM",
                    context_length=4096,
                    parameters="7B"
                ),
                use_cases=[
                    "Complex reasoning",
                    "Long-form content generation",
                    "Professional writing",
                    "Advanced Q&A"
                ],
                limitations=[
                    "High memory usage",
                    "Slower response times",
                    "Requires significant resources"
                ],
                recommended_for=[
                    "High-quality outputs",
                    "Complex tasks",
                    "Professional use"
                ],
                memory_requirement_gb=14.0,
                gpu_required=True,
                tags=["high-quality", "conversational", "meta"]
            ),
            
            "mistral-7b": ModelInfo(
                id="mistral-7b",
                name="Mistral 7B Instruct",
                description="Efficient large model with strong instruction-following capabilities",
                model_type=ModelType.LARGE_LLM,
                category=ModelCategory.GENERAL,
                huggingface_id="mistralai/Mistral-7B-Instruct-v0.2",
                performance=ModelPerformance(
                    speed=7.0,
                    quality=8.8,
                    memory_usage="~16GB RAM",
                    context_length=32768,
                    parameters="7B"
                ),
                use_cases=[
                    "Long context understanding",
                    "Complex instructions",
                    "Professional writing",
                    "Code generation"
                ],
                limitations=[
                    "High memory requirements",
                    "Slower than smaller models"
                ],
                recommended_for=[
                    "Long documents",
                    "Complex instructions",
                    "Professional tasks"
                ],
                memory_requirement_gb=16.0,
                gpu_required=True,
                tags=["long-context", "instruction", "mistral"]
            ),
            
            "codellama-7b": ModelInfo(
                id="codellama-7b",
                name="Code Llama 7B",
                description="Specialized model for code generation and programming tasks",
                model_type=ModelType.SPECIALIZED,
                category=ModelCategory.CODE,
                huggingface_id="codellama/CodeLlama-7b-Instruct-hf",
                performance=ModelPerformance(
                    speed=6.5,
                    quality=9.2,
                    memory_usage="~14GB RAM",
                    context_length=16384,
                    parameters="7B"
                ),
                use_cases=[
                    "Code generation",
                    "Code explanation",
                    "Debugging assistance",
                    "Programming education"
                ],
                limitations=[
                    "Specialized for code only",
                    "High memory usage"
                ],
                recommended_for=[
                    "Software development",
                    "Code review",
                    "Programming assistance"
                ],
                memory_requirement_gb=14.0,
                gpu_required=True,
                tags=["code", "programming", "specialized"]
            ),
            
            # Embedding Models
            "all-minilm": ModelInfo(
                id="all-minilm",
                name="All-MiniLM-L6-v2",
                description="Fast and efficient sentence transformer for embeddings",
                model_type=ModelType.EMBEDDING,
                category=ModelCategory.GENERAL,
                huggingface_id="sentence-transformers/all-MiniLM-L6-v2",
                performance=ModelPerformance(
                    speed=9.5,
                    quality=8.0,
                    memory_usage="~200MB RAM",
                    context_length=256,
                    parameters="22M"
                ),
                use_cases=[
                    "Semantic search",
                    "Document similarity",
                    "Clustering",
                    "Information retrieval"
                ],
                limitations=[
                    "Limited context length",
                    "Basic semantic understanding"
                ],
                recommended_for=[
                    "Fast embeddings",
                    "Search applications",
                    "Document processing"
                ],
                memory_requirement_gb=0.2,
                gpu_required=False,
                is_default=True,
                tags=["embedding", "fast", "search"]
            ),
            
            "all-mpnet": ModelInfo(
                id="all-mpnet",
                name="All-MPNet-Base-v2",
                description="High-quality sentence transformer for better semantic understanding",
                model_type=ModelType.EMBEDDING,
                category=ModelCategory.GENERAL,
                huggingface_id="sentence-transformers/all-mpnet-base-v2",
                performance=ModelPerformance(
                    speed=7.0,
                    quality=9.0,
                    memory_usage="~500MB RAM",
                    context_length=512,
                    parameters="109M"
                ),
                use_cases=[
                    "High-quality embeddings",
                    "Semantic similarity",
                    "Document classification",
                    "Advanced search"
                ],
                limitations=[
                    "Slower than smaller models",
                    "Higher memory usage"
                ],
                recommended_for=[
                    "Quality-critical applications",
                    "Document analysis",
                    "Semantic search"
                ],
                memory_requirement_gb=0.5,
                gpu_required=False,
                tags=["embedding", "high-quality", "semantic"]
            )
        }
    
    @staticmethod
    def get_models_by_type(model_type: ModelType) -> Dict[str, ModelInfo]:
        """Get models filtered by type"""
        all_models = ModelCatalog.get_available_models()
        return {k: v for k, v in all_models.items() if v.model_type == model_type}
    
    @staticmethod
    def get_models_by_category(category: ModelCategory) -> Dict[str, ModelInfo]:
        """Get models filtered by category"""
        all_models = ModelCatalog.get_available_models()
        return {k: v for k, v in all_models.items() if v.category == category}
    
    @staticmethod
    def get_default_models() -> Dict[str, ModelInfo]:
        """Get default models for each type"""
        all_models = ModelCatalog.get_available_models()
        return {k: v for k, v in all_models.items() if v.is_default}
    
    @staticmethod
    def get_recommended_model_for_task(task_description: str) -> Optional[ModelInfo]:
        """Get recommended model based on task description"""
        all_models = ModelCatalog.get_available_models()
        
        # Simple keyword-based recommendation
        task_lower = task_description.lower()
        
        if any(keyword in task_lower for keyword in ["code", "programming", "debug", "software"]):
            return all_models.get("codellama-7b")
        elif any(keyword in task_lower for keyword in ["fast", "quick", "real-time", "chat"]):
            return all_models.get("tiny-llama")
        elif any(keyword in task_lower for keyword in ["long", "document", "analysis", "complex"]):
            return all_models.get("mistral-7b")
        elif any(keyword in task_lower for keyword in ["embedding", "search", "similarity"]):
            return all_models.get("all-minilm")
        else:
            # Default to balanced model
            return all_models.get("phi-2")
    
    @staticmethod
    def get_model_info(model_id: str) -> Optional[ModelInfo]:
        """Get specific model information by ID"""
        all_models = ModelCatalog.get_available_models()
        return all_models.get(model_id)
    
    @staticmethod
    def validate_model_selection(model_id: str, available_memory_gb: float, has_gpu: bool) -> Dict[str, Any]:
        """Validate if a model can be loaded with current system resources"""
        model_info = ModelCatalog.get_model_info(model_id)
        if not model_info:
            return {
                "valid": False,
                "reason": f"Model {model_id} not found in catalog"
            }
        
        if model_info.memory_requirement_gb > available_memory_gb:
            return {
                "valid": False,
                "reason": f"Insufficient memory. Required: {model_info.memory_requirement_gb}GB, Available: {available_memory_gb}GB"
            }
        
        if model_info.gpu_required and not has_gpu:
            return {
                "valid": False,
                "reason": f"Model requires GPU but none detected"
            }
        
        return {
            "valid": True,
            "model_info": model_info,
            "estimated_load_time": "30-60 seconds" if model_info.model_type == ModelType.LARGE_LLM else "10-30 seconds"
        }
