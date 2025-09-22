#!/usr/bin/env python3
"""
API Gateway Startup Script
Starts the GRC Platform API Gateway with proper configuration
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the backend src directory to Python path
backend_src = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(backend_src))

from config.settings import settings


def start_api_gateway():
    """Start the API Gateway service"""
    print("🚀 Starting GRC Platform API Gateway...")
    print(f"📋 Configuration:")
    print(f"   - Debug Mode: {settings.debug}")
    print(f"   - Version: {settings.version}")
    print(f"   - CORS Origins: {settings.cors_origins}")
    
    # Start the API Gateway
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
        access_log=True
    )


if __name__ == "__main__":
    start_api_gateway()
