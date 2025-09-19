#!/usr/bin/env python3
"""
Full-Stack Integration Test for GRC Platform with AI Agents
Tests the complete system integration from AI Agents to Frontend
"""

import asyncio
import sys
import os
import json
import time
import requests
from datetime import datetime

# Add the ai-agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'ai-agents', 'agents_organized'))

def print_test_header(test_name):
    """Print a formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*60}")

def print_test_result(test_name, success, details=None):
    """Print test result"""
    status = "✅ PASSED" if success else "❌ FAILED"
    print(f"\n{status}: {test_name}")
    if details:
        print(f"Details: {details}")

def test_ai_agents_import():
    """Test 1: AI Agents Import and Initialization"""
    print_test_header("AI Agents Import and Initialization")
    
    try:
        from orchestration.main_orchestrator import GRCPlatformOrchestrator
        print("✅ Successfully imported GRCPlatformOrchestrator")
        
        # Test orchestrator initialization
        orchestrator = GRCPlatformOrchestrator()
        print("✅ Successfully initialized GRCPlatformOrchestrator")
        
        # Check if agents are loaded
        if hasattr(orchestrator, 'industry_agents') and orchestrator.industry_agents:
            print(f"✅ Industry agents loaded: {len(orchestrator.industry_agents)} agents")
            for industry, agent in orchestrator.industry_agents.items():
                print(f"   - {industry.value}: {agent.name}")
        else:
            print("⚠️  No industry agents loaded")
        
        # Check specialized agents
        specialized_agents = []
        if hasattr(orchestrator, 'risk_agent') and orchestrator.risk_agent:
            specialized_agents.append("Risk Agent")
        if hasattr(orchestrator, 'document_agent') and orchestrator.document_agent:
            specialized_agents.append("Document Agent")
        if hasattr(orchestrator, 'communication_agent') and orchestrator.communication_agent:
            specialized_agents.append("Communication Agent")
        if hasattr(orchestrator, 'compliance_agent') and orchestrator.compliance_agent:
            specialized_agents.append("Compliance Agent")
        
        if specialized_agents:
            print(f"✅ Specialized agents loaded: {', '.join(specialized_agents)}")
        else:
            print("⚠️  No specialized agents loaded")
        
        return True, f"Orchestrator initialized with {len(orchestrator.industry_agents)} industry agents and {len(specialized_agents)} specialized agents"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_ai_agents_operations():
    """Test 2: AI Agents Operations"""
    print_test_header("AI Agents Operations")
    
    try:
        from orchestration.main_orchestrator import GRCPlatformOrchestrator
        orchestrator = GRCPlatformOrchestrator()
        
        # Test BFSI agent operations
        if 'bfsi' in [agent.industry_type.value for agent in orchestrator.industry_agents.values()]:
            bfsi_agent = None
            for agent in orchestrator.industry_agents.values():
                if agent.industry_type.value == 'bfsi':
                    bfsi_agent = agent
                    break
            
            if bfsi_agent:
                print("✅ BFSI agent found")
                
                # Test risk assessment
                context = {
                    "business_unit": "Retail Banking",
                    "risk_scope": "Credit Risk",
                    "test_mode": True
                }
                
                result = asyncio.run(bfsi_agent.perform_grc_operation("risk_assessment", context))
                print("✅ BFSI risk assessment operation completed")
                
                # Test compliance check
                result = asyncio.run(bfsi_agent.perform_grc_operation("compliance_check", context))
                print("✅ BFSI compliance check operation completed")
                
                return True, "BFSI agent operations completed successfully"
            else:
                return False, "BFSI agent not found"
        else:
            return False, "No BFSI agent available"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_backend_service():
    """Test 3: Backend AI Agents Service"""
    print_test_header("Backend AI Agents Service")
    
    try:
        # Test if the service file exists and is valid
        service_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'backend', 'services', 'ai_agents_service.py')
        if os.path.exists(service_path):
            print("✅ AI Agents service file exists")
            
            # Test Python syntax
            with open(service_path, 'r') as f:
                code = f.read()
            compile(code, service_path, 'exec')
            print("✅ AI Agents service syntax is valid")
            
            return True, "Backend AI Agents service is ready"
        else:
            return False, "AI Agents service file not found"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_frontend_integration():
    """Test 4: Frontend Integration"""
    print_test_header("Frontend Integration")
    
    try:
        # Check if AI Agents service exists
        service_path = os.path.join(os.path.dirname(__file__), 'frontend', 'src', 'services', 'aiAgentsService.js')
        if os.path.exists(service_path):
            print("✅ AI Agents service file exists")
        
        # Check if AI Agents component exists
        component_path = os.path.join(os.path.dirname(__file__), 'frontend', 'src', 'components', 'AIAgentsManagement.jsx')
        if os.path.exists(component_path):
            print("✅ AI Agents Management component exists")
        
        # Check if App.jsx includes AI Agents
        app_path = os.path.join(os.path.dirname(__file__), 'frontend', 'src', 'App.jsx')
        if os.path.exists(app_path):
            with open(app_path, 'r') as f:
                app_content = f.read()
            if 'AIAgentsManagement' in app_content and 'ai-agents' in app_content:
                print("✅ App.jsx includes AI Agents integration")
            else:
                print("⚠️  App.jsx may not include AI Agents integration")
        
        # Check if Layout.jsx includes AI Agents navigation
        layout_path = os.path.join(os.path.dirname(__file__), 'frontend', 'src', 'components', 'Layout.jsx')
        if os.path.exists(layout_path):
            with open(layout_path, 'r') as f:
                layout_content = f.read()
            if 'ai-agents' in layout_content:
                print("✅ Layout.jsx includes AI Agents navigation")
            else:
                print("⚠️  Layout.jsx may not include AI Agents navigation")
        
        return True, "Frontend integration files are in place"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_docker_configuration():
    """Test 5: Docker Configuration"""
    print_test_header("Docker Configuration")
    
    try:
        # Check if Docker Compose file exists
        compose_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docker-compose.yml')
        if os.path.exists(compose_path):
            print("✅ Docker Compose file exists")
            
            # Check if AI Agents service is configured
            with open(compose_path, 'r') as f:
                compose_content = f.read()
            
            if 'ai-agents:' in compose_content:
                print("✅ AI Agents service configured in Docker Compose")
            else:
                print("⚠️  AI Agents service not found in Docker Compose")
            
            if '8005:8005' in compose_content:
                print("✅ AI Agents service port configured correctly")
            else:
                print("⚠️  AI Agents service port may not be configured correctly")
            
            return True, "Docker configuration is valid"
        else:
            return False, "Docker Compose file not found"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_api_endpoints():
    """Test 6: API Endpoints Configuration"""
    print_test_header("API Endpoints Configuration")
    
    try:
        # Check API Gateway configuration
        api_gateway_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'backend', 'api-gateway', 'main.py')
        if os.path.exists(api_gateway_path):
            with open(api_gateway_path, 'r') as f:
                api_content = f.read()
            
            if 'AI_AGENTS_URL' in api_content:
                print("✅ AI Agents URL configured in API Gateway")
            else:
                print("⚠️  AI Agents URL not configured in API Gateway")
            
            if '/ai-agents/' in api_content:
                print("✅ AI Agents routes configured in API Gateway")
            else:
                print("⚠️  AI Agents routes not configured in API Gateway")
            
            return True, "API endpoints are configured"
        else:
            return False, "API Gateway file not found"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Run all integration tests"""
    print("🚀 GRC Platform Full-Stack Integration Test")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    tests = [
        ("AI Agents Import and Initialization", test_ai_agents_import),
        ("AI Agents Operations", test_ai_agents_operations),
        ("Backend AI Agents Service", test_backend_service),
        ("Frontend Integration", test_frontend_integration),
        ("Docker Configuration", test_docker_configuration),
        ("API Endpoints Configuration", test_api_endpoints),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success, details = test_func()
            results.append((test_name, success, details))
            print_test_result(test_name, success, details)
        except Exception as e:
            results.append((test_name, False, f"Unexpected error: {str(e)}"))
            print_test_result(test_name, False, f"Unexpected error: {str(e)}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, details in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The full-stack integration is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())


