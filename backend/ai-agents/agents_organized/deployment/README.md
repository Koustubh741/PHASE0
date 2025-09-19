# 🐳 Deployment - Containerization & Configuration

## Overview
This directory contains deployment-related files including Docker configurations, requirements, and environment setup for the GRC Platform AI Agents.

## Files

### Docker Configuration
- **`Dockerfile`**: Standard Docker configuration for the AI agents
- **`Dockerfile.enhanced`**: Enhanced Docker configuration with optimizations

### Dependencies
- **`requirements.txt`**: Python package dependencies
- **`env.example`**: Environment variables template

## Deployment Options

### Standard Deployment
```bash
# Build standard image
docker build -f deployment/Dockerfile -t grc-ai-agents .

# Run standard container
docker run -p 8000:8000 grc-ai-agents
```

### Enhanced Deployment
```bash
# Build enhanced image
docker build -f deployment/Dockerfile.enhanced -t grc-ai-agents-enhanced .

# Run enhanced container
docker run -p 8000:8000 grc-ai-agents-enhanced
```

### Environment Setup
```bash
# Copy environment template
cp deployment/env.example .env

# Edit environment variables
nano .env

# Install dependencies
pip install -r deployment/requirements.txt
```

## Key Features

### Docker Configurations
- **Multi-stage Builds**: Optimized image sizes
- **Security Hardening**: Non-root user execution
- **Health Checks**: Container health monitoring
- **Volume Mounts**: Persistent data storage

### Dependencies
- **Core Dependencies**: Essential Python packages
- **AI/ML Libraries**: Ollama, Chroma, OpenAI integration
- **Web Frameworks**: FastAPI, Uvicorn
- **Database Drivers**: PostgreSQL, Redis connectors

### Environment Configuration
- **Database Settings**: Connection strings and credentials
- **AI Service Settings**: API keys and endpoints
- **Logging Configuration**: Log levels and outputs
- **Performance Tuning**: Optimization parameters

## Production Deployment

### Docker Compose
```yaml
version: '3.8'
services:
  grc-ai-agents:
    build:
      context: .
      dockerfile: deployment/Dockerfile.enhanced
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/grc
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grc-ai-agents
spec:
  replicas: 3
  selector:
    matchLabels:
      app: grc-ai-agents
  template:
    metadata:
      labels:
        app: grc-ai-agents
    spec:
      containers:
      - name: grc-ai-agents
        image: grc-ai-agents:latest
        ports:
        - containerPort: 8000
```

## Monitoring & Maintenance

### Health Checks
- **Container Health**: Docker health check endpoints
- **Application Health**: API health endpoints
- **Dependency Health**: Database and service connectivity

### Logging
- **Structured Logging**: JSON-formatted logs
- **Log Levels**: Configurable verbosity
- **Log Rotation**: Automatic log management

### Updates
- **Rolling Updates**: Zero-downtime deployments
- **Version Management**: Semantic versioning
- **Rollback Capability**: Quick rollback procedures
