# Local AI Services Setup for GRC Platform

This document provides complete instructions for setting up and using local AI services (Ollama and Hugging Face transformers) with the GRC Platform.

## 🚀 Quick Start

### 1. Start All Services
```bash
python start_local_ai_services.py
```

### 2. Test Services
```bash
python test_local_services.py
```

### 3. Use in Your Code
```python
from local_ai_client import chat, get_embeddings

# Chat with AI
response = chat("Hello, how are you?")
print(response.response)

# Get embeddings
embeddings = get_embeddings("Your text here")
print(embeddings.embedding)
```

## 📋 Services Overview

### 🦙 Ollama Service
- **Purpose**: Local LLM inference using downloaded models
- **URL**: http://localhost:11434
- **Default Model**: llama2 (3.8GB)
- **Features**: 
  - Full LLM capabilities
  - Multiple model support
  - High-quality responses
  - GPU acceleration (if available)

### 🤗 Hugging Face Service
- **Purpose**: Lightweight AI service with simple models
- **URL**: http://localhost:8007
- **Default Model**: simple (rule-based)
- **Features**:
  - Fast response times
  - Embedding generation
  - Lightweight operation
  - No large model downloads

## 🔧 Installation

### Ollama Installation
1. **Automatic Installation** (Windows):
   ```bash
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download from: https://ollama.ai/download
   - Install the Windows version
   - Restart your terminal/PowerShell

### Hugging Face Transformers Installation
```bash
pip install -r requirements_huggingface_local.txt
```

## 📁 File Structure

```
phase0/
├── local_ai_client.py          # Main client library
├── local_ai_config.py          # Configuration management
├── simple_huggingface_service.py # Lightweight HF service
├── local_huggingface_service.py  # Full HF service (optional)
├── start_local_ai_services.py   # Service startup script
├── test_local_services.py       # Service testing script
├── requirements_huggingface_local.txt # Dependencies
└── LOCAL_AI_SETUP_README.md    # This file
```

## 🛠️ Configuration

### Environment Variables
```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama2

# Hugging Face Configuration
HUGGINGFACE_BASE_URL=http://localhost:8007
```

### Service Configuration
Edit `local_ai_config.py` to customize:
- Service URLs
- Default models
- Timeout settings
- Model parameters

## 💻 Usage Examples

### Basic Chat
```python
from local_ai_client import chat

# Auto-select best available service
response = chat("What is machine learning?")
print(f"Response: {response.response}")
print(f"Model: {response.model_used}")
print(f"Time: {response.processing_time:.2f}s")
```

### Service-Specific Chat
```python
from local_ai_client import ai_client

# Use Ollama specifically
response = ai_client.chat_with_ollama("Explain quantum computing")
print(response.response)

# Use Hugging Face specifically
response = ai_client.chat_with_huggingface("Hello there!")
print(response.response)
```

### Embeddings
```python
from local_ai_client import get_embeddings

embeddings = get_embeddings("This is a sample text")
print(f"Dimension: {embeddings.dimension}")
print(f"Vector: {embeddings.embedding}")
```

### Health Monitoring
```python
from local_ai_client import health_check

health = health_check()
print(f"Services status: {health}")
# Output: {'ollama': True, 'huggingface': True}
```

## 🔍 API Endpoints

### Ollama API
- **Generate**: `POST http://localhost:11434/api/generate`
- **List Models**: `GET http://localhost:11434/api/tags`
- **Pull Model**: `POST http://localhost:11434/api/pull`

### Hugging Face API
- **Chat**: `POST http://localhost:8007/chat`
- **Embeddings**: `POST http://localhost:8007/embeddings`
- **Health**: `GET http://localhost:8007/health`
- **Models**: `GET http://localhost:8007/models`

## 🐛 Troubleshooting

### Common Issues

1. **Ollama not found**
   ```bash
   # Check installation
   Test-Path "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\ollama.exe"
   
   # Start manually
   & "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\ollama.exe" serve
   ```

2. **Port conflicts**
   ```bash
   # Check port usage
   netstat -an | findstr :11434  # Ollama
   netstat -an | findstr :8007   # Hugging Face
   ```

3. **Model download issues**
   ```bash
   # Pull Ollama model manually
   & "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\ollama.exe" pull llama2
   ```

4. **Service not responding**
   ```bash
   # Test connectivity
   curl http://localhost:11434/api/tags
   curl http://localhost:8007/health
   ```

### Performance Optimization

1. **GPU Acceleration** (Ollama):
   - Ensure NVIDIA drivers are installed
   - Ollama will automatically use GPU if available

2. **Memory Management**:
   - Ollama models are loaded on-demand
   - Hugging Face service uses minimal memory
   - Monitor system resources during heavy usage

3. **Response Time**:
   - Ollama: 2-10 seconds (depending on model and hardware)
   - Hugging Face: <1 second (simple responses)

## 🔄 Integration with GRC Platform

### Backend Integration
```python
# In your FastAPI backend
from local_ai_client import chat, get_embeddings

@app.post("/ai/chat")
async def ai_chat(request: ChatRequest):
    response = chat(request.message, service="auto")
    return {
        "response": response.response,
        "model": response.model_used,
        "processing_time": response.processing_time
    }

@app.post("/ai/embeddings")
async def ai_embeddings(request: EmbeddingRequest):
    embeddings = get_embeddings(request.text)
    return {
        "embedding": embeddings.embedding,
        "dimension": embeddings.dimension
    }
```

### Frontend Integration
```javascript
// In your React frontend
const sendChatMessage = async (message) => {
  const response = await fetch('/api/ai/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  return await response.json();
};

const getTextEmbeddings = async (text) => {
  const response = await fetch('/api/ai/embeddings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return await response.json();
};
```

## 📊 Monitoring and Logs

### Service Logs
- **Ollama**: Check Windows Event Viewer or start with `ollama serve` in terminal
- **Hugging Face**: Check console output when running `python simple_huggingface_service.py`

### Health Monitoring
```python
from local_ai_client import ai_client

# Check service health
health = ai_client.health_check()
print(f"Services: {health}")

# Get available models
models = ai_client.get_available_models()
print(f"Models: {models}")
```

## 🚀 Advanced Usage

### Custom Models
```python
# Pull additional Ollama models
& "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\ollama.exe" pull codellama
& "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\ollama.exe" pull mistral

# Use specific models
response = chat("Write Python code", service="ollama", model="codellama")
```

### Batch Processing
```python
from local_ai_client import ai_client

messages = ["Hello", "How are you?", "What's the weather?"]
responses = []

for message in messages:
    response = ai_client.chat(message)
    responses.append(response.response)

print(responses)
```

## 📝 Notes

- **Security**: Services run locally, no external API calls
- **Privacy**: All data stays on your machine
- **Offline**: Works without internet connection (after initial setup)
- **Cost**: Free to run (except electricity)
- **Performance**: Depends on your hardware specifications

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Run the test script: `python test_local_services.py`
3. Check service health: `python local_ai_client.py`
4. Review logs and console output

---

**Happy AI-ing! 🤖✨**



