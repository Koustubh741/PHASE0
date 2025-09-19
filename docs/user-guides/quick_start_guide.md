# 🚀 GRC Platform Quick Start Guide

## Prerequisites

Before starting, ensure you have the following installed:

### Required Software
- **Node.js 18+** - [Download here]
- **Python 3.9+** - [Download here](https://python.org/)
- **Docker Desktop** - [Download here](https://docker.com/products/docker-desktop/)
- **Git** - [Download here](https://git-scm.com/)

### API Keys (Optional for basic setup)
- **OpenAI API Key** - [Get from OpenAI](https://platform.openai.com/api-keys)
- **Pinecone API Key** - [Get from Pinecone](https://pinecone.io/)

## 🏃‍♂️ Quick Setup (5 minutes)

### Step 1: Start Docker Services
```bash
# Start PostgreSQL and Redis
docker-compose -f docker-compose.dev.yml up -d
```

### Step 2: Install Dependencies
```bash
# Backend dependencies
cd backend
npm install
cd ..

# Frontend dependencies  
cd frontend
npm install
cd ..

# AI Agents dependencies
cd ai-agents
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cd ..
```

### Step 3: Configure Environment
```bash
# Copy environment files
cp backend/env.example backend/.env
cp frontend/env.example frontend/.env
cp ai-agents/env.example ai-agents/.env
```

### Step 4: Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
npm run dev
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - AI Agents:**
```bash
cd ai-agents
# Activate virtual environment first
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
python main.py
```

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **AI Agents**: http://localhost:8000
- **API Documentation**: http://localhost:3001/docs

## 🔧 Default Login Credentials

- **Email**: admin@grcplatform.com
- **Password**: admin123

## 📋 What's Included

### ✅ Backend (Node.js + TypeScript)
- Express.js API server
- PostgreSQL database with sample data
- Redis for caching
- JWT authentication
- RESTful API endpoints

### ✅ Frontend (React + TypeScript)
- Material-UI components
- Redux state management
- Responsive design
- Dashboard with sample data
- Policy, Risk, and Compliance modules

### ✅ AI Agents (Python + FastAPI)
- Compliance monitoring agent
- Risk assessment agent
- Document analysis agent
- MCP communication protocol
- OpenAI GPT-4 integration

### ✅ Database
- PostgreSQL with sample data
- Pre-configured tables and relationships
- Sample policies and risks
- Admin user account

## 🛠️ Development Commands

### Backend
```bash
cd backend
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run tests
npm run migrate      # Run database migrations
```

### Frontend
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run tests
npm run lint         # Run linting
```

### AI Agents
```bash
cd ai-agents
python main.py       # Start AI agents
pytest              # Run tests
```

## 🐳 Docker Commands

### Start all services
```bash
docker-compose up -d
```

### Stop all services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Rebuild services
```bash
docker-compose up --build
```

## 🔍 Troubleshooting

### Common Issues

**1. Docker not running**
```bash
# Start Docker Desktop application
# Wait for it to fully start, then try again
```

**2. Port already in use**
```bash
# Check what's using the port
netstat -ano | findstr :3000  # Windows
lsof -i :3000                 # macOS/Linux

# Kill the process or change ports in .env files
```

**3. Database connection failed**
```bash
# Make sure PostgreSQL container is running
docker ps

# Check database logs
docker-compose logs postgres
```

**4. AI Agents not starting**
```bash
# Check if virtual environment is activated
# Make sure all dependencies are installed
pip install -r requirements.txt
```

**5. Frontend build errors**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📚 Next Steps

1. **Explore the Code**: Check out the project structure in the documentation
2. **Customize**: Modify the sample data and configurations
3. **Add Features**: Implement additional GRC functionality
4. **Deploy**: Use the deployment guides for production setup

## 🆘 Getting Help

- Check the [README.md](README.md) for detailed information
- Review the [Implementation Guides](Implementation_Guides.md)
- Look at the [Project Structure](Project_Structure.md)
- Check the [System Architecture](GRC_Platform_Architecture.md)

## 🎯 Development Phases

The platform is designed to be developed in phases:

1. **Phase 1**: Foundation (✅ Complete)
2. **Phase 2**: Core GRC Features (🔄 In Progress)
3. **Phase 3**: AI Integration (🔄 In Progress)
4. **Phase 4**: Advanced Features (⏳ Pending)
5. **Phase 5**: Testing & Deployment (⏳ Pending)

You're currently in **Phase 1** with a working foundation. The next steps involve implementing the core GRC features and AI integration.

---

**🎉 Congratulations! You now have a working GRC platform development environment!**

