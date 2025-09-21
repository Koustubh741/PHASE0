"""
Unit tests for SecurityManager.
"""

import pytest
import jwt
from datetime import datetime, timedelta
import hashlib

# Import the SecurityManager
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'utils'))
from security import SecurityManager


class TestSecurityManager:
    """Test cases for SecurityManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.security_manager = SecurityManager("test-secret-key")
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password"
        hashed = self.security_manager.hash_password(password)
        
        # Should be a hex string
        assert isinstance(hashed, str)
        assert len(hashed) == 64  # SHA-256 hex length
        
        # Should be deterministic
        hashed2 = self.security_manager.hash_password(password)
        assert hashed == hashed2
    
    def test_verify_password(self):
        """Test password verification."""
        password = "test_password"
        hashed = self.security_manager.hash_password(password)
        
        # Correct password should verify
        assert self.security_manager.verify_password(password, hashed) is True
        
        # Wrong password should not verify
        assert self.security_manager.verify_password("wrong_password", hashed) is False
    
    def test_generate_token(self):
        """Test token generation."""
        user_id = "test_user_123"
        token = self.security_manager.generate_token(user_id)
        
        # Token should be a string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Should be a valid JWT
        try:
            decoded = jwt.decode(token, self.security_manager.secret_key, algorithms=[self.security_manager.algorithm])
            assert decoded['user_id'] == user_id
        except jwt.InvalidTokenError:
            pytest.fail("Generated token is not valid JWT")
    
    def test_verify_token(self):
        """Test token verification."""
        user_id = "test_user_123"
        token = self.security_manager.generate_token(user_id)
        
        # Valid token should be verified
        payload = self.security_manager.verify_token(token)
        assert payload is not None
        assert payload['user_id'] == user_id
    
    def test_verify_expired_token(self):
        """Test verification of expired token."""
        # Create a token with very short expiry
        payload = {
            'user_id': 'test_user',
            'exp': datetime.utcnow() - timedelta(seconds=1),  # Expired
            'iat': datetime.utcnow() - timedelta(seconds=2)
        }
        token = jwt.encode(payload, self.security_manager.secret_key, algorithm=self.security_manager.algorithm)
        
        # Expired token should return None
        result = self.security_manager.verify_token(token)
        assert result is None
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        # Invalid token should return None
        result = self.security_manager.verify_token("invalid_token")
        assert result is None
    
    def test_generate_api_key(self):
        """Test API key generation."""
        api_key = self.security_manager.generate_api_key()
        
        # Should be a string
        assert isinstance(api_key, str)
        assert len(api_key) > 0
        
        # Should be URL-safe
        assert api_key.replace('-', '').replace('_', '').isalnum()


if __name__ == "__main__":
    pytest.main([__file__])
