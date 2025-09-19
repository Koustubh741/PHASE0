FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY workflow_service.py .

# Expose port
EXPOSE 8004

# Run the service
CMD ["uvicorn", "workflow_service:app", "--host", "0.0.0.0", "--port", "8004"]
