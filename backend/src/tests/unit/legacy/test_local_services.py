#!/usr/bin/env python3
"""
Test script for local Ollama and Hugging Face services
"""

import requests
import subprocess
import time
import json

def test_ollama_service():
    """Test Ollama service"""
    print("Testing Ollama service...")
    try:
        # Test Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama service is running. Available models: {[m['name'] for m in models.get('models', [])]}")
            return True
        else:
            print(f"❌ Ollama service returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama service test failed: {e}")
        return False

def test_huggingface_service():
    """Test Hugging Face service"""
    print("Testing Hugging Face service...")
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8007/health", timeout=30)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Hugging Face service is running. Loaded models: {health_data.get('loaded_models', [])}")
            return True
        else:
            print(f"❌ Hugging Face service returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Hugging Face service test failed: {e}")
        return False

def test_ollama_chat():
    """Test Ollama chat functionality"""
    print("Testing Ollama chat...")
    try:
        chat_data = {
            "model": "llama2",
            "prompt": "Hello, how are you?",
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/generate", 
                               json=chat_data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama chat working. Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Ollama chat failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama chat test failed: {e}")
        return False

def test_huggingface_chat():
    """Test Hugging Face chat functionality"""
    print("Testing Hugging Face chat...")
    try:
        chat_data = {
            "message": "Hello, how are you?",
            "model_name": "microsoft/DialoGPT-medium",
            "max_length": 50,
            "temperature": 0.7
        }
        response = requests.post("http://localhost:8007/chat", 
                               json=chat_data, timeout=120)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Hugging Face chat working. Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Hugging Face chat failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Hugging Face chat test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Local AI Services")
    print("=" * 50)
    
    # Wait a moment for services to start
    print("Waiting for services to start...")
    time.sleep(5)
    
    results = []
    
    # Test services
    results.append(("Ollama Service", test_ollama_service()))
    results.append(("Hugging Face Service", test_huggingface_service()))
    
    # Test chat functionality
    results.append(("Ollama Chat", test_ollama_chat()))
    results.append(("Hugging Face Chat", test_huggingface_chat()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All services are working correctly!")
    else:
        print("⚠️  Some services need attention.")

if __name__ == "__main__":
    main()



