FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional AI/ML dependencies
RUN pip install --no-cache-dir \
    torch \
    transformers \
    sentence-transformers \
    scikit-learn \
    pandas \
    numpy \
    fastapi \
    uvicorn

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p /app/models /app/data /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV BACKEND_URL=http://backend:8000
ENV REDIS_URL=redis://redis:6379

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Start the BFSI AI service
CMD ["python", "bfsi_local_ai_api.py"]
