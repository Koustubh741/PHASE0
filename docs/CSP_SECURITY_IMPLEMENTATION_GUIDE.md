# Content Security Policy (CSP) Security Implementation Guide

## Overview

This guide documents the implementation of secure Content Security Policy (CSP) for the BFSI GRC Platform, removing `'unsafe-inline'` directives and implementing proper security controls.

## Security Improvements Made

### 1. Removed Unsafe Inline Directives

**Before:**
```env
CONTENT_SECURITY_POLICY="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
```

**After:**
```env
CONTENT_SECURITY_POLICY="default-src 'self'; script-src 'self' 'nonce-{NONCE}'; style-src 'self' 'nonce-{NONCE}'; img-src 'self' data:; font-src 'self'; connect-src 'self' ws: wss:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
```

### 2. Externalized Inline Content

#### CSS Files Created:
- `static/css/archer-dashboard.css` - Styles for Archer dashboard
- `static/css/functional-dashboard.css` - Styles for functional dashboard

#### JavaScript Files Created:
- `static/js/archer-dashboard.js` - Scripts for Archer dashboard  
- `static/js/functional-dashboard.js` - Scripts for functional dashboard

#### HTML Files Updated:
- `bfsi-archer-dashboard.html` - Now uses external CSS/JS
- `bfsi-functional-dashboard.html` - Now uses external CSS/JS

### 3. CSP Middleware Implementation

Created `security_csp_middleware.py` with two approaches:

#### Nonce-Based CSP (Recommended)
```python
from security_csp_middleware import CSPNonceMiddleware

# Generate unique nonces for each request
app.add_middleware(CSPNonceMiddleware)
```

#### Hash-Based CSP (Alternative)
```python
from security_csp_middleware import CSPHashMiddleware

# Use SHA256 hashes of allowed inline content
allowed_hashes = {
    'script': ['sha256-hash1', 'sha256-hash2'],
    'style': ['sha256-hash3', 'sha256-hash4']
}
app.add_middleware(CSPHashMiddleware, allowed_hashes=allowed_hashes)
```

## Implementation Options

### Option 1: API-Only Endpoints (Strictest)

For pure API services, use the strictest CSP:

```python
def create_api_only_csp() -> str:
    return (
        "default-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'none'; "
        "form-action 'none'"
    )
```

### Option 2: Mixed Application (Current Setup)

For applications serving both APIs and HTML dashboards:

```python
def create_mixed_csp() -> str:
    return (
        "default-src 'self'; "
        "script-src 'self' 'nonce-{NONCE}'; "
        "style-src 'self' 'nonce-{NONCE}'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
```

## Security Benefits

### 1. XSS Protection
- **Before**: `'unsafe-inline'` allowed any inline script/style
- **After**: Only explicitly allowed scripts/styles with valid nonces

### 2. Content Injection Prevention
- **Before**: Attackers could inject malicious inline content
- **After**: All inline content must have valid nonces

### 3. Resource Control
- **Before**: Limited control over resource loading
- **After**: Granular control over all resource types

## Deployment Instructions

### 1. Update Production Environment

```bash
# Update production.env
CONTENT_SECURITY_POLICY="default-src 'self'; script-src 'self' 'nonce-{NONCE}'; style-src 'self' 'nonce-{NONCE}'; img-src 'self' data:; font-src 'self'; connect-src 'self' ws: wss:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
```

### 2. Deploy Static Assets

```bash
# Ensure static files are served correctly
mkdir -p static/css static/js
# Files are already created in the project
```

### 3. Update Application Code

```python
# Add CSP middleware to your FastAPI app
from security_csp_middleware import create_csp_middleware

app.add_middleware(create_csp_middleware, mode="nonce")
```

### 4. Test Implementation

```bash
# Test CSP headers
curl -I https://your-domain.com/api/health
# Should see Content-Security-Policy header with nonce

# Test HTML dashboards
curl -I https://your-domain.com/dashboard
# Should see CSP header and nonce in HTML
```

## Monitoring and Maintenance

### 1. CSP Violation Reporting

Add violation reporting to monitor CSP effectiveness:

```python
# Add to CSP policy
"report-uri /api/csp-violations; report-to csp-endpoint"
```

### 2. Regular Security Audits

- Review CSP violations in logs
- Update nonces regularly
- Monitor for new security threats
- Test CSP effectiveness with security tools

### 3. Performance Considerations

- Nonces are generated per request (minimal overhead)
- External CSS/JS files are cached by browsers
- Consider CDN for static assets

## Troubleshooting

### Common Issues

1. **Scripts not loading**: Check nonce generation and injection
2. **Styles not applying**: Verify CSS file paths and CSP policy
3. **CSP violations**: Check browser console for violation reports

### Debug Mode

```python
# Enable CSP reporting for debugging
CSP_REPORT_ONLY = True  # Set to False for enforcement
```

## Security Best Practices

1. **Never use `'unsafe-inline'`** in production
2. **Use nonces** for dynamic inline content
3. **Use hashes** for static inline content
4. **Regularly rotate** nonces and secrets
5. **Monitor violations** and adjust policies
6. **Test thoroughly** before deployment

## Compliance Benefits

- **PCI DSS**: Enhanced XSS protection
- **SOX**: Improved data integrity controls  
- **GDPR**: Better data protection mechanisms
- **Basel III**: Strengthened operational risk controls

## Next Steps

1. Deploy the updated CSP configuration
2. Monitor for any violations or issues
3. Consider implementing additional security headers
4. Regular security assessments and updates
