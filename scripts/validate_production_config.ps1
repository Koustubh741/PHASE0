# PowerShell script for production configuration validation
# Validates environment configuration files for placeholder values

param(
    [string]$ConfigFile = "config/environment/production.env",
    [switch]$NoFail,
    [switch]$Verbose
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Placeholder patterns that should not be in production
$PlaceholderPatterns = @(
    "change_me",
    "yourdomain",
    "your_domain",
    "yourdomain\.com",
    "your-domain\.com",
    "your_backup_bucket",
    "your-backup-bucket",
    "your_super_secret_key",
    "your_jwt_secret_key",
    "your_32_byte_encryption_key",
    "your_master_api_key",
    "your_smtp_password",
    "placeholder",
    "example",
    "test_",
    "demo_",
    "sample_",
    "default_",
    "localhost.*production",
    "127\.0\.0\.1.*production",
    "admin.*password",
    "root.*password",
    "password123",
    "123456",
    "abcdef",
    "secret123",
    "changeme",
    "password",
    "secret",
    "temp",
    "temporary"
)

# Critical environment variables that must be set with non-placeholder values
$CriticalVariables = @(
    "SECRET_KEY",
    "JWT_SECRET_KEY",
    "ENCRYPTION_KEY",
    "API_KEY_MASTER",
    "DB_PASSWORD",
    "REDIS_PASSWORD",
    "SMTP_PASSWORD"
)

# Variables that should not contain placeholder domains
$DomainVariables = @(
    "CORS_ORIGINS",
    "SMTP_HOST",
    "SMTP_USER"
)

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp - $Level - $Message"
    
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARNING" { Write-Host $logMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage -ForegroundColor White }
    }
}

function Test-PlaceholderValue {
    param(
        [string]$Value,
        [string]$Pattern
    )
    
    return $Value -match $Pattern
}

function Test-CriticalVariable {
    param(
        [string]$Key,
        [string]$Value
    )
    
    $isValid = $true
    $errors = @()
    
    # Check for placeholder patterns
    foreach ($pattern in $PlaceholderPatterns) {
        if (Test-PlaceholderValue -Value $Value -Pattern $pattern) {
            $errors += "Placeholder value detected: $Key=$Value (matches pattern: $pattern)"
            $isValid = $false
        }
    }
    
    # Additional validation for specific variables
    switch ($Key) {
        "SECRET_KEY" {
            if ($Value.Length -lt 32) {
                $errors += "SECRET_KEY should be at least 32 characters long"
                $isValid = $false
            }
        }
        "ENCRYPTION_KEY" {
            if ($Value.Length -ne 32) {
                $errors += "ENCRYPTION_KEY should be exactly 32 characters long"
                $isValid = $false
            }
        }
        "DB_PASSWORD" {
            if ($Value.Length -lt 12) {
                $errors += "Database password should be at least 12 characters long"
                $isValid = $false
            }
        }
        "CORS_ORIGINS" {
            if ($Value -match "yourdomain\.com|your-domain\.com") {
                $errors += "CORS_ORIGINS contains placeholder domain"
                $isValid = $false
            }
        }
    }
    
    return @{
        IsValid = $isValid
        Errors = $errors
    }
}

function Test-ConfigurationFile {
    param(
        [string]$FilePath
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Log "Configuration file not found: $FilePath" -Level "ERROR"
        return $false
    }
    
    Write-Log "Validating configuration file: $FilePath"
    
    $errors = @()
    $warnings = @()
    $lineNumber = 0
    
    try {
        $content = Get-Content $FilePath -ErrorAction Stop
        
        foreach ($line in $content) {
            $lineNumber++
            $line = $line.Trim()
            
            # Skip comments and empty lines
            if (-not $line -or $line.StartsWith("#")) {
                continue
            }
            
            # Check for environment variable assignments
            if ($line -match "^([^=]+)=(.*)$") {
                $key = $Matches[1].Trim()
                $value = $Matches[2].Trim().Trim('"').Trim("'")
                
                # Check if this is a critical variable
                if ($CriticalVariables -contains $key) {
                    $validation = Test-CriticalVariable -Key $key -Value $value
                    if (-not $validation.IsValid) {
                        $errors += "Line $lineNumber`: $($validation.Errors -join ', ')"
                    }
                }
                
                # Check for placeholder patterns in any variable
                foreach ($pattern in $PlaceholderPatterns) {
                    if (Test-PlaceholderValue -Value $value -Pattern $pattern) {
                        $errors += "Line $lineNumber`: Placeholder value detected: $key=$value (matches pattern: $pattern)"
                        break
                    }
                }
                
                # Check domain variables
                if ($DomainVariables -contains $key) {
                    if ($value -match "yourdomain|your-domain|example\.com|localhost|127\.0\.0\.1|test\.com|demo\.com") {
                        $errors += "Line $lineNumber`: Domain variable contains placeholder: $key=$value"
                    }
                }
            }
        }
        
        # Report results
        if ($errors.Count -eq 0) {
            Write-Log "Configuration validation passed!" -Level "SUCCESS"
            return $true
        } else {
            Write-Log "Found $($errors.Count) validation errors:" -Level "ERROR"
            foreach ($error in $errors) {
                Write-Log "  $error" -Level "ERROR"
            }
            return $false
        }
        
    } catch {
        Write-Log "Error reading configuration file: $($_.Exception.Message)" -Level "ERROR"
        return $false
    }
}

function Show-Usage {
    Write-Host @"
Production Configuration Validation Script

Usage: .\validate_production_config.ps1 [options]

Options:
  -ConfigFile <path>    Path to the configuration file to validate (default: config/environment/production.env)
  -NoFail              Do not exit with error code on validation failures
  -Verbose             Enable verbose output

Examples:
  .\validate_production_config.ps1
  .\validate_production_config.ps1 -ConfigFile "config/prod.env"
  .\validate_production_config.ps1 -NoFail -Verbose

"@
}

# Main execution
try {
    if ($Verbose) {
        Write-Log "Starting production configuration validation..."
        Write-Log "Config file: $ConfigFile"
        Write-Log "NoFail mode: $NoFail"
    }
    
    # Validate the configuration file
    $validationPassed = Test-ConfigurationFile -FilePath $ConfigFile
    
    if (-not $validationPassed) {
        Write-Log "Configuration validation failed. Deployment aborted." -Level "ERROR"
        if (-not $NoFail) {
            exit 1
        }
    } else {
        Write-Log "Configuration validation successful!" -Level "SUCCESS"
        exit 0
    }
    
} catch {
    Write-Log "Unexpected error: $($_.Exception.Message)" -Level "ERROR"
    if (-not $NoFail) {
        exit 1
    }
}
