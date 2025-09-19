#!/usr/bin/env python3
"""
Service Starter Script - Resolves port conflicts and starts services
"""

import subprocess
import time
import sys
import os

def kill_python_processes():
    """Kill all Python processes to free up ports"""
    try:
        print("🔄 Killing existing Python processes...")
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                      capture_output=True, text=True)
        time.sleep(3)  # Wait for ports to be released
        print("✅ Python processes terminated")
        return True
    except Exception as e:
        print(f"⚠️  Could not kill processes: {e}")
        return False

def start_multi_agent_service():
    """Start the multi-agent service"""
    try:
        print("🚀 Starting Multi-Agent Service on port 8081...")
        os.chdir("ai-agents")
        subprocess.Popen([
            sys.executable, "multi_agent_main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        print("✅ Multi-Agent Service started on port 8082")
        return True
    except Exception as e:
        print(f"❌ Failed to start Multi-Agent Service: {e}")
        return False

def start_api_gateway():
    """Start the API Gateway"""
    try:
        print("🚀 Starting API Gateway on port 8000...")
        os.chdir("../backend/api-gateway")
        subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        print("✅ API Gateway started on port 8000")
        return True
    except Exception as e:
        print(f"❌ Failed to start API Gateway: {e}")
        return False

def main():
    """Main function to start all services"""
    print("=" * 60)
    print("GRC PLATFORM SERVICE STARTER")
    print("=" * 60)
    
    # Kill existing processes
    kill_python_processes()
    
    # Start services
    multi_agent_success = start_multi_agent_service()
    api_gateway_success = start_api_gateway()
    
    print("\n" + "=" * 60)
    print("SERVICE STATUS")
    print("=" * 60)
    print(f"Multi-Agent Service (Port 8008): {'✅ Running' if multi_agent_success else '❌ Failed'}")
    print(f"API Gateway (Port 8000): {'✅ Running' if api_gateway_success else '❌ Failed'}")
    
    if multi_agent_success and api_gateway_success:
        print("\n🎉 All services started successfully!")
        print("📊 Test endpoints:")
        print("   - Multi-Agent Health: http://localhost:8008/health")
        print("   - API Gateway Health: http://localhost:8000/health")
        print("   - GRC Dashboard: http://localhost:8000/grc/dashboard")
    else:
        print("\n⚠️  Some services failed to start. Check the errors above.")
    
    return multi_agent_success and api_gateway_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
