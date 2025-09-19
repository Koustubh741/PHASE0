# GRC Platform API Test Script
Write-Host "🧪 GRC Platform API Test Suite" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Test 1: Health Check
Write-Host "`n1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3001/health" -Method GET
    Write-Host "✅ Health Check: PASSED" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor Cyan
    Write-Host "   Uptime: $($health.uptime)s" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Health Check: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: API Info
Write-Host "`n2. Testing API Info..." -ForegroundColor Yellow
try {
    $api = Invoke-RestMethod -Uri "http://localhost:3001/api" -Method GET
    Write-Host "✅ API Info: PASSED" -ForegroundColor Green
    Write-Host "   Message: $($api.message)" -ForegroundColor Cyan
    Write-Host "   Version: $($api.version)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ API Info: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: User Registration
Write-Host "`n3. Testing User Registration..." -ForegroundColor Yellow
$testUser = @{
    email = "test@example.com"
    password = "password123"
    firstName = "Test"
    lastName = "User"
    role = "admin"
} | ConvertTo-Json

try {
    $register = Invoke-RestMethod -Uri "http://localhost:3001/api/auth/register" -Method POST -Body $testUser -ContentType "application/json"
    Write-Host "✅ User Registration: PASSED" -ForegroundColor Green
    Write-Host "   User ID: $($register.data.user.id)" -ForegroundColor Cyan
    Write-Host "   Email: $($register.data.user.email)" -ForegroundColor Cyan
    $token = $register.data.token
    Write-Host "   Token received: ✅" -ForegroundColor Cyan
} catch {
    Write-Host "❌ User Registration: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    $token = $null
}

# Test 4: User Login
Write-Host "`n4. Testing User Login..." -ForegroundColor Yellow
$loginData = @{
    email = "test@example.com"
    password = "password123"
} | ConvertTo-Json

try {
    $login = Invoke-RestMethod -Uri "http://localhost:3001/api/auth/login" -Method POST -Body $loginData -ContentType "application/json"
    Write-Host "✅ User Login: PASSED" -ForegroundColor Green
    Write-Host "   User: $($login.data.user.firstName) $($login.data.user.lastName)" -ForegroundColor Cyan
    $token = $login.data.token
    Write-Host "   Token received: ✅" -ForegroundColor Cyan
} catch {
    Write-Host "❌ User Login: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Get User Profile (if token available)
if ($token) {
    Write-Host "`n5. Testing Get User Profile..." -ForegroundColor Yellow
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    try {
        $profile = Invoke-RestMethod -Uri "http://localhost:3001/api/auth/profile" -Method GET -Headers $headers
        Write-Host "✅ Get Profile: PASSED" -ForegroundColor Green
        Write-Host "   Name: $($profile.data.firstName) $($profile.data.lastName)" -ForegroundColor Cyan
        Write-Host "   Role: $($profile.data.role)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Get Profile: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 6: Create Policy (if token available)
    Write-Host "`n6. Testing Create Policy..." -ForegroundColor Yellow
    $policyData = @{
        title = "Test Policy"
        content = "This is a test policy content"
        version = "1.0"
        status = "draft"
    } | ConvertTo-Json

    try {
        $policy = Invoke-RestMethod -Uri "http://localhost:3001/api/policies" -Method POST -Body $policyData -ContentType "application/json" -Headers $headers
        Write-Host "✅ Create Policy: PASSED" -ForegroundColor Green
        Write-Host "   Policy ID: $($policy.data.id)" -ForegroundColor Cyan
        Write-Host "   Title: $($policy.data.title)" -ForegroundColor Cyan
        $policyId = $policy.data.id
    } catch {
        Write-Host "❌ Create Policy: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        $policyId = $null
    }

    # Test 7: Get All Policies
    Write-Host "`n7. Testing Get All Policies..." -ForegroundColor Yellow
    try {
        $policies = Invoke-RestMethod -Uri "http://localhost:3001/api/policies" -Method GET -Headers $headers
        Write-Host "✅ Get Policies: PASSED" -ForegroundColor Green
        Write-Host "   Count: $($policies.data.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Get Policies: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 8: Get Policy Statistics
    Write-Host "`n8. Testing Policy Statistics..." -ForegroundColor Yellow
    try {
        $stats = Invoke-RestMethod -Uri "http://localhost:3001/api/policies/stats" -Method GET -Headers $headers
        Write-Host "✅ Policy Stats: PASSED" -ForegroundColor Green
        Write-Host "   Total: $($stats.data.total)" -ForegroundColor Cyan
        Write-Host "   Draft: $($stats.data.draft)" -ForegroundColor Cyan
        Write-Host "   Approved: $($stats.data.approved)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Policy Stats: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "`n⚠️ Skipping authenticated tests (no token available)" -ForegroundColor Yellow
}

Write-Host "`n🎉 API Test Suite Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
