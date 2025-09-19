# Conda Error Prevention Guide

## 🚨 **CRITICAL: This Error Must Never Occur Again**

This guide provides comprehensive procedures to prevent the conda command recognition and pydantic-settings compatibility errors from ever happening again.

## 📋 **Error Summary**

### **Primary Error:**
```
conda : The term 'conda' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

### **Secondary Error:**
```
Error while loading conda entry point: anaconda-cloud-auth (cannot import name 'PyprojectTomlConfigSettingsSource' from 'pydantic_settings')
```

## 🛡️ **Prevention System Components**

### 1. **Automatic Health Monitoring**
- **Script**: `scripts/maintenance/conda_health_check.py`
- **Purpose**: Continuous monitoring and automatic fixing
- **Usage**: 
  ```bash
  python scripts/maintenance/conda_health_check.py --fix --verbose
  ```

### 2. **Real-time Monitoring Daemon**
- **Script**: `scripts/maintenance/conda_monitor.py`
- **Purpose**: Background monitoring with automatic fixes
- **Usage**:
  ```bash
  python scripts/maintenance/conda_monitor.py --daemon --interval 300
  ```

### 3. **Backup and Restore System**
- **Script**: `scripts/maintenance/conda_backup_restore.py`
- **Purpose**: Configuration backup and disaster recovery
- **Usage**:
  ```bash
  python scripts/maintenance/conda_backup_restore.py backup
  python scripts/maintenance/conda_backup_restore.py restore --backup-file backup_file.tar.gz
  ```

## 🔧 **Prevention Procedures**

### **Daily Prevention Checklist**

1. **Morning Health Check**
   ```bash
   python scripts/maintenance/conda_health_check.py --fix
   ```

2. **Verify Conda Status**
   ```bash
   conda --version
   conda info --envs
   ```

3. **Check for Warnings**
   - Run any conda command
   - Ensure no error messages appear
   - If warnings appear, run health check immediately

### **Weekly Prevention Tasks**

1. **Create Configuration Backup**
   ```bash
   python scripts/maintenance/conda_backup_restore.py backup
   ```

2. **Review Monitoring Logs**
   ```bash
   tail -n 50 scripts/maintenance/conda_monitor.log
   ```

3. **Clean Old Backups**
   ```bash
   python scripts/maintenance/conda_backup_restore.py cleanup --keep-count 5
   ```

### **Monthly Prevention Tasks**

1. **Full System Health Check**
   ```bash
   python scripts/maintenance/conda_health_check.py --fix --verbose --report
   ```

2. **Update Prevention Scripts**
   - Check for script updates
   - Test all prevention tools

3. **Review and Update Documentation**

## 🚀 **Automatic Startup Configuration**

### **Option 1: Windows Task Scheduler (Recommended)**

1. **Create Task XML**:
   ```bash
   python scripts/maintenance/conda_monitor.py --create-task
   ```

2. **Install Task** (Run as Administrator):
   ```cmd
   schtasks /create /xml "scripts\maintenance\conda_monitor_task.xml" /tn "CondaHealthMonitor"
   ```

### **Option 2: Startup Script**

1. **Create Startup Script**:
   ```bash
   python scripts/maintenance/conda_monitor.py --create-startup
   ```

2. **Add to Windows Startup**:
   - Copy `scripts/maintenance/start_conda_monitor.bat` to Startup folder
   - Or add to Windows Task Scheduler

## 🔍 **Early Warning Signs**

### **Watch for These Indicators:**

1. **PATH Issues**:
   - Conda commands work in Anaconda Prompt but not PowerShell
   - Need to use full path to conda executable

2. **Package Compatibility Issues**:
   - Any warnings about pydantic-settings
   - Import errors in conda-related packages
   - Version conflicts in package lists

3. **PowerShell Profile Issues**:
   - Conda not auto-activating in new PowerShell sessions
   - Profile file missing or corrupted

## 🚨 **Emergency Response Procedures**

### **If Conda Command Not Recognized:**

1. **Immediate Fix**:
   ```bash
   python scripts/maintenance/conda_health_check.py --fix
   ```

2. **Manual PATH Fix** (if automatic fails):
   ```powershell
   [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\Users\Admin\anaconda3;C:\Users\Admin\anaconda3\Scripts;C:\Users\Admin\anaconda3\Library\bin", [EnvironmentVariableTarget]::User)
   ```

3. **Manual PowerShell Profile Fix**:
   ```bash
   C:\Users\Admin\anaconda3\Scripts\conda.exe init powershell
   ```

### **If Pydantic-Settings Errors:**

1. **Immediate Fix**:
   ```bash
   pip install --upgrade pydantic-settings
   ```

2. **Verify Fix**:
   ```python
   python -c "import pydantic_settings; print('PyprojectTomlConfigSettingsSource' in dir(pydantic_settings))"
   ```

### **If Complete System Failure:**

1. **Restore from Backup**:
   ```bash
   python scripts/maintenance/conda_backup_restore.py list-backups
   python scripts/maintenance/conda_backup_restore.py restore --backup-file latest_backup.tar.gz
   ```

2. **Reinstall if Necessary**:
   - Download latest Anaconda installer
   - Install with "Add to PATH" option enabled
   - Run prevention scripts immediately after installation

## 📊 **Monitoring and Alerts**

### **Log File Locations**:
- **Health Check Reports**: `scripts/maintenance/conda_health_report_*.json`
- **Monitor Logs**: `scripts/maintenance/conda_monitor.log`
- **Critical Alerts**: `scripts/maintenance/critical_conda_alert_*.json`

### **Alert Conditions**:
- 3 consecutive health check failures
- Critical system status detected
- Backup restoration required

## 🔄 **Maintenance Schedule**

### **Daily** (Automated):
- Health monitoring every 5 minutes
- Automatic fixes applied
- Log file rotation

### **Weekly** (Manual):
- Review monitoring logs
- Create configuration backup
- Clean old backup files

### **Monthly** (Manual):
- Full system health assessment
- Update prevention scripts
- Review and update documentation

## 📞 **Support and Escalation**

### **Level 1 - Automated Fixes**:
- Health check script
- Monitor daemon
- Automatic package updates

### **Level 2 - Manual Intervention**:
- Manual PATH fixes
- PowerShell profile restoration
- Package compatibility resolution

### **Level 3 - System Recovery**:
- Backup restoration
- Complete system reinstall
- Expert consultation

## ✅ **Success Criteria**

### **System is Healthy When**:
- ✅ `conda --version` works without errors
- ✅ `conda activate fastsenv` works without warnings
- ✅ All conda commands run cleanly
- ✅ PowerShell profile loads conda automatically
- ✅ No pydantic-settings compatibility warnings
- ✅ Monitoring system reports "HEALTHY" status

### **Prevention is Working When**:
- ✅ Daily health checks pass
- ✅ Monitoring daemon runs continuously
- ✅ Backups are created regularly
- ✅ No manual intervention required
- ✅ System remains stable across reboots

## 🎯 **Key Success Metrics**

1. **Zero Manual Interventions**: System should self-heal
2. **100% Uptime**: Conda should always be available
3. **Clean Command Output**: No warnings or errors
4. **Automatic Recovery**: Issues resolved within 5 minutes
5. **Proactive Prevention**: Issues prevented before they occur

---

## 🚨 **REMEMBER: This Error Must Never Occur Again**

The prevention system is designed to ensure:
- **Proactive Monitoring**: Issues detected before they become problems
- **Automatic Fixes**: Problems resolved without manual intervention
- **Comprehensive Backup**: Quick recovery from any system state
- **Continuous Operation**: System remains healthy 24/7

**Follow this guide religiously to maintain a bulletproof conda environment.**
