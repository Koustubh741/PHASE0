@echo off
echo Starting GRC Platform with Hugging Face Transformers...
echo.

REM Check if Docker is running
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Navigate to docker compose directory
cd /d "%~dp0docker\compose"

REM Check if .env file exists
if not exist "..\..\.env" (
    echo Creating .env file from template...
    copy "..\env.huggingface.template" "..\..\.env"
    echo.
    echo Please edit .env file to configure your settings before continuing.
    echo Press any key to continue after editing...
    pause
)

REM Start services
echo Starting services...
docker-compose -f docker-compose.huggingface.yml up -d

REM Wait for services to start
echo.
echo Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Check service status
echo.
echo Checking service status...
docker-compose -f docker-compose.huggingface.yml ps

echo.
echo Services started! You can access:
echo - Frontend: http://localhost:3000
echo - API Gateway: http://localhost:8000
echo - Hugging Face Service: http://localhost:8007
echo - AI Agents: http://localhost:8006
echo.
echo To view logs: docker-compose -f docker-compose.huggingface.yml logs -f
echo To stop services: docker-compose -f docker-compose.huggingface.yml down
echo.
pause


