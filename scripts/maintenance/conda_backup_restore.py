#!/usr/bin/env python3
"""
Conda Backup and Restore System
===============================

This script creates backups of conda configuration and provides
restore functionality to prevent data loss and configuration issues.

Usage:
    python conda_backup_restore.py backup [--output-dir backups/]
    python conda_backup_restore.py restore [--backup-file backup_20240101_120000.tar.gz]
    python conda_backup_restore.py list-backups
"""

import subprocess
import sys
import os
import json
import tarfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse
import logging

class CondaBackupRestore:
    """Conda configuration backup and restore system."""
    
    def __init__(self, backup_dir: str = "scripts/maintenance/conda_backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Key conda paths to backup
        self.conda_paths = {
            "anaconda3": Path(r"C:\Users\Admin\anaconda3"),
            "powershell_profile": Path(r"C:\Users\Admin\Documents\WindowsPowerShell\profile.ps1"),
            "conda_config": Path(r"C:\Users\Admin\.condarc"),
            "conda_envs": Path(r"C:\Users\Admin\anaconda3\envs")
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def get_backup_filename(self, backup_type: str = "full") -> str:
        """Generate backup filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"conda_backup_{backup_type}_{timestamp}.tar.gz"
    
    def backup_conda_config(self) -> Dict:
        """Backup conda configuration files."""
        config_backup = {}
        
        # Backup PowerShell profile
        if self.conda_paths["powershell_profile"].exists():
            try:
                with open(self.conda_paths["powershell_profile"], 'r', encoding='utf-8') as f:
                    config_backup["powershell_profile"] = f.read()
                self.logger.info("✅ PowerShell profile backed up")
            except Exception as e:
                self.logger.error(f"❌ Failed to backup PowerShell profile: {e}")
        
        # Backup conda config
        if self.conda_paths["conda_config"].exists():
            try:
                with open(self.conda_paths["conda_config"], 'r', encoding='utf-8') as f:
                    config_backup["conda_config"] = f.read()
                self.logger.info("✅ Conda config backed up")
            except Exception as e:
                self.logger.error(f"❌ Failed to backup conda config: {e}")
        
        # Get conda environment list
        try:
            result = subprocess.run(["conda", "env", "list", "--json"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                config_backup["env_list"] = json.loads(result.stdout)
                self.logger.info("✅ Conda environment list backed up")
        except Exception as e:
            self.logger.error(f"❌ Failed to backup environment list: {e}")
        
        # Get package lists for each environment
        config_backup["package_lists"] = {}
        for env_name in ["base"]:  # Add other environments as needed
            try:
                result = subprocess.run(["conda", "list", "--name", env_name, "--json"], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    config_backup["package_lists"][env_name] = json.loads(result.stdout)
                    self.logger.info(f"✅ Package list for {env_name} backed up")
            except Exception as e:
                self.logger.error(f"❌ Failed to backup package list for {env_name}: {e}")
        
        return config_backup
    
    def backup_conda_environments(self) -> List[str]:
        """Backup conda environments."""
        backed_up_envs = []
        
        try:
            # Get list of environments
            result = subprocess.run(["conda", "env", "list", "--json"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                self.logger.error("Failed to get environment list")
                return backed_up_envs
            
            envs_data = json.loads(result.stdout)
            
            for env_info in envs_data.get("envs", []):
                env_path = Path(env_info)
                env_name = env_path.name
                
                if env_name in ["base"]:  # Skip base environment for now (too large)
                    continue
                
                try:
                    # Export environment
                    export_file = self.backup_dir / f"{env_name}_environment.yml"
                    result = subprocess.run([
                        "conda", "env", "export", "--name", env_name, "--file", str(export_file)
                    ], capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        backed_up_envs.append(str(export_file))
                        self.logger.info(f"✅ Environment {env_name} exported")
                    else:
                        self.logger.error(f"❌ Failed to export environment {env_name}: {result.stderr}")
                
                except Exception as e:
                    self.logger.error(f"❌ Exception exporting environment {env_name}: {e}")
        
        except Exception as e:
            self.logger.error(f"❌ Failed to backup environments: {e}")
        
        return backed_up_envs
    
    def create_backup(self, backup_type: str = "full") -> str:
        """Create a complete conda backup."""
        backup_filename = self.get_backup_filename(backup_type)
        backup_path = self.backup_dir / backup_filename
        
        self.logger.info(f"Creating conda backup: {backup_filename}")
        
        try:
            with tarfile.open(backup_path, "w:gz") as tar:
                # Backup configuration
                config_backup = self.backup_conda_config()
                config_file = self.backup_dir / "conda_config.json"
                
                with open(config_file, 'w') as f:
                    json.dump(config_backup, f, indent=2)
                
                tar.add(config_file, arcname="conda_config.json")
                config_file.unlink()  # Remove temporary file
                
                # Backup environments
                if backup_type == "full":
                    env_files = self.backup_conda_environments()
                    for env_file in env_files:
                        tar.add(env_file, arcname=Path(env_file).name)
                        Path(env_file).unlink()  # Remove temporary file
                
                # Add backup metadata
                metadata = {
                    "backup_type": backup_type,
                    "timestamp": datetime.now().isoformat(),
                    "conda_version": self.get_conda_version(),
                    "python_version": sys.version,
                    "platform": sys.platform
                }
                
                metadata_file = self.backup_dir / "backup_metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                tar.add(metadata_file, arcname="backup_metadata.json")
                metadata_file.unlink()  # Remove temporary file
            
            self.logger.info(f"✅ Backup created successfully: {backup_path}")
            return str(backup_path)
        
        except Exception as e:
            self.logger.error(f"❌ Failed to create backup: {e}")
            if backup_path.exists():
                backup_path.unlink()
            raise
    
    def get_conda_version(self) -> str:
        """Get current conda version."""
        try:
            result = subprocess.run(["conda", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"
    
    def list_backups(self) -> List[Dict]:
        """List available backups."""
        backups = []
        
        for backup_file in self.backup_dir.glob("conda_backup_*.tar.gz"):
            try:
                with tarfile.open(backup_file, "r:gz") as tar:
                    # Try to read metadata
                    try:
                        metadata_member = tar.getmember("backup_metadata.json")
                        metadata_file = tar.extractfile(metadata_member)
                        if metadata_file:
                            metadata = json.load(metadata_file)
                            backups.append({
                                "filename": backup_file.name,
                                "path": str(backup_file),
                                "size": backup_file.stat().st_size,
                                "timestamp": metadata.get("timestamp", "unknown"),
                                "conda_version": metadata.get("conda_version", "unknown"),
                                "backup_type": metadata.get("backup_type", "unknown")
                            })
                    except KeyError:
                        # Fallback for backups without metadata
                        backups.append({
                            "filename": backup_file.name,
                            "path": str(backup_file),
                            "size": backup_file.stat().st_size,
                            "timestamp": "unknown",
                            "conda_version": "unknown",
                            "backup_type": "unknown"
                        })
            except Exception as e:
                self.logger.error(f"Error reading backup {backup_file}: {e}")
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return backups
    
    def restore_backup(self, backup_file: str) -> bool:
        """Restore from backup."""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            self.logger.error(f"Backup file not found: {backup_file}")
            return False
        
        self.logger.info(f"Restoring from backup: {backup_path}")
        
        try:
            # Extract backup
            extract_dir = self.backup_dir / "restore_temp"
            extract_dir.mkdir(exist_ok=True)
            
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(extract_dir)
            
            # Read metadata
            metadata_file = extract_dir / "backup_metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                self.logger.info(f"Backup metadata: {metadata}")
            
            # Restore configuration
            config_file = extract_dir / "conda_config.json"
            if config_file.exists():
                with open(config_file) as f:
                    config_backup = json.load(f)
                
                # Restore PowerShell profile
                if "powershell_profile" in config_backup:
                    profile_path = self.conda_paths["powershell_profile"]
                    profile_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(profile_path, 'w', encoding='utf-8') as f:
                        f.write(config_backup["powershell_profile"])
                    self.logger.info("✅ PowerShell profile restored")
                
                # Restore conda config
                if "conda_config" in config_backup:
                    config_path = self.conda_paths["conda_config"]
                    config_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(config_path, 'w') as f:
                        f.write(config_backup["conda_config"])
                    self.logger.info("✅ Conda config restored")
            
            # Restore environments
            for env_file in extract_dir.glob("*_environment.yml"):
                env_name = env_file.stem.replace("_environment", "")
                try:
                    result = subprocess.run([
                        "conda", "env", "create", "--name", env_name, "--file", str(env_file)
                    ], capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        self.logger.info(f"✅ Environment {env_name} restored")
                    else:
                        self.logger.error(f"❌ Failed to restore environment {env_name}: {result.stderr}")
                
                except Exception as e:
                    self.logger.error(f"❌ Exception restoring environment {env_name}: {e}")
            
            # Cleanup
            shutil.rmtree(extract_dir)
            
            self.logger.info("✅ Backup restore completed")
            return True
        
        except Exception as e:
            self.logger.error(f"❌ Failed to restore backup: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count: int = 5):
        """Clean up old backups, keeping only the most recent ones."""
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            self.logger.info(f"Only {len(backups)} backups found, no cleanup needed")
            return
        
        backups_to_remove = backups[keep_count:]
        
        for backup in backups_to_remove:
            try:
                Path(backup["path"]).unlink()
                self.logger.info(f"🗑️ Removed old backup: {backup['filename']}")
            except Exception as e:
                self.logger.error(f"❌ Failed to remove backup {backup['filename']}: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Conda Backup and Restore System")
    parser.add_argument("action", choices=["backup", "restore", "list-backups", "cleanup"], 
                       help="Action to perform")
    parser.add_argument("--backup-file", help="Backup file to restore")
    parser.add_argument("--backup-dir", default="scripts/maintenance/conda_backups", 
                       help="Backup directory")
    parser.add_argument("--backup-type", choices=["full", "config"], default="full",
                       help="Type of backup to create")
    parser.add_argument("--keep-count", type=int, default=5,
                       help="Number of backups to keep during cleanup")
    
    args = parser.parse_args()
    
    backup_restore = CondaBackupRestore(backup_dir=args.backup_dir)
    
    if args.action == "backup":
        try:
            backup_path = backup_restore.create_backup(args.backup_type)
            print(f"✅ Backup created: {backup_path}")
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            sys.exit(1)
    
    elif args.action == "restore":
        if not args.backup_file:
            print("❌ --backup-file is required for restore action")
            sys.exit(1)
        
        if backup_restore.restore_backup(args.backup_file):
            print("✅ Backup restored successfully")
        else:
            print("❌ Backup restore failed")
            sys.exit(1)
    
    elif args.action == "list-backups":
        backups = backup_restore.list_backups()
        
        if not backups:
            print("No backups found")
            return
        
        print(f"\nFound {len(backups)} backups:")
        print("-" * 80)
        print(f"{'Filename':<40} {'Size':<10} {'Type':<8} {'Timestamp':<20}")
        print("-" * 80)
        
        for backup in backups:
            size_mb = backup["size"] / (1024 * 1024)
            timestamp = backup["timestamp"][:19] if backup["timestamp"] != "unknown" else "unknown"
            print(f"{backup['filename']:<40} {size_mb:>6.1f}MB {backup['backup_type']:<8} {timestamp:<20}")
    
    elif args.action == "cleanup":
        backup_restore.cleanup_old_backups(args.keep_count)
        print(f"✅ Cleanup completed, keeping {args.keep_count} most recent backups")

if __name__ == "__main__":
    main()
