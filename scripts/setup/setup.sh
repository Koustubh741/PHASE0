#!/bin/bash

# GRC Platform Development Environment Setup Script

set -e

echo "🚀 Setting up GRC Platform Development Environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment files if they don't exist
echo "📝 Creating environment files..."

if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "✅ Created backend/.env"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/env.example frontend/.env
    echo "✅ Created frontend/.env"
fi

if [ ! -f ai-agents/.env ]; then
    cp ai-agents/env.example ai-agents/.env
    echo "✅ Created ai-agents/.env"
fi

# Start development databases
echo "🐘 Starting PostgreSQL and Redis..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for databases to be ready
echo "⏳ Waiting for databases to be ready..."
sleep 10

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
npm install
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install AI agents dependencies
echo "📦 Installing AI agents dependencies..."
cd ai-agents
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo "✅ Setup complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Update environment files with your API keys:"
echo "   - backend/.env"
echo "   - frontend/.env"
echo "   - ai-agents/.env"
echo ""
echo "2. Start the development servers:"
echo "   - Backend: cd backend && npm run dev"
echo "   - Frontend: cd frontend && npm run dev"
echo "   - AI Agents: cd ai-agents && source venv/bin/activate && python main.py"
echo ""
echo "3. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:3001"
echo "   - AI Agents: http://localhost:8000"
echo ""
echo "📚 For more information, see the README.md file."

