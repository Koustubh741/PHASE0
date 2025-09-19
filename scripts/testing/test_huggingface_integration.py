#!/usr/bin/env python3
"""
Test script for Hugging Face Transformers integration
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime

class HuggingFaceTester:
    def __init__(self, base_url="http://localhost:8007"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_health(self):
        """Test health endpoint"""
        print("🔍 Testing health endpoint...")
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check passed: {data['status']}")
                    print(f"   Loaded models: {data['loaded_models']}")
                    return True
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    async def test_models(self):
        """Test models endpoint"""
        print("\n🔍 Testing models endpoint...")
        try:
            async with self.session.get(f"{self.base_url}/models") as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("models", [])
                    print(f"✅ Models endpoint working: {len(models)} models loaded")
                    for model in models:
                        print(f"   - {model['model_name']} ({model['model_type']})")
                    return True
                else:
                    print(f"❌ Models endpoint failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Models endpoint error: {e}")
            return False
    
    async def test_chat(self):
        """Test chat functionality"""
        print("\n🔍 Testing chat functionality...")
        try:
            payload = {
                "message": "Hello, how are you?",
                "max_length": 50,
                "temperature": 0.7
            }
            
            start_time = time.time()
            async with self.session.post(
                f"{self.base_url}/chat",
                json=payload
            ) as response:
                end_time = time.time()
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Chat test passed")
                    print(f"   Response: {data['response']}")
                    print(f"   Model used: {data['model_used']}")
                    print(f"   Processing time: {data['processing_time']:.2f}s")
                    print(f"   Total time: {end_time - start_time:.2f}s")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Chat test failed: {response.status} - {error_text}")
                    return False
        except Exception as e:
            print(f"❌ Chat test error: {e}")
            return False
    
    async def test_embeddings(self):
        """Test embeddings functionality"""
        print("\n🔍 Testing embeddings functionality...")
        try:
            payload = {
                "text": "This is a test sentence for embedding generation."
            }
            
            start_time = time.time()
            async with self.session.post(
                f"{self.base_url}/embeddings",
                json=payload
            ) as response:
                end_time = time.time()
                
                if response.status == 200:
                    data = await response.json()
                    embedding = data['embedding']
                    print(f"✅ Embeddings test passed")
                    print(f"   Model used: {data['model_used']}")
                    print(f"   Embedding dimension: {data['dimension']}")
                    print(f"   First 5 values: {embedding[:5]}")
                    print(f"   Processing time: {end_time - start_time:.2f}s")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Embeddings test failed: {response.status} - {error_text}")
                    return False
        except Exception as e:
            print(f"❌ Embeddings test error: {e}")
            return False
    
    async def test_conversation(self):
        """Test conversation with history"""
        print("\n🔍 Testing conversation with history...")
        try:
            # First message
            payload1 = {
                "message": "My name is John. What's your name?",
                "max_length": 50
            }
            
            async with self.session.post(
                f"{self.base_url}/chat",
                json=payload1
            ) as response1:
                if response1.status != 200:
                    print(f"❌ First message failed: {response1.status}")
                    return False
                
                data1 = await response1.json()
                print(f"   First response: {data1['response']}")
            
            # Second message with conversation history
            payload2 = {
                "message": "What's my name?",
                "max_length": 50,
                "conversation_history": [
                    {"role": "user", "content": "My name is John. What's your name?"},
                    {"role": "assistant", "content": data1['response']}
                ]
            }
            
            async with self.session.post(
                f"{self.base_url}/chat",
                json=payload2
            ) as response2:
                if response2.status == 200:
                    data2 = await response2.json()
                    print(f"✅ Conversation test passed")
                    print(f"   Second response: {data2['response']}")
                    return True
                else:
                    error_text = await response2.text()
                    print(f"❌ Conversation test failed: {response2.status} - {error_text}")
                    return False
        except Exception as e:
            print(f"❌ Conversation test error: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Hugging Face Transformers Integration Tests")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health),
            ("Models List", self.test_models),
            ("Chat Generation", self.test_chat),
            ("Embeddings", self.test_embeddings),
            ("Conversation", self.test_conversation)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Results Summary:")
        print("=" * 60)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:<20} {status}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Hugging Face integration is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the service logs for details.")
        
        return passed == total

async def main():
    """Main test function"""
    print(f"Testing Hugging Face service at: http://localhost:8007")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    async with HuggingFaceTester() as tester:
        success = await tester.run_all_tests()
        return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Test runner failed: {e}")
        exit(1)


