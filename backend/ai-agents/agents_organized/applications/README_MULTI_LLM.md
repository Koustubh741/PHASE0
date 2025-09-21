# Enhanced Multi-LLM Service for GRC Platform

## Overview

The Enhanced Multi-LLM Service provides a comprehensive solution for managing multiple Large Language Models (LLMs) and Small Language Models (SLMs) in your GRC platform. Users can dynamically select models based on their specific needs, with automatic model selection, resource management, and performance analytics.

## Features

### 🚀 **Multi-Model Support**
- **Small LLMs**: Fast, lightweight models for quick responses (TinyLlama, Phi-2, Gemma)
- **Large LLMs**: High-quality models for complex tasks (Llama 2, Mistral)
- **Specialized Models**: Task-specific models (Code Llama for programming)
- **Embedding Models**: Multiple embedding options for semantic search

### 🎯 **Smart Model Selection**
- **Automatic Selection**: AI-powered model recommendation based on task description
- **Manual Selection**: Users can specify exact models for their needs
- **Performance-Based**: Selection considers speed, quality, and resource requirements
- **Context-Aware**: Recommendations adapt to conversation context

### 📊 **Resource Management**
- **Dynamic Loading**: Models load/unload based on usage patterns
- **Memory Optimization**: Automatic cleanup of inactive models
- **GPU Support**: Intelligent GPU utilization when available
- **Resource Monitoring**: Real-time system resource tracking

### 📈 **Analytics & Insights**
- **Usage Tracking**: Detailed metrics for each model
- **Performance Analytics**: Speed, quality, and efficiency measurements
- **Comparative Analysis**: Side-by-side model performance comparison
- **Health Monitoring**: System health scoring and recommendations

## Quick Start

### 1. Installation

```bash
# Install required dependencies
pip install -r requirements_huggingface_local.txt

# Additional dependencies for enhanced service
pip install psutil fastapi uvicorn
```

### 2. Start the Service

```bash
# Start the enhanced service
python enhanced_huggingface_service.py

# Service will be available at http://localhost:8007
```

### 3. Basic Usage

```python
from usage_examples import MultiLLMClient

# Initialize client
client = MultiLLMClient("http://localhost:8007")

# Get model recommendations
recommendations = client.get_model_recommendations(
    "I need to generate Python code for data analysis"
)

# Chat with automatic model selection
response = client.chat(
    "Write a function to calculate the mean of a list",
    auto_select=True
)

print(f"Model used: {response['model_used']}")
print(f"Response: {response['response']}")
```

## Model Catalog

### Small LLMs (Fast & Efficient)

| Model | Parameters | Memory | Speed | Quality | Best For |
|-------|------------|---------|-------|---------|----------|
| **TinyLlama** | 1.1B | ~2GB | 9.5/10 | 6.5/10 | Quick responses, real-time chat |
| **Phi-2** | 2.7B | ~6GB | 8.0/10 | 8.5/10 | Balanced performance, code generation |
| **Gemma 2B** | 2B | ~4GB | 8.5/10 | 7.5/10 | Instruction following, dialogue |

### Large LLMs (High Quality)

| Model | Parameters | Memory | Speed | Quality | Best For |
|-------|------------|---------|-------|---------|----------|
| **Llama 2 7B** | 7B | ~14GB | 6.0/10 | 9.0/10 | Complex reasoning, professional writing |
| **Mistral 7B** | 7B | ~16GB | 7.0/10 | 8.8/10 | Long context, complex instructions |

### Specialized Models

| Model | Parameters | Memory | Speed | Quality | Best For |
|-------|------------|---------|-------|---------|----------|
| **Code Llama 7B** | 7B | ~14GB | 6.5/10 | 9.2/10 | Code generation, programming tasks |

### Embedding Models

| Model | Parameters | Memory | Speed | Quality | Best For |
|-------|------------|---------|-------|---------|----------|
| **All-MiniLM** | 22M | ~200MB | 9.5/10 | 8.0/10 | Fast embeddings, search |
| **All-MPNet** | 109M | ~500MB | 7.0/10 | 9.0/10 | High-quality embeddings |

## API Reference

### Core Endpoints

#### `GET /models`
List available models with filtering options.

```python
# Get all models
models = client.get_available_models()

# Filter by type
small_models = client.get_available_models(model_type="small_llm")

# Filter by category
code_models = client.get_available_models(category="code")
```

#### `POST /models/recommend`
Get model recommendations based on task description.

```python
recommendations = client.get_model_recommendations(
    task_description="I need to write Python code",
    preferred_speed="fast"
)
```

#### `POST /chat`
Generate chat responses with model selection.

```python
response = client.chat(
    message="Explain machine learning",
    model_id="phi-2",  # Optional: specify model
    auto_select=True,  # Optional: automatic selection
    max_length=200,
    temperature=0.7
)
```

#### `POST /embeddings`
Generate embeddings for text.

```python
embeddings = client.generate_embeddings(
    text="Sample text for embedding",
    model_id="all-minilm",  # Optional: specify model
    auto_select=True
)
```

#### `GET /system/status`
Get comprehensive system status and resource usage.

```python
status = client.get_system_status()
print(f"Loaded models: {len(status['loaded_models'])}")
print(f"Available memory: {status['system_resources']['available_memory_gb']} GB")
```

### Model Management

#### `POST /models/{model_id}/load`
Load a specific model.

```python
result = client.load_model("phi-2")
```

#### `DELETE /models/{model_id}`
Unload a specific model.

```python
result = client.unload_model("phi-2")
```

## Usage Patterns

### 1. Automatic Model Selection

```python
# Let the system choose the best model
response = client.chat(
    "What is the capital of France?",
    auto_select=True
)
```

### 2. Task-Specific Selection

```python
# Get recommendations for specific tasks
recommendations = client.get_model_recommendations(
    "Generate Python code for data analysis",
    preferred_speed="balanced"
)

# Use the recommended model
response = client.chat(
    "Write a function to calculate standard deviation",
    model_id=recommendations['primary_recommendation']['model_id']
)
```

### 3. Performance Comparison

```python
# Test multiple models with the same question
question = "Explain quantum computing"
models = ["tiny-llama", "phi-2", "gemma-2b"]

results = {}
for model in models:
    response = client.chat(question, model_id=model)
    results[model] = {
        "time": response['processing_time'],
        "tokens": response['tokens_generated']
    }
```

### 4. Conversation with Context

```python
conversation_history = []

# First message
response1 = client.chat(
    "Hello, I need help with software architecture",
    conversation_history=conversation_history
)
conversation_history.extend([
    {"role": "user", "content": "Hello, I need help with software architecture"},
    {"role": "assistant", "content": response1['response']}
])

# Follow-up with context
response2 = client.chat(
    "What are the main considerations for microservices?",
    conversation_history=conversation_history
)
```

## Configuration

### Environment Variables

```bash
# GPU Configuration
ENABLE_GPU=true  # Enable GPU acceleration

# Resource Management
MAX_CONCURRENT_MODELS=3  # Maximum models loaded simultaneously
AUTO_UNLOAD_INACTIVE_MODELS=true  # Auto-unload unused models
INACTIVE_THRESHOLD_MINUTES=30  # Minutes before auto-unload

# Service Configuration
PORT=8007  # Service port
```

### Model Selection Criteria

The system uses the following criteria for automatic model selection:

1. **Task Type Analysis**: Keywords in the request determine model type
2. **Resource Availability**: Memory and GPU requirements
3. **Performance Preferences**: Speed vs. quality trade-offs
4. **Usage Patterns**: Historical performance data
5. **System Load**: Current resource utilization

## Best Practices

### 1. Model Selection Strategy

- **Quick Responses**: Use TinyLlama or Gemma 2B
- **Balanced Performance**: Use Phi-2
- **High Quality**: Use Llama 2 or Mistral
- **Code Generation**: Use Code Llama
- **Embeddings**: Use All-MiniLM for speed, All-MPNet for quality

### 2. Resource Management

- Monitor system resources regularly
- Use automatic model selection to optimize resource usage
- Unload unused models to free memory
- Consider your hardware limitations when choosing models

### 3. Performance Optimization

- Use conversation history for context-aware responses
- Batch similar requests to improve efficiency
- Monitor analytics to identify performance bottlenecks
- Consider model-specific optimizations

### 4. Error Handling

```python
try:
    response = client.chat("Your message here")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 503:
        print("No models available, try loading a model first")
    elif e.response.status_code == 400:
        print("Invalid request format")
    else:
        print(f"Server error: {e}")
```

## Troubleshooting

### Common Issues

1. **"No models available"**
   - Check if models are loaded: `GET /system/status`
   - Load a model: `POST /models/{model_id}/load`

2. **"Insufficient memory"**
   - Check available memory: `GET /system/status`
   - Unload unused models: `DELETE /models/{model_id}`
   - Use smaller models

3. **"Model not found"**
   - Check available models: `GET /models`
   - Verify model ID spelling
   - Ensure model is in the catalog

4. **Slow responses**
   - Check system resources
   - Use faster models (TinyLlama, Gemma 2B)
   - Reduce max_length parameter

### Performance Monitoring

```python
# Check system health
status = client.get_system_status()
health_score = status['system_resources']['memory_usage_percent']

if health_score > 80:
    print("Warning: High memory usage detected")
```

## Advanced Features

### Custom Model Integration

To add custom models to the catalog:

1. Edit `model_catalog.py`
2. Add your model to the `get_available_models()` method
3. Define performance characteristics
4. Restart the service

### Analytics Integration

```python
from model_analytics import analytics

# Record usage
analytics.record_usage(ModelUsageRecord(
    timestamp=time.time(),
    model_id="phi-2",
    task_type="chat",
    processing_time=1.5,
    input_length=50,
    output_length=100,
    tokens_generated=100,
    success=True
))

# Get metrics
metrics = analytics.get_model_metrics("phi-2", time_window_hours=24)
```

## Examples

See `usage_examples.py` for comprehensive examples including:

- Basic usage patterns
- Performance comparison
- Task-specific model selection
- Resource management
- Conversation flows
- Analytics usage

Run examples:
```bash
python usage_examples.py
```

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the API documentation
3. Examine the usage examples
4. Check system logs for detailed error messages

## License

This enhanced multi-LLM service is part of the GRC Platform and follows the same licensing terms.
