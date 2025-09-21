"""
Example application integration with startup validation.
This shows how to integrate the validation system into your main application.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.startup_validation import validate_on_startup, get_validation_status
from config.secrets_management import validate_secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_application():
    """
    Initialize the application with comprehensive validation.
    
    Returns:
        bool: True if initialization succeeds, False otherwise
    """
    logger.info("🚀 Initializing BFSI API application...")
    
    # Determine environment
    environment = os.getenv('ENVIRONMENT', 'production')
    logger.info(f"Running in {environment} environment")
    
    try:
        # Step 1: Validate startup configuration
        logger.info("🔍 Running startup validation...")
        if not validate_on_startup(environment=environment, fail_on_error=False):
            logger.error("❌ Startup validation failed")
            return False
        
        # Step 2: Validate secrets (only in production)
        if environment == 'production':
            logger.info("🔐 Running secrets validation...")
            if not validate_secrets(environment=environment, fail_on_error=False):
                logger.error("❌ Secrets validation failed")
                return False
        
        # Step 3: Get validation status for logging
        validation_status = get_validation_status()
        if validation_status['warnings']:
            logger.warning(f"⚠️  Found {len(validation_status['warnings'])} validation warnings")
            for warning in validation_status['warnings']:
                logger.warning(f"  - {warning.get('error', 'Unknown warning')}")
        
        logger.info("✅ Application initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Application initialization failed: {e}")
        return False

def create_application():
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # Create FastAPI application
        app = FastAPI(
            title="BFSI API",
            description="Banking, Financial Services, and Insurance API",
            version="2.0.0"
        )
        
        # Configure CORS
        cors_origins = os.getenv('CORS_ORIGINS', '[]')
        if cors_origins.startswith('[') and cors_origins.endswith(']'):
            # Parse JSON-like list
            import json
            try:
                origins = json.loads(cors_origins)
            except json.JSONDecodeError:
                origins = ["*"]
        else:
            origins = ["*"]
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=os.getenv('CORS_CREDENTIALS', 'true').lower() == 'true',
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )
        
        # Health check endpoint
        @app.get("/health")
        async def health_check():
            """Health check endpoint with validation status."""
            validation_status = get_validation_status()
            return {
                "status": "healthy",
                "environment": os.getenv('ENVIRONMENT', 'unknown'),
                "validation": {
                    "validated": validation_status['validated'],
                    "errors": len(validation_status['errors']),
                    "warnings": len(validation_status['warnings'])
                }
            }
        
        # Main API endpoint
        @app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "message": "BFSI API is running",
                "version": "2.0.0",
                "environment": os.getenv('ENVIRONMENT', 'unknown')
            }
        
        logger.info("✅ FastAPI application created successfully")
        return app
        
    except ImportError:
        logger.error("❌ FastAPI not available. Please install with: pip install fastapi uvicorn")
        return None
    except Exception as e:
        logger.error(f"❌ Failed to create application: {e}")
        return None

def main():
    """
    Main entry point for the application.
    """
    logger.info("🚀 Starting BFSI API...")
    
    # Initialize application with validation
    if not initialize_application():
        logger.error("❌ Application initialization failed. Exiting.")
        sys.exit(1)
    
    # Create FastAPI application
    app = create_application()
    if not app:
        logger.error("❌ Failed to create application. Exiting.")
        sys.exit(1)
    
    # Start the application
    try:
        import uvicorn
        
        # Get configuration from environment
        host = os.getenv('HOST', '127.0.0.1')
        port = int(os.getenv('PORT', 8000))
        workers = int(os.getenv('WORKERS', 1))
        log_level = os.getenv('LOG_LEVEL', 'info').lower()
        
        logger.info(f"🌐 Starting server on {host}:{port}")
        logger.info(f"📊 Workers: {workers}, Log Level: {log_level}")
        
        # Run the application
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=workers,
            log_level=log_level,
            access_log=os.getenv('ACCESS_LOG', 'true').lower() == 'true'
        )
        
    except ImportError:
        logger.error("❌ Uvicorn not available. Please install with: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
