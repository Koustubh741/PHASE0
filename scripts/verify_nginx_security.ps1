# PowerShell Script to verify Nginx and Alpine security versions
# This script should be run inside the nginx container or used to check Docker container

Write-Host "=== Nginx Security Verification ===" -ForegroundColor Green
Write-Host "Date: $(Get-Date)" -ForegroundColor Green
Write-Host ""

# Function to run commands in Docker container
function Invoke-DockerCommand {
    param(
        [string]$ContainerName,
        [string]$Command
    )
    
    try {
        $result = docker exec $ContainerName sh -c $Command 2>&1
        return $result
    }
    catch {
        Write-Host "Error running command in container: $_" -ForegroundColor Red
        return $null
    }
}

# Check if Docker is running
try {
    docker ps | Out-Null
    $dockerRunning = $true
}
catch {
    Write-Host "Docker is not running or not available" -ForegroundColor Red
    $dockerRunning = $false
}

if ($dockerRunning) {
    # Check if bfsi-nginx-proxy container is running
    $containerExists = docker ps --filter "name=bfsi-nginx-proxy" --format "{{.Names}}" | Select-String "bfsi-nginx-proxy"
    
    if ($containerExists) {
        Write-Host "1. Alpine Linux Version:" -ForegroundColor Yellow
        $alpineVersion = Invoke-DockerCommand -ContainerName "bfsi-nginx-proxy" -Command "cat /etc/alpine-release"
        if ($alpineVersion) {
            Write-Host "   Alpine Release: $alpineVersion"
        } else {
            Write-Host "   Alpine release file not found"
        }
        
        Write-Host ""
        Write-Host "2. Nginx Version Information:" -ForegroundColor Yellow
        $nginxVersion = Invoke-DockerCommand -ContainerName "bfsi-nginx-proxy" -Command "nginx -v"
        Write-Host "   $nginxVersion"
        
        Write-Host ""
        Write-Host "3. Nginx Package Information:" -ForegroundColor Yellow
        $nginxPackage = Invoke-DockerCommand -ContainerName "bfsi-nginx-proxy" -Command "apk info nginx"
        Write-Host "   $nginxPackage"
        
        Write-Host ""
        Write-Host "4. Checking for vulnerable modules:" -ForegroundColor Yellow
        $modules = Invoke-DockerCommand -ContainerName "bfsi-nginx-proxy" -Command "nginx -V 2>&1 | grep -E '(http_mp4_module|http_v3_module)'"
        if ($modules) {
            Write-Host "   WARNING: Potentially vulnerable modules detected!" -ForegroundColor Red
            Write-Host "   $modules"
        } else {
            Write-Host "   ✓ No vulnerable modules detected" -ForegroundColor Green
        }
        
        Write-Host ""
        Write-Host "5. SSL Configuration Check:" -ForegroundColor Yellow
        $sslCache = Invoke-DockerCommand -ContainerName "bfsi-nginx-proxy" -Command "grep -q 'ssl_session_cache off' /etc/nginx/conf.d/bfsi-api.conf && echo 'disabled' || echo 'enabled'"
        if ($sslCache -eq "disabled") {
            Write-Host "   ✓ ssl_session_cache is disabled" -ForegroundColor Green
        } else {
            Write-Host "   ✗ ssl_session_cache may not be properly disabled" -ForegroundColor Red
        }
        
        $sslTickets = Invoke-DockerCommand -ContainerName "bfsi-nginx-proxy" -Command "grep -q 'ssl_session_tickets off' /etc/nginx/conf.d/bfsi-api.conf && echo 'disabled' || echo 'enabled'"
        if ($sslTickets -eq "disabled") {
            Write-Host "   ✓ ssl_session_tickets is disabled" -ForegroundColor Green
        } else {
            Write-Host "   ✗ ssl_session_tickets may not be properly disabled" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host "6. HTTP/3/QUIC Configuration Check:" -ForegroundColor Yellow
        $http3 = Invoke-DockerCommand -ContainerName "bfsi-nginx-proxy" -Command "grep -q 'quic' /etc/nginx/conf.d/bfsi-api.conf && echo 'enabled' || echo 'disabled'"
        if ($http3 -eq "disabled") {
            Write-Host "   ✓ HTTP/3/QUIC is not enabled" -ForegroundColor Green
        } else {
            Write-Host "   ✗ HTTP/3/QUIC is enabled - this should be disabled for security" -ForegroundColor Red
        }
    } else {
        Write-Host "bfsi-nginx-proxy container is not running" -ForegroundColor Red
        Write-Host "Start the container first with: docker-compose -f config/docker/docker-compose.production.yml up -d" -ForegroundColor Yellow
    }
} else {
    Write-Host "Docker is not available. Please start Docker and try again." -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Security Verification Complete ===" -ForegroundColor Green
