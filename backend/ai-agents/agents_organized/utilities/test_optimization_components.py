"""
Test Optimization Components
Simple test script to verify all optimization components are working
"""

import sys
import traceback

def test_imports():
    """Test all optimization component imports"""
    print("🧪 Testing Optimization Components...")
    
    tests = [
        ("SimpleVectorStore", "from simple_vector_store import SimpleVectorStore; print('✅ Simple Vector Store ready')"),
        ("Redis", "import redis; print('✅ Redis ready')"),
        ("PostgreSQL", "import psycopg2; print('✅ PostgreSQL ready')"),
        ("FastAPI", "import fastapi; print('✅ FastAPI ready')"),
        ("Uvicorn", "import uvicorn; print('✅ Uvicorn ready')"),
        ("OpenAI", "import openai; print('✅ OpenAI ready')"),
        ("LangChain", "import langchain; print('✅ LangChain ready')"),
        ("SimpleVectorStore", "from simple_vector_store import SimpleVectorStore; print('✅ Simple Vector Store ready')"),
    ]
    
    results = {}
    
    for name, test_code in tests:
        try:
            exec(test_code)
            results[name] = "✅ PASS"
        except Exception as e:
            results[name] = f"❌ FAIL: {str(e)}"
            print(f"❌ {name} failed: {str(e)}")
    
    print("\n📊 Test Results:")
    for name, result in results.items():
        print(f"  {result}")
    
    return results

def test_optimization_files():
    """Test optimization file imports"""
    print("\n🔧 Testing Optimization Files...")
    
    files_to_test = [
        "agent_integration_layer",
        "ollama_enhanced_agents", 
        "chroma_enhanced_agents",
        "migration_strategy",
        "backward_compatibility_layer",
        "performance_monitoring"
    ]
    
    results = {}
    
    for file_name in files_to_test:
        try:
            module = __import__(file_name)
            results[file_name] = "✅ PASS"
            print(f"✅ {file_name} imported successfully")
        except Exception as e:
            results[file_name] = f"❌ FAIL: {str(e)}"
            print(f"❌ {file_name} failed: {str(e)}")
            # Print detailed error for debugging
            traceback.print_exc()
    
    return results

def test_basic_functionality():
    """Test basic functionality of optimization components"""
    print("\n⚡ Testing Basic Functionality...")
    
    try:
        # Test Simple Vector Store basic functionality
        from simple_vector_store import SimpleVectorStore
        store = SimpleVectorStore("test")
        print("✅ Simple Vector Store created")
        
        # Test Redis basic functionality
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        print("✅ Redis client created")
        
        # Test FastAPI basic functionality
        from fastapi import FastAPI
        app = FastAPI()
        print("✅ FastAPI app created")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 GRC Platform Optimization Components Test")
    print("=" * 50)
    
    # Test imports
    import_results = test_imports()
    
    # Test optimization files
    file_results = test_optimization_files()
    
    # Test basic functionality
    functionality_result = test_basic_functionality()
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 30)
    
    total_tests = len(import_results) + len(file_results) + 1
    passed_tests = sum(1 for r in import_results.values() if "✅" in r) + \
                   sum(1 for r in file_results.values() if "✅" in r) + \
                   (1 if functionality_result else 0)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! System is ready for deployment.")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
