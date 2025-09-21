#!/usr/bin/env python3
"""
Security Testing Script for BFSI API
Comprehensive security testing for BFSI compliance
"""

import asyncio
import httpx
import json
import time
import os
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityTester:
    """Comprehensive security testing for BFSI API"""
    
    def __init__(self, base_url: str = "http://localhost:8009", config_file: Optional[str] = None):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
        self.config_file = config_file or "security_test_config.json"
        self.credentials = self._load_credentials()
    
    def _load_credentials(self) -> Dict[str, Dict[str, str]]:
        """Load test credentials from environment variables or config file"""
        credentials = {}
        
        # Try to load from environment variables first
        env_credentials = {
            "admin": {
                "username": os.getenv("SECURITY_TEST_ADMIN_USER", "admin"),
                "password": os.getenv("SECURITY_TEST_ADMIN_PASS", "admin123")
            },
            "compliance": {
                "username": os.getenv("SECURITY_TEST_COMPLIANCE_USER", "compliance"),
                "password": os.getenv("SECURITY_TEST_COMPLIANCE_PASS", "comp123")
            },
            "risk": {
                "username": os.getenv("SECURITY_TEST_RISK_USER", "risk"),
                "password": os.getenv("SECURITY_TEST_RISK_PASS", "risk123")
            }
        }
        
        # Try to load from config file if it exists
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    credentials = file_config.get("test_credentials", env_credentials)
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to load config file {self.config_file}: {e}")
                credentials = env_credentials
        else:
            credentials = env_credentials
        
        return credentials
    
    async def close(self):
        """Properly close the HTTP client to prevent resource leaks"""
        if self.client and not self.client.is_closed:
            await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with proper cleanup"""
        await self.close()
    
    async def test_authentication(self):
        """Test authentication and authorization"""
        logger.info("Testing authentication...")
        
        # Test 1: Login with valid credentials
        try:
            response = await self.client.post(
                f"{self.base_url}/auth/login",
                data={"username": self.credentials["admin"]["username"], "password": self.credentials["admin"]["password"]}
            )
            assert response.status_code == 200
            token_data = response.json()
            assert "access_token" in token_data
            assert "refresh_token" in token_data
            self.test_results.append({"test": "valid_login", "status": "PASS"})
        except Exception as e:
            self.test_results.append({"test": "valid_login", "status": "FAIL", "error": str(e)})
        
        # Test 2: Login with invalid credentials
        try:
            response = await self.client.post(
                f"{self.base_url}/auth/login",
                data={"username": "invalid", "password": "invalid"}
            )
            assert response.status_code == 401
            self.test_results.append({"test": "invalid_login", "status": "PASS"})
        except Exception as e:
            self.test_results.append({"test": "invalid_login", "status": "FAIL", "error": str(e)})
        
        # Test 3: Access protected endpoint without token
        try:
            response = await self.client.get(f"{self.base_url}/status")
            assert response.status_code == 401
            self.test_results.append({"test": "no_token_access", "status": "PASS"})
        except Exception as e:
            self.test_results.append({"test": "no_token_access", "status": "FAIL", "error": str(e)})
    
    async def test_rate_limiting(self):
        """Test rate limiting functionality"""
        logger.info("Testing rate limiting...")
        
        # Get valid token first
        try:
            response = await self.client.post(
                f"{self.base_url}/auth/login",
                data={"username": self.credentials["admin"]["username"], "password": self.credentials["admin"]["password"]}
            )
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test rate limiting by making many requests
            for i in range(150):  # Exceed rate limit
                response = await self.client.get(
                    f"{self.base_url}/health",
                    headers=headers
                )
                if response.status_code == 429:
                    self.test_results.append({"test": "rate_limiting", "status": "PASS"})
                    break
            else:
                self.test_results.append({"test": "rate_limiting", "status": "FAIL", "error": "Rate limit not triggered"})
                
        except Exception as e:
            self.test_results.append({"test": "rate_limiting", "status": "FAIL", "error": str(e)})
    
    async def test_input_validation(self):
        """Test input validation and sanitization"""
        logger.info("Testing input validation...")
        
        # Get valid token
        try:
            response = await self.client.post(
                f"{self.base_url}/auth/login",
                data={"username": self.credentials["admin"]["username"], "password": self.credentials["admin"]["password"]}
            )
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test 1: Valid transaction request
            valid_transaction = {
                "amount": 100.50,
                "customer_id": "CUST001",
                "transaction_type": "debit",
                "location": "New York, NY"
            }
            response = await self.client.post(
                f"{self.base_url}/transactions",
                json=valid_transaction,
                headers=headers
            )
            assert response.status_code in [200, 201]
            self.test_results.append({"test": "valid_transaction", "status": "PASS"})
            
            # Test 2: Invalid transaction request (negative amount)
            invalid_transaction = {
                "amount": -100.50,
                "customer_id": "CUST001",
                "transaction_type": "debit",
                "location": "New York, NY"
            }
            response = await self.client.post(
                f"{self.base_url}/transactions",
                json=invalid_transaction,
                headers=headers
            )
            assert response.status_code == 422  # Validation error
            self.test_results.append({"test": "invalid_transaction", "status": "PASS"})
            
            # Test 3: XSS attempt
            xss_payload = {
                "amount": 100.50,
                "customer_id": "<script>alert('xss')</script>",
                "transaction_type": "debit",
                "location": "New York, NY"
            }
            response = await self.client.post(
                f"{self.base_url}/transactions",
                json=xss_payload,
                headers=headers
            )
            # Should be rejected by validation
            assert response.status_code == 422
            self.test_results.append({"test": "xss_prevention", "status": "PASS"})
            
        except Exception as e:
            self.test_results.append({"test": "input_validation", "status": "FAIL", "error": str(e)})
    
    async def test_authorization(self):
        """Test role-based access control"""
        logger.info("Testing authorization...")
        
        # Test with different user roles
        test_users = [
            {"username": self.credentials["admin"]["username"], "password": self.credentials["admin"]["password"], "role": "admin"},
            {"username": self.credentials["compliance"]["username"], "password": self.credentials["compliance"]["password"], "role": "compliance_officer"},
            {"username": self.credentials["risk"]["username"], "password": self.credentials["risk"]["password"], "role": "risk_manager"}
        ]
        
        for user in test_users:
            try:
                # Login
                response = await self.client.post(
                    f"{self.base_url}/auth/login",
                    json={"username": user["username"], "password": user["password"]}
                )
                token = response.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test admin-only endpoint
                response = await self.client.get(
                    f"{self.base_url}/security/status",
                    headers=headers
                )
                
                if user["role"] == "admin":
                    assert response.status_code == 200
                    self.test_results.append({"test": f"admin_access_{user['role']}", "status": "PASS"})
                else:
                    assert response.status_code == 403
                    self.test_results.append({"test": f"admin_access_{user['role']}", "status": "PASS"})
                
                # Test compliance endpoint
                response = await self.client.get(
                    f"{self.base_url}/compliance",
                    headers=headers
                )
                
                if user["role"] in ["admin", "compliance_officer"]:
                    assert response.status_code == 200
                    self.test_results.append({"test": f"compliance_access_{user['role']}", "status": "PASS"})
                else:
                    assert response.status_code == 403
                    self.test_results.append({"test": f"compliance_access_{user['role']}", "status": "PASS"})
                
            except Exception as e:
                self.test_results.append({"test": f"authorization_{user['role']}", "status": "FAIL", "error": str(e)})
    
    async def test_encryption(self):
        """Test data encryption functionality"""
        logger.info("Testing encryption...")
        
        try:
            # Get admin token
            response = await self.client.post(
                f"{self.base_url}/auth/login",
                data={"username": self.credentials["admin"]["username"], "password": self.credentials["admin"]["password"]}
            )
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test encryption endpoint
            test_data = "sensitive_data_12345"
            response = await self.client.post(
                f"{self.base_url}/security/encrypt",
                params={"data": test_data},
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.json()
            assert "encrypted_data" in result
            assert result["encrypted_data"] != test_data  # Should be encrypted
            self.test_results.append({"test": "encryption", "status": "PASS"})
            
        except Exception as e:
            self.test_results.append({"test": "encryption", "status": "FAIL", "error": str(e)})
    
    async def test_security_headers(self):
        """Test security headers"""
        logger.info("Testing security headers...")
        
        try:
            response = await self.client.get(f"{self.base_url}/health")
            headers = response.headers
            
            # Check for security headers
            security_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "X-XSS-Protection",
                "Strict-Transport-Security",
                "Content-Security-Policy"
            ]
            
            missing_headers = []
            for header in security_headers:
                if header not in headers:
                    missing_headers.append(header)
            
            if not missing_headers:
                self.test_results.append({"test": "security_headers", "status": "PASS"})
            else:
                self.test_results.append({"test": "security_headers", "status": "FAIL", "error": f"Missing headers: {missing_headers}"})
                
        except Exception as e:
            self.test_results.append({"test": "security_headers", "status": "FAIL", "error": str(e)})
    
    async def test_audit_logging(self):
        """Test audit logging functionality"""
        logger.info("Testing audit logging...")
        
        try:
            # Get admin token
            response = await self.client.post(
                f"{self.base_url}/auth/login",
                data={"username": self.credentials["admin"]["username"], "password": self.credentials["admin"]["password"]}
            )
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Perform actions that should be logged
            await self.client.get(f"{self.base_url}/status", headers=headers)
            await self.client.get(f"{self.base_url}/transactions", headers=headers)
            
            # Check audit logs
            response = await self.client.get(f"{self.base_url}/audit", headers=headers)
            assert response.status_code == 200
            audit_logs = response.json()["audit_logs"]
            assert len(audit_logs) > 0
            self.test_results.append({"test": "audit_logging", "status": "PASS"})
            
        except Exception as e:
            self.test_results.append({"test": "audit_logging", "status": "FAIL", "error": str(e)})
    
    async def test_compliance_endpoints(self):
        """Test compliance-related endpoints"""
        logger.info("Testing compliance endpoints...")
        
        try:
            # Get compliance officer token
            response = await self.client.post(
                f"{self.base_url}/auth/login",
                data={"username": self.credentials["compliance"]["username"], "password": self.credentials["compliance"]["password"]}
            )
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test compliance frameworks endpoint
            response = await self.client.get(
                f"{self.base_url}/compliance/frameworks",
                headers=headers
            )
            assert response.status_code == 200
            frameworks = response.json()["frameworks"]
            assert "PCI-DSS" in frameworks
            assert "GDPR" in frameworks
            self.test_results.append({"test": "compliance_frameworks", "status": "PASS"})
            
        except Exception as e:
            self.test_results.append({"test": "compliance_frameworks", "status": "FAIL", "error": str(e)})
    
    async def run_all_tests(self):
        """Run all security tests"""
        logger.info("Starting comprehensive security testing...")
        
        await self.test_authentication()
        await self.test_rate_limiting()
        await self.test_input_validation()
        await self.test_authorization()
        await self.test_encryption()
        await self.test_security_headers()
        await self.test_audit_logging()
        await self.test_compliance_endpoints()
        
        # Generate test report
        self.generate_report()
    
    def generate_report(self):
        """Generate security test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%"
            },
            "test_results": self.test_results,
            "timestamp": time.time()
        }
        
        # Save report
        with open("security_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Security testing completed: {passed_tests}/{total_tests} tests passed")
        logger.info(f"Test report saved to security_test_report.json")
        
        return report

async def main():
    """Main testing function"""
    async with SecurityTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
