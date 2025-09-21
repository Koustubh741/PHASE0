"""
Application Startup Validation Module
Validates environment variables and configuration on application startup.
"""

import os
import sys
import re
import logging
from typing import List, Dict, Optional, Set
from functools import wraps

logger = logging.getLogger(__name__)

class StartupValidator:
    """Validates application configuration on startup."""
    
    # Placeholder patterns that should not be in production
    PLACEHOLDER_PATTERNS = {
        'change_me',
        'yourdomain',
        'your_domain', 
        'yourdomain.com',
        'your-domain.com',
        'your_backup_bucket',
        'your-backup-bucket',
        'your_super_secret_key',
        'your_jwt_secret_key',
        'your_32_byte_encryption_key',
        'your_master_api_key',
        'your_smtp_password',
        'placeholder',
        'example',
        'test_',
        'demo_',
        'sample_',
        'default_',
        'localhost',
        '127.0.0.1',
        'admin',
        'root',
        'password123',
        '123456',
        'abcdef',
        'secret123',
        'changeme',
        'password',
        'secret',
        'temp',
        'temporary'
    }
    
    # Critical variables that must be properly configured
    CRITICAL_VARIABLES = {
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'ENCRYPTION_KEY',
        'API_KEY_MASTER',
        'DB_PASSWORD',
        'REDIS_PASSWORD'
    }
    
    # Variables that should not contain placeholder domains
    DOMAIN_VARIABLES = {
        'CORS_ORIGINS',
        'SMTP_HOST',
        'SMTP_USER'
    }
    
    def __init__(self, environment: str = 'production'):
        """Initialize the startup validator."""
        self.environment = environment
        self.validation_errors: List[Dict[str, str]] = []
        self.validation_warnings: List[Dict[str, str]] = []
        self._is_validated = False
        
    def validate_all(self) -> bool:
        """
        Perform comprehensive validation of all environment variables.
        
        Returns:
            bool: True if validation passes, False otherwise
        """
        logger.info("Starting application startup validation...")
        
        # Only validate in production environment
        if self.environment != 'production':
            logger.info("Skipping production validation in non-production environment")
            return True
        
        # Clear previous validation results
        self.validation_errors.clear()
        self.validation_warnings.clear()
        
        # Perform validations
        self._validate_critical_variables()
        self._validate_placeholder_patterns()
        self._validate_domain_variables()
        self._validate_security_settings()
        self._validate_database_configuration()
        
        # Log results
        self._log_validation_results()
        
        self._is_validated = True
        return len(self.validation_errors) == 0
    
    def _validate_critical_variables(self) -> None:
        """Validate that critical variables are set and not placeholders."""
        for var_name in self.CRITICAL_VARIABLES:
            value = os.getenv(var_name)
            
            if not value:
                self.validation_errors.append({
                    'variable': var_name,
                    'error': 'Critical variable not set',
                    'severity': 'error'
                })
            elif self._contains_placeholder(value):
                self.validation_errors.append({
                    'variable': var_name,
                    'error': f'Critical variable contains placeholder value: {value}',
                    'severity': 'error'
                })
            else:
                # Additional validation for specific variables
                self._validate_specific_variable(var_name, value)
    
    def _validate_placeholder_patterns(self) -> None:
        """Scan all environment variables for placeholder patterns."""
        for key, value in os.environ.items():
            if self._contains_placeholder(value):
                # Skip variables that are expected to contain certain patterns
                if self._is_expected_placeholder(key, value):
                    continue
                    
                self.validation_errors.append({
                    'variable': key,
                    'error': f'Environment variable contains placeholder: {value}',
                    'severity': 'error'
                })
    
    def _validate_domain_variables(self) -> None:
        """Validate domain-related variables."""
        for var_name in self.DOMAIN_VARIABLES:
            value = os.getenv(var_name)
            if value and self._contains_placeholder_domain(value):
                self.validation_errors.append({
                    'variable': var_name,
                    'error': f'Domain variable contains placeholder: {value}',
                    'severity': 'error'
                })
    
    def _validate_security_settings(self) -> None:
        """Validate security-related configuration."""
        # Validate SECRET_KEY length
        secret_key = os.getenv('SECRET_KEY')
        if secret_key and len(secret_key) < 32:
            self.validation_errors.append({
                'variable': 'SECRET_KEY',
                'error': 'SECRET_KEY should be at least 32 characters long',
                'severity': 'error'
            })
        
        # Validate ENCRYPTION_KEY length
        encryption_key = os.getenv('ENCRYPTION_KEY')
        if encryption_key and len(encryption_key) != 32:
            self.validation_errors.append({
                'variable': 'ENCRYPTION_KEY',
                'error': 'ENCRYPTION_KEY should be exactly 32 characters long',
                'severity': 'error'
            })
        
        # Validate password strength
        db_password = os.getenv('DB_PASSWORD')
        if db_password and len(db_password) < 12:
            self.validation_warnings.append({
                'variable': 'DB_PASSWORD',
                'error': 'Database password should be at least 12 characters long',
                'severity': 'warning'
            })
    
    def _validate_database_configuration(self) -> None:
        """Validate database configuration."""
        db_host = os.getenv('DB_HOST')
        if db_host in ['localhost', '127.0.0.1'] and self.environment == 'production':
            self.validation_warnings.append({
                'variable': 'DB_HOST',
                'error': 'Using localhost for database in production environment',
                'severity': 'warning'
            })
    
    def _validate_specific_variable(self, var_name: str, value: str) -> None:
        """Validate specific variables with custom rules."""
        if var_name == 'CORS_ORIGINS':
            if 'yourdomain.com' in value or 'your-domain.com' in value:
                self.validation_errors.append({
                    'variable': var_name,
                    'error': 'CORS_ORIGINS contains placeholder domain',
                    'severity': 'error'
                })
    
    def _contains_placeholder(self, value: str) -> bool:
        """Check if a value contains placeholder patterns."""
        value_lower = value.lower()
        
        # Check for exact placeholder patterns
        for pattern in self.PLACEHOLDER_PATTERNS:
            if pattern in value_lower:
                return True
        
        # Check for regex patterns
        placeholder_regex = [
            r'change_me',
            r'your_.*_change_me',
            r'secure_.*_password_change_me',
            r'.*_change_me.*'
        ]
        
        for regex in placeholder_regex:
            if re.search(regex, value_lower):
                return True
        
        return False
    
    def _contains_placeholder_domain(self, value: str) -> bool:
        """Check if a value contains placeholder domain patterns."""
        domain_patterns = [
            'yourdomain', 'your-domain', 'example.com', 'localhost',
            '127.0.0.1', 'test.com', 'demo.com'
        ]
        
        value_lower = value.lower()
        return any(pattern in value_lower for pattern in domain_patterns)
    
    def _is_expected_placeholder(self, key: str, value: str) -> bool:
        """Check if a placeholder is expected for this variable."""
        # Variables that might legitimately contain certain patterns
        expected_patterns = {
            'LOG_LEVEL': ['debug', 'info', 'warning', 'error'],
            'ENVIRONMENT': ['development', 'staging', 'production'],
            'SSL_MINIMUM_VERSION': ['TLSv1.2', 'TLSv1.3']
        }
        
        for var_name, patterns in expected_patterns.items():
            if key == var_name and value.lower() in patterns:
                return True
        
        return False
    
    def _log_validation_results(self) -> None:
        """Log validation results."""
        if not self.validation_errors and not self.validation_warnings:
            logger.info("✅ Startup validation passed!")
            return
        
        if self.validation_errors:
            logger.error(f"❌ Found {len(self.validation_errors)} validation errors:")
            for error in self.validation_errors:
                logger.error(f"  {error['variable']}: {error['error']}")
        
        if self.validation_warnings:
            logger.warning(f"⚠️  Found {len(self.validation_warnings)} warnings:")
            for warning in self.validation_warnings:
                logger.warning(f"  {warning['variable']}: {warning['error']}")
    
    def get_errors(self) -> List[Dict[str, str]]:
        """Get validation errors."""
        return self.validation_errors.copy()
    
    def get_warnings(self) -> List[Dict[str, str]]:
        """Get validation warnings."""
        return self.validation_warnings.copy()
    
    def is_validated(self) -> bool:
        """Check if validation has been performed."""
        return self._is_validated


# Global validator instance
_startup_validator: Optional[StartupValidator] = None


def initialize_startup_validation(environment: str = 'production') -> StartupValidator:
    """
    Initialize the startup validator.
    
    Args:
        environment: The environment name (production, development, etc.)
        
    Returns:
        StartupValidator: The validator instance
    """
    global _startup_validator
    _startup_validator = StartupValidator(environment)
    return _startup_validator


def validate_on_startup(environment: str = 'production', fail_on_error: bool = True) -> bool:
    """
    Validate configuration on startup and optionally fail if validation fails.
    
    Args:
        environment: The environment name
        fail_on_error: Whether to exit the application on validation failure
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    validator = initialize_startup_validation(environment)
    
    if not validator.validate_all():
        if fail_on_error:
            logger.error("❌ Startup validation failed. Application will exit.")
            sys.exit(1)
        return False
    
    return True


def require_validated_startup(fail_on_error: bool = True):
    """
    Decorator to ensure startup validation has been performed.
    
    Args:
        fail_on_error: Whether to exit on validation failure
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global _startup_validator
            
            if not _startup_validator or not _startup_validator.is_validated():
                logger.warning("Startup validation not performed. Running validation now...")
                if not validate_on_startup(fail_on_error=fail_on_error):
                    if fail_on_error:
                        return None
                    raise RuntimeError("Startup validation failed")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_validation_status() -> Dict[str, any]:
    """
    Get the current validation status.
    
    Returns:
        Dict containing validation status information
    """
    global _startup_validator
    
    if not _startup_validator:
        return {
            'validated': False,
            'errors': [],
            'warnings': []
        }
    
    return {
        'validated': _startup_validator.is_validated(),
        'errors': _startup_validator.get_errors(),
        'warnings': _startup_validator.get_warnings()
    }
