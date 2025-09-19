#!/usr/bin/env python3
"""
System Update Checker and Updater
=================================

This script checks for updates across all system components and provides
options to update them to the latest versions.

Usage:
    python system_update_checker.py [--check] [--update] [--all] [--verbose]
"""

import subprocess
import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
import logging
from datetime import datetime
import requests
from packaging import version

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemUpdateChecker:
    """Comprehensive system update checker and updater."""
    
    def __init__(self):
        self.conda_paths = [
            r"C:\Users\Admin\anaconda3\Scripts\conda.exe",
            r"C:\Users\Admin\anaconda3\condabin\conda.bat"
        ]
        self.update_results = {}
        
    def get_latest_version_info(self, tool_name: str) -> Optional[str]:
        """Get latest version information from various sources."""
        try:
            if tool_name == "python":
                response = requests.get("https://api.github.com/repos/python/cpython/releases/latest", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return data["tag_name"].replace("v", "")
            
            elif tool_name == "node":
                response = requests.get("https://nodejs.org/dist/latest/", timeout=10)
                if response.status_code == 200:
                    # Extract version from HTML
                    version_match = re.search(r'node-v(\d+\.\d+\.\d+)', response.text)
                    if version_match:
                        return version_match.group(1)
            
            elif tool_name == "npm":
                response = requests.get("https://registry.npmjs.org/npm/latest", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return data["version"]
            
            elif tool_name == "docker":
                response = requests.get("https://api.github.com/repos/docker/docker-ce/releases/latest", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return data["tag_name"].replace("v", "")
            
            elif tool_name == "git":
                response = requests.get("https://api.github.com/repos/git/git/releases/latest", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return data["tag_name"].replace("v", "")
        
        except Exception as e:
            logger.debug(f"Failed to get latest version for {tool_name}: {e}")
        
        return None
    
    def check_conda_updates(self) -> Dict:
        """Check for conda and Anaconda updates."""
        result = {
            "tool": "conda",
            "current_version": "unknown",
            "latest_version": "unknown",
            "needs_update": False,
            "update_available": False,
            "error": None
        }
        
        # Find working conda executable
        conda_exe = None
        for conda_path in self.conda_paths:
            if os.path.exists(conda_path):
                conda_exe = conda_path
                break
        
        if not conda_exe:
            result["error"] = "Conda executable not found"
            return result
        
        try:
            # Get current version
            version_result = subprocess.run([conda_exe, "--version"], 
                                          capture_output=True, text=True, timeout=10)
            if version_result.returncode == 0:
                version_match = re.search(r'conda (\d+\.\d+\.\d+)', version_result.stdout)
                if version_match:
                    result["current_version"] = version_match.group(1)
            
            # Check for updates
            update_result = subprocess.run([conda_exe, "update", "--dry-run", "conda"], 
                                         capture_output=True, text=True, timeout=30)
            if update_result.returncode == 0:
                if "The following packages will be UPDATED" in update_result.stdout:
                    result["update_available"] = True
                    result["needs_update"] = True
            
            # Get latest version info
            latest_version = self.get_latest_version_info("conda")
            if latest_version:
                result["latest_version"] = latest_version
                
                if result["current_version"] != "unknown":
                    current_v = version.parse(result["current_version"])
                    latest_v = version.parse(latest_version)
                    if current_v < latest_v:
                        result["needs_update"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def check_python_updates(self) -> Dict:
        """Check for Python updates."""
        result = {
            "tool": "python",
            "current_version": "unknown",
            "latest_version": "unknown",
            "needs_update": False,
            "update_available": False,
            "error": None
        }
        
        try:
            # Get current version
            version_result = subprocess.run([sys.executable, "--version"], 
                                          capture_output=True, text=True, timeout=10)
            if version_result.returncode == 0:
                version_match = re.search(r'Python (\d+\.\d+\.\d+)', version_result.stdout)
                if version_match:
                    result["current_version"] = version_match.group(1)
            
            # Get latest version
            latest_version = self.get_latest_version_info("python")
            if latest_version:
                result["latest_version"] = latest_version
                
                if result["current_version"] != "unknown":
                    current_v = version.parse(result["current_version"])
                    latest_v = version.parse(latest_version)
                    if current_v < latest_v:
                        result["needs_update"] = True
                        result["update_available"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def check_pip_updates(self) -> Dict:
        """Check for pip updates."""
        result = {
            "tool": "pip",
            "current_version": "unknown",
            "latest_version": "unknown",
            "needs_update": False,
            "update_available": False,
            "error": None
        }
        
        try:
            # Get current version
            version_result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                          capture_output=True, text=True, timeout=10)
            if version_result.returncode == 0:
                version_match = re.search(r'pip (\d+\.\d+\.\d+)', version_result.stdout)
                if version_match:
                    result["current_version"] = version_match.group(1)
            
            # Check for updates
            outdated_result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated"], 
                                           capture_output=True, text=True, timeout=30)
            if outdated_result.returncode == 0:
                if "pip" in outdated_result.stdout:
                    result["update_available"] = True
                    result["needs_update"] = True
            
            # Get latest version
            latest_version = self.get_latest_version_info("npm")  # pip uses npm registry
            if latest_version:
                result["latest_version"] = latest_version
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def check_node_updates(self) -> Dict:
        """Check for Node.js updates."""
        result = {
            "tool": "node",
            "current_version": "unknown",
            "latest_version": "unknown",
            "needs_update": False,
            "update_available": False,
            "error": None
        }
        
        try:
            # Get current version
            version_result = subprocess.run(["node", "--version"], 
                                          capture_output=True, text=True, timeout=10)
            if version_result.returncode == 0:
                result["current_version"] = version_result.stdout.strip().replace("v", "")
            
            # Get latest version
            latest_version = self.get_latest_version_info("node")
            if latest_version:
                result["latest_version"] = latest_version
                
                if result["current_version"] != "unknown":
                    current_v = version.parse(result["current_version"])
                    latest_v = version.parse(latest_version)
                    if current_v < latest_v:
                        result["needs_update"] = True
                        result["update_available"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def check_npm_updates(self) -> Dict:
        """Check for npm updates."""
        result = {
            "tool": "npm",
            "current_version": "unknown",
            "latest_version": "unknown",
            "needs_update": False,
            "update_available": False,
            "error": None
        }
        
        try:
            # Get current version
            version_result = subprocess.run(["npm", "--version"], 
                                          capture_output=True, text=True, timeout=10)
            if version_result.returncode == 0:
                result["current_version"] = version_result.stdout.strip()
            
            # Check for global updates
            outdated_result = subprocess.run(["npm", "outdated", "-g"], 
                                           capture_output=True, text=True, timeout=30)
            if outdated_result.returncode == 0:
                if "npm" in outdated_result.stdout:
                    result["update_available"] = True
                    result["needs_update"] = True
            
            # Get latest version
            latest_version = self.get_latest_version_info("npm")
            if latest_version:
                result["latest_version"] = latest_version
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def check_docker_updates(self) -> Dict:
        """Check for Docker updates."""
        result = {
            "tool": "docker",
            "current_version": "unknown",
            "latest_version": "unknown",
            "needs_update": False,
            "update_available": False,
            "error": None
        }
        
        try:
            # Get current version
            version_result = subprocess.run(["docker", "--version"], 
                                          capture_output=True, text=True, timeout=10)
            if version_result.returncode == 0:
                version_match = re.search(r'Docker version (\d+\.\d+\.\d+)', version_result.stdout)
                if version_match:
                    result["current_version"] = version_match.group(1)
            
            # Get latest version
            latest_version = self.get_latest_version_info("docker")
            if latest_version:
                result["latest_version"] = latest_version
                
                if result["current_version"] != "unknown":
                    current_v = version.parse(result["current_version"])
                    latest_v = version.parse(latest_version)
                    if current_v < latest_v:
                        result["needs_update"] = True
                        result["update_available"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def check_git_updates(self) -> Dict:
        """Check for Git updates."""
        result = {
            "tool": "git",
            "current_version": "unknown",
            "latest_version": "unknown",
            "needs_update": False,
            "update_available": False,
            "error": None
        }
        
        try:
            # Get current version
            version_result = subprocess.run(["git", "--version"], 
                                          capture_output=True, text=True, timeout=10)
            if version_result.returncode == 0:
                version_match = re.search(r'git version (\d+\.\d+\.\d+)', version_result.stdout)
                if version_match:
                    result["current_version"] = version_match.group(1)
            
            # Get latest version
            latest_version = self.get_latest_version_info("git")
            if latest_version:
                result["latest_version"] = latest_version
                
                if result["current_version"] != "unknown":
                    current_v = version.parse(result["current_version"])
                    latest_v = version.parse(latest_version)
                    if current_v < latest_v:
                        result["needs_update"] = True
                        result["update_available"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def check_python_packages(self) -> Dict:
        """Check for outdated Python packages."""
        result = {
            "tool": "python_packages",
            "outdated_packages": [],
            "total_outdated": 0,
            "error": None
        }
        
        try:
            # Get outdated packages
            outdated_result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated"], 
                                           capture_output=True, text=True, timeout=60)
            if outdated_result.returncode == 0:
                lines = outdated_result.stdout.strip().split('\n')[2:]  # Skip header
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            result["outdated_packages"].append({
                                "name": parts[0],
                                "current": parts[1],
                                "latest": parts[2]
                            })
                
                result["total_outdated"] = len(result["outdated_packages"])
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def run_all_checks(self) -> Dict:
        """Run all update checks."""
        logger.info("Starting comprehensive system update check...")
        
        checks = {
            "conda": self.check_conda_updates(),
            "python": self.check_python_updates(),
            "pip": self.check_pip_updates(),
            "node": self.check_node_updates(),
            "npm": self.check_npm_updates(),
            "docker": self.check_docker_updates(),
            "git": self.check_git_updates(),
            "python_packages": self.check_python_packages()
        }
        
        self.update_results = checks
        return checks
    
    def update_conda(self) -> bool:
        """Update conda."""
        conda_exe = None
        for conda_path in self.conda_paths:
            if os.path.exists(conda_path):
                conda_exe = conda_path
                break
        
        if not conda_exe:
            logger.error("Conda executable not found")
            return False
        
        try:
            logger.info("Updating conda...")
            result = subprocess.run([conda_exe, "update", "-y", "conda"], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                logger.info("✅ Conda updated successfully")
                return True
            else:
                logger.error(f"❌ Conda update failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ Conda update exception: {e}")
            return False
    
    def update_pip(self) -> bool:
        """Update pip."""
        try:
            logger.info("Updating pip...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                logger.info("✅ pip updated successfully")
                return True
            else:
                logger.error(f"❌ pip update failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ pip update exception: {e}")
            return False
    
    def update_npm(self) -> bool:
        """Update npm."""
        try:
            logger.info("Updating npm...")
            result = subprocess.run(["npm", "install", "-g", "npm@latest"], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                logger.info("✅ npm updated successfully")
                return True
            else:
                logger.error(f"❌ npm update failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ npm update exception: {e}")
            return False
    
    def update_python_packages(self) -> bool:
        """Update all outdated Python packages."""
        try:
            logger.info("Updating Python packages...")
            
            # Get list of outdated packages
            outdated_result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated"], 
                                           capture_output=True, text=True, timeout=60)
            if outdated_result.returncode != 0:
                logger.error("Failed to get outdated packages list")
                return False
            
            lines = outdated_result.stdout.strip().split('\n')[2:]  # Skip header
            packages_to_update = []
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        packages_to_update.append(parts[0])
            
            if not packages_to_update:
                logger.info("No packages to update")
                return True
            
            # Update packages
            for package in packages_to_update:
                logger.info(f"Updating {package}...")
                result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    logger.info(f"✅ {package} updated successfully")
                else:
                    logger.warning(f"⚠️ {package} update failed: {result.stderr}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Python packages update exception: {e}")
            return False
    
    def print_results(self, verbose: bool = False):
        """Print update check results."""
        print("\n" + "="*80)
        print("SYSTEM UPDATE CHECK RESULTS")
        print("="*80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        total_updates = 0
        
        for tool_name, result in self.update_results.items():
            if tool_name == "python_packages":
                print(f"📦 Python Packages:")
                if result["error"]:
                    print(f"   ❌ Error: {result['error']}")
                else:
                    print(f"   📊 Total outdated: {result['total_outdated']}")
                    if verbose and result["outdated_packages"]:
                        for pkg in result["outdated_packages"][:10]:  # Show first 10
                            print(f"      - {pkg['name']}: {pkg['current']} → {pkg['latest']}")
                        if len(result["outdated_packages"]) > 10:
                            print(f"      ... and {len(result['outdated_packages']) - 10} more")
                    if result["total_outdated"] > 0:
                        total_updates += 1
                print()
            else:
                status_icon = "✅" if not result["needs_update"] else "🔄"
                error_icon = "❌" if result["error"] else ""
                
                print(f"{status_icon} {result['tool'].title()}:")
                if result["error"]:
                    print(f"   {error_icon} Error: {result['error']}")
                else:
                    print(f"   📍 Current: {result['current_version']}")
                    if result["latest_version"] != "unknown":
                        print(f"   🆕 Latest: {result['latest_version']}")
                    if result["needs_update"]:
                        print(f"   🔄 Update available: YES")
                        total_updates += 1
                    else:
                        print(f"   ✅ Up to date")
                print()
        
        print("-" * 80)
        print(f"📊 SUMMARY: {total_updates} components need updates")
        print("-" * 80)
    
    def save_results(self, filename: str = "system_update_report.json"):
        """Save results to file."""
        try:
            report_path = Path("scripts/maintenance") / filename
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "results": self.update_results,
                "summary": {
                    "total_components": len(self.update_results),
                    "components_needing_updates": sum(1 for r in self.update_results.values() 
                                                    if r.get("needs_update", False) or r.get("total_outdated", 0) > 0)
                }
            }
            
            with open(report_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            logger.info(f"Update report saved to {report_path}")
        except Exception as e:
            logger.error(f"Failed to save update report: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="System Update Checker and Updater")
    parser.add_argument("--check", action="store_true", help="Check for updates only")
    parser.add_argument("--update", action="store_true", help="Update components")
    parser.add_argument("--all", action="store_true", help="Update all components")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--report", action="store_true", help="Save detailed report")
    
    args = parser.parse_args()
    
    checker = SystemUpdateChecker()
    
    # Run checks
    results = checker.run_all_checks()
    checker.print_results(verbose=args.verbose)
    
    if args.report:
        checker.save_results()
    
    # Perform updates if requested
    if args.update or args.all:
        print("\n" + "="*80)
        print("STARTING UPDATES")
        print("="*80)
        
        updates_performed = 0
        
        # Update conda
        if args.all or (args.update and results["conda"]["needs_update"]):
            if checker.update_conda():
                updates_performed += 1
        
        # Update pip
        if args.all or (args.update and results["pip"]["needs_update"]):
            if checker.update_pip():
                updates_performed += 1
        
        # Update npm
        if args.all or (args.update and results["npm"]["needs_update"]):
            if checker.update_npm():
                updates_performed += 1
        
        # Update Python packages
        if args.all or (args.update and results["python_packages"]["total_outdated"] > 0):
            if checker.update_python_packages():
                updates_performed += 1
        
        print(f"\n✅ Updates completed: {updates_performed} components updated")
        
        # Re-run checks to verify updates
        print("\n" + "="*80)
        print("VERIFYING UPDATES")
        print("="*80)
        checker.run_all_checks()
        checker.print_results(verbose=args.verbose)
    
    # Exit with appropriate code
    total_updates_needed = sum(1 for r in results.values() 
                              if r.get("needs_update", False) or r.get("total_outdated", 0) > 0)
    
    if total_updates_needed == 0:
        sys.exit(0)  # All up to date
    else:
        sys.exit(1)  # Updates available

if __name__ == "__main__":
    main()

