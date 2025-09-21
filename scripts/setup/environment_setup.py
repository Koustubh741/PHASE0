#!/usr/bin/env python3
"""
Environment setup script for GRC Platform.
This script sets up the development environment with all necessary dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed."""
    print("📦 Checking Node.js...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed. Please install Node.js 16 or higher")
    return False

def setup_python_environment():
    """Set up Python environment."""
    print("🐍 Setting up Python environment...")
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install requirements
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements-dev.txt", "Installing development dependencies"):
        return False
    
    return True

def setup_node_environment():
    """Set up Node.js environment."""
    print("📦 Setting up Node.js environment...")
    
    # Install frontend dependencies
    if not run_command("cd frontend && npm install", "Installing frontend dependencies"):
        return False
    
    return True

def setup_database():
    """Set up database."""
    print("🗄️ Setting up database...")
    
    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("✅ Docker is available")
        
        # Start database services
        if not run_command("docker-compose up -d postgres redis", "Starting database services"):
            return False
        
        # Wait for services to be ready
        print("⏳ Waiting for database services to be ready...")
        import time
        time.sleep(10)
        
        # Run database migrations
        if not run_command("cd backend && alembic upgrade head", "Running database migrations"):
            return False
        
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not available. Please install Docker and Docker Compose")
        print("📝 Manual setup required:")
        print("   1. Install PostgreSQL 12+")
        print("   2. Install Redis 6+")
        print("   3. Create database: grc_platform")
        print("   4. Run migrations: cd backend && alembic upgrade head")
        return False

def create_env_file():
    """Create environment file from template."""
    print("📝 Creating environment file...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✅ Created .env file from template")
        return True
    else:
        # Create basic .env file
        env_content = """# Database Configuration
DATABASE_URL=postgresql://grc_user:grc_password@localhost:5432/grc_platform
REDIS_URL=redis://localhost:6379/0

# Security Configuration
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Service Configuration
COMPLIANCE_PORT=8003
COMPLIANCE_HOST=0.0.0.0
RISK_PORT=8002
RISK_HOST=0.0.0.0
POLICY_PORT=8001
POLICY_HOST=0.0.0.0

# Vector Store Configuration
VECTOR_STORE_DIR=./vector_store
VECTOR_COLLECTION=compliance-policies

# Development Configuration
DEBUG=True
LOG_LEVEL=INFO
"""
        env_file.write_text(env_content)
        print("✅ Created basic .env file")
        return True

def run_tests():
    """Run tests to verify setup."""
    print("🧪 Running tests to verify setup...")
    
    # Run Python tests
    if not run_command("cd backend && python -m pytest tests/unit/ -v", "Running unit tests"):
        print("⚠️ Unit tests failed, but setup may still be functional")
    
    # Run frontend tests
    if not run_command("cd frontend && npm test -- --watchAll=false", "Running frontend tests"):
        print("⚠️ Frontend tests failed, but setup may still be functional")
    
    return True

def main():
    """Main setup function."""
    print("🚀 GRC Platform Environment Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Set up environments
    if not setup_python_environment():
        print("❌ Python environment setup failed")
        sys.exit(1)
    
    if not setup_node_environment():
        print("❌ Node.js environment setup failed")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("❌ Environment file creation failed")
        sys.exit(1)
    
    # Set up database
    if not setup_database():
        print("⚠️ Database setup failed, but you can set it up manually")
    
    # Run tests
    run_tests()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Review and update .env file with your configuration")
    print("   2. Start the development servers:")
    print("      - Backend: cd backend && python -m uvicorn src.api.main:app --reload")
    print("      - Frontend: cd frontend && npm start")
    print("   3. Visit http://localhost:3000 to see the application")

if __name__ == "__main__":
    main()
