# 🐳 Docker Organization - GRC Platform

## Overview
This directory contains all Docker-related files organized according to the GRC Platform system architecture. All containers, services, and orchestration files are centralized here for easy management and deployment.

## 📁 Directory Structure

```
docker/
├── README.md                    # This overview document
├── compose/                     # Docker Compose files
│   ├── docker-compose.yml      # Main production compose
│   ├── docker-compose.dev.yml  # Development environment
│   ├── docker-compose.fullstack.yml # Full stack deployment
│   ├── docker-compose.enhanced.yml # Enhanced with AI agents
│   └── docker-compose.industry-enhanced.yml # Industry-specific enhanced
├── services/                    # Service-specific Dockerfiles
│   ├── api-gateway.Dockerfile  # API Gateway service
│   ├── frontend.Dockerfile     # Frontend React application
│   ├── Dockerfile.compliance   # Compliance service
│   ├── Dockerfile.policy       # Policy service
│   ├── Dockerfile.risk         # Risk service
│   └── Dockerfile.workflow     # Workflow service
└── ai-agents/                   # AI Agents Docker files
    ├── Dockerfile              # Standard AI agents
    ├── Dockerfile.enhanced     # Enhanced AI agents
    ├── requirements.txt        # Python dependencies
    └── env.example            # Environment variables template
```

## 🚀 Deployment Options

### Development Environment
```bash
# Start development environment
docker-compose -f docker/compose/docker-compose.dev.yml up -d

# Stop development environment
docker-compose -f docker/compose/docker-compose.dev.yml down
```

### Production Environment
```bash
# Start production environment
docker-compose -f docker/compose/docker-compose.yml up -d

# Stop production environment
docker-compose -f docker/compose/docker-compose.yml down
```

### Full Stack Deployment
```bash
# Start full stack (Frontend + Backend + AI Agents)
docker-compose -f docker/compose/docker-compose.fullstack.yml up -d

# Stop full stack
docker-compose -f docker/compose/docker-compose.fullstack.yml down
```

### Enhanced AI Agents
```bash
# Start with enhanced AI agents (Ollama + Chroma)
docker-compose -f docker/compose/docker-compose.enhanced.yml up -d

# Stop enhanced environment
docker-compose -f docker/compose/docker-compose.enhanced.yml down
```

## 🏗️ Architecture Alignment

### System Architecture Components
- **Frontend Layer**: React.js application (Port 3000)
- **API Gateway**: FastAPI gateway (Port 8000)
- **Backend Services**: Microservices (Ports 8001-8005)
- **AI Agents Layer**: Multi-agent system (Ports 8006-8010)
- **Infrastructure Layer**: PostgreSQL, Redis, Ollama, Chroma

### Container Architecture
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           GRC PLATFORM CONTAINERS                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   FRONTEND      │  │   API GATEWAY   │  │   BACKEND       │  │   AI AGENTS │ │
│  │   (React)       │  │   (FastAPI)     │  │   SERVICES      │  │   (Python)  │ │
│  │   Port: 3000    │  │   Port: 8000    │  │   Port: 8001-5  │  │   Port: 8006│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                       │                       │               │     │
│           │                       │                       │               │     │
│           ▼                       ▼                       ▼               ▼     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        INFRASTRUCTURE LAYER                                │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │  │   POSTGRESQL    │  │     REDIS       │  │     OLLAMA      │             │ │
│  │  │   Port: 5432    │  │   Port: 6379    │  │   Port: 11434   │             │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │  │     CHROMA      │  │   MONITORING    │  │   VOLUMES       │             │ │
│  │  │   Port: 8001    │  │   Port: 9090    │  │   (Persistent)  │             │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Service Configuration

### API Gateway Service
- **Image**: Custom FastAPI application
- **Port**: 8000
- **Dependencies**: PostgreSQL, Redis
- **Health Check**: `/health` endpoint

### Frontend Service
- **Image**: React.js application
- **Port**: 3000
- **Build**: Multi-stage build with Nginx
- **Static Files**: Served via Nginx

### Backend Services
- **Compliance Service**: Port 8001
- **Policy Service**: Port 8002
- **Risk Service**: Port 8003
- **Workflow Service**: Port 8004
- **Mock Data Service**: Port 8005

### AI Agents Service
- **Standard Agents**: Port 8006
- **Enhanced Agents**: Port 8007 (with Ollama/Chroma)
- **Orchestration**: Port 8008
- **Communication**: Port 8009

### Infrastructure Services
- **PostgreSQL**: Port 5432
- **Redis**: Port 6379
- **Ollama**: Port 11434
- **Chroma**: Port 8001
- **Monitoring**: Port 9090

## 📊 Environment Variables

### Common Variables
```bash
# Database
POSTGRES_DB=grc_platform
POSTGRES_USER=grc_user
POSTGRES_PASSWORD=grc_password

# Redis
REDIS_URL=redis://redis:6379

# API Gateway
API_GATEWAY_PORT=8000
API_GATEWAY_HOST=0.0.0.0

# AI Agents
OLLAMA_URL=http://ollama:11434
CHROMA_URL=http://chroma:8001
```

### Service-Specific Variables
```bash
# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws

# Backend Services
COMPLIANCE_SERVICE_PORT=8001
POLICY_SERVICE_PORT=8002
RISK_SERVICE_PORT=8003
WORKFLOW_SERVICE_PORT=8004

# AI Agents
AI_AGENTS_PORT=8006
ORCHESTRATION_PORT=8008
COMMUNICATION_PORT=8009
```

## 🚀 Quick Start

### 1. Development Setup
```bash
# Clone repository and navigate to docker directory
cd docker

# Start development environment
docker-compose -f compose/docker-compose.dev.yml up -d

# Check service status
docker-compose -f compose/docker-compose.dev.yml ps

# View logs
docker-compose -f compose/docker-compose.dev.yml logs -f
```

### 2. Production Setup
```bash
# Start production environment
docker-compose -f compose/docker-compose.yml up -d

# Scale services if needed
docker-compose -f compose/docker-compose.yml up -d --scale api-gateway=3
```

### 3. Full Stack with AI Agents
```bash
# Start complete stack with enhanced AI agents
docker-compose -f compose/docker-compose.enhanced.yml up -d

# Access services
# Frontend: http://localhost:3000
# API Gateway: http://localhost:8000
# AI Agents: http://localhost:8006
```

## 🔍 Monitoring and Maintenance

### Health Checks
```bash
# Check all services health
docker-compose -f compose/docker-compose.yml ps

# Check specific service logs
docker-compose -f compose/docker-compose.yml logs -f api-gateway

# Check resource usage
docker stats
```

### Backup and Restore
```bash
# Backup database
docker exec grc-postgres pg_dump -U grc_user grc_platform > backup.sql

# Restore database
docker exec -i grc-postgres psql -U grc_user grc_platform < backup.sql
```

### Updates and Scaling
```bash
# Update services
docker-compose -f compose/docker-compose.yml pull
docker-compose -f compose/docker-compose.yml up -d

# Scale specific services
docker-compose -f compose/docker-compose.yml up -d --scale api-gateway=3 --scale ai-agents=2
```

## 🛠️ Development

### Building Custom Images
```bash
# Build AI agents image
docker build -f ai-agents/Dockerfile.enhanced -t grc-ai-agents:latest .

# Build API gateway image
docker build -f services/api-gateway.Dockerfile -t grc-api-gateway:latest .
```

### Local Development
```bash
# Start only infrastructure services
docker-compose -f compose/docker-compose.dev.yml up -d postgres redis

# Run services locally for development
python -m uvicorn main:app --reload --port 8000
npm start  # For frontend development
```

This organized Docker structure provides a clean, maintainable, and scalable deployment solution for the GRC Platform that aligns perfectly with the system architecture.
