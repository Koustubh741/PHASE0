# CORS Security Implementation Guide

## Overview

The CORS (Cross-Origin Resource Sharing) configuration has been refactored to use environment variables for enhanced security. This implementation ensures that production environments never expose localhost URLs and follows security best practices.

## Environment-Specific Configuration

### Development Environment
- **Default**: Allows localhost and development URLs
- **Environment Variable**: `BFSI_SECURITY_ENVIRONMENT=development`
- **CORS Origins**: Automatically includes localhost URLs for development
- **Security**: Relaxed for development convenience

### Staging Environment
- **Environment Variable**: `BFSI_SECURITY_ENVIRONMENT=staging`
- **CORS Origins**: Combines configured domains with limited localhost for testing
- **Security**: Moderate security with testing capabilities

### Production Environment
- **Environment Variable**: `BFSI_SECURITY_ENVIRONMENT=production`
- **CORS Origins**: Only explicitly configured domains allowed
- **Security**: Strict security - no localhost URLs allowed

## Configuration Examples

### Development Setup
```bash
# .env file for development
BFSI_SECURITY_ENVIRONMENT=development
# Optional: Add custom development origins
BFSI_SECURITY_CORS_ORIGINS=https://localhost:3000,https://localhost:8080
```

### Staging Setup
```bash
# .env file for staging
BFSI_SECURITY_ENVIRONMENT=staging
BFSI_SECURITY_CORS_ORIGINS=https://staging.your-bfsi-domain.com,https://dashboard-staging.your-bfsi-domain.com
```

### Production Setup
```bash
# .env file for production
BFSI_SECURITY_ENVIRONMENT=production
BFSI_SECURITY_CORS_ORIGINS=https://your-bfsi-domain.com,https://dashboard.your-bfsi-domain.com,https://api.your-bfsi-domain.com
```

## Security Features

### Production Validation
The system automatically validates CORS origins in production:

1. **HTTPS Required**: All production origins must use HTTPS
2. **No Localhost**: Localhost and local IP addresses are forbidden
3. **Domain Validation**: Must be valid domain format
4. **Private IP Blocking**: Blocks private IP ranges (192.168.x.x, 10.x.x.x, 172.16-31.x.x)

### Forbidden Patterns in Production
- `localhost`
- `127.0.0.1`
- `0.0.0.0`
- `::1`
- Private IP ranges (192.168.x.x, 10.x.x.x, 172.16-31.x.x)

## Implementation Details

### Dynamic CORS Loading
```python
# The system automatically loads CORS origins based on environment
cors_origins = SecurityConfig._get_cors_origins()
```

### Environment Detection
```python
# Environment is detected from BFSI_SECURITY_ENVIRONMENT variable
env = os.getenv("BFSI_SECURITY_ENVIRONMENT", "development").lower()
```

### Production Validation
```python
# Each origin is validated for production security
if SecurityConfig._validate_production_origin(origin):
    validated_origins.append(origin)
```

## Migration Guide

### From Hardcoded to Environment Variables

**Before (Insecure):**
```python
cors_origins: list = [
    "https://localhost:3000", 
    "https://localhost:8080",
    "https://127.0.0.1:3000",
    "https://127.0.0.1:8080",
    # Production domains mixed with localhost
]
```

**After (Secure):**
```python
# Environment-specific configuration
cors_origins: list = Field(default_factory=lambda: SecurityConfig._get_cors_origins())
```

### Deployment Checklist

1. **Set Environment Variable**: `BFSI_SECURITY_ENVIRONMENT=production`
2. **Configure CORS Origins**: Set `BFSI_SECURITY_CORS_ORIGINS` with your production domains
3. **Validate Configuration**: Ensure all origins use HTTPS and valid domains
4. **Test CORS**: Verify that only configured origins can access the API

## Security Benefits

1. **Environment Isolation**: Development and production configurations are completely separate
2. **No Localhost in Production**: Eliminates security risk of localhost URLs in production
3. **HTTPS Enforcement**: Production requires HTTPS for all CORS origins
4. **Domain Validation**: Prevents invalid or malicious origin configurations
5. **Private IP Protection**: Blocks private IP ranges in production

## Troubleshooting

### Common Issues

1. **CORS Errors in Production**
   - Ensure `BFSI_SECURITY_CORS_ORIGINS` is set with valid HTTPS domains
   - Verify domains are not localhost or private IPs

2. **Development CORS Issues**
   - Check that `BFSI_SECURITY_ENVIRONMENT=development`
   - Ensure localhost URLs are properly formatted

3. **Staging CORS Issues**
   - Verify staging domains are configured in `BFSI_SECURITY_CORS_ORIGINS`
   - Check that environment is set to `staging`

### Validation Commands

```bash
# Check current environment
echo $BFSI_SECURITY_ENVIRONMENT

# Check CORS origins
echo $BFSI_SECURITY_CORS_ORIGINS

# Test CORS configuration
python -c "from security_config import security_config; print(security_config.cors_origins)"
```

## Best Practices

1. **Never hardcode localhost in production**
2. **Always use HTTPS in production**
3. **Validate all CORS origins before deployment**
4. **Use environment-specific configuration files**
5. **Regularly audit CORS origins for security**

## Security Audit

The implementation includes comprehensive security validation:

- ✅ Environment-based configuration
- ✅ Production localhost blocking
- ✅ HTTPS enforcement
- ✅ Domain validation
- ✅ Private IP protection
- ✅ Dynamic loading from environment variables
- ✅ No hardcoded production URLs
