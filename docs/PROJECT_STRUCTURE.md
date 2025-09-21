# GRC Platform - Clean Project Structure

A comprehensive Governance, Risk, and Compliance (GRC) management platform with clean separation between frontend and backend services.

## 📁 Complete Project Structure

```
PHASE0/
├── 📁 frontend/                          # React Frontend Application
│   ├── 📁 public/                        # Static assets
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   └── manifest.json
│   ├── 📁 src/                          # Source code
│   │   ├── 📁 components/               # Reusable UI components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Navigation.jsx
│   │   │   ├── PolicyManagement.jsx
│   │   │   ├── RiskAssessment.jsx
│   │   │   ├── ComplianceMonitoring.jsx
│   │   │   ├── WorkflowManagement.jsx
│   │   │   ├── AIAgents.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Settings.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── UserProfile.jsx
│   │   │   ├── NotificationCenter.jsx
│   │   │   ├── DataVisualization.jsx
│   │   │   └── DocumentViewer.jsx
│   │   ├── 📁 features/                 # Feature-based modules
│   │   │   ├── 📁 dashboard/
│   │   │   ├── 📁 policy/
│   │   │   ├── 📁 risk/
│   │   │   ├── 📁 compliance/
│   │   │   ├── 📁 workflow/
│   │   │   ├── 📁 ai-agents/
│   │   │   ├── 📁 analytics/
│   │   │   └── 📁 settings/
│   │   ├── 📁 hooks/                    # Custom React hooks
│   │   │   ├── 📁 api/
│   │   │   └── 📁 custom/
│   │   ├── 📁 services/                 # API and external integrations
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   ├── policyService.js
│   │   │   ├── riskService.js
│   │   │   ├── complianceService.js
│   │   │   ├── workflowService.js
│   │   │   └── aiAgentsService.js
│   │   ├── 📁 store/                    # Redux state management
│   │   ├── 📁 types/                    # TypeScript type definitions
│   │   ├── 📁 utils/                    # Utility functions
│   │   ├── 📁 assets/                   # Static assets
│   │   │   ├── 📁 icons/
│   │   │   ├── 📁 images/
│   │   │   └── 📁 styles/
│   │   ├── App.jsx                      # Main application component
│   │   ├── index.js                     # Application entry point
│   │   └── index.css                    # Global styles
│   ├── 📁 build/                        # Production build output
│   ├── 📁 tests/                        # Frontend tests
│   │   ├── 📁 unit/
│   │   ├── 📁 integration/
│   │   └── 📁 e2e/
│   ├── package.json                     # Frontend dependencies
│   ├── package-lock.json               # Lock file
│   └── README.md                        # Frontend documentation
│
├── 📁 backend/                          # Python Backend Services
│   ├── 📁 src/                          # Source code (Clean Architecture)
│   │   ├── 📁 core/                     # Core business logic
│   │   │   ├── 📁 application/          # Application layer (use cases)
│   │   │   ├── 📁 domain/               # Domain layer (entities, rules)
│   │   │   ├── 📁 infrastructure/       # Infrastructure layer (DB, external)
│   │   │   └── 📁 presentation/         # Presentation layer (API endpoints)
│   │   └── 📁 shared/                   # Shared components
│   │       ├── 📁 constants/
│   │       ├── 📁 exceptions/
│   │       └── 📁 utils/
│   ├── 📁 ai-agents/                    # AI Agents Service
│   │   ├── 📁 agents_organized/         # Organized agent implementations
│   │   │   ├── 📁 bfsi_agent/          # Banking & Financial Services
│   │   │   ├── 📁 healthcare_agent/    # Healthcare industry agent
│   │   │   ├── 📁 manufacturing_agent/ # Manufacturing industry agent
│   │   │   ├── 📁 telecom_agent/       # Telecommunications agent
│   │   │   ├── 📁 communication_agent/ # Inter-agent communication
│   │   │   ├── 📁 document_agent/      # Document processing
│   │   │   ├── 📁 compliance_agent/    # Compliance monitoring
│   │   │   ├── 📁 risk_agent/          # Risk assessment
│   │   │   ├── 📁 orchestration/       # Multi-agent orchestration
│   │   │   ├── 📁 shared_components/   # Shared agent components
│   │   │   ├── 📁 applications/        # Agent applications
│   │   │   ├── 📁 utilities/           # Agent utilities
│   │   │   └── 📁 documentation/       # Agent documentation
│   │   ├── Dockerfile.enhanced         # Enhanced AI agents Docker
│   │   └── Dockerfile.huggingface      # Hugging Face integration
│   ├── 📁 deployment/                   # Deployment configurations
│   ├── 📁 tests/                        # Backend tests
│   │   ├── 📁 unit/
│   │   ├── 📁 integration/
│   │   └── 📁 e2e/
│   ├── pyproject.toml                   # Python project configuration
│   ├── requirements.txt                 # Python dependencies
│   └── README.md                        # Backend documentation
│
├── 📁 config/                           # Configuration files
│   ├── 📁 database/                     # Database configurations
│   │   ├── schema.sql                   # Database schema
│   │   ├── populate_all_sample_data.sql # Sample data
│   │   ├── bfsi_sample_data.sql        # BFSI sample data
│   │   ├── healthcare_sample_data.sql  # Healthcare sample data
│   │   ├── manufacturing_sample_data.sql # Manufacturing sample data
│   │   ├── telecom_sample_data.sql     # Telecom sample data
│   │   └── users_and_organizations_data.sql # User data
│   ├── 📁 environments/                 # Environment configurations
│   └── 📁 infrastructure/               # Infrastructure configs
│       └── 📁 nginx/                    # Nginx configuration
│           ├── nginx.conf
│           └── 📁 ssl/
│
├── 📁 deployment/                       # Deployment configurations
│   ├── 📁 docker/                       # Docker configurations
│   │   ├── 📁 ai-agents/               # AI agents Docker configs
│   │   ├── 📁 compose/                 # Docker Compose files
│   │   └── 📁 services/                # Service-specific Dockerfiles
│   ├── 📁 kubernetes/                   # Kubernetes configurations
│   └── 📁 scripts/                      # Deployment scripts
│
├── 📁 docs/                             # Documentation
│   ├── 📁 api/                          # API documentation
│   ├── 📁 architecture/                 # Architecture documentation
│   ├── 📁 development/                  # Development guides
│   └── 📁 user-guides/                  # User guides
│
├── 📁 scripts/                          # Utility scripts
│   ├── 📁 data/                         # Data management scripts
│   ├── 📁 deployment/                   # Deployment scripts
│   ├── 📁 maintenance/                  # Maintenance scripts
│   ├── 📁 setup/                        # Setup scripts
│   └── 📁 testing/                      # Testing scripts
│
├── 📁 tests/                            # Integration and E2E tests
│   ├── 📁 e2e/
│   ├── 📁 integration/
│   └── 📁 unit/
│
├── 📁 tools/                            # Development tools
│   ├── 📁 monitoring/                   # Monitoring tools
│   ├── 📁 utilities/                    # Utility tools
│   └── 📁 validation/                   # Validation tools
│
├── 📁 data/                             # Data storage
│   ├── 📁 exports/                      # Data exports
│   ├── 📁 fixtures/                     # Test fixtures
│   ├── 📁 sample/                       # Sample data
│   └── 📁 vector/                       # Vector database data
│
├── 📁 ai-agents/                        # AI agents cache and models
│   ├── 📁 models_cache/                 # Cached AI models
│   └── 📁 vector-db/                    # AI agents vector database
│
├── 📁 vector-db/                        # Vector database storage
│
├── docker-compose.yml                   # Main Docker Compose file
├── package.json                         # Root package.json for scripts
├── pyproject.toml                       # Root Python configuration
├── requirements.txt                     # Root requirements
├── env.example                          # Environment variables template
└── README.md                            # Main project documentation
```

## 🏗️ Architecture Overview

### Frontend Architecture (React)
- **Component-Based**: Modular, reusable UI components
- **Feature-Driven**: Organized by business features
- **State Management**: Redux for global state
- **API Integration**: Centralized service layer
- **Testing**: Unit, integration, and E2E tests

### Backend Architecture (Python/FastAPI)
- **Clean Architecture**: Domain-driven design with clear separation
- **Microservices**: Multiple specialized services
- **AI Integration**: Advanced AI agents for industry-specific GRC
- **Database**: PostgreSQL with Redis caching
- **API Gateway**: Central entry point for all services

## 🚀 Service Structure

### Core Services
1. **API Gateway** (Port 8000) - Central entry point
2. **Policy Service** (Port 8001) - Policy management
3. **Risk Service** (Port 8002) - Risk assessment
4. **Compliance Service** (Port 8003) - Compliance monitoring
5. **Workflow Service** (Port 8004) - Business processes
6. **AI Agents** (Port 8005) - AI-powered analysis

### AI Agents
- **Industry-Specific Agents**: BFSI, Healthcare, Manufacturing, Telecom
- **Specialized Agents**: Communication, Document, Compliance, Risk
- **Orchestration Layer**: Multi-agent coordination and management

## 📦 Key Files and Their Purposes

### Frontend Key Files
- `frontend/src/App.jsx` - Main application component
- `frontend/src/index.js` - Application entry point
- `frontend/package.json` - Dependencies and scripts
- `frontend/public/index.html` - HTML template

### Backend Key Files
- `backend/src/core/` - Clean architecture layers
- `backend/ai-agents/agents_organized/` - AI agent implementations
- `backend/pyproject.toml` - Python project configuration
- `backend/requirements.txt` - Python dependencies

### Configuration Files
- `docker-compose.yml` - Service orchestration
- `config/database/schema.sql` - Database structure
- `config/infrastructure/nginx/nginx.conf` - Web server config
- `env.example` - Environment variables template

### Documentation
- `README.md` - Main project documentation
- `docs/` - Comprehensive documentation
- `backend/README.md` - Backend-specific docs
- `frontend/README.md` - Frontend-specific docs

## 🔧 Development Workflow

### Frontend Development
```bash
cd frontend
npm install          # Install dependencies
npm start            # Start development server
npm test             # Run tests
npm run build        # Build for production
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt  # Install dependencies
python -m pytest                 # Run tests
uvicorn main:app --reload        # Start development server
```

### Full Stack Development
```bash
# From root directory
docker-compose up -d             # Start all services
npm run dev                      # Start both frontend and backend
```

## 📊 Data Flow

1. **Frontend** → API Gateway → Individual Services
2. **Services** → Database (PostgreSQL) + Cache (Redis)
3. **AI Agents** → Vector Database + External APIs
4. **Real-time Updates** → WebSocket connections

## 🛡️ Security & Compliance

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Data Encryption**: At rest and in transit
- **Audit Logging**: Comprehensive audit trails
- **Compliance**: Industry-specific compliance frameworks

## 🧹 Cleanup Actions Required

### Remove Duplicate Directories
The following directories contain duplicates and should be removed:
- `src/frontend/` (duplicate of `frontend/`)
- `src/backend/` (duplicate of `backend/`)
- `src/ai-agents/` (duplicate of `backend/ai-agents/`)

### Consolidate Configuration
- Keep main configuration files in root
- Remove duplicate configuration files
- Update Docker Compose to reference correct paths

### Update Scripts
- Update all scripts to reference the clean structure
- Remove references to duplicate directories
- Ensure all paths are consistent

This structure provides a clean separation between frontend and backend while maintaining flexibility for both development and production deployments.
