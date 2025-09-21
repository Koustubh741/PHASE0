#!/usr/bin/env python3
"""
Service startup script for GRC Platform.
This script starts all necessary services for development.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class ServiceManager:
    """Manages GRC Platform services."""
    
    def __init__(self):
        self.processes = []
        self.running = True
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\n🛑 Shutting down services...")
        self.running = False
        self.stop_all_services()
        sys.exit(0)
    
    def start_service(self, name, command, cwd=None):
        """Start a service."""
        print(f"🚀 Starting {name}...")
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append((name, process))
            print(f"✅ {name} started (PID: {process.pid})")
            return True
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return False
    
    def stop_all_services(self):
        """Stop all running services."""
        for name, process in self.processes:
            print(f"🛑 Stopping {name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️ {name} didn't stop gracefully, forcing...")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
    
    def monitor_services(self):
        """Monitor running services."""
        while self.running:
            for name, process in self.processes:
                if process.poll() is not None:
                    print(f"⚠️ {name} has stopped unexpectedly")
                    # Optionally restart the service
                    # self.restart_service(name, process)
            time.sleep(5)
    
    def start_backend_services(self):
        """Start backend services."""
        print("🔧 Starting backend services...")
        
        # Start Policy Service
        self.start_service(
            "Policy Service",
            "python -m uvicorn src.core.infrastructure.external_services.policy_service:app --host 0.0.0.0 --port 8001",
            cwd="backend"
        )
        
        # Start Risk Service
        self.start_service(
            "Risk Service", 
            "python -m uvicorn src.core.infrastructure.external_services.risk_service:app --host 0.0.0.0 --port 8002",
            cwd="backend"
        )
        
        # Start Compliance Service
        self.start_service(
            "Compliance Service",
            "python -m uvicorn src.core.infrastructure.external_services.compliance_service:app --host 0.0.0.0 --port 8003",
            cwd="backend"
        )
        
        # Start AI Agents Service
        self.start_service(
            "AI Agents Service",
            "python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8005",
            cwd="backend/ai-agents"
        )
    
    def start_frontend(self):
        """Start frontend service."""
        print("🎨 Starting frontend...")
        self.start_service(
            "Frontend",
            "npm start",
            cwd="frontend"
        )
    
    def start_database_services(self):
        """Start database services."""
        print("🗄️ Starting database services...")
        
        # Check if Docker is available
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            
            # Start PostgreSQL and Redis
            self.start_service(
                "Database Services",
                "docker-compose up postgres redis",
                cwd="."
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ Docker not available. Please start PostgreSQL and Redis manually.")
            print("   PostgreSQL: Ensure it's running on localhost:5432")
            print("   Redis: Ensure it's running on localhost:6379")
    
    def check_dependencies(self):
        """Check if all dependencies are available."""
        print("🔍 Checking dependencies...")
        
        # Check Python
        try:
            subprocess.run(["python", "--version"], check=True, capture_output=True)
            print("✅ Python is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Python is not available")
            return False
        
        # Check Node.js
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
            print("✅ Node.js is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js is not available")
            return False
        
        # Check if virtual environment exists
        if not Path("venv").exists():
            print("❌ Virtual environment not found. Run setup script first.")
            return False
        
        print("✅ All dependencies are available")
        return True
    
    def run(self):
        """Run all services."""
        print("🚀 GRC Platform Service Manager")
        print("=" * 50)
        
        if not self.check_dependencies():
            print("❌ Dependency check failed")
            sys.exit(1)
        
        # Start database services
        self.start_database_services()
        
        # Wait for database to be ready
        print("⏳ Waiting for database services to be ready...")
        time.sleep(10)
        
        # Start backend services
        self.start_backend_services()
        
        # Start frontend
        self.start_frontend()
        
        print("\n🎉 All services started!")
        print("\n📋 Service URLs:")
        print("   Frontend: http://localhost:3000")
        print("   Policy Service: http://localhost:8001")
        print("   Risk Service: http://localhost:8002")
        print("   Compliance Service: http://localhost:8003")
        print("   AI Agents Service: http://localhost:8005")
        print("\nPress Ctrl+C to stop all services")
        
        # Monitor services
        try:
            self.monitor_services()
        except KeyboardInterrupt:
            self.stop_all_services()

def main():
    """Main function."""
    manager = ServiceManager()
    manager.run()

if __name__ == "__main__":
    main()