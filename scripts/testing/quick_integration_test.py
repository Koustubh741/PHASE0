#!/usr/bin/env python3
"""
Quick Integration Test for GRC Platform
Fast validation without heavy AI operations
"""

import os
import sys

def print_test_header(test_name):
    """Print a formatted test header"""
    print(f"\n🧪 {test_name}")

def print_test_result(test_name, success, details=None):
    """Print test result"""
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")

def test_file_structure():
    """Test 1: File Structure Validation"""
    print_test_header("File Structure Validation")
    
    required_files = [
        "src/ai-agents/agents_organized/orchestration/main_orchestrator.py",
        "src/backend/services/ai_agents_service.py",
        "src/frontend/src/services/aiAgentsService.js",
        "src/frontend/src/components/AIAgentsManagement.jsx",
        "docker-compose.yml"
    ]
    
    results = []
    for file_path in required_files:
        exists = os.path.exists(file_path)
        results.append((file_path, exists))
        print_test_result(f"File: {file_path}", exists)
    
    return all(exists for _, exists in results)

def test_imports():
    """Test 2: Import Validation (without initialization)"""
    print_test_header("Import Validation")
    
    try:
        # Add the ai-agents directory to the path
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'ai-agents', 'agents_organized'))
        
        # Test imports without initialization
        from orchestration.main_orchestrator import GRCPlatformOrchestrator
        print_test_result("Import GRCPlatformOrchestrator", True)
        
        from shared_components.industry_agent import IndustryAgent
        print_test_result("Import IndustryAgent", True)
        
        from bfsi_agent.bfsi_grc_agent import BFSIGRCAgent
        print_test_result("Import BFSIGRCAgent", True)
        
        return True
        
    except Exception as e:
        print_test_result("Import Validation", False, str(e))
        return False

def test_docker_config():
    """Test 3: Docker Configuration Validation"""
    print_test_header("Docker Configuration Validation")
    
    try:
        compose_path = "docker-compose.yml"
        if not os.path.exists(compose_path):
            print_test_result("Docker Compose file", False, "File not found")
            return False
        
        with open(compose_path, 'r') as f:
            content = f.read()
        
        checks = [
            ("AI Agents service", "ai-agents:" in content),
            ("AI Agents port", "AI_AGENTS_PORT:-8005" in content),
            ("AI Agents build context", "context: ." in content),
            ("AI Agents dockerfile", "dockerfile: deployment/docker/services/Dockerfile.ai-agents" in content)
        ]
        
        all_passed = True
        for check_name, passed in checks:
            print_test_result(check_name, passed)
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test_result("Docker Configuration", False, str(e))
        return False

def test_frontend_integration():
    """Test 4: Frontend Integration Validation"""
    print_test_header("Frontend Integration Validation")
    
    try:
        # Check App.jsx
        app_path = "src/frontend/src/App.jsx"
        if os.path.exists(app_path):
            with open(app_path, 'r') as f:
                app_content = f.read()
            
            app_checks = [
                ("AIAgentsManagement import", "AIAgentsManagement" in app_content),
                ("AI Agents case", "'ai-agents'" in app_content)
            ]
            
            for check_name, passed in app_checks:
                print_test_result(f"App.jsx: {check_name}", passed)
        else:
            print_test_result("App.jsx file", False, "File not found")
            return False
        
        # Check Layout.jsx
        layout_path = "src/frontend/src/components/Layout.jsx"
        if os.path.exists(layout_path):
            with open(layout_path, 'r') as f:
                layout_content = f.read()
            
            layout_checks = [
                ("AI Agents navigation", "'ai-agents'" in layout_content)
            ]
            
            for check_name, passed in layout_checks:
                print_test_result(f"Layout.jsx: {check_name}", passed)
        else:
            print_test_result("Layout.jsx file", False, "File not found")
            return False
        
        return True
        
    except Exception as e:
        print_test_result("Frontend Integration", False, str(e))
        return False

def main():
    """Run quick integration tests"""
    print("🚀 GRC Platform Quick Integration Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Import Validation", test_imports),
        ("Docker Configuration", test_docker_config),
        ("Frontend Integration", test_frontend_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            results.append((test_name, False))
            print_test_result(test_name, False, f"Unexpected error: {str(e)}")
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 QUICK TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Quick validation passed! Integration is ready.")
        return 0
    else:
        print("⚠️  Some validations failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())


