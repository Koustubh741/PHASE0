#!/bin/bash

# GRC Platform Full-Stack Startup Script
echo "🚀 Starting GRC Platform Full-Stack Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# GRC Platform Environment Configuration
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
EOF
    echo "⚠️  Please update the .env file with your actual API keys and configuration."
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.fullstack.yml down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.fullstack.yml up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.fullstack.yml ps

# Display access information
echo ""
echo "🎉 GRC Platform is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔌 API Gateway: http://localhost:8000"
echo "📊 API Documentation: http://localhost:8000/docs"
echo ""
echo "🔧 Services:"
echo "  - Policy Service: http://localhost:8001"
echo "  - Risk Service: http://localhost:8002"
echo "  - Compliance Service: http://localhost:8003"
echo "  - Workflow Service: http://localhost:8004"
echo "  - AI Agents: http://localhost:8005"
echo ""
echo "🗄️  Database:"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "📋 To view logs: docker-compose -f docker-compose.fullstack.yml logs -f"
echo "🛑 To stop: docker-compose -f docker-compose.fullstack.yml down"
echo ""
