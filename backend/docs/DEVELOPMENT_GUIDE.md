# GRC Platform Development Guide

## Overview

This guide provides comprehensive instructions for setting up, developing, and contributing to the GRC Platform.

## Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher (for frontend development)
- **PostgreSQL**: 12 or higher
- **Redis**: 6 or higher
- **Docker**: 20 or higher (optional)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/grc-platform.git
cd grc-platform
```

### 2. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install frontend dependencies
cd frontend
npm install
```

### 4. Set Up Database

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run database migrations
alembic upgrade head

# Seed test data
python scripts/seed_data.py
```

### 5. Start Development Servers

```bash
# Start backend services
python scripts/start_services.py

# Start frontend (in another terminal)
cd frontend
npm start
```

## Project Structure

```
grc-platform/
├── backend/                    # Backend services
│   ├── src/                   # Source code
│   │   ├── core/              # Business logic
│   │   │   ├── domain/        # Domain models
│   │   │   ├── application/   # Application services
│   │   │   └── infrastructure/ # Infrastructure layer
│   │   ├── shared/           # Shared components
│   │   ├── api/              # API layer
│   │   └── tests/            # Test suite
│   ├── ai-agents/            # AI agents
│   ├── deployment/           # Deployment configs
│   └── docs/                 # Documentation
├── frontend/                  # React frontend
├── shared/                    # Shared resources
├── infrastructure/           # Infrastructure configs
└── scripts/                  # Utility scripts
```

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... implement feature ...

# Run tests
pytest

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/new-feature
```

### 2. Code Quality

#### Linting

```bash
# Python linting
flake8 src/
black src/
mypy src/

# Frontend linting
cd frontend
npm run lint
npm run lint:fix
```

#### Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=src --cov-report=html
```

### 3. Database Management

#### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

#### Seeding Data

```bash
# Seed development data
python scripts/seed_data.py --env=development

# Seed test data
python scripts/seed_data.py --env=test
```

## API Development

### 1. Creating New Endpoints

```python
# backend/src/api/v1/endpoints/policy_endpoints.py
from fastapi import APIRouter, Depends
from ..schemas.policy_schemas import PolicyCreate, PolicyResponse
from ...core.application.services.policy_service import PolicyService

router = APIRouter(prefix="/policies", tags=["policies"])

@router.post("/", response_model=PolicyResponse)
async def create_policy(
    policy_data: PolicyCreate,
    service: PolicyService = Depends(get_policy_service)
):
    """Create a new policy."""
    return await service.create_policy(policy_data)
```

### 2. Creating Schemas

```python
# backend/src/api/v1/schemas/policy_schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PolicyCreate(BaseModel):
    title: str
    content: str
    category: str
    status: str = "active"

class PolicyResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### 3. Creating Services

```python
# backend/src/core/application/services/policy_service.py
from typing import List
from ..domain.repositories.policy_repository import PolicyRepository
from ..domain.entities.policy_entity import Policy

class PolicyService:
    def __init__(self, repository: PolicyRepository):
        self.repository = repository
    
    async def create_policy(self, policy_data: dict) -> Policy:
        """Create a new policy."""
        policy = Policy(**policy_data)
        return await self.repository.save(policy)
    
    async def get_policy(self, policy_id: str) -> Policy:
        """Get a policy by ID."""
        return await self.repository.get_by_id(policy_id)
```

## AI Agents Development

### 1. Creating New Agents

```python
# backend/ai-agents/src/agents/new_agent.py
from ..core.base_agent import BaseAgent
from typing import Dict, Any

class NewAgent(BaseAgent):
    """New specialized agent."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "new_agent"
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data using the agent."""
        # Implement agent logic
        result = self.analyze_data(data)
        return result
    
    def analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data using agent-specific logic."""
        # Implement analysis logic
        return {"status": "analyzed", "confidence": 0.95}
```

### 2. Agent Orchestration

```python
# backend/ai-agents/src/orchestration/agent_orchestrator.py
from typing import List, Dict, Any
from ..agents.base_agent import BaseAgent

class AgentOrchestrator:
    """Orchestrates multiple AI agents."""
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
    
    async def process_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data through multiple agents."""
        results = {}
        
        for agent in self.agents:
            result = await agent.process(data)
            results[agent.agent_type] = result
        
        return self.aggregate_results(results)
```

## Testing

### 1. Unit Tests

```python
# backend/src/tests/unit/test_policy_service.py
import pytest
from unittest.mock import Mock
from ...core.application.services.policy_service import PolicyService

class TestPolicyService:
    def test_create_policy(self):
        """Test policy creation."""
        mock_repository = Mock()
        service = PolicyService(mock_repository)
        
        policy_data = {
            "title": "Test Policy",
            "content": "Test content",
            "category": "security"
        }
        
        result = service.create_policy(policy_data)
        
        assert result.title == "Test Policy"
        mock_repository.save.assert_called_once()
```

### 2. Integration Tests

```python
# backend/src/tests/integration/test_policy_api.py
import pytest
from fastapi.testclient import TestClient
from ...api.main import app

client = TestClient(app)

def test_create_policy():
    """Test policy creation via API."""
    response = client.post(
        "/api/v1/policies/",
        json={
            "title": "Test Policy",
            "content": "Test content",
            "category": "security"
        }
    )
    
    assert response.status_code == 201
    assert response.json()["title"] == "Test Policy"
```

### 3. End-to-End Tests

```python
# backend/src/tests/e2e/test_complete_workflow.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestCompleteWorkflow:
    def test_policy_creation_workflow(self):
        """Test complete policy creation workflow."""
        driver = webdriver.Chrome()
        
        try:
            # Navigate to policy creation page
            driver.get("http://localhost:3000/policies/new")
            
            # Fill form
            driver.find_element(By.ID, "title").send_keys("Test Policy")
            driver.find_element(By.ID, "content").send_keys("Test content")
            driver.find_element(By.ID, "category").send_keys("security")
            
            # Submit form
            driver.find_element(By.ID, "submit").click()
            
            # Verify success
            assert "Policy created successfully" in driver.page_source
            
        finally:
            driver.quit()
```

## Deployment

### 1. Docker Development

```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.dev.yml up --build

# Run specific services
docker-compose up postgres redis backend
```

### 2. Production Deployment

```bash
# Build production images
docker build -t grc-platform-backend ./backend
docker build -t grc-platform-frontend ./frontend

# Deploy with Kubernetes
kubectl apply -f deployment/kubernetes/
```

## Debugging

### 1. Backend Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debugger
import pdb; pdb.set_trace()

# Use IDE debugger
# Set breakpoints in your IDE
```

### 2. Frontend Debugging

```javascript
// Add console logging
console.log('Debug info:', data);

// Use browser dev tools
// Set breakpoints in browser dev tools
```

### 3. Database Debugging

```bash
# Connect to database
psql -h localhost -U grc_user -d grc_platform

# Check logs
docker logs grc-platform-postgres
```

## Performance Optimization

### 1. Backend Optimization

```python
# Use async/await for I/O operations
async def get_policies():
    return await repository.get_all()

# Use connection pooling
from sqlalchemy.pool import QueuePool

# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_policy_template(template_id):
    return repository.get_template(template_id)
```

### 2. Frontend Optimization

```javascript
// Use React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{data}</div>;
});

// Use lazy loading
const LazyComponent = React.lazy(() => import('./LazyComponent'));

// Optimize bundle size
// Use dynamic imports
const module = await import('./module');
```

## Contributing

### 1. Code Style

- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write comprehensive docstrings
- Use meaningful variable names

### 2. Commit Messages

```
feat: add new feature
fix: fix bug
docs: update documentation
style: formatting changes
refactor: code refactoring
test: add tests
chore: maintenance tasks
```

### 3. Pull Request Process

1. Create feature branch
2. Make changes
3. Add tests
4. Update documentation
5. Create pull request
6. Address review feedback
7. Merge when approved

## Troubleshooting

### Common Issues

1. **Import Errors**: Check Python path and virtual environment
2. **Database Connection**: Verify PostgreSQL is running and accessible
3. **Redis Connection**: Check Redis server status
4. **Port Conflicts**: Ensure ports 8000-8005 are available

### Getting Help

- **Documentation**: Check this guide and API docs
- **Issues**: Create GitHub issue with detailed description
- **Discussions**: Use GitHub discussions for questions
- **Slack**: Join our development Slack channel
