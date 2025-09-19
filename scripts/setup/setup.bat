@echo off
REM GRC Platform Development Environment Setup Script for Windows

echo 🚀 Setting up GRC Platform Development Environment...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Create environment files if they don't exist
echo 📝 Creating environment files...

if not exist "backend\.env" (
    copy "backend\env.example" "backend\.env"
    echo ✅ Created backend\.env
)

if not exist "frontend\.env" (
    copy "frontend\env.example" "frontend\.env"
    echo ✅ Created frontend\.env
)

if not exist "ai-agents\.env" (
    copy "ai-agents\env.example" "ai-agents\.env"
    echo ✅ Created ai-agents\.env
)

REM Start development databases
echo 🐘 Starting PostgreSQL and Redis...
docker-compose -f docker-compose.dev.yml up -d

REM Wait for databases to be ready
echo ⏳ Waiting for databases to be ready...
timeout /t 10 /nobreak >nul

REM Install backend dependencies
echo 📦 Installing backend dependencies...
cd backend
call npm install
cd ..

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
call npm install
cd ..

REM Install AI agents dependencies
echo 📦 Installing AI agents dependencies...
cd ai-agents
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo ✅ Setup complete!
echo.
echo 🔧 Next steps:
echo 1. Update environment files with your API keys:
echo    - backend\.env
echo    - frontend\.env
echo    - ai-agents\.env
echo.
echo 2. Start the development servers:
echo    - Backend: cd backend ^&^& npm run dev
echo    - Frontend: cd frontend ^&^& npm run dev
echo    - AI Agents: cd ai-agents ^&^& venv\Scripts\activate ^&^& python main.py
echo.
echo 3. Access the application:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:3001
echo    - AI Agents: http://localhost:8000
echo.
echo 📚 For more information, see the README.md file.
pause

