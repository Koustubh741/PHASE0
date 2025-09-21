#!/usr/bin/env python3
"""
Start Local AI Services Script
Starts both Ollama and Hugging Face services locally
"""

import subprocess
import time
import os
import sys
import requests
from pathlib import Path

def get_ollama_path():
    """Get the Ollama executable path"""
    return Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"

def check_ollama_installed():
    """Check if Ollama is installed"""
    ollama_path = get_ollama_path()
    return ollama_path.exists()

def start_ollama_service():
    """Start Ollama service"""
    print("🦙 Starting Ollama service...")
    
    if not check_ollama_installed():
        print("❌ Ollama not found. Please install Ollama first.")
        return False
    
    ollama_path = get_ollama_path()
    
    try:
        # Start Ollama service in background
        subprocess.Popen([str(ollama_path), "serve"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait for service to start
        print("⏳ Waiting for Ollama to start...")
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    print("✅ Ollama service started successfully!")
                    return True
            except:
                time.sleep(1)
                print(f"   Waiting... ({i+1}/30)")
        
        print("❌ Ollama service failed to start within 30 seconds")
        return False
        
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def start_huggingface_service():
    """Start Hugging Face service"""
    print("🤗 Starting Hugging Face service...")
    
    try:
        # Start the simple Hugging Face service
        subprocess.Popen([sys.executable, "simple_huggingface_service.py"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait for service to start
        print("⏳ Waiting for Hugging Face service to start...")
        for i in range(15):  # Wait up to 15 seconds
            try:
                response = requests.get("http://localhost:8007/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Hugging Face service started successfully!")
                    return True
            except:
                time.sleep(1)
                print(f"   Waiting... ({i+1}/15)")
        
        print("❌ Hugging Face service failed to start within 15 seconds")
        return False
        
    except Exception as e:
        print(f"❌ Error starting Hugging Face service: {e}")
        return False

def check_services():
    """Check if both services are running"""
    print("\n🔍 Checking services status...")
    
    ollama_running = False
    hf_running = False
    
    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            ollama_running = True
            print("✅ Ollama service is running")
        else:
            print("❌ Ollama service is not responding")
    except:
        print("❌ Ollama service is not running")
    
    # Check Hugging Face
    try:
        response = requests.get("http://localhost:8007/health", timeout=5)
        if response.status_code == 200:
            hf_running = True
            print("✅ Hugging Face service is running")
        else:
            print("❌ Hugging Face service is not responding")
    except:
        print("❌ Hugging Face service is not running")
    
    return ollama_running and hf_running

def main():
    """Main function"""
    print("🚀 Starting Local AI Services for GRC Platform")
    print("=" * 60)
    
    # Check if services are already running
    if check_services():
        print("✅ Both services are already running!")
        return
    
    # Start services
    ollama_ok = start_ollama_service()
    hf_ok = start_huggingface_service()
    
    # Final check
    if ollama_ok and hf_ok:
        print("\n🎉 All AI services are now running!")
        print("\nService URLs:")
        print("  • Ollama API: http://localhost:11434")
        print("  • Hugging Face API: http://localhost:8007")
        print("\nYou can now use these services in your GRC Platform.")
    else:
        print("\n⚠️  Some services failed to start. Please check the logs.")

if __name__ == "__main__":
    main()



