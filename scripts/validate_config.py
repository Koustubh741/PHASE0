#!/usr/bin/env python3
"""
Configuration Validation Script
Validates environment configuration for GRC Platform
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from config.environment import EnvironmentManager, Environment

class ConfigValidator:
    """Configuration validator"""
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv("ENVIRONMENT", "development")
        self.manager = EnvironmentManager(Environment(self.environment))
        self.issues = []
        self.warnings = []
    
    def validate_all(self) -> Dict[str, Any]:
        """Validate all configuration aspects"""
        print(f"🔍 Validating {self.environment} configuration...")
        
        # Validate environment variables
        self._validate_environment_variables()
        
        # Validate database configuration
        self._validate_database_config()
        
        # Validate security configuration
        self._validate_security_config()
        
        # Validate API configuration
        self._validate_api_config()
        
        # Validate Redis configuration
        self._validate_redis_config()
        
        # Validate file paths
        self._validate_file_paths()
        
        # Validate network configuration
        self._validate_network_config()
        
        return {
            "valid": len(self.issues) == 0,
            "issues": self.issues,
            "warnings": self.warnings,
            "environment": self.environment
        }
    
    def _validate_environment_variables(self):
        """Validate required environment variables"""
        required_vars = {
            "development": ["DATABASE_URL"],
            "testing": ["DATABASE_URL", "TEST_DATABASE_URL"],
            "staging": ["DATABASE_URL", "SECRET_KEY", "POSTGRES_PASSWORD"],
            "production": ["DATABASE_URL", "SECRET_KEY", "POSTGRES_PASSWORD", "REDIS_PASSWORD"]
        }
        
        for var in required_vars.get(self.environment, []):
            if not os.getenv(var):
                self.issues.append(f"Required environment variable {var} not set")
    
    def _validate_database_config(self):
        """Validate database configuration"""
        db_config = self.manager.get("database")
        
        # Check database URL format
        if not db_config.url.startswith("postgresql://"):
            self.issues.append("Invalid database URL format")
        
        # Check password security
        if self.environment == "production":
            if db_config.password in ["grc_password", "demo-secret-key-change-in-production"]:
                self.issues.append("Production database password not changed from default")
        
        # Check connection pool settings
        if db_config.pool_size < 5:
            self.warnings.append("Database pool size is low for production")
        
        if db_config.max_overflow < 10:
            self.warnings.append("Database max overflow is low for production")
    
    def _validate_security_config(self):
        """Validate security configuration"""
        security_config = self.manager.get("security")
        
        # Check secret key security
        if self.environment == "production":
            if security_config.secret_key in ["demo-secret-key-change-in-production", "test-secret-key-for-testing"]:
                self.issues.append("Production secret key not changed from default")
        
        # Check password requirements
        if security_config.password_min_length < 8:
            self.warnings.append("Password minimum length is less than 8 characters")
        
        # Check token expiration
        if security_config.access_token_expire_minutes > 60:
            self.warnings.append("Access token expiration is longer than 60 minutes")
        
        # Check lockout settings
        if security_config.max_login_attempts > 10:
            self.warnings.append("Max login attempts is high, consider reducing for security")
    
    def _validate_api_config(self):
        """Validate API configuration"""
        api_config = self.manager.get("api")
        
        # Check CORS configuration
        if self.environment == "production":
            if "*" in api_config.cors_origins:
                self.issues.append("CORS origins should not include '*' in production")
        
        # Check worker configuration
        if self.environment == "production" and api_config.workers < 2:
            self.warnings.append("Consider using more workers for production")
        
        # Check debug settings
        if api_config.debug and self.environment == "production":
            self.issues.append("Debug mode should be disabled in production")
    
    def _validate_redis_config(self):
        """Validate Redis configuration"""
        redis_config = self.manager.get("redis")
        
        # Check Redis URL format
        if not redis_config.url.startswith("redis://"):
            self.issues.append("Invalid Redis URL format")
        
        # Check password security
        if self.environment == "production":
            if not redis_config.password:
                self.warnings.append("Redis password not set for production")
    
    def _validate_file_paths(self):
        """Validate file paths"""
        logging_config = self.manager.get("logging")
        
        if logging_config.file_path:
            log_dir = Path(logging_config.file_path).parent
            if not log_dir.exists():
                self.warnings.append(f"Log directory does not exist: {log_dir}")
    
    def _validate_network_config(self):
        """Validate network configuration"""
        api_config = self.manager.get("api")
        
        # Check port configuration
        if api_config.port < 1024 and os.geteuid() != 0:
            self.warnings.append("API port requires root privileges")
        
        # Check host configuration
        if api_config.host == "127.0.0.1" and self.environment == "production":
            self.warnings.append("API host should not be localhost in production")
    
    def print_results(self, results: Dict[str, Any]):
        """Print validation results"""
        print(f"\n📊 Configuration Validation Results for {results['environment']}")
        print("=" * 60)
        
        if results["valid"]:
            print("✅ Configuration is valid!")
        else:
            print("❌ Configuration has issues:")
            for issue in results["issues"]:
                print(f"  • {issue}")
        
        if results["warnings"]:
            print("\n⚠️  Warnings:")
            for warning in results["warnings"]:
                print(f"  • {warning}")
        
        print(f"\n📈 Summary:")
        print(f"  • Issues: {len(results['issues'])}")
        print(f"  • Warnings: {len(results['warnings'])}")
        print(f"  • Valid: {'Yes' if results['valid'] else 'No'}")
    
    def generate_config_template(self, output_file: str = None):
        """Generate configuration template"""
        if not output_file:
            output_file = f"config/environments/{self.environment}.env.template"
        
        template_content = f"""# {self.environment.title()} Environment Configuration Template
# GRC Platform {self.environment.title()} Settings

# Environment
ENVIRONMENT={self.environment}
DEBUG={'true' if self.environment == 'development' else 'false'}
LOG_LEVEL={'DEBUG' if self.environment == 'development' else 'INFO'}

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=grc_platform
POSTGRES_USER=grc_user
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
DATABASE_URL=postgresql://grc_user:CHANGE_ME_SECURE_PASSWORD@localhost:5432/grc_platform

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD={'CHANGE_ME_REDIS_PASSWORD' if self.environment == 'production' else ''}
REDIS_URL=redis://localhost:6379/0

# Security Configuration
SECRET_KEY=CHANGE_ME_JWT_SECRET_KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES={'60' if self.environment == 'development' else '15'}
REFRESH_TOKEN_EXPIRE_DAYS={'7' if self.environment == 'development' else '1'}
PASSWORD_MIN_LENGTH=8
MAX_LOGIN_ATTEMPTS={'10' if self.environment == 'development' else '3'}
LOCKOUT_DURATION_MINUTES={'5' if self.environment == 'development' else '30'}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
WORKERS={'1' if self.environment == 'development' else '4'}
RELOAD={'true' if self.environment == 'development' else 'false'}
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_ENVIRONMENT={self.environment}
REACT_APP_DEBUG={'true' if self.environment == 'development' else 'false'}

# BFSI AI Configuration
BFSI_AI_HOST=localhost
BFSI_AI_PORT=8001
BFSI_AI_MODEL_PATH=./models
BFSI_AI_MAX_WORKERS={'2' if self.environment == 'development' else '8'}
BFSI_AI_TIMEOUT=300
BFSI_AI_CACHE_TTL=3600

# Logging Configuration
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE_PATH=./logs/{self.environment}.log
LOG_MAX_FILE_SIZE=10485760
LOG_BACKUP_COUNT=5
"""
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(template_content)
        
        print(f"📝 Configuration template generated: {output_file}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Validate GRC Platform configuration")
    parser.add_argument("--environment", "-e", choices=["development", "testing", "staging", "production"],
                       default=os.getenv("ENVIRONMENT", "development"),
                       help="Environment to validate")
    parser.add_argument("--generate-template", "-t", action="store_true",
                       help="Generate configuration template")
    parser.add_argument("--output", "-o", help="Output file for template")
    
    args = parser.parse_args()
    
    validator = ConfigValidator(args.environment)
    
    if args.generate_template:
        validator.generate_config_template(args.output)
    else:
        results = validator.validate_all()
        validator.print_results(results)
        
        if not results["valid"]:
            sys.exit(1)

if __name__ == "__main__":
    main()
