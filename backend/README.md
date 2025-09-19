# GRC Platform Backend

This is the backend services for the GRC (Governance, Risk, and Compliance) Platform, built with FastAPI and following Clean Architecture principles.

## Architecture

The backend follows Clean Architecture with Domain-Driven Design (DDD) patterns:

```
backend/
├── src/
│   └── core/
│       ├── domain/           # Business logic and entities
│       │   ├── entities/     # Domain entities
│       │   ├── value_objects/ # Value objects
│       │   └── repositories/ # Repository interfaces
│       ├── application/      # Use cases and application services
│       │   ├── use_cases/    # Business use cases
│       │   ├── services/     # Application services
│       │   └── interfaces/   # Application interfaces
│       ├── infrastructure/   # External concerns
│       │   ├── database/     # Database implementations
│       │   ├── external_services/ # External API integrations
│       │   ├── repositories/ # Repository implementations
│       │   └── config/       # Configuration management
│       └── presentation/     # API layer
│           ├── api/          # FastAPI routes and controllers
│           └── middleware/   # Custom middleware
├── ai-agents/               # AI agents and orchestration
├── deployment/              # Deployment configurations
└── tests/                   # Test suites
    ├── unit/               # Unit tests
    ├── integration/        # Integration tests
    └── e2e/               # End-to-end tests
```

## Services

### Core Services
- **API Gateway** (`src/core/presentation/api/main.py`) - Central entry point for all requests
- **Compliance Service** - Manages compliance assessments and evidence
- **Risk Service** - Handles risk identification, assessment, and treatment
- **Policy Service** - Policy management and governance
- **Workflow Service** - Business process automation

### AI Agents
- **Industry-specific Agents** - BFSI, Healthcare, Manufacturing, Telecom
- **Communication Agent** - Inter-agent communication
- **Document Agent** - Document processing and analysis
- **Orchestration Layer** - Multi-agent coordination

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd grc-platform/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or for development
   pip install -e ".[dev,testing]"
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb grc_platform
   
   # Run migrations (when available)
   alembic upgrade head
   ```

### Running the Services

#### Development Mode
```bash
# API Gateway
uvicorn src.core.presentation.api.main:app --reload --port 8000

# Individual services
uvicorn src.core.infrastructure.external_services.compliance_service:app --reload --port 8003
uvicorn src.core.infrastructure.external_services.risk_service:app --reload --port 8002
uvicorn src.core.infrastructure.external_services.policy_service:app --reload --port 8001
uvicorn src.core.infrastructure.external_services.workflow_service:app --reload --port 8004

# AI Agents
python ai-agents/agents_organized/applications/main.py
```

#### Production Mode
```bash
# Using Docker Compose
docker-compose -f deployment/docker-compose.yml up -d

# Or using individual Docker containers
docker build -t grc-backend .
docker run -p 8000:8000 grc-backend
```

## API Documentation

Once the services are running, you can access:

- **API Gateway**: http://localhost:8000/docs
- **Compliance Service**: http://localhost:8003/docs
- **Risk Service**: http://localhost:8002/docs
- **Policy Service**: http://localhost:8001/docs
- **Workflow Service**: http://localhost:8004/docs

## Testing

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/          # End-to-end tests

# Run with coverage
pytest --cov=src --cov-report=html
```

## Development

### Code Style
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pre-commit** hooks for automated checks

```bash
# Format code
black src tests

# Lint code
flake8 src tests

# Type check
mypy src

# Install pre-commit hooks
pre-commit install
```

### Adding New Features

1. **Domain Layer**: Define entities and business rules
2. **Application Layer**: Create use cases and services
3. **Infrastructure Layer**: Implement repositories and external services
4. **Presentation Layer**: Add API endpoints and controllers
5. **Tests**: Write comprehensive tests for all layers

## Configuration

Environment variables are managed through `.env` files:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/grc_platform

# Redis
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=your_openai_key
OLLAMA_BASE_URL=http://localhost:11434

# Service URLs
POLICY_SERVICE_URL=http://localhost:8001
RISK_SERVICE_URL=http://localhost:8002
COMPLIANCE_SERVICE_URL=http://localhost:8003
WORKFLOW_SERVICE_URL=http://localhost:8004
AI_AGENTS_URL=http://localhost:8005
```

## Monitoring and Logging

- **Health Checks**: `/health` endpoint on all services
- **Metrics**: Prometheus-compatible metrics
- **Logging**: Structured logging with configurable levels
- **Tracing**: Distributed tracing support (when configured)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Ensure all checks pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details.
