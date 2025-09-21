#!/usr/bin/env python3
"""
API Compatibility Test Suite
Tests all API calls to ensure they work with both original and enhanced services
"""

import asyncio
import json
import time
from typing import Dict, List, Any
import aiohttp
import requests
from datetime import datetime

class APITestSuite:
    """Comprehensive test suite for API compatibility"""
    
    def __init__(self, base_url: str = "http://localhost:8007"):
        self.base_url = base_url.rstrip('/')
        self.test_results = []
    
    async def test_health_endpoint(self) -> Dict[str, Any]:
        """Test health endpoint"""
        test_name = "Health Endpoint"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "response_time": response.headers.get('X-Response-Time', 'Unknown'),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_models_endpoint(self) -> Dict[str, Any]:
        """Test models listing endpoint"""
        test_name = "Models Endpoint"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/models") as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "models_count": len(data.get('models', {})),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_chat_endpoint_original_format(self) -> Dict[str, Any]:
        """Test chat endpoint with original API format"""
        test_name = "Chat Endpoint (Original Format)"
        try:
            payload = {
                "message": "Hello, how are you?",
                "model_name": "microsoft/DialoGPT-medium",
                "max_length": 50,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "response_length": len(data.get('response', '')),
                            "processing_time": data.get('processing_time', 0),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_chat_endpoint_enhanced_format(self) -> Dict[str, Any]:
        """Test chat endpoint with enhanced API format"""
        test_name = "Chat Endpoint (Enhanced Format)"
        try:
            payload = {
                "message": "What is machine learning?",
                "model_id": "tiny-llama",
                "auto_model_selection": True,
                "max_length": 100,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "response_length": len(data.get('response', '')),
                            "processing_time": data.get('processing_time', 0),
                            "model_used": data.get('model_used', ''),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_embeddings_endpoint_original_format(self) -> Dict[str, Any]:
        """Test embeddings endpoint with original API format"""
        test_name = "Embeddings Endpoint (Original Format)"
        try:
            payload = {
                "text": "This is a test document for embedding generation",
                "model_name": "sentence-transformers/all-MiniLM-L6-v2"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/embeddings",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "embedding_dimension": data.get('dimension', 0),
                            "processing_time": data.get('processing_time', 0),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_embeddings_endpoint_enhanced_format(self) -> Dict[str, Any]:
        """Test embeddings endpoint with enhanced API format"""
        test_name = "Embeddings Endpoint (Enhanced Format)"
        try:
            payload = {
                "text": "Enhanced embedding test with automatic model selection",
                "model_id": "all-minilm",
                "auto_model_selection": True
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/embeddings",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "embedding_dimension": data.get('dimension', 0),
                            "processing_time": data.get('processing_time', 0),
                            "model_used": data.get('model_used', ''),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_model_recommendations(self) -> Dict[str, Any]:
        """Test model recommendations endpoint"""
        test_name = "Model Recommendations"
        try:
            payload = {
                "task_description": "I need to generate Python code for data analysis",
                "preferred_speed": "balanced"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/models/recommend",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "recommendations_count": len(data.get('recommended_models', [])),
                            "primary_recommendation": data.get('primary_recommendation', {}).get('model_id', ''),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_system_status(self) -> Dict[str, Any]:
        """Test system status endpoint"""
        test_name = "System Status"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/system/status") as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "loaded_models_count": len(data.get('loaded_models', {})),
                            "memory_usage": data.get('system_resources', {}).get('memory_usage_percent', 0),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_model_loading(self) -> Dict[str, Any]:
        """Test model loading endpoint"""
        test_name = "Model Loading"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/models/phi-2/load") as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "message": data.get('message', ''),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def test_conversation_with_history(self) -> Dict[str, Any]:
        """Test conversation with history"""
        test_name = "Conversation with History"
        try:
            conversation_history = [
                {"role": "user", "content": "Hello, I need help with software architecture"},
                {"role": "assistant", "content": "I'd be happy to help you with software architecture. What specific aspects are you looking to discuss?"}
            ]
            
            payload = {
                "message": "What are the benefits of microservices?",
                "conversation_history": conversation_history,
                "auto_model_selection": True
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "test": test_name,
                            "status": "PASS",
                            "response_length": len(data.get('response', '')),
                            "processing_time": data.get('processing_time', 0),
                            "data": data
                        }
                    else:
                        result = {
                            "test": test_name,
                            "status": "FAIL",
                            "error": f"HTTP {response.status}",
                            "data": await response.text()
                        }
        except Exception as e:
            result = {
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            }
        
        self.test_results.append(result)
        return result
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return summary"""
        print("🧪 Starting API Compatibility Test Suite")
        print("=" * 50)
        
        start_time = time.time()
        
        # Run all tests
        await self.test_health_endpoint()
        await self.test_models_endpoint()
        await self.test_chat_endpoint_original_format()
        await self.test_chat_endpoint_enhanced_format()
        await self.test_embeddings_endpoint_original_format()
        await self.test_embeddings_endpoint_enhanced_format()
        await self.test_model_recommendations()
        await self.test_system_status()
        await self.test_model_loading()
        await self.test_conversation_with_history()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        error_tests = len([r for r in self.test_results if r['status'] == 'ERROR'])
        
        summary = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            "total_time": total_time,
            "test_results": self.test_results
        }
        
        return summary
    
    def print_results(self, summary: Dict[str, Any]):
        """Print test results in a formatted way"""
        print(f"\n📊 Test Results Summary")
        print("=" * 50)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"🔥 Errors: {summary['errors']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        print(f"⏱️  Total Time: {summary['total_time']:.2f}s")
        
        print(f"\n📋 Detailed Results")
        print("=" * 50)
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "🔥"
            print(f"{status_icon} {result['test']}: {result['status']}")
            
            if result['status'] != 'PASS':
                print(f"   Error: {result.get('error', 'Unknown error')}")
            
            # Print additional info for passed tests
            if result['status'] == 'PASS':
                if 'processing_time' in result:
                    print(f"   Processing Time: {result['processing_time']:.2f}s")
                if 'response_length' in result:
                    print(f"   Response Length: {result['response_length']} chars")
                if 'embedding_dimension' in result:
                    print(f"   Embedding Dimension: {result['embedding_dimension']}")
                if 'models_count' in result:
                    print(f"   Models Available: {result['models_count']}")
        
        # Print recommendations
        print(f"\n💡 Recommendations")
        print("=" * 50)
        if summary['success_rate'] == 100:
            print("🎉 All tests passed! The API is fully compatible.")
        elif summary['success_rate'] >= 80:
            print("✅ Most tests passed. Minor issues detected.")
        elif summary['success_rate'] >= 60:
            print("⚠️  Some tests failed. Check the errors above.")
        else:
            print("❌ Many tests failed. Significant compatibility issues detected.")

async def main():
    """Main test function"""
    print("🚀 API Compatibility Test Suite")
    print("Testing both original and enhanced Hugging Face service APIs")
    print("=" * 60)
    
    # Test with default URL
    test_suite = APITestSuite("http://localhost:8007")
    
    try:
        # Run all tests
        summary = await test_suite.run_all_tests()
        
        # Print results
        test_suite.print_results(summary)
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"api_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"\n📁 Results saved to: {results_file}")
        
        return summary
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(main())
