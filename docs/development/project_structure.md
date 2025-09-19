# GRC Platform Project Structure

## Complete Directory Structure

```
grc-platform/
├── README.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── docs/
│   ├── api/
│   │   ├── authentication.md
│   │   ├── policies.md
│   │   ├── risks.md
│   │   └── compliance.md
│   ├── architecture/
│   │   ├── system-design.md
│   │   ├── database-schema.md
│   │   └── api-design.md
│   └── deployment/
│       ├── docker.md
│       ├── kubernetes.md
│       └── aws.md
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── kubernetes/
│   │   ├── namespaces/
│   │   ├── deployments/
│   │   ├── services/
│   │   ├── ingress/
│   │   └── secrets/
│   └── monitoring/
│       ├── prometheus/
│       ├── grafana/
│       └── elk/
├── backend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── .env.example
│   ├── src/
│   │   ├── app.ts
│   │   ├── server.ts
│   │   ├── config/
│   │   │   ├── database.ts
│   │   │   ├── redis.ts
│   │   │   └── environment.ts
│   │   ├── controllers/
│   │   │   ├── auth.controller.ts
│   │   │   ├── user.controller.ts
│   │   │   ├── policy.controller.ts
│   │   │   ├── risk.controller.ts
│   │   │   └── compliance.controller.ts
│   │   ├── services/
│   │   │   ├── auth.service.ts
│   │   │   ├── user.service.ts
│   │   │   ├── policy.service.ts
│   │   │   ├── risk.service.ts
│   │   │   ├── compliance.service.ts
│   │   │   ├── notification.service.ts
│   │   │   └── ai.service.ts
│   │   ├── models/
│   │   │   ├── user.model.ts
│   │   │   ├── policy.model.ts
│   │   │   ├── risk.model.ts
│   │   │   ├── compliance.model.ts
│   │   │   └── audit.model.ts
│   │   ├── middleware/
│   │   │   ├── auth.middleware.ts
│   │   │   ├── validation.middleware.ts
│   │   │   ├── rate-limit.middleware.ts
│   │   │   └── error.middleware.ts
│   │   ├── routes/
│   │   │   ├── auth.routes.ts
│   │   │   ├── user.routes.ts
│   │   │   ├── policy.routes.ts
│   │   │   ├── risk.routes.ts
│   │   │   └── compliance.routes.ts
│   │   ├── utils/
│   │   │   ├── logger.ts
│   │   │   ├── encryption.ts
│   │   │   ├── validation.ts
│   │   │   └── helpers.ts
│   │   ├── database/
│   │   │   ├── migrations/
│   │   │   ├── seeds/
│   │   │   └── connection.ts
│   │   └── types/
│   │       ├── auth.types.ts
│   │       ├── policy.types.ts
│   │       ├── risk.types.ts
│   │       └── common.types.ts
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   └── scripts/
│       ├── setup-db.js
│       ├── seed-data.js
│       └── backup-db.js
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Header/
│   │   │   │   ├── Sidebar/
│   │   │   │   ├── Footer/
│   │   │   │   ├── LoadingSpinner/
│   │   │   │   └── ErrorBoundary/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm/
│   │   │   │   ├── RegisterForm/
│   │   │   │   └── PasswordReset/
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard/
│   │   │   │   ├── StatsCards/
│   │   │   │   └── RecentActivity/
│   │   │   ├── policies/
│   │   │   │   ├── PolicyList/
│   │   │   │   ├── PolicyForm/
│   │   │   │   ├── PolicyViewer/
│   │   │   │   └── PolicyApproval/
│   │   │   ├── risks/
│   │   │   │   ├── RiskList/
│   │   │   │   ├── RiskForm/
│   │   │   │   ├── RiskAssessment/
│   │   │   │   └── RiskMatrix/
│   │   │   ├── compliance/
│   │   │   │   ├── ComplianceDashboard/
│   │   │   │   ├── ComplianceCheck/
│   │   │   │   ├── AuditTrail/
│   │   │   │   └── Reports/
│   │   │   ├── charts/
│   │   │   │   ├── RiskChart/
│   │   │   │   ├── ComplianceChart/
│   │   │   │   └── TrendChart/
│   │   │   └── forms/
│   │   │       ├── FormField/
│   │   │       ├── FormValidation/
│   │   │       └── FormSubmit/
│   │   ├── pages/
│   │   │   ├── Dashboard/
│   │   │   ├── Policies/
│   │   │   ├── Risks/
│   │   │   ├── Compliance/
│   │   │   ├── Reports/
│   │   │   ├── Settings/
│   │   │   └── Profile/
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useApi.ts
│   │   │   ├── useWebSocket.ts
│   │   │   └── useLocalStorage.ts
│   │   ├── store/
│   │   │   ├── index.ts
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.ts
│   │   │   │   ├── policySlice.ts
│   │   │   │   ├── riskSlice.ts
│   │   │   │   └── complianceSlice.ts
│   │   │   └── middleware/
│   │   │       ├── apiMiddleware.ts
│   │   │       └── websocketMiddleware.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── policy.service.ts
│   │   │   ├── risk.service.ts
│   │   │   ├── compliance.service.ts
│   │   │   └── websocket.service.ts
│   │   ├── utils/
│   │   │   ├── constants.ts
│   │   │   ├── helpers.ts
│   │   │   ├── validation.ts
│   │   │   └── formatters.ts
│   │   ├── types/
│   │   │   ├── auth.types.ts
│   │   │   ├── policy.types.ts
│   │   │   ├── risk.types.ts
│   │   │   ├── compliance.types.ts
│   │   │   └── common.types.ts
│   │   └── styles/
│   │       ├── globals.css
│   │       ├── theme.ts
│   │       └── components/
│   └── tests/
│       ├── components/
│       ├── pages/
│       └── utils/
├── ai-agents/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── main.py
│   ├── base/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── mcp_broker.py
│   │   └── message_types.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── compliance/
│   │   │   ├── __init__.py
│   │   │   ├── compliance_agent.py
│   │   │   ├── policy_analyzer.py
│   │   │   └── violation_detector.py
│   │   ├── risk/
│   │   │   ├── __init__.py
│   │   │   ├── risk_agent.py
│   │   │   ├── risk_assessor.py
│   │   │   └── risk_predictor.py
│   │   ├── document/
│   │   │   ├── __init__.py
│   │   │   ├── document_agent.py
│   │   │   ├── pdf_processor.py
│   │   │   └── text_extractor.py
│   │   └── communication/
│   │       ├── __init__.py
│   │       ├── communication_agent.py
│   │       ├── notification_sender.py
│   │       └── report_generator.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── compliance_model.py
│   │   ├── risk_model.py
│   │   └── document_model.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── openai_client.py
│   │   ├── vector_store.py
│   │   ├── database.py
│   │   └── logger.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── prompts.py
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── fixtures/
├── shared/
│   ├── types/
│   │   ├── user.types.ts
│   │   ├── policy.types.ts
│   │   ├── risk.types.ts
│   │   └── compliance.types.ts
│   ├── constants/
│   │   ├── api.constants.ts
│   │   ├── roles.constants.ts
│   │   └── status.constants.ts
│   └── utils/
│       ├── validation.ts
│       ├── formatters.ts
│       └── helpers.ts
└── scripts/
    ├── setup.sh
    ├── deploy.sh
    ├── backup.sh
    └── migrate.sh
```

## Key File Descriptions

### Backend Structure
- **app.ts**: Main application entry point
- **controllers/**: Handle HTTP requests and responses
- **services/**: Business logic and data processing
- **models/**: Data models and database schemas
- **middleware/**: Request processing middleware
- **routes/**: API endpoint definitions
- **database/**: Database migrations and seeds

### Frontend Structure
- **components/**: Reusable UI components organized by feature
- **pages/**: Page-level components for routing
- **hooks/**: Custom React hooks for state and side effects
- **store/**: Redux store configuration and slices
- **services/**: API communication and external services
- **types/**: TypeScript type definitions

### AI Agents Structure
- **base/**: Base classes and common functionality
- **agents/**: Individual AI agent implementations
- **models/**: Machine learning models and algorithms
- **utils/**: Utility functions and helpers
- **config/**: Configuration and prompt templates

### Infrastructure Structure
- **terraform/**: Infrastructure as Code for cloud resources
- **kubernetes/**: Kubernetes manifests for container orchestration
- **monitoring/**: Monitoring and observability configurations

## Development Workflow

### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd grc-platform

# Setup backend
cd backend
npm install
cp .env.example .env
# Configure environment variables

# Setup frontend
cd ../frontend
npm install
cp .env.example .env

# Setup AI agents
cd ../ai-agents
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Start development environment
cd ..
docker-compose up -d postgres redis
```

### 2. Development Commands
```bash
# Backend development
cd backend
npm run dev          # Start development server
npm run test         # Run tests
npm run build        # Build for production

# Frontend development
cd frontend
npm run dev          # Start development server
npm run test         # Run tests
npm run build        # Build for production

# AI agents development
cd ai-agents
python main.py       # Start AI agents
pytest              # Run tests
```

### 3. Database Management
```bash
# Run migrations
cd backend
npm run migrate

# Seed database
npm run seed

# Backup database
npm run backup
```

### 4. Deployment
```bash
# Build all services
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Deploy to Kubernetes
kubectl apply -f infrastructure/kubernetes/
```

## Configuration Files

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost:5432/grc_platform
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-jwt-secret
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key

# Frontend (.env)
REACT_APP_API_URL=http://localhost:3001
REACT_APP_WS_URL=ws://localhost:3001

# AI Agents (.env)
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
```

### Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: grc_platform
      POSTGRES_USER: grc_user
      POSTGRES_PASSWORD: grc_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://grc_user:grc_password@postgres:5432/grc_platform
      REDIS_URL: redis://redis:6379
    ports:
      - "3001:3001"
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  ai-agents:
    build: ./ai-agents
    environment:
      REDIS_URL: redis://redis:6379
    depends_on:
      - redis

volumes:
  postgres_data:
```

This project structure provides a scalable, maintainable foundation for building the GRC platform with clear separation of concerns and organized codebase.

