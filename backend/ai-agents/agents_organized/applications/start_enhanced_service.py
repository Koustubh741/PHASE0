#!/usr/bin/env python3
"""
Enhanced Multi-LLM Service Startup Script
Provides easy startup with configuration validation and health checks
"""

import os
import sys
import argparse
import asyncio
import time
import requests
from typing import Dict, Any
import json

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'transformers',
        'torch',
        'fastapi',
        'uvicorn',
        'psutil',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required dependencies are installed")
    return True

def check_system_resources() -> Dict[str, Any]:
    """Check system resources and provide recommendations"""
    import psutil
    
    memory = psutil.virtual_memory()
    cpu_count = psutil.cpu_count()
    
    # Check if GPU is available
    try:
        import torch
        has_gpu = torch.cuda.is_available()
        gpu_count = torch.cuda.device_count() if has_gpu else 0
    except ImportError:
        has_gpu = False
        gpu_count = 0
    
    resources = {
        "total_memory_gb": round(memory.total / (1024**3), 2),
        "available_memory_gb": round(memory.available / (1024**3), 2),
        "memory_usage_percent": memory.percent,
        "cpu_count": cpu_count,
        "has_gpu": has_gpu,
        "gpu_count": gpu_count
    }
    
    print("🔍 System Resources:")
    print(f"   Memory: {resources['available_memory_gb']:.1f} GB available / {resources['total_memory_gb']:.1f} GB total")
    print(f"   CPU: {resources['cpu_count']} cores")
    print(f"   GPU: {'Available' if resources['has_gpu'] else 'Not available'} ({resources['gpu_count']} devices)")
    
    # Provide recommendations
    recommendations = []
    
    if resources['available_memory_gb'] < 4:
        recommendations.append("⚠️  Low memory available. Consider using only small models (TinyLlama, Gemma 2B)")
    elif resources['available_memory_gb'] < 8:
        recommendations.append("💡 Medium memory available. You can use small to medium models (Phi-2, Gemma 2B)")
    else:
        recommendations.append("✅ Good memory available. You can use large models (Llama 2, Mistral)")
    
    if not resources['has_gpu']:
        recommendations.append("💡 No GPU detected. Models will run on CPU (slower but functional)")
    else:
        recommendations.append("🚀 GPU available! Models will run faster with GPU acceleration")
    
    if recommendations:
        print("\n📋 Recommendations:")
        for rec in recommendations:
            print(f"   {rec}")
    
    return resources

def validate_configuration():
    """Validate service configuration"""
    print("\n🔧 Configuration Validation:")
    
    # Check environment variables
    config_vars = {
        "ENABLE_GPU": os.getenv("ENABLE_GPU", "false"),
        "MAX_CONCURRENT_MODELS": os.getenv("MAX_CONCURRENT_MODELS", "3"),
        "PORT": os.getenv("PORT", "8007"),
        "AUTO_UNLOAD_INACTIVE_MODELS": os.getenv("AUTO_UNLOAD_INACTIVE_MODELS", "true")
    }
    
    for var, value in config_vars.items():
        print(f"   {var}: {value}")
    
    # Validate port
    try:
        port = int(config_vars["PORT"])
        if port < 1024 or port > 65535:
            print(f"   ⚠️  Port {port} may require admin privileges")
    except ValueError:
        print(f"   ❌ Invalid port: {config_vars['PORT']}")
        return False
    
    # Validate max concurrent models
    try:
        max_models = int(config_vars["MAX_CONCURRENT_MODELS"])
        if max_models < 1 or max_models > 10:
            print(f"   ⚠️  MAX_CONCURRENT_MODELS should be between 1 and 10")
    except ValueError:
        print(f"   ❌ Invalid MAX_CONCURRENT_MODELS: {config_vars['MAX_CONCURRENT_MODELS']}")
        return False
    
    print("   ✅ Configuration is valid")
    return True

def create_sample_env_file():
    """Create a sample .env file with recommended settings"""
    env_content = """# Enhanced Multi-LLM Service Configuration

# GPU Configuration
ENABLE_GPU=false

# Resource Management
MAX_CONCURRENT_MODELS=3
AUTO_UNLOAD_INACTIVE_MODELS=true
INACTIVE_THRESHOLD_MINUTES=30

# Service Configuration
PORT=8007

# Model Configuration
DEFAULT_MODEL_NAME=tiny-llama
EMBEDDING_MODEL=all-minilm
"""
    
    env_file = ".env.enhanced"
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write(env_content)
        print(f"📝 Created sample configuration file: {env_file}")
        print("   Edit this file to customize your settings")
    else:
        print(f"📝 Configuration file already exists: {env_file}")

async def test_model_catalog():
    """Test the model catalog functionality"""
    print("\n📚 Testing Model Catalog:")
    
    try:
        from model_catalog import ModelCatalog, ModelType
        
        # Test catalog access
        all_models = ModelCatalog.get_available_models()
        print(f"   ✅ Model catalog loaded: {len(all_models)} models available")
        
        # Test model types
        small_models = ModelCatalog.get_models_by_type(ModelType.SMALL_LLM)
        large_models = ModelCatalog.get_models_by_type(ModelType.LARGE_LLM)
        
        print(f"   📊 Small LLMs: {len(small_models)}")
        print(f"   📊 Large LLMs: {len(large_models)}")
        
        # Test recommendations
        recommendation = ModelCatalog.get_recommended_model_for_task("Quick question and answer")
        if recommendation:
            print(f"   🎯 Sample recommendation: {recommendation.name}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Model catalog test failed: {e}")
        return False

def wait_for_service(port: int, timeout: int = 60):
    """Wait for the service to become available"""
    print(f"\n⏳ Waiting for service to start on port {port}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"   ✅ Service is healthy!")
                print(f"   📊 Status: {health_data.get('status', 'unknown')}")
                print(f"   🔄 Version: {health_data.get('version', 'unknown')}")
                print(f"   🤖 Loaded models: {len(health_data.get('loaded_models', []))}")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(".", end="", flush=True)
        time.sleep(2)
    
    print(f"\n   ❌ Service failed to start within {timeout} seconds")
    return False

def test_service_endpoints(port: int):
    """Test key service endpoints"""
    print(f"\n🧪 Testing Service Endpoints:")
    
    base_url = f"http://localhost:{port}"
    
    # Test models endpoint
    try:
        response = requests.get(f"{base_url}/models", timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            print(f"   ✅ /models: {len(models_data.get('models', {}))} models listed")
        else:
            print(f"   ❌ /models: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ /models: {e}")
    
    # Test recommendations endpoint
    try:
        payload = {"task_description": "Quick question and answer"}
        response = requests.post(f"{base_url}/models/recommend", json=payload, timeout=10)
        if response.status_code == 200:
            rec_data = response.json()
            primary = rec_data.get('primary_recommendation', {})
            if primary:
                print(f"   ✅ /models/recommend: {primary.get('model_info', {}).get('name', 'Unknown')} recommended")
        else:
            print(f"   ❌ /models/recommend: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ /models/recommend: {e}")
    
    # Test system status
    try:
        response = requests.get(f"{base_url}/system/status", timeout=10)
        if response.status_code == 200:
            status_data = response.json()
            resources = status_data.get('system_resources', {})
            print(f"   ✅ /system/status: {resources.get('available_memory_gb', 0):.1f} GB available")
        else:
            print(f"   ❌ /system/status: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ /system/status: {e}")

def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(description="Start Enhanced Multi-LLM Service")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 8007)), help="Service port")
    parser.add_argument("--skip-checks", action="store_true", help="Skip dependency and configuration checks")
    parser.add_argument("--test-only", action="store_true", help="Run tests only, don't start service")
    parser.add_argument("--create-config", action="store_true", help="Create sample configuration file")
    
    args = parser.parse_args()
    
    print("🚀 Enhanced Multi-LLM Service Startup")
    print("=" * 50)
    
    # Create configuration file if requested
    if args.create_config:
        create_sample_env_file()
        return
    
    # Run checks unless skipped
    if not args.skip_checks:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Check system resources
        resources = check_system_resources()
        
        # Validate configuration
        if not validate_configuration():
            print("❌ Configuration validation failed")
            sys.exit(1)
        
        # Test model catalog
        if not asyncio.run(test_model_catalog()):
            print("❌ Model catalog test failed")
            sys.exit(1)
    
    if args.test_only:
        print("✅ All tests passed!")
        return
    
    # Start the service
    print(f"\n🚀 Starting Enhanced Multi-LLM Service on port {args.port}...")
    
    # Set port environment variable
    os.environ["PORT"] = str(args.port)
    
    try:
        # Import and start the service
        import uvicorn
        from enhanced_huggingface_service import app
        
        # Start in a separate process
        import subprocess
        import threading
        
        def start_service():
            uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="info")
        
        # Start service in background
        service_thread = threading.Thread(target=start_service, daemon=True)
        service_thread.start()
        
        # Wait for service to be ready
        if wait_for_service(args.port):
            print(f"\n🎉 Enhanced Multi-LLM Service is running!")
            print(f"   🌐 API Documentation: http://localhost:{args.port}/docs")
            print(f"   🔍 Health Check: http://localhost:{args.port}/health")
            print(f"   📊 System Status: http://localhost:{args.port}/system/status")
            
            # Test endpoints
            test_service_endpoints(args.port)
            
            print(f"\n💡 Example usage:")
            print(f"   python usage_examples.py")
            print(f"   curl http://localhost:{args.port}/models")
            
            print(f"\n⏹️  Press Ctrl+C to stop the service")
            
            # Keep the main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n🛑 Service stopped by user")
        else:
            print("❌ Failed to start service")
            sys.exit(1)
            
    except ImportError as e:
        print(f"❌ Failed to import service: {e}")
        print("Make sure all dependencies are installed and the service files are in the current directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
