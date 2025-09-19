# GRC Platform Complete API Test Suite
Write-Host "🧪 GRC Platform Complete API Test Suite" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

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
    Write-Host "   Available Endpoints:" -ForegroundColor Cyan
    foreach ($endpoint in $api.endpoints.PSObject.Properties) {
        Write-Host "     - $($endpoint.Name): $($endpoint.Value)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ API Info: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: User Login
Write-Host "`n3. Testing User Login..." -ForegroundColor Yellow
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
    $token = $null
}

if ($token) {
    $headers = @{
        "Authorization" = "Bearer $token"
    }

    # Test 4: Create Risk
    Write-Host "`n4. Testing Create Risk..." -ForegroundColor Yellow
    $riskData = @{
        title = "Test Security Risk"
        description = "This is a test security risk for demonstration"
        category = "Information Security"
        severity = "high"
        likelihood = "medium"
        impact = "critical"
        mitigation_plan = "Implement additional security controls"
    } | ConvertTo-Json

    try {
        $risk = Invoke-RestMethod -Uri "http://localhost:3001/api/risks" -Method POST -Body $riskData -ContentType "application/json" -Headers $headers
        Write-Host "✅ Create Risk: PASSED" -ForegroundColor Green
        Write-Host "   Risk ID: $($risk.data.id)" -ForegroundColor Cyan
        Write-Host "   Title: $($risk.data.title)" -ForegroundColor Cyan
        Write-Host "   Risk Score: $($risk.data.risk_score)" -ForegroundColor Cyan
        $riskId = $risk.data.id
    } catch {
        Write-Host "❌ Create Risk: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        $riskId = $null
    }

    # Test 5: Get All Risks
    Write-Host "`n5. Testing Get All Risks..." -ForegroundColor Yellow
    try {
        $risks = Invoke-RestMethod -Uri "http://localhost:3001/api/risks" -Method GET -Headers $headers
        Write-Host "✅ Get Risks: PASSED" -ForegroundColor Green
        Write-Host "   Count: $($risks.data.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Get Risks: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 6: Get Risk Statistics
    Write-Host "`n6. Testing Risk Statistics..." -ForegroundColor Yellow
    try {
        $riskStats = Invoke-RestMethod -Uri "http://localhost:3001/api/risks/stats" -Method GET -Headers $headers
        Write-Host "✅ Risk Stats: PASSED" -ForegroundColor Green
        Write-Host "   Total: $($riskStats.data.total)" -ForegroundColor Cyan
        Write-Host "   High Severity: $($riskStats.data.high_severity)" -ForegroundColor Cyan
        Write-Host "   Critical Severity: $($riskStats.data.critical_severity)" -ForegroundColor Cyan
        Write-Host "   Average Risk Score: $($riskStats.data.average_risk_score)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Risk Stats: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 7: Create Compliance Check
    Write-Host "`n7. Testing Create Compliance Check..." -ForegroundColor Yellow
    $complianceData = @{
        name = "Test GDPR Compliance Check"
        description = "Verify compliance with GDPR requirements"
        framework = "GDPR"
        requirement = "Data Protection Impact Assessment"
        due_date = (Get-Date).AddDays(30).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        evidence = "Documentation and audit reports"
    } | ConvertTo-Json

    try {
        $compliance = Invoke-RestMethod -Uri "http://localhost:3001/api/compliance" -Method POST -Body $complianceData -ContentType "application/json" -Headers $headers
        Write-Host "✅ Create Compliance Check: PASSED" -ForegroundColor Green
        Write-Host "   Compliance ID: $($compliance.data.id)" -ForegroundColor Cyan
        Write-Host "   Name: $($compliance.data.name)" -ForegroundColor Cyan
        Write-Host "   Framework: $($compliance.data.framework)" -ForegroundColor Cyan
        $complianceId = $compliance.data.id
    } catch {
        Write-Host "❌ Create Compliance Check: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        $complianceId = $null
    }

    # Test 8: Get All Compliance Checks
    Write-Host "`n8. Testing Get All Compliance Checks..." -ForegroundColor Yellow
    try {
        $complianceChecks = Invoke-RestMethod -Uri "http://localhost:3001/api/compliance" -Method GET -Headers $headers
        Write-Host "✅ Get Compliance Checks: PASSED" -ForegroundColor Green
        Write-Host "   Count: $($complianceChecks.data.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Get Compliance Checks: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 9: Get Compliance Statistics
    Write-Host "`n9. Testing Compliance Statistics..." -ForegroundColor Yellow
    try {
        $complianceStats = Invoke-RestMethod -Uri "http://localhost:3001/api/compliance/stats" -Method GET -Headers $headers
        Write-Host "✅ Compliance Stats: PASSED" -ForegroundColor Green
        Write-Host "   Total: $($complianceStats.data.total)" -ForegroundColor Cyan
        Write-Host "   Pending: $($complianceStats.data.pending)" -ForegroundColor Cyan
        Write-Host "   Completed: $($complianceStats.data.completed)" -ForegroundColor Cyan
        Write-Host "   Overdue: $($complianceStats.data.overdue)" -ForegroundColor Cyan
        Write-Host "   Average Score: $($complianceStats.data.average_compliance_score)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Compliance Stats: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 10: Get High Risks
    Write-Host "`n10. Testing Get High Risks..." -ForegroundColor Yellow
    try {
        $highRisks = Invoke-RestMethod -Uri "http://localhost:3001/api/risks/high-risk" -Method GET -Headers $headers
        Write-Host "✅ Get High Risks: PASSED" -ForegroundColor Green
        Write-Host "   High Risk Count: $($highRisks.data.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Get High Risks: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 11: Get Overdue Compliance Checks
    Write-Host "`n11. Testing Get Overdue Compliance Checks..." -ForegroundColor Yellow
    try {
        $overdueChecks = Invoke-RestMethod -Uri "http://localhost:3001/api/compliance/overdue" -Method GET -Headers $headers
        Write-Host "✅ Get Overdue Checks: PASSED" -ForegroundColor Green
        Write-Host "   Overdue Count: $($overdueChecks.data.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Get Overdue Checks: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

    # Test 12: Search Risks
    Write-Host "`n12. Testing Search Risks..." -ForegroundColor Yellow
    try {
        $searchResults = Invoke-RestMethod -Uri "http://localhost:3001/api/risks/search?q=security" -Method GET -Headers $headers
        Write-Host "✅ Search Risks: PASSED" -ForegroundColor Green
        Write-Host "   Search Results: $($searchResults.data.Count)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Search Risks: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }

} else {
    Write-Host "`n⚠️ Skipping authenticated tests (no token available)" -ForegroundColor Yellow
}

Write-Host "`n🎉 Complete API Test Suite Finished!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
