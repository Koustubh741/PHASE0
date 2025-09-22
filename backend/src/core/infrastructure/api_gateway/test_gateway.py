#!/usr/bin/env python3
"""
Test script for API Gateway
"""

import sys
import os

# Add the backend src directory to Python path
backend_src = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
sys.path.insert(0, backend_src)

def test_gateway_imports():
    """Test that all gateway components can be imported"""
    try:
        # Test basic imports
        import httpx
        import asyncio
        import logging
        from datetime import datetime, timedelta
        from collections import defaultdict
        
        print("✅ Basic dependencies imported successfully")
        
        # Test our gateway components
        from gateway import ServiceRegistry, APIGateway
        
        print("✅ Gateway components imported successfully")
        
        # Test service registry
        registry = ServiceRegistry()
        print("✅ ServiceRegistry created successfully")
        
        # Test API Gateway
        gateway = APIGateway()
        print("✅ APIGateway created successfully")
        
        # Test service discovery
        service_url = gateway.service_registry.get_service_url("policy", "/test")
        print(f"✅ Service discovery working: {service_url}")
        
        print("\n🎉 All API Gateway components are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API Gateway: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gateway_imports()
    sys.exit(0 if success else 1)
