"""
Test database configuration module
"""

import os
import pytest
from unittest.mock import patch
from database_config import DatabaseConfig, get_database_url, is_secure_config

def test_database_url_from_env():
    """Test getting DATABASE_URL from environment"""
    with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://user:pass@host:5432/db'}):
        config = DatabaseConfig()
        assert config.database_url == 'postgresql://user:pass@host:5432/db'
        assert config.is_secure_config is True

def test_database_url_from_components():
    """Test constructing DATABASE_URL from individual components"""
    with patch.dict(os.environ, {
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass'
    }, clear=True):
        config = DatabaseConfig()
        expected_url = 'postgresql://test_user:test_pass@localhost:5432/test_db'
        assert config.database_url == expected_url
        assert config.is_secure_config is False

def test_production_validation():
    """Test production environment validation"""
    with patch.dict(os.environ, {
        'ENVIRONMENT': 'production',
        'DB_HOST': 'localhost',  # Using default values should fail in production
        'DB_NAME': 'grc_platform',
        'DB_USER': 'grc_user',
        'DB_PASSWORD': 'grc_password'
    }, clear=True):
        with pytest.raises(ValueError, match="Missing or default values"):
            DatabaseConfig()

def test_get_database_url_function():
    """Test the get_database_url function"""
    with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://user:pass@host:5432/db'}):
        assert get_database_url() == 'postgresql://user:pass@host:5432/db'

def test_is_secure_config_function():
    """Test the is_secure_config function"""
    with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://user:pass@host:5432/db'}):
        assert is_secure_config() is True
    
    with patch.dict(os.environ, {}, clear=True):
        # This will use fallback configuration
        assert is_secure_config() is False

if __name__ == "__main__":
    pytest.main([__file__])
