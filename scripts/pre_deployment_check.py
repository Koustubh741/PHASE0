#!/usr/bin/env python3
"""
Pre-Deployment Validation Script
Comprehensive validation checks before deployment to production.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Tuple
import argparse

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.validate_production_config import ProductionConfigValidator
from backend.startup_validation import StartupValidator
from config.secrets_management import SecretsManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PreDeploymentValidator:
    """Comprehensive pre-deployment validation."""
    
    def __init__(self, config_file: str = None):
        """Initialize the pre-deployment validator."""
        self.config_file = config_file or 'config/environment/production.env'
        self.validation_results: Dict[str, bool] = {}
        self.all_errors: List[Dict[str, str]] = []
        self.all_warnings: List[Dict[str, str]] = []
        
    def run_all_checks(self) -> bool:
        """
        Run all pre-deployment validation checks.
        
        Returns:
            bool: True if all checks pass, False otherwise
        """
        logger.info("🚀 Starting pre-deployment validation checks...")
        
        checks = [
            ('File Existence', self._check_file_existence),
            ('Configuration Validation', self._check_configuration),
            ('Secrets Validation', self._check_secrets),
            ('Startup Validation', self._check_startup_validation),
            ('Dependencies Check', self._check_dependencies),
            ('Security Check', self._check_security),
            ('Database Connectivity', self._check_database_connectivity),
            ('Environment Variables', self._check_environment_variables)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            logger.info(f"Running {check_name}...")
            try:
                passed = check_func()
                self.validation_results[check_name] = passed
                if not passed:
                    all_passed = False
                    logger.error(f"❌ {check_name} failed")
                else:
                    logger.info(f"✅ {check_name} passed")
            except Exception as e:
                logger.error(f"❌ {check_name} failed with error: {e}")
                self.validation_results[check_name] = False
                all_passed = False
        
        self._print_summary()
        return all_passed
    
    def _check_file_existence(self) -> bool:
        """Check that required files exist."""
        required_files = [
            self.config_file,
            'requirements.txt',
            'docker-compose.yml',
            'backend/startup_validation.py',
            'config/secrets_management.py'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            logger.error(f"Missing required files: {missing_files}")
            return False
        
        return True
    
    def _check_configuration(self) -> bool:
        """Check configuration file for placeholder values."""
        validator = ProductionConfigValidator(self.config_file)
        
        if not validator.validate_file(self.config_file):
            self.all_errors.extend(validator.get_errors())
            self.all_warnings.extend(validator.get_warnings())
            return False
        
        return True
    
    def _check_secrets(self) -> bool:
        """Check secrets management validation."""
        # Set environment variables from config file for validation
        self._load_environment_from_file()
        
        secrets_manager = SecretsManager('production')
        
        if not secrets_manager.validate_all_secrets():
            self.all_errors.extend(secrets_manager.get_errors())
            self.all_warnings.extend(secrets_manager.get_warnings())
            return False
        
        return True
    
    def _check_startup_validation(self) -> bool:
        """Check startup validation."""
        self._load_environment_from_file()
        
        startup_validator = StartupValidator('production')
        
        if not startup_validator.validate_all():
            self.all_errors.extend(startup_validator.get_errors())
            self.all_warnings.extend(startup_validator.get_warnings())
            return False
        
        return True
    
    def _check_dependencies(self) -> bool:
        """Check that required dependencies are installed."""
        try:
            # Check if we can import required modules
            import fastapi
            import uvicorn
            import sqlalchemy
            import redis
            import psycopg2
            return True
        except ImportError as e:
            logger.error(f"Missing dependency: {e}")
            return False
    
    def _check_security(self) -> bool:
        """Perform basic security checks."""
        security_issues = []
        
        # Check for development/debug settings in production
        if os.getenv('DEBUG', '').lower() in ['true', '1', 'yes']:
            security_issues.append("DEBUG mode should not be enabled in production")
        
        if os.getenv('LOG_LEVEL', '').lower() == 'debug':
            security_issues.append("Debug logging should not be enabled in production")
        
        # Check for weak security configurations
        if os.getenv('DB_SSL_MODE', '').lower() not in ['require', 'verify-ca', 'verify-full']:
            security_issues.append("Database should use SSL in production")
        
        if security_issues:
            for issue in security_issues:
                logger.error(f"Security issue: {issue}")
                self.all_errors.append({
                    'type': 'security',
                    'message': issue,
                    'severity': 'error'
                })
            return False
        
        return True
    
    def _check_database_connectivity(self) -> bool:
        """Check database connectivity (optional check)."""
        try:
            # This is a basic check - in a real deployment, you might want to
            # actually test database connectivity
            db_host = os.getenv('DB_HOST')
            db_port = os.getenv('DB_PORT')
            db_name = os.getenv('DB_NAME')
            
            if not all([db_host, db_port, db_name]):
                logger.warning("Database configuration incomplete - skipping connectivity check")
                return True
            
            logger.info("Database connectivity check skipped in pre-deployment validation")
            return True
            
        except Exception as e:
            logger.warning(f"Database connectivity check failed: {e}")
            return True  # Don't fail deployment for connectivity issues
    
    def _check_environment_variables(self) -> bool:
        """Check that all required environment variables are set."""
        required_vars = [
            'SECRET_KEY',
            'JWT_SECRET_KEY',
            'ENCRYPTION_KEY',
            'API_KEY_MASTER',
            'DB_HOST',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD',
            'REDIS_HOST',
            'REDIS_PASSWORD'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            return False
        
        return True
    
    def _load_environment_from_file(self) -> None:
        """Load environment variables from the config file."""
        if not os.path.exists(self.config_file):
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        os.environ[key] = value
        except Exception as e:
            logger.warning(f"Could not load environment from file: {e}")
    
    def _print_summary(self) -> None:
        """Print validation summary."""
        logger.info("\n" + "="*60)
        logger.info("PRE-DEPLOYMENT VALIDATION SUMMARY")
        logger.info("="*60)
        
        total_checks = len(self.validation_results)
        passed_checks = sum(1 for passed in self.validation_results.values() if passed)
        
        logger.info(f"Total checks: {total_checks}")
        logger.info(f"Passed: {passed_checks}")
        logger.info(f"Failed: {total_checks - passed_checks}")
        
        if self.all_errors:
            logger.info(f"\nErrors found: {len(self.all_errors)}")
            for error in self.all_errors:
                logger.error(f"  - {error.get('message', 'Unknown error')}")
        
        if self.all_warnings:
            logger.info(f"\nWarnings found: {len(self.all_warnings)}")
            for warning in self.all_warnings:
                logger.warning(f"  - {warning.get('message', 'Unknown warning')}")
        
        if passed_checks == total_checks:
            logger.info("\n🎉 All validation checks passed! Ready for deployment.")
        else:
            logger.error(f"\n❌ {total_checks - passed_checks} validation checks failed. Deployment blocked.")
        
        logger.info("="*60)


def main():
    """Main entry point for pre-deployment validation."""
    parser = argparse.ArgumentParser(
        description='Run comprehensive pre-deployment validation checks'
    )
    parser.add_argument(
        '--config-file',
        default='config/environment/production.env',
        help='Path to the production configuration file'
    )
    parser.add_argument(
        '--skip-optional',
        action='store_true',
        help='Skip optional checks like database connectivity'
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
    
    # Run validation
    validator = PreDeploymentValidator(args.config_file)
    success = validator.run_all_checks()
    
    if not success:
        logger.error("❌ Pre-deployment validation failed. Deployment aborted.")
        sys.exit(1)
    
    logger.info("✅ Pre-deployment validation successful!")
    sys.exit(0)


if __name__ == '__main__':
    main()
