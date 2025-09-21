# Quick Start - Enhanced Multi-LLM Service

## ✅ What's Been Updated

### 1. **Enhanced Service Created**
- `enhanced_huggingface_service.py` - Multi-LLM service with 8 models
- `model_catalog.py` - Centralized model definitions
- `model_analytics.py` - Performance tracking

### 2. **API Compatibility Ensured**
- Updated `huggingface_client.py` to support both original and enhanced APIs
- Created `compatibility_layer.py` for backward compatibility
- Updated `bfsi_llm_integrated_agent.py` to use enhanced features

### 3. **Requirements Updated**
- `requirements_huggingface_local.txt` - Added all necessary dependencies

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_huggingface_local.txt
```

### 2. Start Enhanced Service
```bash
# Option 1: Use the startup script
python start_enhanced_service.py

# Option 2: Direct start
python enhanced_huggingface_service.py
```

### 3. Test API Calls
```bash
# Test all endpoints
python test_api_compatibility.py
```

## 📋 Available Models

| Model | Type | Size | Speed | Quality | Best For |
|-------|------|------|-------|---------|----------|
| **tiny-llama** | Small | 1.1B | 9.5/10 | 6.5/10 | Quick responses |
| **phi-2** | Small | 2.7B | 8.0/10 | 8.5/10 | Balanced |
| **gemma-2b** | Small | 2B | 8.5/10 | 7.5/10 | Instructions |
| **llama2-7b** | Large | 7B | 6.0/10 | 9.0/10 | High quality |
| **mistral-7b** | Large | 7B | 7.0/10 | 8.8/10 | Long context |
| **codellama-7b** | Specialized | 7B | 6.5/10 | 9.2/10 | Code generation |
| **all-minilm** | Embedding | 22M | 9.5/10 | 8.0/10 | Fast embeddings |
| **all-mpnet** | Embedding | 109M | 7.0/10 | 9.0/10 | Quality embeddings |

## 🔧 API Usage

### Automatic Model Selection
```python
import requests

# Chat with auto-selection
response = requests.post("http://localhost:8007/chat", json={
    "message": "Write Python code for data analysis",
    "auto_model_selection": True
})

# Get recommendations
response = requests.post("http://localhost:8007/models/recommend", json={
    "task_description": "Quick Q&A",
    "preferred_speed": "fast"
})
```

### Manual Model Selection
```python
# Use specific model
response = requests.post("http://localhost:8007/chat", json={
    "message": "Explain quantum computing",
    "model_id": "phi-2"
})
```

### Original API Still Works
```python
# Original format still supported
response = requests.post("http://localhost:8007/chat", json={
    "message": "Hello",
    "model_name": "microsoft/DialoGPT-medium"
})
```

## 🎯 Key Features

1. **Multi-Model Support** - 8 different models to choose from
2. **Automatic Selection** - AI picks the best model for your task
3. **Backward Compatibility** - Original API calls still work
4. **Resource Management** - Automatic memory optimization
5. **Analytics** - Performance tracking and insights
6. **BFSI Integration** - Updated agent supports enhanced features

## 🚨 Important Notes

- **Service runs on port 8007** by default
- **Original service** (`huggingface_service.py`) still works for backward compatibility
- **Enhanced service** provides new features while maintaining compatibility
- **All existing integrations** continue to work without changes

## 📊 Performance

- **Small models** (1-3B): ~1-3 seconds response time
- **Large models** (7B): ~3-8 seconds response time  
- **Embeddings**: ~0.1-0.5 seconds
- **Auto-selection**: Adds ~0.1 seconds for model recommendation

The enhanced service is now ready to use with full backward compatibility!
