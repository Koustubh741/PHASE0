#!/usr/bin/env python3
"""
Conda Health Check and Prevention Script
========================================

This script ensures conda is always working properly and prevents
the pydantic-settings compatibility issues from recurring.

Usage:
    python conda_health_check.py [--fix] [--verbose]
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CondaHealthChecker:
    """Comprehensive conda health monitoring and prevention system."""
    
    def __init__(self):
        self.conda_paths = [
            r"C:\Users\Admin\anaconda3\Scripts\conda.exe",
            r"C:\Users\Admin\anaconda3\condabin\conda.bat"
        ]
        self.required_paths = [
            r"C:\Users\Admin\anaconda3",
            r"C:\Users\Admin\anaconda3\Scripts", 
            r"C:\Users\Admin\anaconda3\Library\bin"
        ]
        self.powershell_profile = Path(r"C:\Users\Admin\Documents\WindowsPowerShell\profile.ps1")
        self.min_pydantic_settings_version = "2.10.0"
        
    def check_conda_executable(self) -> Tuple[bool, str]:
        """Check if conda executable is accessible."""
        for conda_path in self.conda_paths:
            if os.path.exists(conda_path):
                try:
                    result = subprocess.run([conda_path, "--version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        return True, result.stdout.strip()
                except Exception as e:
                    logger.warning(f"Error testing conda at {conda_path}: {e}")
        return False, "Conda executable not found or not working"
    
    def check_path_environment(self) -> Tuple[bool, List[str]]:
        """Check if conda paths are in system PATH."""
        try:
            # Get user PATH
            user_path = os.environ.get('PATH', '')
            missing_paths = []
            
            for required_path in self.required_paths:
                if required_path not in user_path:
                    missing_paths.append(required_path)
            
            return len(missing_paths) == 0, missing_paths
        except Exception as e:
            logger.error(f"Error checking PATH: {e}")
            return False, self.required_paths
    
    def check_powershell_profile(self) -> Tuple[bool, str]:
        """Check if PowerShell profile has conda initialization."""
        if not self.powershell_profile.exists():
            return False, "PowerShell profile does not exist"
        
        try:
            with open(self.powershell_profile, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "conda initialize" in content and "conda.exe" in content:
                return True, "PowerShell profile properly configured"
            else:
                return False, "PowerShell profile missing conda initialization"
        except Exception as e:
            return False, f"Error reading PowerShell profile: {e}"
    
    def check_pydantic_settings(self) -> Tuple[bool, str, str]:
        """Check pydantic-settings version and compatibility."""
        try:
            # Try to import and check version
            import pydantic_settings
            
            # Check if required class exists
            has_required_class = hasattr(pydantic_settings, 'PyprojectTomlConfigSettingsSource')
            
            # Get version
            version = getattr(pydantic_settings, '__version__', 'unknown')
            
            # Check version compatibility
            if version != 'unknown':
                from packaging import version as pkg_version
                is_compatible = pkg_version.parse(version) >= pkg_version.parse(self.min_pydantic_settings_version)
            else:
                is_compatible = has_required_class
            
            if has_required_class and is_compatible:
                return True, version, "pydantic-settings is compatible"
            else:
                return False, version, f"pydantic-settings version {version} is incompatible or missing required class"
                
        except ImportError:
            return False, "not installed", "pydantic-settings is not installed"
        except Exception as e:
            return False, "unknown", f"Error checking pydantic-settings: {e}"
    
    def test_conda_commands(self) -> Tuple[bool, List[str]]:
        """Test basic conda commands for warnings/errors."""
        test_commands = [
            ["conda", "--version"],
            ["conda", "info", "--envs"],
            ["conda", "list", "--name", "base"]
        ]
        
        errors = []
        for cmd in test_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    errors.append(f"Command {' '.join(cmd)} failed: {result.stderr}")
                elif "Error while loading conda entry point" in result.stderr:
                    errors.append(f"Command {' '.join(cmd)} has conda entry point errors")
            except Exception as e:
                errors.append(f"Command {' '.join(cmd)} exception: {e}")
        
        return len(errors) == 0, errors
    
    def fix_path_environment(self) -> bool:
        """Fix PATH environment variable."""
        try:
            import winreg
            
            # Get current user PATH
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                current_path, _ = winreg.QueryValueEx(key, "PATH")
                
                # Add missing paths
                path_parts = current_path.split(';') if current_path else []
                for required_path in self.required_paths:
                    if required_path not in path_parts:
                        path_parts.append(required_path)
                
                # Update PATH
                new_path = ';'.join(path_parts)
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                
            logger.info("PATH environment variable updated successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to fix PATH environment: {e}")
            return False
    
    def fix_pydantic_settings(self) -> bool:
        """Fix pydantic-settings compatibility."""
        try:
            # Upgrade pydantic-settings
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pydantic-settings"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("pydantic-settings upgraded successfully")
                return True
            else:
                logger.error(f"Failed to upgrade pydantic-settings: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Exception upgrading pydantic-settings: {e}")
            return False
    
    def fix_powershell_profile(self) -> bool:
        """Fix PowerShell profile."""
        try:
            # Ensure directory exists
            self.powershell_profile.parent.mkdir(parents=True, exist_ok=True)
            
            # Initialize conda for PowerShell
            conda_exe = None
            for conda_path in self.conda_paths:
                if os.path.exists(conda_path):
                    conda_exe = conda_path
                    break
            
            if not conda_exe:
                logger.error("Conda executable not found for PowerShell initialization")
                return False
            
            result = subprocess.run([conda_exe, "init", "powershell"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("PowerShell profile initialized successfully")
                return True
            else:
                logger.error(f"Failed to initialize PowerShell profile: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Exception fixing PowerShell profile: {e}")
            return False
    
    def run_health_check(self, fix_issues: bool = False, verbose: bool = False) -> Dict:
        """Run comprehensive health check."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "conda_executable": {"status": False, "message": "", "version": ""},
            "path_environment": {"status": False, "message": "", "missing_paths": []},
            "powershell_profile": {"status": False, "message": ""},
            "pydantic_settings": {"status": False, "message": "", "version": ""},
            "conda_commands": {"status": False, "message": "", "errors": []},
            "overall_status": "UNKNOWN",
            "fixes_applied": []
        }
        
        if verbose:
            logger.info("Starting comprehensive conda health check...")
        
        # Check conda executable
        conda_ok, conda_msg = self.check_conda_executable()
        results["conda_executable"]["status"] = conda_ok
        results["conda_executable"]["message"] = conda_msg
        if conda_ok:
            results["conda_executable"]["version"] = conda_msg
        
        # Check PATH environment
        path_ok, missing_paths = self.check_path_environment()
        results["path_environment"]["status"] = path_ok
        results["path_environment"]["missing_paths"] = missing_paths
        results["path_environment"]["message"] = "PATH configured correctly" if path_ok else f"Missing paths: {missing_paths}"
        
        # Check PowerShell profile
        profile_ok, profile_msg = self.check_powershell_profile()
        results["powershell_profile"]["status"] = profile_ok
        results["powershell_profile"]["message"] = profile_msg
        
        # Check pydantic-settings
        pydantic_ok, pydantic_version, pydantic_msg = self.check_pydantic_settings()
        results["pydantic_settings"]["status"] = pydantic_ok
        results["pydantic_settings"]["version"] = pydantic_version
        results["pydantic_settings"]["message"] = pydantic_msg
        
        # Test conda commands
        commands_ok, command_errors = self.test_conda_commands()
        results["conda_commands"]["status"] = commands_ok
        results["conda_commands"]["errors"] = command_errors
        results["conda_commands"]["message"] = "All conda commands working" if commands_ok else f"Command errors: {command_errors}"
        
        # Determine overall status
        all_checks = [conda_ok, path_ok, profile_ok, pydantic_ok, commands_ok]
        if all(all_checks):
            results["overall_status"] = "HEALTHY"
        elif any(all_checks):
            results["overall_status"] = "DEGRADED"
        else:
            results["overall_status"] = "CRITICAL"
        
        # Apply fixes if requested
        if fix_issues and results["overall_status"] != "HEALTHY":
            if verbose:
                logger.info("Applying fixes for detected issues...")
            
            if not path_ok:
                if self.fix_path_environment():
                    results["fixes_applied"].append("PATH environment fixed")
            
            if not pydantic_ok:
                if self.fix_pydantic_settings():
                    results["fixes_applied"].append("pydantic-settings upgraded")
            
            if not profile_ok:
                if self.fix_powershell_profile():
                    results["fixes_applied"].append("PowerShell profile initialized")
        
        return results
    
    def save_health_report(self, results: Dict, filename: str = "conda_health_report.json"):
        """Save health check results to file."""
        try:
            report_path = Path("scripts/maintenance") / filename
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Health report saved to {report_path}")
        except Exception as e:
            logger.error(f"Failed to save health report: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Conda Health Check and Prevention System")
    parser.add_argument("--fix", action="store_true", help="Automatically fix detected issues")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--report", action="store_true", help="Save detailed report to file")
    
    args = parser.parse_args()
    
    checker = CondaHealthChecker()
    results = checker.run_health_check(fix_issues=args.fix, verbose=args.verbose)
    
    # Print results
    print("\n" + "="*60)
    print("CONDA HEALTH CHECK RESULTS")
    print("="*60)
    print(f"Overall Status: {results['overall_status']}")
    print(f"Timestamp: {results['timestamp']}")
    print()
    
    for check_name, check_result in results.items():
        if isinstance(check_result, dict) and 'status' in check_result:
            status_icon = "✅" if check_result['status'] else "❌"
            print(f"{status_icon} {check_name.replace('_', ' ').title()}: {check_result['message']}")
    
    if results['fixes_applied']:
        print(f"\n🔧 Fixes Applied:")
        for fix in results['fixes_applied']:
            print(f"   - {fix}")
    
    if args.report:
        checker.save_health_report(results)
    
    # Exit with appropriate code
    if results['overall_status'] == "HEALTHY":
        sys.exit(0)
    elif results['overall_status'] == "DEGRADED":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
