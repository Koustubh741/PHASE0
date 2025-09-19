#!/usr/bin/env python3
"""
GRC Platform Service Startup Script
Structured startup script following industry standards
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ServiceManager:
    """Manages GRC Platform services with proper structure"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent.parent
        self.services: Dict[str, subprocess.Popen] = {}
        self.service_configs = {
            'postgres': {
                'command': ['docker', 'run', '-d', '--name', 'grc-postgres', 
                           '-p', '5432:5432', '-e', 'POSTGRES_PASSWORD=password',
                           'postgres:15-alpine'],
                'health_check': 'docker ps --filter name=grc-postgres --filter status=running',
                'port': 5432
            },
            'redis': {
                'command': ['docker', 'run', '-d', '--name', 'grc-redis',
                           '-p', '6379:6379', 'redis:7-alpine'],
                'health_check': 'docker ps --filter name=grc-redis --filter status=running',
                'port': 6379
            },
            'api-gateway': {
                'command': ['python', 'main.py'],
                'working_dir': self.project_root / 'src' / 'backend' / 'api-gateway',
                'port': 8000,
                'health_check': 'curl -f http://localhost:8000/health'
            },
            'ai-agents': {
                'command': ['python', 'ai_agents_service.py'],
                'working_dir': self.project_root / 'src' / 'backend' / 'services',
                'port': 8005,
                'health_check': 'curl -f http://localhost:8005/health'
            },
            'frontend': {
                'command': ['npm', 'start'],
                'working_dir': self.project_root / 'src' / 'frontend',
                'port': 3000,
                'health_check': 'curl -f http://localhost:3000'
            }
        }
    
    def start_service(self, service_name: str) -> bool:
        """Start a specific service"""
        if service_name not in self.service_configs:
            logger.error(f"Unknown service: {service_name}")
            return False
        
        config = self.service_configs[service_name]
        logger.info(f"Starting {service_name}...")
        
        try:
            # Set working directory if specified
            cwd = config.get('working_dir')
            if cwd and not cwd.exists():
                logger.error(f"Working directory does not exist: {cwd}")
                return False
            
            # Start the service
            process = subprocess.Popen(
                config['command'],
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.services[service_name] = process
            logger.info(f"✅ {service_name} started with PID {process.pid}")
            
            # Wait a moment for service to initialize
            time.sleep(2)
            
            # Check if service is healthy
            if self.check_service_health(service_name):
                logger.info(f"✅ {service_name} is healthy")
                return True
            else:
                logger.warning(f"⚠️ {service_name} started but health check failed")
                return True  # Still consider it started
                
        except Exception as e:
            logger.error(f"Failed to start {service_name}: {e}")
            return False
    
    def check_service_health(self, service_name: str) -> bool:
        """Check if a service is healthy"""
        config = self.service_configs.get(service_name)
        if not config:
            return False
        
        health_check = config.get('health_check')
        if not health_check:
            return True  # No health check defined
        
        try:
            result = subprocess.run(
                health_check.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logger.debug(f"Health check failed for {service_name}: {e}")
            return False
    
    def start_all_services(self) -> Dict[str, bool]:
        """Start all services in the correct order"""
        logger.info("🚀 Starting GRC Platform Services...")
        
        # Define startup order
        startup_order = ['postgres', 'redis', 'api-gateway', 'ai-agents', 'frontend']
        results = {}
        
        for service in startup_order:
            results[service] = self.start_service(service)
            if not results[service]:
                logger.error(f"Failed to start {service}, stopping startup process")
                break
            time.sleep(3)  # Wait between services
        
        return results
    
    def stop_all_services(self):
        """Stop all running services"""
        logger.info("🛑 Stopping all services...")
        
        for service_name, process in self.services.items():
            try:
                logger.info(f"Stopping {service_name}...")
                process.terminate()
                process.wait(timeout=10)
                logger.info(f"✅ {service_name} stopped")
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {service_name}...")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {service_name}: {e}")
        
        self.services.clear()
    
    def get_service_status(self) -> Dict[str, Dict]:
        """Get status of all services"""
        status = {}
        
        for service_name, config in self.service_configs.items():
            is_running = service_name in self.services
            is_healthy = self.check_service_health(service_name) if is_running else False
            
            status[service_name] = {
                'running': is_running,
                'healthy': is_healthy,
                'port': config.get('port'),
                'pid': self.services[service_name].pid if is_running else None
            }
        
        return status
    
    def print_status(self):
        """Print current service status"""
        status = self.get_service_status()
        
        print("\n" + "="*60)
        print("📊 GRC PLATFORM SERVICE STATUS")
        print("="*60)
        
        for service_name, info in status.items():
            status_icon = "✅" if info['healthy'] else "🟡" if info['running'] else "❌"
            health_text = "Healthy" if info['healthy'] else "Running" if info['running'] else "Stopped"
            port_text = f" (Port {info['port']})" if info['port'] else ""
            pid_text = f" [PID: {info['pid']}]" if info['pid'] else ""
            
            print(f"{status_icon} {service_name.upper()}: {health_text}{port_text}{pid_text}")
        
        print("="*60)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GRC Platform Service Manager')
    parser.add_argument('action', choices=['start', 'stop', 'status', 'restart'],
                       help='Action to perform')
    parser.add_argument('--service', help='Specific service to manage')
    parser.add_argument('--project-root', help='Project root directory')
    
    args = parser.parse_args()
    
    # Initialize service manager
    manager = ServiceManager(args.project_root)
    
    try:
        if args.action == 'start':
            if args.service:
                success = manager.start_service(args.service)
                sys.exit(0 if success else 1)
            else:
                results = manager.start_all_services()
                manager.print_status()
                sys.exit(0 if all(results.values()) else 1)
        
        elif args.action == 'stop':
            manager.stop_all_services()
            print("✅ All services stopped")
        
        elif args.action == 'status':
            manager.print_status()
        
        elif args.action == 'restart':
            manager.stop_all_services()
            time.sleep(2)
            results = manager.start_all_services()
            manager.print_status()
            sys.exit(0 if all(results.values()) else 1)
    
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
        manager.stop_all_services()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
