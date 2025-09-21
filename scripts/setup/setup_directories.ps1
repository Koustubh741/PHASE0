# PowerShell script to create directory structure
$directories = @(
    "backend\src\core\application\use_cases",
    "backend\src\core\application\services", 
    "backend\src\core\application\dto",
    "backend\src\core\infrastructure\database",
    "backend\src\core\infrastructure\persistence",
    "backend\src\api\v1\endpoints",
    "backend\src\api\v1\schemas",
    "backend\src\api\v1\dependencies",
    "backend\src\api\middleware",
    "backend\src\tests\unit",
    "backend\src\tests\integration",
    "backend\src\tests\e2e",
    "backend\ai-agents\src\core",
    "backend\ai-agents\src\agents",
    "backend\ai-agents\src\orchestration",
    "backend\ai-agents\src\shared",
    "backend\ai-agents\tests",
    "backend\deployment\docker",
    "backend\deployment\kubernetes",
    "backend\deployment\scripts",
    "backend\docs",
    "shared\types",
    "shared\constants",
    "shared\utils",
    "infrastructure\database",
    "infrastructure\monitoring",
    "infrastructure\security",
    "scripts",
    "docs"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "Created directory: $dir"
    } else {
        Write-Host "Directory already exists: $dir"
    }
}

Write-Host "Directory structure setup complete!"

