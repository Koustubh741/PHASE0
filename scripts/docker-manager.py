#!/usr/bin/env python3
"""
Docker Management Script for GRC Platform
Manages Docker containers and services for development and production
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

class DockerManager:
    """Docker management utility for GRC Platform"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.docker_compose_file = self.project_root / "docker-compose.yml"
        self.docker_compose_prod_file = self.project_root / "docker-compose.prod.yml"
        self.env_file = self.project_root / "docker.env"
    
    def run_command(self, command, check=True):
        """Run a command and return the result"""
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result
    
    def check_docker(self):
        """Check if Docker and Docker Compose are available"""
        try:
            self.run_command(["docker", "--version"])
            self.run_command(["docker-compose", "--version"])
            print("✅ Docker and Docker Compose are available")
            return True
        except subprocess.CalledProcessError:
            print("❌ Docker or Docker Compose not found")
            return False
    
    def build_services(self, production=False):
        """Build all Docker services"""
        compose_file = self.docker_compose_prod_file if production else self.docker_compose_file
        env_file = f"--env-file {self.env_file}" if self.env_file.exists() else ""
        
        command = [
            "docker-compose",
            "-f", str(compose_file),
            "build",
            "--no-cache"
        ]
        
        if env_file:
            command.extend(env_file.split())
        
        print("🔨 Building Docker services...")
        self.run_command(command)
        print("✅ All services built successfully")
    
    def start_services(self, production=False, services=None):
        """Start Docker services"""
        compose_file = self.docker_compose_prod_file if production else self.docker_compose_file
        env_file = f"--env-file {self.env_file}" if self.env_file.exists() else ""
        
        command = [
            "docker-compose",
            "-f", str(compose_file),
            "up",
            "-d"
        ]
        
        if env_file:
            command.extend(env_file.split())
        
        if services:
            command.extend(services)
        
        print("🚀 Starting Docker services...")
        self.run_command(command)
        print("✅ Services started successfully")
    
    def stop_services(self, production=False):
        """Stop Docker services"""
        compose_file = self.docker_compose_prod_file if production else self.docker_compose_file
        env_file = f"--env-file {self.env_file}" if self.env_file.exists() else ""
        
        command = [
            "docker-compose",
            "-f", str(compose_file),
            "down"
        ]
        
        if env_file:
            command.extend(env_file.split())
        
        print("🛑 Stopping Docker services...")
        self.run_command(command)
        print("✅ Services stopped successfully")
    
    def restart_services(self, production=False, services=None):
        """Restart Docker services"""
        compose_file = self.docker_compose_prod_file if production else self.docker_compose_file
        env_file = f"--env-file {self.env_file}" if self.env_file.exists() else ""
        
        command = [
            "docker-compose",
            "-f", str(compose_file),
            "restart"
        ]
        
        if env_file:
            command.extend(env_file.split())
        
        if services:
            command.extend(services)
        
        print("🔄 Restarting Docker services...")
        self.run_command(command)
        print("✅ Services restarted successfully")
    
    def show_logs(self, production=False, services=None, follow=False):
        """Show service logs"""
        compose_file = self.docker_compose_prod_file if production else self.docker_compose_file
        env_file = f"--env-file {self.env_file}" if self.env_file.exists() else ""
        
        command = [
            "docker-compose",
            "-f", str(compose_file),
            "logs"
        ]
        
        if env_file:
            command.extend(env_file.split())
        
        if follow:
            command.append("-f")
        
        if services:
            command.extend(services)
        
        print("📋 Showing service logs...")
        self.run_command(command, check=False)
    
    def show_status(self, production=False):
        """Show service status"""
        compose_file = self.docker_compose_prod_file if production else self.docker_compose_file
        env_file = f"--env-file {self.env_file}" if self.env_file.exists() else ""
        
        command = [
            "docker-compose",
            "-f", str(compose_file),
            "ps"
        ]
        
        if env_file:
            command.extend(env_file.split())
        
        print("📊 Service status:")
        self.run_command(command)
    
    def health_check(self, production=False):
        """Check service health"""
        services = [
            "postgres", "redis", "backend", "frontend", 
            "api-gateway", "bfsi-ai-agents", "nginx"
        ]
        
        print("🏥 Checking service health...")
        
        for service in services:
            try:
                # Check if service is running
                result = self.run_command([
                    "docker", "ps", "--filter", f"name={service}", "--format", "table {{.Names}}\t{{.Status}}"
                ], check=False)
                
                if service in result.stdout:
                    print(f"✅ {service}: Running")
                else:
                    print(f"❌ {service}: Not running")
                    
            except Exception as e:
                print(f"❌ {service}: Error checking status - {e}")
    
    def clean_up(self):
        """Clean up Docker resources"""
        print("🧹 Cleaning up Docker resources...")
        
        # Stop and remove containers
        self.run_command(["docker-compose", "down", "-v"], check=False)
        
        # Remove unused images
        self.run_command(["docker", "image", "prune", "-f"], check=False)
        
        # Remove unused volumes
        self.run_command(["docker", "volume", "prune", "-f"], check=False)
        
        print("✅ Cleanup completed")
    
    def setup_development(self):
        """Setup development environment"""
        print("🔧 Setting up development environment...")
        
        # Check Docker
        if not self.check_docker():
            return False
        
        # Build services
        self.build_services(production=False)
        
        # Start services
        self.start_services(production=False)
        
        # Wait for services to be ready
        print("⏳ Waiting for services to be ready...")
        time.sleep(30)
        
        # Health check
        self.health_check(production=False)
        
        print("✅ Development environment ready!")
        print("🌐 Access the application at: http://localhost")
        print("📊 API Gateway: http://localhost:8080")
        print("🤖 BFSI AI Agents: http://localhost:8001")
        
        return True
    
    def setup_production(self):
        """Setup production environment"""
        print("🚀 Setting up production environment...")
        
        # Check Docker
        if not self.check_docker():
            return False
        
        # Build services
        self.build_services(production=True)
        
        # Start services
        self.start_services(production=True)
        
        # Wait for services to be ready
        print("⏳ Waiting for services to be ready...")
        time.sleep(60)
        
        # Health check
        self.health_check(production=True)
        
        print("✅ Production environment ready!")
        print("🌐 Access the application at: http://localhost")
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Docker Manager for GRC Platform")
    parser.add_argument("command", choices=[
        "check", "build", "start", "stop", "restart", "logs", "status", 
        "health", "clean", "dev", "prod"
    ], help="Command to execute")
    parser.add_argument("--production", "-p", action="store_true", 
                       help="Use production configuration")
    parser.add_argument("--services", "-s", nargs="+", 
                       help="Specific services to target")
    parser.add_argument("--follow", "-f", action="store_true", 
                       help="Follow logs in real-time")
    
    args = parser.parse_args()
    
    manager = DockerManager()
    
    if args.command == "check":
        manager.check_docker()
    elif args.command == "build":
        manager.build_services(production=args.production)
    elif args.command == "start":
        manager.start_services(production=args.production, services=args.services)
    elif args.command == "stop":
        manager.stop_services(production=args.production)
    elif args.command == "restart":
        manager.restart_services(production=args.production, services=args.services)
    elif args.command == "logs":
        manager.show_logs(production=args.production, services=args.services, follow=args.follow)
    elif args.command == "status":
        manager.show_status(production=args.production)
    elif args.command == "health":
        manager.health_check(production=args.production)
    elif args.command == "clean":
        manager.clean_up()
    elif args.command == "dev":
        manager.setup_development()
    elif args.command == "prod":
        manager.setup_production()

if __name__ == "__main__":
    main()
