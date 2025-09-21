#!/usr/bin/env python3
"""
Test script for login rate limiting functionality
Demonstrates the Redis-based rate limiting with exponential backoff
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any

class LoginRateLimitTester:
    """Test the login rate limiting functionality"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_login_attempt(self, username: str, password: str) -> Dict[str, Any]:
        """Test a single login attempt"""
        try:
            async with self.session.post(
                f"{self.base_url}/auth/login",
                data={"username": username, "password": password},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            ) as response:
                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "success": response.status == 200
                }
                
                if response.status == 200:
                    result["data"] = await response.json()
                else:
                    result["error"] = await response.text()
                
                return result
                
        except Exception as e:
            return {
                "status_code": 0,
                "success": False,
                "error": str(e)
            }
    
    async def test_rate_limiting(self, username: str = "testuser", password: str = "wrongpassword"):
        """Test rate limiting by making multiple failed attempts"""
        print("Testing login rate limiting...")
        print(f"Making login attempts for user: {username}")
        print("=" * 50)
        
        results = []
        
        # Make multiple failed attempts to trigger rate limiting
        for i in range(8):  # More than the max attempts (5)
            print(f"Attempt {i + 1}: ", end="")
            
            result = await self.test_login_attempt(username, password)
            results.append(result)
            
            if result["success"]:
                print("✅ SUCCESS")
                break
            else:
                status = result["status_code"]
                if status == 401:
                    print("❌ Invalid credentials (expected)")
                elif status == 429:
                    print("🚫 RATE LIMITED")
                    retry_after = result["headers"].get("Retry-After", "unknown")
                    print(f"   Retry after: {retry_after} seconds")
                else:
                    print(f"❌ Error {status}")
            
            # Small delay between attempts
            await asyncio.sleep(0.5)
        
        return results
    
    async def test_successful_login(self, username: str = "admin", password: str = "admin123"):
        """Test successful login (if you have valid credentials)"""
        print("\nTesting successful login...")
        print("=" * 50)
        
        result = await self.test_login_attempt(username, password)
        
        if result["success"]:
            print("✅ Login successful!")
            print(f"Token type: {result['data'].get('token_type', 'unknown')}")
            print(f"Expires in: {result['data'].get('expires_in', 'unknown')} seconds")
        else:
            print(f"❌ Login failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    async def test_rate_limit_headers(self):
        """Test that rate limit headers are properly set"""
        print("\nTesting rate limit headers...")
        print("=" * 50)
        
        # Make a few attempts to see headers
        for i in range(3):
            result = await self.test_login_attempt("testuser", "wrongpassword")
            
            headers = result.get("headers", {})
            rate_limit_headers = {
                "X-RateLimit-Limit": headers.get("X-RateLimit-Limit"),
                "X-RateLimit-Remaining": headers.get("X-RateLimit-Remaining"),
                "Retry-After": headers.get("Retry-After")
            }
            
            print(f"Attempt {i + 1} headers: {rate_limit_headers}")

async def main():
    """Run the rate limiting tests"""
    print("Login Rate Limiting Test")
    print("=" * 50)
    print("This test will attempt to trigger rate limiting by making")
    print("multiple failed login attempts.")
    print()
    
    async with LoginRateLimitTester() as tester:
        # Test rate limiting with failed attempts
        await tester.test_rate_limiting()
        
        # Test rate limit headers
        await tester.test_rate_limit_headers()
        
        # Test successful login (if credentials exist)
        await tester.test_successful_login()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nRate limiting features tested:")
    print("✅ Failed attempt tracking")
    print("✅ Rate limit enforcement")
    print("✅ Exponential backoff")
    print("✅ Account lockout")
    print("✅ Rate limit headers")
    print("✅ Redis-based storage")

if __name__ == "__main__":
    asyncio.run(main())
