# Hugging Face Transformers Docker Setup

This guide explains how to set up and use Hugging Face transformers with Docker in the GRC Platform, similar to how Ollama was integrated.

## Overview

The Hugging Face transformers integration provides:
- **Local LLM capabilities** using Hugging Face models
- **Embedding generation** for semantic search and document analysis
- **Model management** with dynamic loading/unloading
- **RESTful API** for easy integration with other services
- **Docker containerization** for consistent deployment

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GRC Platform Stack                      │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React)     │  API Gateway (FastAPI)             │
├─────────────────────────────────────────────────────────────┤
│  AI Agents Service    │  Hugging Face Transformers Service │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL           │  Redis Cache    │  Chroma Vector DB │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Start the Services

```bash
# Navigate to the docker compose directory
cd docker/compose

# Start all services including Hugging Face transformers
docker-compose -f docker-compose.huggingface.yml up -d

# Check service status
docker-compose -f docker-compose.huggingface.yml ps
```

### 2. Verify Installation

```bash
# Check Hugging Face service health
curl http://localhost:8007/health

# List loaded models
curl http://localhost:8007/models

# Test chat functionality
curl -X POST http://localhost:8007/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

## Service Configuration

### Environment Variables

Copy the environment template and configure:

```bash
cp docker/env.huggingface.template .env
```

Key configuration options:

```env
# Model Configuration
DEFAULT_MODEL_NAME=microsoft/DialoGPT-medium
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_MODEL_SIZE=2GB
ENABLE_GPU=false

# Service URLs
HUGGINGFACE_SERVICE_URL=http://localhost:8007
CHROMA_HOST=chroma
CHROMA_PORT=8000
```

### Available Models

#### Chat Models
- `microsoft/DialoGPT-medium` (Default) - Conversational AI
- `distilgpt2` - Lightweight GPT-2 variant
- `gpt2` - Standard GPT-2 model
- `facebook/blenderbot-400M-distill` - Facebook's BlenderBot

#### Embedding Models
- `sentence-transformers/all-MiniLM-L6-v2` (Default) - Fast, general-purpose
- `sentence-transformers/all-mpnet-base-v2` - Higher quality, slower
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` - Multilingual

## API Endpoints

### Health Check
```http
GET /health
```

### List Models
```http
GET /models
```

### Chat Generation
```http
POST /chat
Content-Type: application/json

{
  "message": "Your message here",
  "model_name": "microsoft/DialoGPT-medium",
  "max_length": 100,
  "temperature": 0.7,
  "conversation_history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

### Generate Embeddings
```http
POST /embeddings
Content-Type: application/json

{
  "text": "Text to embed",
  "model_name": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### Model Management
```http
# Load a model
POST /models/{model_name}/load

# Unload a model
DELETE /models/{model_name}
```

## Integration with AI Agents

### Using the HuggingFaceClient

```python
from shared_components.huggingface_client import HuggingFaceClient, HuggingFaceAgent

# Initialize client
async with HuggingFaceClient() as client:
    # Generate chat response
    response = await client.chat("Hello, how are you?")
    print(response["response"])
    
    # Generate embeddings
    embeddings = await client.generate_embeddings("Document text")
    print(f"Embedding dimension: {len(embeddings['embedding'])}")

# Using the agent wrapper
agent = HuggingFaceAgent()
await agent.initialize()

result = await agent.process_message(
    "Analyze this compliance document",
    context={"document_type": "policy", "industry": "banking"}
)
print(result["response"])
```

### Integration in Existing Agents

```python
# In your agent class
from shared_components.huggingface_client import HuggingFaceAgent

class ComplianceAgent:
    def __init__(self):
        self.hf_agent = HuggingFaceAgent()
    
    async def analyze_policy(self, policy_text):
        prompt = f"Analyze this policy for compliance issues: {policy_text}"
        return await self.hf_agent.process_message(prompt)
```

## Docker Services

### Service Details

| Service | Port | Description |
|---------|------|-------------|
| `huggingface-transformers` | 8007 | Hugging Face transformers service |
| `ai-agents-hf` | 8006 | Enhanced AI agents with HF integration |
| `api-gateway` | 8000 | API gateway with HF routing |
| `frontend` | 3000 | React frontend |
| `postgres` | 5432 | PostgreSQL database |
| `redis` | 6379 | Redis cache |
| `chroma` | 8001 | Chroma vector database |

### Resource Requirements

- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2-10GB for model cache (depending on models)
- **CPU**: Multi-core recommended for better performance

## Model Management

### Loading Models

Models are loaded automatically on startup, but you can also load them dynamically:

```python
# Load a specific model
async with HuggingFaceClient() as client:
    await client.load_model("gpt2")
```

### Memory Management

To free memory, unload unused models:

```python
# Unload a model
async with HuggingFaceClient() as client:
    await client.unload_model("gpt2")
```

### Model Caching

Models are cached in the `huggingface_models` Docker volume. This persists across container restarts.

## Performance Optimization

### GPU Support

To enable GPU support (if available):

```env
ENABLE_GPU=true
CUDA_VISIBLE_DEVICES=0
```

### Model Selection

Choose models based on your needs:

- **Speed**: `distilgpt2`, `sentence-transformers/all-MiniLM-L6-v2`
- **Quality**: `gpt2`, `sentence-transformers/all-mpnet-base-v2`
- **Multilingual**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

### Batch Processing

For multiple requests, use the agent wrapper which maintains conversation history:

```python
agent = HuggingFaceAgent()
await agent.initialize()

# Process multiple messages efficiently
for message in messages:
    response = await agent.process_message(message)
    # Process response...
```

## Troubleshooting

### Common Issues

1. **Model Loading Timeout**
   ```bash
   # Increase timeout in docker-compose
   environment:
     - MODEL_LOAD_TIMEOUT=1200
   ```

2. **Out of Memory**
   ```bash
   # Reduce model size or enable model swapping
   environment:
     - MAX_MODEL_SIZE=1GB
   ```

3. **Service Not Responding**
   ```bash
   # Check logs
   docker-compose -f docker-compose.huggingface.yml logs huggingface-transformers
   ```

### Logs and Monitoring

```bash
# View service logs
docker-compose -f docker-compose.huggingface.yml logs -f huggingface-transformers

# Monitor resource usage
docker stats grc-huggingface-transformers
```

## Comparison with Ollama

| Feature | Hugging Face | Ollama |
|---------|--------------|--------|
| **Model Variety** | Extensive (100k+ models) | Curated selection |
| **Setup Complexity** | Medium | Low |
| **Memory Usage** | Variable (1-10GB) | Optimized (2-8GB) |
| **API Compatibility** | Custom REST API | OpenAI-compatible |
| **Model Management** | Dynamic loading | Pre-installed |
| **Performance** | Good | Excellent |
| **Community** | Large | Growing |

## Security Considerations

1. **Model Security**: Only use trusted models from Hugging Face Hub
2. **API Security**: Implement authentication for production use
3. **Data Privacy**: Models run locally, no data sent to external services
4. **Resource Limits**: Set appropriate memory and CPU limits

## Production Deployment

### Scaling

For production, consider:

1. **Load Balancing**: Multiple Hugging Face service instances
2. **Model Caching**: Shared model cache across instances
3. **Monitoring**: Health checks and metrics collection
4. **Backup**: Regular model cache backups

### Environment Configuration

```env
# Production settings
ENABLE_GPU=true
MAX_CONCURRENT_REQUESTS=50
REQUEST_TIMEOUT=60
LOG_LEVEL=WARNING
```

## Support and Resources

- **Hugging Face Hub**: https://huggingface.co/models
- **Transformers Documentation**: https://huggingface.co/docs/transformers
- **Model Cards**: Check individual model pages for specific requirements
- **Community**: Hugging Face Discord and forums

## Next Steps

1. **Custom Models**: Fine-tune models for your specific use case
2. **Model Optimization**: Use quantization for smaller models
3. **Integration**: Connect with existing GRC workflows
4. **Monitoring**: Set up comprehensive logging and metrics


