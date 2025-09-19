@echo off
REM GRC Platform Full-Stack Startup Script for Windows

echo 🚀 Starting GRC Platform Full-Stack Application...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose and try again.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    (
        echo # GRC Platform Environment Configuration
        echo OPENAI_API_KEY=your-openai-api-key-here
        echo.
        echo # Database Configuration
        echo POSTGRES_DB=grc_platform
        echo POSTGRES_USER=grc_user
        echo POSTGRES_PASSWORD=grc_password
        echo.
        echo # Redis Configuration
        echo REDIS_URL=redis://localhost:6379
        echo.
        echo # Service URLs
        echo POLICY_SERVICE_URL=http://localhost:8001
        echo RISK_SERVICE_URL=http://localhost:8002
        echo COMPLIANCE_SERVICE_URL=http://localhost:8003
        echo WORKFLOW_SERVICE_URL=http://localhost:8004
        echo AI_AGENTS_URL=http://localhost:8005
        echo.
        echo # Frontend Configuration
        echo REACT_APP_API_URL=http://localhost:8000
        echo REACT_APP_ENVIRONMENT=development
    ) > .env
    echo ⚠️  Please update the .env file with your actual API keys and configuration.
)

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker-compose -f docker-compose.fullstack.yml down

REM Build and start services
echo 🔨 Building and starting services...
docker-compose -f docker-compose.fullstack.yml up --build -d

REM Wait for services to be healthy
echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak >nul

REM Check service health
echo 🏥 Checking service health...
docker-compose -f docker-compose.fullstack.yml ps

REM Display access information
echo.
echo 🎉 GRC Platform is now running!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔌 API Gateway: http://localhost:8000
echo 📊 API Documentation: http://localhost:8000/docs
echo.
echo 🔧 Services:
echo   - Policy Service: http://localhost:8001
echo   - Risk Service: http://localhost:8002
echo   - Compliance Service: http://localhost:8003
echo   - Workflow Service: http://localhost:8004
echo   - AI Agents: http://localhost:8005
echo.
echo 🗄️  Database:
echo   - PostgreSQL: localhost:5432
echo   - Redis: localhost:6379
echo.
echo 📋 To view logs: docker-compose -f docker-compose.fullstack.yml logs -f
echo 🛑 To stop: docker-compose -f docker-compose.fullstack.yml down
echo.
pause
