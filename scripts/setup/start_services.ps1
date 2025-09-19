# GRC Platform Service Startup Script (PowerShell)
# Structured startup script following industry standards

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "status", "restart")]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("postgres", "redis", "api-gateway", "ai-agents", "frontend")]
    [string]$Service,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectRoot = (Get-Location).Path
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Service configurations
$ServiceConfigs = @{
    "postgres" = @{
        Command = @("docker", "run", "-d", "--name", "grc-postgres", "-p", "5432:5432", "-e", "POSTGRES_PASSWORD=password", "postgres:15-alpine")
        HealthCheck = "docker ps --filter name=grc-postgres --filter status=running"
        Port = 5432
        WorkingDir = $null
    }
    "redis" = @{
        Command = @("docker", "run", "-d", "--name", "grc-redis", "-p", "6379:6379", "redis:7-alpine")
        HealthCheck = "docker ps --filter name=grc-redis --filter status=running"
        Port = 6379
        WorkingDir = $null
    }
    "api-gateway" = @{
        Command = @("python", "main.py")
        HealthCheck = "curl -f http://localhost:8000/health"
        Port = 8000
        WorkingDir = Join-Path $ProjectRoot "src\backend\api-gateway"
    }
    "ai-agents" = @{
        Command = @("python", "ai_agents_service.py")
        HealthCheck = "curl -f http://localhost:8005/health"
        Port = 8005
        WorkingDir = Join-Path $ProjectRoot "src\backend\services"
    }
    "frontend" = @{
        Command = @("npm", "start")
        HealthCheck = "curl -f http://localhost:3000"
        Port = 3000
        WorkingDir = Join-Path $ProjectRoot "src\frontend"
    }
}

# Global variables for tracking processes
$Global:ServiceProcesses = @{}

function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "WARN", "ERROR", "SUCCESS")]
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "White" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
    }
    
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

function Start-Service {
    param([string]$ServiceName)
    
    if (-not $ServiceConfigs.ContainsKey($ServiceName)) {
        Write-Log "Unknown service: $ServiceName" "ERROR"
        return $false
    }
    
    $config = $ServiceConfigs[$ServiceName]
    Write-Log "Starting $ServiceName..." "INFO"
    
    try {
        # Check if working directory exists
        if ($config.WorkingDir -and -not (Test-Path $config.WorkingDir)) {
            Write-Log "Working directory does not exist: $($config.WorkingDir)" "ERROR"
            return $false
        }
        
        # Start the service
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = $config.Command[0]
        $processInfo.Arguments = $config.Command[1..($config.Command.Length-1)] -join " "
        
        if ($config.WorkingDir) {
            $processInfo.WorkingDirectory = $config.WorkingDir
        }
        
        $processInfo.UseShellExecute = $false
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.CreateNoWindow = $true
        
        $process = [System.Diagnostics.Process]::Start($processInfo)
        $Global:ServiceProcesses[$ServiceName] = $process
        
        Write-Log "✅ $ServiceName started with PID $($process.Id)" "SUCCESS"
        
        # Wait for service to initialize
        Start-Sleep -Seconds 2
        
        # Check service health
        if (Test-ServiceHealth -ServiceName $ServiceName) {
            Write-Log "✅ $ServiceName is healthy" "SUCCESS"
            return $true
        } else {
            Write-Log "⚠️ $ServiceName started but health check failed" "WARN"
            return $true  # Still consider it started
        }
        
    } catch {
        Write-Log "Failed to start $ServiceName`: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-ServiceHealth {
    param([string]$ServiceName)
    
    $config = $ServiceConfigs[$ServiceName]
    $healthCheck = $config.HealthCheck
    
    if (-not $healthCheck) {
        return $true  # No health check defined
    }
    
    try {
        $result = Invoke-Expression $healthCheck 2>$null
        return $LASTEXITCODE -eq 0
    } catch {
        Write-Log "Health check failed for $ServiceName`: $($_.Exception.Message)" "WARN"
        return $false
    }
}

function Stop-Service {
    param([string]$ServiceName)
    
    if (-not $Global:ServiceProcesses.ContainsKey($ServiceName)) {
        Write-Log "Service $ServiceName is not running" "WARN"
        return
    }
    
    try {
        Write-Log "Stopping $ServiceName..." "INFO"
        $process = $Global:ServiceProcesses[$ServiceName]
        
        if (-not $process.HasExited) {
            $process.Kill()
            $process.WaitForExit(10000)  # Wait up to 10 seconds
            Write-Log "✅ $ServiceName stopped" "SUCCESS"
        }
        
        $Global:ServiceProcesses.Remove($ServiceName)
    } catch {
        Write-Log "Error stopping $ServiceName`: $($_.Exception.Message)" "ERROR"
    }
}

function Start-AllServices {
    Write-Log "🚀 Starting GRC Platform Services..." "INFO"
    
    $startupOrder = @("postgres", "redis", "api-gateway", "ai-agents", "frontend")
    $results = @{}
    
    foreach ($service in $startupOrder) {
        $results[$service] = Start-Service -ServiceName $service
        if (-not $results[$service]) {
            Write-Log "Failed to start $service, stopping startup process" "ERROR"
            break
        }
        Start-Sleep -Seconds 3  # Wait between services
    }
    
    return $results
}

function Stop-AllServices {
    Write-Log "🛑 Stopping all services..." "INFO"
    
    foreach ($serviceName in $Global:ServiceProcesses.Keys) {
        Stop-Service -ServiceName $serviceName
    }
}

function Get-ServiceStatus {
    $status = @{}
    
    foreach ($serviceName in $ServiceConfigs.Keys) {
        $isRunning = $Global:ServiceProcesses.ContainsKey($ServiceName)
        $isHealthy = if ($isRunning) { Test-ServiceHealth -ServiceName $ServiceName } else { $false }
        
        $status[$serviceName] = @{
            Running = $isRunning
            Healthy = $isHealthy
            Port = $ServiceConfigs[$serviceName].Port
            PID = if ($isRunning) { $Global:ServiceProcesses[$serviceName].Id } else { $null }
        }
    }
    
    return $status
}

function Show-ServiceStatus {
    $status = Get-ServiceStatus
    
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "📊 GRC PLATFORM SERVICE STATUS" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    
    foreach ($serviceName in $status.Keys) {
        $info = $status[$serviceName]
        $statusIcon = if ($info.Healthy) { "✅" } elseif ($info.Running) { "🟡" } else { "❌" }
        $healthText = if ($info.Healthy) { "Healthy" } elseif ($info.Running) { "Running" } else { "Stopped" }
        $portText = if ($info.Port) { " (Port $($info.Port))" } else { "" }
        $pidText = if ($info.PID) { " [PID: $($info.PID)]" } else { "" }
        
        Write-Host "$statusIcon $($serviceName.ToUpper()): $healthText$portText$pidText" -ForegroundColor White
    }
    
    Write-Host "=" * 60 -ForegroundColor Cyan
}

# Main execution
try {
    switch ($Action) {
        "start" {
            if ($Service) {
                $success = Start-Service -ServiceName $Service
                exit $(if ($success) { 0 } else { 1 })
            } else {
                $results = Start-AllServices
                Show-ServiceStatus
                exit $(if ($results.Values -contains $false) { 1 } else { 0 })
            }
        }
        "stop" {
            Stop-AllServices
            Write-Log "✅ All services stopped" "SUCCESS"
        }
        "status" {
            Show-ServiceStatus
        }
        "restart" {
            Stop-AllServices
            Start-Sleep -Seconds 2
            $results = Start-AllServices
            Show-ServiceStatus
            exit $(if ($results.Values -contains $false) { 1 } else { 0 })
        }
    }
} catch {
    Write-Log "Unexpected error: $($_.Exception.Message)" "ERROR"
    exit 1
}
