@echo off
REM GRC Platform Service Startup Script (Batch)
REM Structured startup script following industry standards

setlocal enabledelayedexpansion

REM Check if PowerShell is available
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PowerShell is required but not available
    exit /b 1
)

REM Default action
set ACTION=start
set SERVICE=
set PROJECT_ROOT=%CD%

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :execute
if "%~1"=="start" set ACTION=start
if "%~1"=="stop" set ACTION=stop
if "%~1"=="status" set ACTION=status
if "%~1"=="restart" set ACTION=restart
if "%~1"=="--service" (
    shift
    set SERVICE=%~1
)
if "%~1"=="--project-root" (
    shift
    set PROJECT_ROOT=%~1
)
shift
goto :parse_args

:execute
echo.
echo ============================================================
echo 🚀 GRC PLATFORM SERVICE MANAGER
echo ============================================================
echo Action: %ACTION%
if not "%SERVICE%"=="" echo Service: %SERVICE%
echo Project Root: %PROJECT_ROOT%
echo ============================================================
echo.

REM Execute PowerShell script
powershell -ExecutionPolicy Bypass -File "%~dp0start_services_structured.ps1" -Action %ACTION% -ProjectRoot "%PROJECT_ROOT%" %SERVICE_ARG%

if %errorlevel% neq 0 (
    echo.
    echo ❌ Service operation failed
    exit /b %errorlevel%
) else (
    echo.
    echo ✅ Service operation completed successfully
)

endlocal
