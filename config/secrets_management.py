"""
Secrets Management Configuration
Provides centralized secrets validation and management.
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
import hashlib
import base64

logger = logging.getLogger(__name__)

class SecretType(Enum):
    """Types of secrets that need special handling."""
    API_KEY = "api_key"
    PASSWORD = "password"
    ENCRYPTION_KEY = "encryption_key"
    JWT_SECRET = "jwt_secret"
    DATABASE_CREDENTIAL = "database_credential"
    EXTERNAL_SERVICE_CREDENTIAL = "external_service_credential"

@dataclass
class SecretValidation:
    """Configuration for secret validation."""
    min_length: int
    max_length: Optional[int] = None
    require_special_chars: bool = False
    require_numbers: bool = True
    require_uppercase: bool = True
    require_lowercase: bool = True
    forbidden_patterns: List[str] = None
    custom_validators: List[str] = None

class SecretsManager:
    """Manages and validates application secrets."""
    
    # Secret validation configurations
    SECRET_VALIDATIONS = {
        SecretType.API_KEY: SecretValidation(
            min_length=32,
            max_length=128,
            require_special_chars=False,
            require_numbers=True,
            require_uppercase=True,
            require_lowercase=True,
            forbidden_patterns=['password', 'secret', 'key', 'token']
        ),
        SecretType.PASSWORD: SecretValidation(
            min_length=12,
            require_special_chars=True,
            require_numbers=True,
            require_uppercase=True,
            require_lowercase=True,
            forbidden_patterns=['password', '123456', 'qwerty', 'admin']
        ),
        SecretType.ENCRYPTION_KEY: SecretValidation(
            min_length=32,
            max_length=32,
            require_special_chars=False,
            require_numbers=True,
            require_uppercase=False,
            require_lowercase=False
        ),
        SecretType.JWT_SECRET: SecretValidation(
            min_length=32,
            require_special_chars=False,
            require_numbers=True,
            require_uppercase=True,
            require_lowercase=True
        ),
        SecretType.DATABASE_CREDENTIAL: SecretValidation(
            min_length=12,
            require_special_chars=True,
            require_numbers=True,
            require_uppercase=True,
            require_lowercase=True,
            forbidden_patterns=['password', 'admin', 'root', 'test']
        ),
        SecretType.EXTERNAL_SERVICE_CREDENTIAL: SecretValidation(
            min_length=16,
            require_special_chars=True,
            require_numbers=True,
            require_uppercase=True,
            require_lowercase=True
        )
    }
    
    # Environment variables mapped to their secret types
    SECRET_MAPPINGS = {
        'SECRET_KEY': SecretType.API_KEY,
        'JWT_SECRET_KEY': SecretType.JWT_SECRET,
        'ENCRYPTION_KEY': SecretType.ENCRYPTION_KEY,
        'API_KEY_MASTER': SecretType.API_KEY,
        'DB_PASSWORD': SecretType.DATABASE_CREDENTIAL,
        'REDIS_PASSWORD': SecretType.DATABASE_CREDENTIAL,
        'SMTP_PASSWORD': SecretType.EXTERNAL_SERVICE_CREDENTIAL,
    }
    
    # Placeholder patterns that should not be in production secrets
    PLACEHOLDER_PATTERNS = {
        'change_me', 'your_', 'placeholder', 'example', 'test_',
        'demo_', 'sample_', 'default_', 'temp', 'temporary',
        'password123', '123456', 'secret123', 'changeme'
    }
    
    def __init__(self, environment: str = 'production'):
        """Initialize the secrets manager."""
        self.environment = environment
        self.validation_errors: List[Dict[str, str]] = []
        self.validation_warnings: List[Dict[str, str]] = []
        
    def validate_all_secrets(self) -> bool:
        """
        Validate all secrets in the environment.
        
        Returns:
            bool: True if all secrets are valid, False otherwise
        """
        logger.info("Starting secrets validation...")
        
        # Only validate in production environment
        if self.environment != 'production':
            logger.info("Skipping secrets validation in non-production environment")
            return True
        
        # Clear previous validation results
        self.validation_errors.clear()
        self.validation_warnings.clear()
        
        # Validate mapped secrets
        for env_var, secret_type in self.SECRET_MAPPINGS.items():
            value = os.getenv(env_var)
            if value:
                self._validate_secret(env_var, value, secret_type)
            else:
                self.validation_errors.append({
                    'variable': env_var,
                    'error': f'Required secret not set: {env_var}',
                    'severity': 'error'
                })
        
        # Scan for any remaining placeholder patterns
        self._scan_for_placeholders()
        
        # Log results
        self._log_validation_results()
        
        return len(self.validation_errors) == 0
    
    def _validate_secret(self, variable_name: str, value: str, secret_type: SecretType) -> None:
        """Validate a specific secret."""
        validation_config = self.SECRET_VALIDATIONS.get(secret_type)
        if not validation_config:
            logger.warning(f"No validation configuration for secret type: {secret_type}")
            return
        
        # Check for placeholder patterns
        if self._contains_placeholder(value):
            self.validation_errors.append({
                'variable': variable_name,
                'error': f'Secret contains placeholder value: {value[:10]}...',
                'severity': 'error'
            })
            return
        
        # Validate length
        if len(value) < validation_config.min_length:
            self.validation_errors.append({
                'variable': variable_name,
                'error': f'Secret too short: minimum {validation_config.min_length} characters',
                'severity': 'error'
            })
        
        if validation_config.max_length and len(value) > validation_config.max_length:
            self.validation_errors.append({
                'variable': variable_name,
                'error': f'Secret too long: maximum {validation_config.max_length} characters',
                'severity': 'error'
            })
        
        # Validate character requirements
        if validation_config.require_numbers and not any(c.isdigit() for c in value):
            self.validation_errors.append({
                'variable': variable_name,
                'error': 'Secret must contain at least one number',
                'severity': 'error'
            })
        
        if validation_config.require_uppercase and not any(c.isupper() for c in value):
            self.validation_errors.append({
                'variable': variable_name,
                'error': 'Secret must contain at least one uppercase letter',
                'severity': 'error'
            })
        
        if validation_config.require_lowercase and not any(c.islower() for c in value):
            self.validation_errors.append({
                'variable': variable_name,
                'error': 'Secret must contain at least one lowercase letter',
                'severity': 'error'
            })
        
        if validation_config.require_special_chars:
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in special_chars for c in value):
                self.validation_errors.append({
                    'variable': variable_name,
                    'error': 'Secret must contain at least one special character',
                    'severity': 'error'
                })
        
        # Check forbidden patterns
        if validation_config.forbidden_patterns:
            value_lower = value.lower()
            for pattern in validation_config.forbidden_patterns:
                if pattern in value_lower:
                    self.validation_errors.append({
                        'variable': variable_name,
                        'error': f'Secret contains forbidden pattern: {pattern}',
                        'severity': 'error'
                    })
        
        # Additional validation for specific secret types
        self._validate_specific_secret(variable_name, value, secret_type)
    
    def _validate_specific_secret(self, variable_name: str, value: str, secret_type: SecretType) -> None:
        """Perform type-specific validation."""
        if secret_type == SecretType.ENCRYPTION_KEY:
            # Encryption keys should be exactly 32 bytes (256 bits)
            if len(value) != 32:
                self.validation_errors.append({
                    'variable': variable_name,
                    'error': 'Encryption key must be exactly 32 characters long',
                    'severity': 'error'
                })
            
            # Check if it's a valid base64 or hex string
            try:
                if len(value) == 64:  # Hex string
                    bytes.fromhex(value)
                else:
                    base64.b64decode(value)
            except (ValueError, TypeError):
                self.validation_errors.append({
                    'variable': variable_name,
                    'error': 'Encryption key must be valid base64 or hex string',
                    'severity': 'error'
                })
        
        elif secret_type == SecretType.JWT_SECRET:
            # JWT secrets should be cryptographically secure
            if len(set(value)) < len(value) * 0.5:  # At least 50% unique characters
                self.validation_warnings.append({
                    'variable': variable_name,
                    'error': 'JWT secret has low character diversity',
                    'severity': 'warning'
                })
        
        elif secret_type == SecretType.DATABASE_CREDENTIAL:
            # Database passwords should not be easily guessable
            common_passwords = ['password', 'admin', 'root', 'test', 'user', 'guest']
            if value.lower() in common_passwords:
                self.validation_errors.append({
                    'variable': variable_name,
                    'error': 'Database password is too common',
                    'severity': 'error'
                })
    
    def _contains_placeholder(self, value: str) -> bool:
        """Check if a value contains placeholder patterns."""
        value_lower = value.lower()
        return any(pattern in value_lower for pattern in self.PLACEHOLDER_PATTERNS)
    
    def _scan_for_placeholders(self) -> None:
        """Scan all environment variables for placeholder patterns."""
        for key, value in os.environ.items():
            if self._contains_placeholder(value):
                # Skip variables that might legitimately contain these patterns
                if self._is_legitimate_pattern(key, value):
                    continue
                
                self.validation_errors.append({
                    'variable': key,
                    'error': f'Environment variable contains placeholder: {value[:20]}...',
                    'severity': 'error'
                })
    
    def _is_legitimate_pattern(self, key: str, value: str) -> bool:
        """Check if a pattern is legitimate for a specific variable."""
        legitimate_patterns = {
            'LOG_LEVEL': ['debug', 'info', 'warning', 'error'],
            'ENVIRONMENT': ['development', 'staging', 'production'],
            'DB_SSL_MODE': ['disable', 'allow', 'prefer', 'require', 'verify-ca', 'verify-full']
        }
        
        patterns = legitimate_patterns.get(key, [])
        return value.lower() in patterns
    
    def _log_validation_results(self) -> None:
        """Log validation results."""
        if not self.validation_errors and not self.validation_warnings:
            logger.info("✅ Secrets validation passed!")
            return
        
        if self.validation_errors:
            logger.error(f"❌ Found {len(self.validation_errors)} secret validation errors:")
            for error in self.validation_errors:
                logger.error(f"  {error['variable']}: {error['error']}")
        
        if self.validation_warnings:
            logger.warning(f"⚠️  Found {len(self.validation_warnings)} secret validation warnings:")
            for warning in self.validation_warnings:
                logger.warning(f"  {warning['variable']}: {warning['error']}")
    
    def get_errors(self) -> List[Dict[str, str]]:
        """Get validation errors."""
        return self.validation_errors.copy()
    
    def get_warnings(self) -> List[Dict[str, str]]:
        """Get validation warnings."""
        return self.validation_warnings.copy()
    
    def generate_secret_suggestions(self, secret_type: SecretType) -> List[str]:
        """
        Generate suggestions for creating secure secrets.
        
        Args:
            secret_type: The type of secret to generate suggestions for
            
        Returns:
            List of suggestions for creating secure secrets
        """
        suggestions = []
        validation_config = self.SECRET_VALIDATIONS.get(secret_type)
        
        if not validation_config:
            return ["No validation configuration available"]
        
        suggestions.append(f"Minimum length: {validation_config.min_length} characters")
        
        if validation_config.max_length:
            suggestions.append(f"Maximum length: {validation_config.max_length} characters")
        
        if validation_config.require_numbers:
            suggestions.append("Include numbers (0-9)")
        
        if validation_config.require_uppercase:
            suggestions.append("Include uppercase letters (A-Z)")
        
        if validation_config.require_lowercase:
            suggestions.append("Include lowercase letters (a-z)")
        
        if validation_config.require_special_chars:
            suggestions.append("Include special characters (!@#$%^&*)")
        
        if validation_config.forbidden_patterns:
            suggestions.append(f"Avoid these patterns: {', '.join(validation_config.forbidden_patterns)}")
        
        return suggestions


# Global secrets manager instance
_secrets_manager: Optional[SecretsManager] = None


def initialize_secrets_manager(environment: str = 'production') -> SecretsManager:
    """
    Initialize the secrets manager.
    
    Args:
        environment: The environment name
        
    Returns:
        SecretsManager: The secrets manager instance
    """
    global _secrets_manager
    _secrets_manager = SecretsManager(environment)
    return _secrets_manager


def validate_secrets(environment: str = 'production', fail_on_error: bool = True) -> bool:
    """
    Validate all secrets and optionally fail if validation fails.
    
    Args:
        environment: The environment name
        fail_on_error: Whether to exit the application on validation failure
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    secrets_manager = initialize_secrets_manager(environment)
    
    if not secrets_manager.validate_all_secrets():
        if fail_on_error:
            logger.error("❌ Secrets validation failed. Application will exit.")
            sys.exit(1)
        return False
    
    return True


def get_secret_suggestions(secret_type: SecretType) -> List[str]:
    """
    Get suggestions for creating secure secrets.
    
    Args:
        secret_type: The type of secret
        
    Returns:
        List of suggestions
    """
    secrets_manager = initialize_secrets_manager()
    return secrets_manager.generate_secret_suggestions(secret_type)
