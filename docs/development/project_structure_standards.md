# GRC Platform - Project Structure Standards

## 📁 Directory Structure

```
PHASE0/
├── 📁 ai-agents/                    # AI Agents Implementation
│   ├── 📁 agents_organized/         # Organized Agent Structure
│   │   ├── 📁 bfsi_agent/          # Banking & Financial Services
│   │   ├── 📁 telecom_agent/       # Telecommunications
│   │   ├── 📁 manufacturing_agent/ # Manufacturing
│   │   ├── 📁 healthcare_agent/    # Healthcare
│   │   ├── 📁 compliance_agent/    # Compliance Management
│   │   ├── 📁 risk_agent/          # Risk Management
│   │   ├── 📁 document_agent/      # Document Processing
│   │   ├── 📁 communication_agent/ # Communication Management
│   │   ├── 📁 orchestration/       # Multi-Agent Orchestration
│   │   ├── 📁 shared_components/   # Shared Components
│   │   └── 📁 utilities/           # Utility Functions
│   └── 📁 vector-db/               # Vector Database
├── 📁 backend/                      # Backend Services
│   ├── 📁 api-gateway/             # API Gateway Service
│   └── 📁 services/                # Microservices
├── 📁 frontend/                     # React Frontend
├── 📁 database/                     # Database Scripts
├── 📁 docker/                       # Docker Configuration
│   ├── 📁 compose/                 # Docker Compose Files
│   ├── 📁 services/                # Service Dockerfiles
│   └── 📁 ai-agents/               # AI Agents Docker
├── 📁 infrastructure/               # Infrastructure Config
│   └── 📁 nginx/                   # Nginx Configuration
├── 📁 scripts/                      # Utility Scripts
└── 📁 docs/                         # Documentation
```

## 🚀 Service Startup Standards

### 1. Service Manager Scripts

#### Python Service Manager (`start_services_structured.py`)
- **Purpose**: Cross-platform service management
- **Features**: 
  - Health checks
  - Process monitoring
  - Graceful shutdown
  - Logging
- **Usage**: `python start_services_structured.py [start|stop|status|restart] [--service SERVICE_NAME]`

#### PowerShell Service Manager (`start_services_structured.ps1`)
- **Purpose**: Windows-native service management
- **Features**:
  - PowerShell-native process management
  - Windows service integration
  - Detailed logging
- **Usage**: `.\start_services_structured.ps1 -Action [start|stop|status|restart] [-Service SERVICE_NAME]`

#### Batch Wrapper (`start_services_structured.bat`)
- **Purpose**: Simple Windows batch interface
- **Features**:
  - PowerShell script wrapper
  - Command line argument parsing
  - Error handling
- **Usage**: `start_services_structured.bat [start|stop|status|restart] [--service SERVICE_NAME]`

### 2. Service Configuration

#### Service Definitions
```python
service_configs = {
    'postgres': {
        'command': ['docker', 'run', '-d', '--name', 'grc-postgres', 
                   '-p', '5432:5432', '-e', 'POSTGRES_PASSWORD=password',
                   'postgres:15-alpine'],
        'health_check': 'docker ps --filter name=grc-postgres --filter status=running',
        'port': 5432
    },
    'api-gateway': {
        'command': ['python', 'main.py'],
        'working_dir': 'backend/api-gateway',
        'port': 8000,
        'health_check': 'curl -f http://localhost:8000/health'
    }
    # ... other services
}
```

#### Startup Order
1. **Database Services**: PostgreSQL, Redis
2. **Backend Services**: API Gateway, AI Agents Service
3. **Frontend Services**: React Application

### 3. Health Check Standards

#### Database Health Checks
```bash
# PostgreSQL
docker ps --filter name=grc-postgres --filter status=running

# Redis
docker ps --filter name=grc-redis --filter status=running
```

#### API Health Checks
```bash
# API Gateway
curl -f http://localhost:8000/health

# AI Agents Service
curl -f http://localhost:8005/health
```

#### Frontend Health Checks
```bash
# React Frontend
curl -f http://localhost:3000
```

## 📋 Service Management Commands

### Start All Services
```bash
# Python
python start_services_structured.py start

# PowerShell
.\start_services_structured.ps1 -Action start

# Batch
start_services_structured.bat start
```

### Start Specific Service
```bash
# Python
python start_services_structured.py start --service api-gateway

# PowerShell
.\start_services_structured.ps1 -Action start -Service api-gateway

# Batch
start_services_structured.bat start --service api-gateway
```

### Check Service Status
```bash
# Python
python start_services_structured.py status

# PowerShell
.\start_services_structured.ps1 -Action status

# Batch
start_services_structured.bat status
```

### Stop All Services
```bash
# Python
python start_services_structured.py stop

# PowerShell
.\start_services_structured.ps1 -Action stop

# Batch
start_services_structured.bat stop
```

### Restart All Services
```bash
# Python
python start_services_structured.py restart

# PowerShell
.\start_services_structured.ps1 -Action restart

# Batch
start_services_structured.bat restart
```

## 🔧 Development Standards

### 1. File Naming Conventions
- **Python Files**: `snake_case.py`
- **Configuration Files**: `kebab-case.yml`, `kebab-case.json`
- **Documentation**: `UPPER_CASE.md`
- **Scripts**: `descriptive_name.py`, `descriptive_name.ps1`

### 2. Directory Naming Conventions
- **Main Directories**: `kebab-case`
- **Subdirectories**: `snake_case`
- **Service Directories**: `service-name`

### 3. Import Standards
```python
# Standard library imports
import os
import sys
import logging

# Third-party imports
import fastapi
import uvicorn

# Local imports
from shared_components.industry_agent import IndustryAgent
from .subagents import SubAgentOrchestrator
```

### 4. Logging Standards
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Usage
logger.info("Service started successfully")
logger.error("Service failed to start")
```

## 🐳 Docker Standards

### 1. Docker Compose Structure
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 2. Dockerfile Standards
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["python", "main.py"]
```

## 📊 Monitoring Standards

### 1. Health Check Endpoints
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "redis": "connected",
            "ai_agents": "ready"
        }
    }
```

### 2. Status Monitoring
```python
def get_service_status():
    return {
        "postgres": {"running": True, "healthy": True, "port": 5432},
        "redis": {"running": True, "healthy": True, "port": 6379},
        "api-gateway": {"running": True, "healthy": True, "port": 8000},
        "ai-agents": {"running": True, "healthy": True, "port": 8005},
        "frontend": {"running": True, "healthy": True, "port": 3000}
    }
```

## 🚨 Error Handling Standards

### 1. Service Startup Errors
```python
try:
    process = subprocess.Popen(command, cwd=working_dir)
    logger.info(f"Service started with PID {process.pid}")
except Exception as e:
    logger.error(f"Failed to start service: {e}")
    return False
```

### 2. Health Check Failures
```python
def check_service_health(service_name):
    try:
        result = subprocess.run(health_check, timeout=10)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.warning(f"Health check timeout for {service_name}")
        return False
    except Exception as e:
        logger.error(f"Health check failed for {service_name}: {e}")
        return False
```

## 📝 Documentation Standards

### 1. README Files
- **Project README**: Overview, setup, usage
- **Service README**: Service-specific documentation
- **API README**: API documentation and examples

### 2. Code Documentation
```python
def start_service(service_name: str) -> bool:
    """
    Start a specific service.
    
    Args:
        service_name: Name of the service to start
        
    Returns:
        bool: True if service started successfully, False otherwise
        
    Raises:
        ValueError: If service_name is not recognized
        RuntimeError: If service fails to start
    """
```

This structure ensures:
- ✅ **Consistency** across all services
- ✅ **Maintainability** with clear organization
- ✅ **Scalability** for future additions
- ✅ **Reliability** with proper error handling
- ✅ **Monitoring** with health checks
- ✅ **Documentation** for all components
