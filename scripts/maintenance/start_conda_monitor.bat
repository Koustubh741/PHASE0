@echo off
REM Conda Monitor Startup Script
REM This script starts the conda monitoring system automatically

cd /d "C:\Users\Admin\PHASE0"
python scripts\maintenance\conda_monitor.py --daemon --interval 300 --log-file scripts\maintenance\conda_monitor.log

pause
