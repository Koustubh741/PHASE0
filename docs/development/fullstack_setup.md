# GRC Platform - Full-Stack Setup Guide

## 🚀 Complete Full-Stack GRC Platform

This guide will help you set up and run the complete GRC Platform with both frontend and backend services integrated.

## 📋 Prerequisites

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Node.js** (version 18 or higher) - for local development
- **Python** (version 3.11 or higher) - for local development
- **OpenAI API Key** - for AI functionality

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   API Gateway   │    │  Backend Services│
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│  (Ports 8001-5) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AI Agents     │
                       │   (Port 8005)   │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   (Port 5432)   │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Port 6379)   │
                       └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone and Navigate**
   ```bash
   cd PHASE0
   ```

2. **Set Environment Variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your-actual-openai-api-key-here
   ```

3. **Start All Services**
   ```bash
   # For Linux/Mac
   chmod +x start-fullstack.sh
   ./start-fullstack.sh
   
   # For Windows
   start-fullstack.bat
   ```

4. **Access the Platform**
   - **Frontend**: http://localhost:3000
   - **API Gateway**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Option 2: Manual Docker Compose

```bash
# Build and start all services
docker-compose -f docker-compose.fullstack.yml up --build -d

# Check service status
docker-compose -f docker-compose.fullstack.yml ps

# View logs
docker-compose -f docker-compose.fullstack.yml logs -f
```

## 🔧 Services Overview

### Frontend Services
- **React Frontend** (Port 3000)
  - Modern Material-UI interface
  - Real-time data visualization
  - Responsive design
  - Error boundaries and loading states

### Backend Services
- **API Gateway** (Port 8000)
  - Central routing and authentication
  - CORS configuration
  - Service orchestration
  - Unified API endpoints

- **Policy Service** (Port 8001)
  - Policy management and approval workflows
  - Document storage and versioning
  - Compliance tracking

- **Risk Service** (Port 8002)
  - Risk assessment and scoring
  - Risk heat maps and trends
  - Mitigation planning

- **Compliance Service** (Port 8003)
  - Compliance monitoring
  - Framework management (GDPR, SOX, ISO 27001)
  - Gap analysis and reporting

- **Workflow Service** (Port 8004)
  - Process automation
  - Approval workflows
  - Task management

- **AI Agents Service** (Port 8005)
  - Multi-agent orchestration
  - Industry-specific agents
  - Vector database integration
  - Advanced MCP protocol

### Infrastructure Services
- **PostgreSQL** (Port 5432)
  - Primary database
  - ACID compliance
  - Full-text search

- **Redis** (Port 6379)
  - Caching layer
  - Session storage
  - Message queuing

## 📱 Frontend Features

### Core Modules
1. **Dashboard**
   - Real-time KPIs
   - Service status monitoring
   - Quick actions

2. **Policy Management**
   - CRUD operations
   - Approval workflows
   - Version control
   - Document upload

3. **Risk Management**
   - Risk assessment
   - Heat map visualization
   - Trend analysis
   - Mitigation tracking

4. **Compliance Management**
   - Framework compliance
   - Gap analysis
   - Evidence management
   - Reporting

5. **Workflow Management**
   - Process automation
   - Task assignment
   - Progress tracking
   - Template management

6. **Analytics & Reporting**
   - Interactive charts
   - Executive summaries
   - Custom reports
   - Data export

7. **Settings**
   - System configuration
   - User preferences
   - Security settings
   - AI model selection

### Technical Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live data synchronization
- **Error Handling**: Comprehensive error boundaries
- **Loading States**: Smooth user experience
- **Search & Filter**: Advanced data filtering
- **Export Capabilities**: PDF, CSV, Excel export

## 🔌 API Integration

### Frontend-Backend Communication
The frontend communicates with the backend through a comprehensive API service layer:

```javascript
// Example API usage
import { policyService } from './services/policyService';

// Get all policies
const policies = await policyService.getAllPolicies();

// Create new policy
const newPolicy = await policyService.createPolicy({
  title: 'New Policy',
  description: 'Policy description',
  category: 'Security'
});
```

### API Endpoints
- **Policies**: `/policies/*`
- **Risks**: `/risks/*`
- **Compliance**: `/compliance/*`
- **Workflows**: `/workflows/*`
- **Analytics**: `/analytics/*`
- **AI Agents**: `/ai-agents/*`

## 🛠️ Development

### Local Development Setup

1. **Backend Development**
   ```bash
   # Start backend services
   cd backend/api-gateway
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend Development**
   ```bash
   # Start frontend
   cd frontend
   npm install
   npm start
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose -f docker-compose.fullstack.yml up postgres redis -d
   ```

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Database Configuration
POSTGRES_DB=grc_platform
POSTGRES_USER=grc_user
POSTGRES_PASSWORD=grc_password

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Service URLs
POLICY_SERVICE_URL=http://localhost:8001
RISK_SERVICE_URL=http://localhost:8002
COMPLIANCE_SERVICE_URL=http://localhost:8003
WORKFLOW_SERVICE_URL=http://localhost:8004
AI_AGENTS_URL=http://localhost:8005

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

## 🔍 Monitoring & Debugging

### Service Health Checks
```bash
# Check all services
curl http://localhost:8000/health

# Check individual services
curl http://localhost:8001/health  # Policy Service
curl http://localhost:8002/health  # Risk Service
curl http://localhost:8003/health  # Compliance Service
curl http://localhost:8004/health  # Workflow Service
curl http://localhost:8005/health  # AI Agents
```

### Logs
```bash
# View all logs
docker-compose -f docker-compose.fullstack.yml logs -f

# View specific service logs
docker-compose -f docker-compose.fullstack.yml logs -f frontend
docker-compose -f docker-compose.fullstack.yml logs -f api-gateway
```

### Database Access
```bash
# Connect to PostgreSQL
docker exec -it grc-postgres psql -U grc_user -d grc_platform

# Connect to Redis
docker exec -it grc-redis redis-cli
```

## 🚀 Deployment

### Production Deployment

1. **Update Environment Variables**
   ```env
   REACT_APP_ENVIRONMENT=production
   REACT_APP_API_URL=https://your-domain.com
   ```

2. **Use Production Profile**
   ```bash
   docker-compose -f docker-compose.fullstack.yml --profile production up -d
   ```

3. **SSL Configuration**
   - Update nginx configuration
   - Add SSL certificates
   - Configure domain names

### Scaling
```bash
# Scale specific services
docker-compose -f docker-compose.fullstack.yml up --scale policy-service=3 -d
docker-compose -f docker-compose.fullstack.yml up --scale risk-service=2 -d
```

## 🛑 Stopping Services

```bash
# Stop all services
docker-compose -f docker-compose.fullstack.yml down

# Stop and remove volumes
docker-compose -f docker-compose.fullstack.yml down -v

# Stop specific services
docker-compose -f docker-compose.fullstack.yml stop frontend api-gateway
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8000
   ```

2. **Docker Issues**
   ```bash
   # Restart Docker
   sudo systemctl restart docker
   
   # Clean up containers
   docker system prune -a
   ```

3. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose -f docker-compose.fullstack.yml logs postgres
   
   # Reset database
   docker-compose -f docker-compose.fullstack.yml down -v
   docker-compose -f docker-compose.fullstack.yml up postgres -d
   ```

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs)
- [Frontend Components Guide](./ai-agents/GRC_Platform_Components_Guide.md)
- [System Architecture](./ai-agents/CURRENT_SYSTEM_DESIGN.md)
- [Management Presentation](./ai-agents/GRC_PLATFORM_MANAGEMENT_PRESENTATION.md)

## 🎯 Next Steps

1. **Configure OpenAI API Key** in `.env` file
2. **Start the platform** using the startup script
3. **Access the frontend** at http://localhost:3000
4. **Explore the API** at http://localhost:8000/docs
5. **Customize** the platform for your organization

---

**🎉 Your complete GRC Platform is now ready to use!**
