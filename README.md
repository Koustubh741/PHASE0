# GRC Platform

A comprehensive Governance, Risk, and Compliance (GRC) management platform built with modern microservices architecture and AI-powered agents.

## 🏗️ Architecture Overview

This is a monorepo containing both frontend and backend services, organized following modern software architecture patterns:

```
grc-platform/
├── frontend/              # React-based frontend application
├── backend/               # Python FastAPI backend services
├── config/                # Configuration files
├── deployment/            # Docker and deployment configs
├── docs/                  # Documentation
├── scripts/               # Utility scripts
│   └── starters/          # Local demo/integration launchers
└── tests/                 # Integration and E2E tests
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm 9+
- **Python** 3.11+
- **PostgreSQL** 13+
- **Redis** 6+
- **Docker** and Docker Compose (optional)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd grc-platform
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:8000/docs
   - Individual services: http://localhost:8001-8005/docs

### Option 2: Local Development

1. **Install dependencies**
   ```bash
   npm run install:all
   ```

2. **Set up databases**
   ```bash
   # PostgreSQL
   createdb grc_platform
   
   # Redis (if not using Docker)
   redis-server
   ```

3. **Start backend services**
   ```bash
   npm run start:backend
   ```

4. **Start frontend (in another terminal)**
   ```bash
   npm run start:frontend
   ```

## 📁 Project Structure

### Backend (`/backend`)
Clean Architecture with Domain-Driven Design:

- **Domain Layer** - Business entities and rules
- **Application Layer** - Use cases and services
- **Infrastructure Layer** - Database and external services
- **Presentation Layer** - API endpoints and middleware

### Frontend (`/frontend`)
Feature-based React architecture:

- **Components** - Reusable UI components
- **Features** - Business feature modules
- **Services** - API and external integrations
- **Store** - Redux state management
- **Hooks** - Custom React hooks

## 🛠️ Development

### Available Scripts

```bash
# Installation
npm run install:all          # Install all dependencies
npm run install:frontend     # Install frontend dependencies
npm run install:backend      # Install backend dependencies

# Development
npm run dev                  # Start both frontend and backend
npm run start:frontend       # Start frontend only
npm run start:backend        # Start backend only

# Building
npm run build                # Build both frontend and backend
npm run build:frontend       # Build frontend only
npm run build:backend        # Build backend only

# Testing
npm run test                 # Run all tests
npm run test:frontend        # Run frontend tests
npm run test:backend         # Run backend tests

# Linting
npm run lint                 # Lint all code
npm run lint:fix             # Fix linting issues

# Docker
npm run docker:build         # Build Docker images
npm run docker:up            # Start Docker services
npm run docker:down          # Stop Docker services
```

### Code Style

- **Frontend**: ESLint + Prettier + TypeScript
- **Backend**: Black + Flake8 + MyPy
- **Pre-commit hooks** for automated checks

## 🔧 Configuration

### Environment Variables

Create `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://grc_user:grc_password@localhost:5432/grc_platform
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

# Frontend
REACT_APP_API_BASE_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest                    # Run all tests
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only
pytest --cov=src          # With coverage
```

### Frontend Testing
```bash
cd frontend
npm test                  # Run all tests
npm run test:unit         # Unit tests only
npm run test:integration  # Integration tests only
npm run test:coverage     # With coverage
```

## 📊 Services

### Core Services
- **API Gateway** (Port 8000) - Central entry point
- **Policy Service** (Port 8001) - Policy management
- **Risk Service** (Port 8002) - Risk assessment and treatment
- **Compliance Service** (Port 8003) - Compliance monitoring
- **Workflow Service** (Port 8004) - Business process automation
- **AI Agents** (Port 8005) - AI-powered analysis

### AI Agents
- **Industry-specific Agents** - BFSI, Healthcare, Manufacturing, Telecom
- **Communication Agent** - Inter-agent coordination
- **Document Agent** - Document processing
- **Orchestration Layer** - Multi-agent management

## 🔍 API Documentation

Once services are running, access API documentation:

- **API Gateway**: http://localhost:8000/docs
- **Policy Service**: http://localhost:8001/docs
- **Risk Service**: http://localhost:8002/docs
- **Compliance Service**: http://localhost:8003/docs
- **Workflow Service**: http://localhost:8004/docs
- **AI Agents**: http://localhost:8005/docs

## 🚀 Deployment

### Production Deployment

1. **Build production images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy to production**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Kubernetes Deployment

```bash
kubectl apply -f deployment/kubernetes/
```

## 📈 Monitoring

- **Health Checks**: `/health` endpoint on all services
- **Metrics**: Prometheus-compatible metrics
- **Logging**: Structured logging with configurable levels
- **Tracing**: Distributed tracing support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`npm run test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Follow the existing code style and patterns
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure backward compatibility
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/grc-platform/grc-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/grc-platform/grc-platform/discussions)

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [React](https://reactjs.org/)
- AI capabilities powered by [LangChain](https://langchain.com/) and [Ollama](https://ollama.ai/)
- UI components from [Material-UI](https://mui.com/)
- Database powered by [PostgreSQL](https://postgresql.org/) and [Redis](https://redis.io/)