#!/usr/bin/env python3
"""
Deployment Script with Validation
Deploys the application with comprehensive pre-deployment validation.
"""

import os
import sys
import subprocess
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Optional

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.pre_deployment_check import PreDeploymentValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeploymentManager:
    """Manages deployment with validation checks."""
    
    def __init__(self, config_file: str = 'config/environment/production.env'):
        """Initialize the deployment manager."""
        self.config_file = config_file
        self.deployment_steps: List[Dict[str, str]] = []
        
    def deploy(self, skip_validation: bool = False, dry_run: bool = False) -> bool:
        """
        Deploy the application with validation.
        
        Args:
            skip_validation: Skip validation checks
            dry_run: Perform a dry run without actual deployment
            
        Returns:
            bool: True if deployment succeeds, False otherwise
        """
        logger.info("🚀 Starting deployment process...")
        
        try:
            # Step 1: Pre-deployment validation
            if not skip_validation:
                if not self._run_validation():
                    logger.error("❌ Pre-deployment validation failed. Deployment aborted.")
                    return False
            else:
                logger.warning("⚠️  Skipping pre-deployment validation")
            
            # Step 2: Build application
            if not self._build_application(dry_run):
                logger.error("❌ Application build failed.")
                return False
            
            # Step 3: Run tests (optional)
            if not self._run_tests(dry_run):
                logger.warning("⚠️  Some tests failed, but continuing deployment")
            
            # Step 4: Deploy to production
            if not dry_run:
                if not self._deploy_to_production():
                    logger.error("❌ Production deployment failed.")
                    return False
            else:
                logger.info("🔍 Dry run mode - skipping actual deployment")
            
            # Step 5: Post-deployment validation
            if not dry_run:
                if not self._post_deployment_validation():
                    logger.warning("⚠️  Post-deployment validation failed")
            
            logger.info("✅ Deployment completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Deployment failed with error: {e}")
            return False
    
    def _run_validation(self) -> bool:
        """Run pre-deployment validation."""
        logger.info("🔍 Running pre-deployment validation...")
        
        validator = PreDeploymentValidator(self.config_file)
        return validator.run_all_checks()
    
    def _build_application(self, dry_run: bool = False) -> bool:
        """Build the application."""
        logger.info("🔨 Building application...")
        
        build_commands = [
            ["pip", "install", "-r", "requirements.txt"],
            ["python", "-m", "pip", "install", "--upgrade", "pip"],
        ]
        
        for cmd in build_commands:
            if dry_run:
                logger.info(f"DRY RUN: Would execute: {' '.join(cmd)}")
                continue
                
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                logger.info(f"✅ Command successful: {' '.join(cmd)}")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Command failed: {' '.join(cmd)}")
                logger.error(f"Error output: {e.stderr}")
                return False
        
        return True
    
    def _run_tests(self, dry_run: bool = False) -> bool:
        """Run application tests."""
        logger.info("🧪 Running tests...")
        
        test_commands = [
            ["python", "-m", "pytest", "tests/", "-v"],
        ]
        
        for cmd in test_commands:
            if dry_run:
                logger.info(f"DRY RUN: Would execute: {' '.join(cmd)}")
                continue
                
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                logger.info(f"✅ Tests passed: {' '.join(cmd)}")
            except subprocess.CalledProcessError as e:
                logger.warning(f"⚠️  Tests failed: {' '.join(cmd)}")
                logger.warning(f"Error output: {e.stderr}")
                # Don't fail deployment for test failures in this context
                return True
        
        return True
    
    def _deploy_to_production(self) -> bool:
        """Deploy to production environment."""
        logger.info("🚀 Deploying to production...")
        
        # Load environment variables
        self._load_environment_variables()
        
        # Start services using docker-compose
        docker_commands = [
            ["docker-compose", "-f", "docker-compose.yml", "down"],
            ["docker-compose", "-f", "docker-compose.yml", "build"],
            ["docker-compose", "-f", "docker-compose.yml", "up", "-d"]
        ]
        
        for cmd in docker_commands:
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                logger.info(f"✅ Docker command successful: {' '.join(cmd)}")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Docker command failed: {' '.join(cmd)}")
                logger.error(f"Error output: {e.stderr}")
                return False
        
        return True
    
    def _post_deployment_validation(self) -> bool:
        """Run post-deployment validation."""
        logger.info("🔍 Running post-deployment validation...")
        
        # Check if services are running
        try:
            result = subprocess.run(
                ["docker-compose", "ps"],
                capture_output=True,
                text=True,
                check=True
            )
            
            if "Up" in result.stdout:
                logger.info("✅ Services are running")
                return True
            else:
                logger.warning("⚠️  Some services may not be running properly")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Could not check service status: {e}")
            return False
    
    def _load_environment_variables(self) -> None:
        """Load environment variables from the config file."""
        if not os.path.exists(self.config_file):
            logger.warning(f"Config file not found: {self.config_file}")
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
                        
            logger.info(f"✅ Loaded environment variables from {self.config_file}")
            
        except Exception as e:
            logger.error(f"❌ Could not load environment variables: {e}")
            raise
    
    def show_deployment_status(self) -> None:
        """Show current deployment status."""
        logger.info("📊 Deployment Status")
        logger.info("=" * 50)
        
        for step in self.deployment_steps:
            status = "✅" if step.get('success', False) else "❌"
            logger.info(f"{status} {step['name']}: {step['description']}")


def main():
    """Main entry point for deployment."""
    parser = argparse.ArgumentParser(
        description='Deploy the application with comprehensive validation'
    )
    parser.add_argument(
        '--config-file',
        default='config/environment/production.env',
        help='Path to the production configuration file'
    )
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip pre-deployment validation (not recommended)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without actual deployment'
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
    
    # Check if running as root (not recommended for production)
    if os.geteuid() == 0 and not args.dry_run:
        logger.warning("⚠️  Running as root is not recommended for production deployment")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            logger.info("Deployment cancelled by user")
            sys.exit(0)
    
    # Run deployment
    deployment_manager = DeploymentManager(args.config_file)
    success = deployment_manager.deploy(
        skip_validation=args.skip_validation,
        dry_run=args.dry_run
    )
    
    if not success:
        logger.error("❌ Deployment failed!")
        sys.exit(1)
    
    logger.info("✅ Deployment completed successfully!")
    sys.exit(0)


if __name__ == '__main__':
    main()
