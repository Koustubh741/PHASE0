 #!/usr/bin/env python3
"""
Production Configuration Validation Script
Scans environment configuration files for placeholder values that should not be deployed.
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProductionConfigValidator:
    """Validates production configuration files for placeholder values."""
    
    # Common placeholder patterns that should not be in production
    PLACEHOLDER_PATTERNS = [
        r'change_me',
        r'yourdomain',
        r'your_domain',
        r'yourdomain\.com',
        r'your-domain\.com',
        r'your_backup_bucket',
        r'your-backup-bucket',
        r'your_super_secret_key',
        r'your_jwt_secret_key',
        r'your_32_byte_encryption_key',
        r'your_master_api_key',
        r'your_smtp_password',
        r'secure_.*_password_change_me',
        r'.*_change_me.*',
        r'placeholder',
        r'example',
        r'test_',
        r'demo_',
        r'sample_',
        r'default_',
        r'localhost.*production',
        r'127\.0\.0\.1.*production',
        r'admin.*password',
        r'root.*password',
        r'password123',
        r'123456',
        r'abcdef',
        r'secret123',
        r'changeme',
        r'password',
        r'secret',
        r'temp',
        r'temporary',
    ]
    
    # Critical environment variables that must be set with non-placeholder values
    CRITICAL_VARS = [
        'SECRET_KEY',
        'JWT_SECRET_KEY', 
        'ENCRYPTION_KEY',
        'API_KEY_MASTER',
        'DB_PASSWORD',
        'REDIS_PASSWORD',
        'SMTP_PASSWORD'
    ]
    
    # Variables that should not contain placeholder domains
    DOMAIN_VARS = [
        'CORS_ORIGINS',
        'SMTP_HOST',
        'SMTP_USER'
    ]
    
    def __init__(self, config_file: str = None):
        """Initialize the validator with optional config file path."""
        self.config_file = config_file
        self.errors: List[Dict[str, str]] = []
        self.warnings: List[Dict[str, str]] = []
        
    def validate_file(self, file_path: str) -> bool:
        """
        Validate a configuration file for placeholder values.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        if not os.path.exists(file_path):
            logger.error(f"Configuration file not found: {file_path}")
            return False
            
        logger.info(f"Validating configuration file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self._validate_content(content, file_path)
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return False
            
        return len(self.errors) == 0
    
    def _validate_content(self, content: str, file_path: str) -> None:
        """Validate file content for placeholder values."""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
                
            # Check for environment variable assignments
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                
                self._validate_variable(key, value, line_num, file_path)
    
    def _validate_variable(self, key: str, value: str, line_num: int, file_path: str) -> None:
        """Validate a single environment variable."""
        
        # Check for placeholder patterns
        for pattern in self.PLACEHOLDER_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                error_msg = f"Placeholder value detected: {key}={value}"
                self.errors.append({
                    'type': 'placeholder',
                    'message': error_msg,
                    'file': file_path,
                    'line': line_num,
                    'variable': key,
                    'value': value,
                    'pattern': pattern
                })
                break
        
        # Check critical variables
        if key in self.CRITICAL_VARS:
            if self._is_placeholder_value(value):
                error_msg = f"Critical variable contains placeholder: {key}"
                self.errors.append({
                    'type': 'critical_placeholder',
                    'message': error_msg,
                    'file': file_path,
                    'line': line_num,
                    'variable': key,
                    'value': value
                })
        
        # Check domain variables
        if key in self.DOMAIN_VARS:
            if self._contains_placeholder_domain(value):
                error_msg = f"Domain variable contains placeholder: {key}={value}"
                self.errors.append({
                    'type': 'domain_placeholder',
                    'message': error_msg,
                    'file': file_path,
                    'line': line_num,
                    'variable': key,
                    'value': value
                })
        
        # Additional validation for specific variables
        self._validate_specific_variables(key, value, line_num, file_path)
    
    def _is_placeholder_value(self, value: str) -> bool:
        """Check if a value appears to be a placeholder."""
        placeholder_indicators = [
            'change_me', 'your_', 'placeholder', 'example', 'test_',
            'demo_', 'sample_', 'default_', 'temp', 'temporary'
        ]
        
        value_lower = value.lower()
        return any(indicator in value_lower for indicator in placeholder_indicators)
    
    def _contains_placeholder_domain(self, value: str) -> bool:
        """Check if a value contains placeholder domain patterns."""
        domain_patterns = [
            'yourdomain', 'your-domain', 'example.com', 'localhost',
            '127.0.0.1', 'test.com', 'demo.com'
        ]
        
        value_lower = value.lower()
        return any(pattern in value_lower for pattern in domain_patterns)
    
    def _validate_specific_variables(self, key: str, value: str, line_num: int, file_path: str) -> None:
        """Validate specific variables with custom rules."""
        
        if key == 'SECRET_KEY' and len(value) < 32:
            self.errors.append({
                'type': 'weak_secret',
                'message': f"SECRET_KEY should be at least 32 characters long",
                'file': file_path,
                'line': line_num,
                'variable': key,
                'value': value
            })
        
        if key == 'ENCRYPTION_KEY' and len(value) != 32:
            self.errors.append({
                'type': 'invalid_encryption_key',
                'message': f"ENCRYPTION_KEY should be exactly 32 characters long",
                'file': file_path,
                'line': line_num,
                'variable': key,
                'value': value
            })
        
        if key == 'DB_PASSWORD' and len(value) < 12:
            self.errors.append({
                'type': 'weak_password',
                'message': f"Database password should be at least 12 characters long",
                'file': file_path,
                'line': line_num,
                'variable': key,
                'value': value
            })
        
        if key == 'CORS_ORIGINS':
            # Check for placeholder domains in CORS origins
            if 'yourdomain.com' in value or 'your-domain.com' in value:
                self.errors.append({
                    'type': 'cors_placeholder',
                    'message': f"CORS_ORIGINS contains placeholder domain",
                    'file': file_path,
                    'line': line_num,
                    'variable': key,
                    'value': value
                })
    
    def print_results(self) -> None:
        """Print validation results."""
        if not self.errors and not self.warnings:
            logger.info("✅ Configuration validation passed!")
            return
        
        if self.errors:
            logger.error(f"❌ Found {len(self.errors)} validation errors:")
            for error in self.errors:
                logger.error(f"  {error['file']}:{error['line']} - {error['message']}")
                if error.get('pattern'):
                    logger.error(f"    Matched pattern: {error['pattern']}")
        
        if self.warnings:
            logger.warning(f"⚠️  Found {len(self.warnings)} warnings:")
            for warning in self.warnings:
                logger.warning(f"  {warning['file']}:{warning['line']} - {warning['message']}")
    
    def get_errors(self) -> List[Dict[str, str]]:
        """Get list of validation errors."""
        return self.errors
    
    def get_warnings(self) -> List[Dict[str, str]]:
        """Get list of validation warnings."""
        return self.warnings


def validate_environment_file(file_path: str, fail_on_errors: bool = True) -> bool:
    """
    Validate an environment configuration file.
    
    Args:
        file_path: Path to the environment file
        fail_on_errors: Whether to exit with error code on validation failures
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    validator = ProductionConfigValidator()
    
    if not validator.validate_file(file_path):
        validator.print_results()
        if fail_on_errors:
            logger.error("❌ Configuration validation failed. Deployment aborted.")
            sys.exit(1)
        return False
    
    validator.print_results()
    logger.info("✅ Configuration validation successful!")
    return True


def main():
    """Main entry point for the validation script."""
    parser = argparse.ArgumentParser(
        description='Validate production configuration files for placeholder values'
    )
    parser.add_argument(
        'config_file',
        nargs='?',
        default='config/environment/production.env',
        help='Path to the configuration file to validate'
    )
    parser.add_argument(
        '--no-fail',
        action='store_true',
        help='Do not exit with error code on validation failures'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check if file exists
    if not os.path.exists(args.config_file):
        logger.error(f"Configuration file not found: {args.config_file}")
        sys.exit(1)
    
    # Validate the configuration
    success = validate_environment_file(args.config_file, fail_on_errors=not args.no_fail)
    
    if not success and not args.no_fail:
        sys.exit(1)


if __name__ == '__main__':
    main()
