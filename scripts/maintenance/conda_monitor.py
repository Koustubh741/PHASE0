#!/usr/bin/env python3
"""
Conda Automatic Monitoring System
=================================

This script runs continuous monitoring to prevent conda issues
from occurring and automatically fixes them when detected.

Usage:
    python conda_monitor.py [--daemon] [--interval 300] [--log-file conda_monitor.log]
"""

import subprocess
import sys
import os
import time
import json
import signal
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
import argparse
import logging
import schedule

# Import our health checker
sys.path.append(str(Path(__file__).parent))
from conda_health_check import CondaHealthChecker

class CondaMonitor:
    """Automatic conda monitoring and prevention system."""
    
    def __init__(self, log_file: str = "conda_monitor.log", check_interval: int = 300):
        self.log_file = log_file
        self.check_interval = check_interval
        self.running = False
        self.health_checker = CondaHealthChecker()
        self.last_healthy_check = None
        self.consecutive_failures = 0
        self.max_consecutive_failures = 3
        
        # Setup logging
        self.setup_logging()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def check_conda_health(self) -> Dict:
        """Run health check and return results."""
        try:
            results = self.health_checker.run_health_check(fix_issues=True, verbose=False)
            return results
        except Exception as e:
            self.logger.error(f"Error during health check: {e}")
            return {"overall_status": "ERROR", "error": str(e)}
    
    def log_health_status(self, results: Dict):
        """Log health status with appropriate level."""
        status = results.get("overall_status", "UNKNOWN")
        
        if status == "HEALTHY":
            self.logger.info(f"✅ Conda health check: {status}")
            self.consecutive_failures = 0
            self.last_healthy_check = datetime.now()
        elif status == "DEGRADED":
            self.logger.warning(f"⚠️ Conda health check: {status}")
            self.consecutive_failures += 1
        elif status == "CRITICAL":
            self.logger.error(f"🚨 Conda health check: {status}")
            self.consecutive_failures += 1
        else:
            self.logger.error(f"❌ Conda health check failed: {status}")
            self.consecutive_failures += 1
        
        # Log detailed issues
        for check_name, check_result in results.items():
            if isinstance(check_result, dict) and 'status' in check_result and not check_result['status']:
                self.logger.warning(f"   - {check_name}: {check_result.get('message', 'Unknown issue')}")
        
        # Log fixes applied
        fixes = results.get("fixes_applied", [])
        if fixes:
            self.logger.info(f"🔧 Applied fixes: {', '.join(fixes)}")
    
    def should_alert(self) -> bool:
        """Determine if we should send an alert."""
        return self.consecutive_failures >= self.max_consecutive_failures
    
    def send_alert(self, results: Dict):
        """Send alert about critical conda issues."""
        self.logger.critical("🚨 CRITICAL ALERT: Conda system has persistent issues!")
        self.logger.critical(f"   Consecutive failures: {self.consecutive_failures}")
        self.logger.critical(f"   Last healthy check: {self.last_healthy_check}")
        
        # Save critical report
        critical_report = {
            "timestamp": datetime.now().isoformat(),
            "consecutive_failures": self.consecutive_failures,
            "last_healthy_check": self.last_healthy_check.isoformat() if self.last_healthy_check else None,
            "health_results": results
        }
        
        report_path = Path("scripts/maintenance") / f"critical_conda_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(report_path, 'w') as f:
                json.dump(critical_report, f, indent=2)
            self.logger.critical(f"   Critical report saved: {report_path}")
        except Exception as e:
            self.logger.error(f"   Failed to save critical report: {e}")
    
    def monitor_cycle(self):
        """Single monitoring cycle."""
        try:
            self.logger.debug("Starting conda health check cycle...")
            results = self.check_conda_health()
            self.log_health_status(results)
            
            if self.should_alert():
                self.send_alert(results)
            
            # Save periodic report
            if results.get("overall_status") != "HEALTHY":
                self.health_checker.save_health_report(results, f"conda_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
        except Exception as e:
            self.logger.error(f"Error in monitoring cycle: {e}")
            self.consecutive_failures += 1
    
    def run_daemon(self):
        """Run monitoring daemon."""
        self.logger.info(f"Starting conda monitor daemon (interval: {self.check_interval}s)")
        self.running = True
        
        # Schedule the monitoring task
        schedule.every(self.check_interval).seconds.do(self.monitor_cycle)
        
        # Run initial check
        self.monitor_cycle()
        
        # Main monitoring loop
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Received keyboard interrupt, shutting down...")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Wait before retrying
        
        self.logger.info("Conda monitor daemon stopped")
    
    def run_single_check(self):
        """Run a single health check."""
        self.logger.info("Running single conda health check...")
        results = self.check_conda_health()
        self.log_health_status(results)
        
        # Print summary
        print("\n" + "="*60)
        print("CONDA MONITORING RESULTS")
        print("="*60)
        print(f"Overall Status: {results.get('overall_status', 'UNKNOWN')}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if results.get("fixes_applied"):
            print(f"\n🔧 Fixes Applied:")
            for fix in results["fixes_applied"]:
                print(f"   - {fix}")
        
        return results

def create_startup_script():
    """Create a startup script for automatic monitoring."""
    startup_script = """@echo off
REM Conda Monitor Startup Script
REM This script starts the conda monitoring system automatically

cd /d "C:\\Users\\Admin\\PHASE0"
python scripts\\maintenance\\conda_monitor.py --daemon --interval 300 --log-file scripts\\maintenance\\conda_monitor.log

pause
"""
    
    script_path = Path("scripts/maintenance/start_conda_monitor.bat")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(startup_script)
    
    print(f"Startup script created: {script_path}")
    return script_path

def create_windows_task():
    """Create Windows Task Scheduler task for automatic monitoring."""
    task_xml = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Conda Health Monitor - Prevents conda issues automatically</Description>
    <Author>PHASE0 System</Author>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>PT2M</Delay>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions>
    <Exec>
      <Command>python</Command>
      <Arguments>scripts\\maintenance\\conda_monitor.py --daemon --interval 300</Arguments>
      <WorkingDirectory>C:\\Users\\Admin\\PHASE0</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""
    
    task_path = Path("scripts/maintenance/conda_monitor_task.xml")
    task_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(task_path, 'w') as f:
        f.write(task_xml)
    
    print(f"Windows Task XML created: {task_path}")
    print("To install the task, run as Administrator:")
    print(f"schtasks /create /xml \"{task_path.absolute()}\" /tn \"CondaHealthMonitor\"")
    
    return task_path

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Conda Automatic Monitoring System")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon (continuous monitoring)")
    parser.add_argument("--interval", type=int, default=300, help="Check interval in seconds (default: 300)")
    parser.add_argument("--log-file", default="conda_monitor.log", help="Log file path")
    parser.add_argument("--create-startup", action="store_true", help="Create startup script")
    parser.add_argument("--create-task", action="store_true", help="Create Windows Task Scheduler task")
    
    args = parser.parse_args()
    
    if args.create_startup:
        create_startup_script()
        return
    
    if args.create_task:
        create_windows_task()
        return
    
    monitor = CondaMonitor(log_file=args.log_file, check_interval=args.interval)
    
    if args.daemon:
        monitor.run_daemon()
    else:
        monitor.run_single_check()

if __name__ == "__main__":
    main()
