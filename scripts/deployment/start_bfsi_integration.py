#!/usr/bin/env python3
"""
BFSI Frontend-Backend Integration Startup Script
This script starts both the backend API server and frontend development server
for the BFSI GRC Platform integration testing.
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def run_backend():
    """Start the backend API server"""
    print("🚀 Starting BFSI Backend API Server...")
    backend_dir = Path("backend/ai-agents/agents_organized/applications")
    
    try:
        # Start the FastAPI backend
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], cwd=backend_dir)
        
        print("✅ Backend API server started on http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def run_frontend():
    """Start the frontend development server"""
    print("🎨 Starting BFSI Frontend Development Server...")
    frontend_dir = Path("frontend")
    
    try:
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Start the React development server
        process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir)
        
        print("✅ Frontend development server starting on http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def check_services():
    """Check if services are running"""
    import requests
    
    services = [
        ("Backend API", "http://localhost:8000/grc/status"),
        ("Frontend", "http://localhost:3000")
    ]
    
    print("\n🔍 Checking service status...")
    for name, url in services:
        try:
            if "8000" in url:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: Running")
                else:
                    print(f"⚠️ {name}: Responding but status {response.status_code}")
            else:
                # For frontend, just check if it's accessible
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: Running")
                else:
                    print(f"⚠️ {name}: Responding but status {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"❌ {name}: Not accessible")

def main():
    """Main function to start both services"""
    print("🏦 BFSI GRC Platform Integration Test")
    print("=" * 50)
    
    # Start backend
    backend_process = run_backend()
    if not backend_process:
        print("❌ Cannot continue without backend")
        return
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Start frontend
    frontend_process = run_frontend()
    if not frontend_process:
        print("❌ Cannot continue without frontend")
        backend_process.terminate()
        return
    
    # Wait for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(10)
    
    # Check service status
    check_services()
    
    print("\n🎉 BFSI GRC Platform Integration is ready!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n💡 Features Available:")
    print("   • BFSI-specific dashboard")
    print("   • Industry standard policy toggle")
    print("   • Policy management")
    print("   • Real-time BFSI agent monitoring")
    print("   • No mock data - ready for real data integration")
    
    print("\n⌨️  Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        print("👋 BFSI GRC Platform integration test completed!")

if __name__ == "__main__":
    main()
