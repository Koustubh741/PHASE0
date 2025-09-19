#!/bin/bash

echo "Starting GRC Platform with Hugging Face Transformers..."
echo

# Check if Docker is running
if ! docker version >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Navigate to docker compose directory
cd "$(dirname "$0")/docker/compose"

# Check if .env file exists
if [ ! -f "../../.env" ]; then
    echo "Creating .env file from template..."
    cp "../env.huggingface.template" "../../.env"
    echo
    echo "Please edit .env file to configure your settings before continuing."
    echo "Press Enter to continue after editing..."
    read
fi

# Start services
echo "Starting services..."
docker-compose -f docker-compose.huggingface.yml up -d

# Wait for services to start
echo
echo "Waiting for services to start..."
sleep 30

# Check service status
echo
echo "Checking service status..."
docker-compose -f docker-compose.huggingface.yml ps

echo
echo "Services started! You can access:"
echo "- Frontend: http://localhost:3000"
echo "- API Gateway: http://localhost:8000"
echo "- Hugging Face Service: http://localhost:8007"
echo "- AI Agents: http://localhost:8006"
echo
echo "To view logs: docker-compose -f docker-compose.huggingface.yml logs -f"
echo "To stop services: docker-compose -f docker-compose.huggingface.yml down"
echo


