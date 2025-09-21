#!/usr/bin/env python3
"""
Usage Examples for Enhanced Multi-LLM Service
Demonstrates how to use the enhanced Hugging Face service with multiple models
"""

import asyncio
import json
from typing import Dict, List, Any
import requests
from model_catalog import ModelCatalog, ModelType, ModelCategory

class MultiLLMClient:
    """Client for interacting with the Enhanced Multi-LLM Service"""
    
    def __init__(self, base_url: str = "http://localhost:8007"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def get_available_models(self, model_type: str = None, category: str = None) -> Dict[str, Any]:
        """Get available models with optional filtering"""
        params = {}
        if model_type:
            params['model_type'] = model_type
        if category:
            params['category'] = category
        
        response = self.session.get(f"{self.base_url}/models", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_model_recommendations(self, task_description: str, preferred_speed: str = None) -> Dict[str, Any]:
        """Get model recommendations for a specific task"""
        payload = {
            "task_description": task_description,
            "preferred_speed": preferred_speed
        }
        
        response = self.session.post(f"{self.base_url}/models/recommend", json=payload)
        response.raise_for_status()
        return response.json()
    
    def chat(self, message: str, model_id: str = None, auto_select: bool = True, **kwargs) -> Dict[str, Any]:
        """Send a chat message"""
        payload = {
            "message": message,
            "model_id": model_id,
            "auto_model_selection": auto_select,
            **kwargs
        }
        
        response = self.session.post(f"{self.base_url}/chat", json=payload)
        response.raise_for_status()
        return response.json()
    
    def generate_embeddings(self, text: str, model_id: str = None, auto_select: bool = True) -> Dict[str, Any]:
        """Generate embeddings for text"""
        payload = {
            "text": text,
            "model_id": model_id,
            "auto_model_selection": auto_select
        }
        
        response = self.session.post(f"{self.base_url}/embeddings", json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and resource usage"""
        response = self.session.get(f"{self.base_url}/system/status")
        response.raise_for_status()
        return response.json()
    
    def load_model(self, model_id: str) -> Dict[str, Any]:
        """Load a specific model"""
        response = self.session.post(f"{self.base_url}/models/{model_id}/load")
        response.raise_for_status()
        return response.json()
    
    def unload_model(self, model_id: str) -> Dict[str, Any]:
        """Unload a specific model"""
        response = self.session.delete(f"{self.base_url}/models/{model_id}")
        response.raise_for_status()
        return response.json()

# Example usage scenarios
async def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    client = MultiLLMClient()
    
    # 1. Get available models
    print("\n1. Available Models:")
    models = client.get_available_models()
    for model_id, info in models['models'].items():
        print(f"  - {model_id}: {info['model_info']['name']} ({info['model_info']['model_type']})")
    
    # 2. Get recommendations for a task
    print("\n2. Model Recommendations for 'Quick Q&A':")
    recommendations = client.get_model_recommendations("Quick question and answer")
    primary = recommendations['primary_recommendation']
    print(f"  Recommended: {primary['model_info']['name']}")
    print(f"  Reasoning: {recommendations['reasoning']}")
    
    # 3. Chat with automatic model selection
    print("\n3. Chat with Auto-Selection:")
    response = client.chat("What is machine learning?", auto_select=True)
    print(f"  Model used: {response['model_used']}")
    print(f"  Response: {response['response'][:100]}...")
    print(f"  Processing time: {response['processing_time']:.2f}s")
    
    # 4. Chat with specific model
    print("\n4. Chat with Specific Model (TinyLlama):")
    response = client.chat("Explain quantum computing", model_id="tiny-llama")
    print(f"  Model used: {response['model_used']}")
    print(f"  Response: {response['response'][:100]}...")

async def example_performance_comparison():
    """Compare performance across different models"""
    print("\n=== Performance Comparison Example ===")
    
    client = MultiLLMClient()
    
    # Test the same question with different models
    question = "What are the benefits of using microservices architecture?"
    models_to_test = ["tiny-llama", "phi-2", "gemma-2b"]
    
    results = {}
    
    for model_id in models_to_test:
        try:
            print(f"\nTesting with {model_id}...")
            response = client.chat(question, model_id=model_id, auto_select=False)
            
            results[model_id] = {
                "processing_time": response['processing_time'],
                "tokens_generated": response['tokens_generated'],
                "response_length": len(response['response']),
                "model_name": response['model_info']['name']
            }
            
            print(f"  Processing time: {response['processing_time']:.2f}s")
            print(f"  Tokens generated: {response['tokens_generated']}")
            print(f"  Response preview: {response['response'][:150]}...")
            
        except Exception as e:
            print(f"  Error with {model_id}: {e}")
    
    # Compare results
    print("\n=== Performance Summary ===")
    for model_id, result in results.items():
        print(f"{result['model_name']}:")
        print(f"  Speed: {result['processing_time']:.2f}s")
        print(f"  Efficiency: {result['tokens_generated']/result['processing_time']:.1f} tokens/sec")

async def example_task_specific_models():
    """Example of using task-specific models"""
    print("\n=== Task-Specific Model Usage ===")
    
    client = MultiLLMClient()
    
    # 1. Code generation task
    print("\n1. Code Generation Task:")
    code_request = "Write a Python function to calculate fibonacci numbers"
    
    recommendations = client.get_model_recommendations(code_request)
    print(f"Recommended for coding: {recommendations['primary_recommendation']['model_info']['name']}")
    
    response = client.chat(code_request, auto_select=True)
    print(f"Model used: {response['model_used']}")
    print(f"Code generated:\n{response['response']}")
    
    # 2. Fast Q&A task
    print("\n2. Fast Q&A Task:")
    qa_request = "What is the capital of France?"
    
    recommendations = client.get_model_recommendations(qa_request, preferred_speed="fast")
    print(f"Recommended for fast Q&A: {recommendations['primary_recommendation']['model_info']['name']}")
    
    response = client.chat(qa_request, auto_select=True)
    print(f"Model used: {response['model_used']}")
    print(f"Response: {response['response']}")
    print(f"Speed: {response['processing_time']:.2f}s")
    
    # 3. Embedding generation
    print("\n3. Embedding Generation:")
    text = "This is a sample document for embedding generation"
    
    response = client.generate_embeddings(text, auto_select=True)
    print(f"Embedding model used: {response['model_used']}")
    print(f"Embedding dimension: {response['dimension']}")
    print(f"Processing time: {response['processing_time']:.2f}s")

async def example_resource_management():
    """Example of resource management and monitoring"""
    print("\n=== Resource Management Example ===")
    
    client = MultiLLMClient()
    
    # 1. Check system status
    print("\n1. System Status:")
    status = client.get_system_status()
    
    print(f"Loaded models: {len(status['loaded_models'])}")
    for model_id, info in status['loaded_models'].items():
        print(f"  - {model_id}: {info['model_info']['name']}")
    
    print(f"\nSystem Resources:")
    resources = status['system_resources']
    print(f"  Available memory: {resources['available_memory_gb']:.1f} GB")
    print(f"  Memory usage: {resources['memory_usage_percent']:.1f}%")
    print(f"  GPU available: {resources['has_gpu']}")
    
    # 2. Load a specific model
    print("\n2. Loading a Specific Model:")
    try:
        result = client.load_model("phi-2")
        print(f"Load result: {result['message']}")
    except Exception as e:
        print(f"Load error: {e}")
    
    # 3. Check recommendations
    print("\n3. System Recommendations:")
    recommendations = status['recommendations']
    print(f"Can load more models: {recommendations['can_load_more_models']}")
    if recommendations['resource_warnings']:
        print("Resource warnings:")
        for warning in recommendations['resource_warnings']:
            print(f"  - {warning}")

async def example_conversation_flow():
    """Example of a conversation flow with context"""
    print("\n=== Conversation Flow Example ===")
    
    client = MultiLLMClient()
    
    # Simulate a conversation
    conversation = [
        "Hello, I need help with software architecture decisions.",
        "What are the main considerations when choosing between monolithic and microservices architecture?",
        "For a team of 5 developers, which would you recommend?",
        "What are the main challenges I should expect with microservices?"
    ]
    
    conversation_history = []
    
    for i, message in enumerate(conversation, 1):
        print(f"\n{i}. User: {message}")
        
        # Get recommendation for this type of question
        if i == 1:
            recommendations = client.get_model_recommendations(message)
            recommended_model = recommendations['primary_recommendation']['model_id']
            print(f"   Recommended model: {recommended_model}")
        
        # Send message with conversation history
        response = client.chat(
            message=message,
            model_id="phi-2",  # Use a balanced model for architecture discussions
            conversation_history=conversation_history,
            auto_select=False
        )
        
        print(f"   Assistant ({response['model_used']}): {response['response']}")
        print(f"   Processing time: {response['processing_time']:.2f}s")
        
        # Update conversation history
        conversation_history.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": response['response']}
        ])
        
        # Keep only last 4 exchanges (8 messages)
        if len(conversation_history) > 8:
            conversation_history = conversation_history[-8:]

def example_model_catalog_usage():
    """Example of using the model catalog directly"""
    print("\n=== Model Catalog Usage ===")
    
    # 1. Get all available models
    all_models = ModelCatalog.get_available_models()
    print(f"Total models available: {len(all_models)}")
    
    # 2. Get models by type
    small_models = ModelCatalog.get_models_by_type(ModelType.SMALL_LLM)
    print(f"\nSmall LLMs ({len(small_models)}):")
    for model_id, info in small_models.items():
        print(f"  - {info.name}: {info.performance.parameters} parameters")
    
    large_models = ModelCatalog.get_models_by_type(ModelType.LARGE_LLM)
    print(f"\nLarge LLMs ({len(large_models)}):")
    for model_id, info in large_models.items():
        print(f"  - {info.name}: {info.performance.parameters} parameters")
    
    # 3. Get models by category
    code_models = ModelCatalog.get_models_by_category(ModelCategory.CODE)
    print(f"\nCode Models ({len(code_models)}):")
    for model_id, info in code_models.items():
        print(f"  - {info.name}: {info.description}")
    
    # 4. Get recommendations
    recommendation = ModelCatalog.get_recommended_model_for_task("Generate Python code for data analysis")
    if recommendation:
        print(f"\nRecommended model for coding: {recommendation.name}")
    
    # 5. Validate model selection
    validation = ModelCatalog.validate_model_selection("tiny-llama", 4.0, False)
    print(f"\nTinyLlama validation (4GB RAM, no GPU): {validation['valid']}")
    if not validation['valid']:
        print(f"Reason: {validation['reason']}")

async def main():
    """Run all examples"""
    print("Enhanced Multi-LLM Service Usage Examples")
    print("=" * 50)
    
    try:
        # Direct catalog usage (no server required)
        example_model_catalog_usage()
        
        # Server-based examples (requires running service)
        print("\n" + "=" * 50)
        print("Server-based Examples (requires running service)")
        print("=" * 50)
        
        await example_basic_usage()
        await example_performance_comparison()
        await example_task_specific_models()
        await example_resource_management()
        await example_conversation_flow()
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the service.")
        print("Make sure the Enhanced Hugging Face service is running on localhost:8007")
        print("You can start it with: python enhanced_huggingface_service.py")
    except Exception as e:
        print(f"\nError running examples: {e}")

if __name__ == "__main__":
    asyncio.run(main())
