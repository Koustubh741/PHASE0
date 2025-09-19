#!/usr/bin/env python3
"""
Service Status Checker for GRC Platform
Quickly checks if all services are running
"""

import requests
import time
import subprocess
import sys

def check_service(name, url, timeout=5):
    """Check if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True, f"✅ {name} is running (Status: {response.status_code})"
        else:
            return False, f"⚠️ {name} responded with status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"❌ {name} is not responding (Connection refused)"
    except requests.exceptions.Timeout:
        return False, f"⏰ {name} is not responding (Timeout)"
    except Exception as e:
        return False, f"❌ {name} error: {str(e)}"

def check_docker_containers():
    """Check Docker containers status"""
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print("🐳 Docker Containers:")
            for line in lines[1:]:  # Skip header
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print("❌ Docker not responding")
            return False
    except Exception as e:
        print(f"❌ Docker check error: {e}")
        return False

def main():
    """Check all services status"""
    print("🚀 GRC Platform Service Status Check")
    print("=" * 50)
    
    # Services to check
    services = [
        ("API Gateway", "http://localhost:8000/health"),
        ("AI Agents Service", "http://localhost:8005/health"),
        ("Frontend", "http://localhost:3000"),
    ]
    
    print("\n📡 Checking Services:")
    all_services_running = True
    
    for name, url in services:
        is_running, message = check_service(name, url)
        print(f"   {message}")
        if not is_running:
            all_services_running = False
    
    print("\n" + "=" * 50)
    
    # Check Docker containers
    check_docker_containers()
    
    print("\n" + "=" * 50)
    
    if all_services_running:
        print("🎉 All services are running!")
        print("\n🌐 Access URLs:")
        print("   Frontend: http://localhost:3000")
        print("   API Gateway: http://localhost:8000")
        print("   AI Agents: http://localhost:8005")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print("⚠️ Some services are not running yet.")
        print("   Services may still be starting up...")
        print("   Wait a moment and run this script again.")
    
    return 0 if all_services_running else 1

if __name__ == "__main__":
    exit(main())


