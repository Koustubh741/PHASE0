# JWT Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the BFSI Policy Service with production-ready JWT authentication. The implementation includes enterprise-grade security features, monitoring, and compliance requirements.

## Security Features Implemented

### 1. JWT Token Validation
- **Algorithm**: HS256 (configurable)
- **Token Expiration**: Configurable via environment variables
- **Signature Verification**: Comprehensive signature and claims validation
- **Audience/Issuer Validation**: Strict validation of token issuer and audience
- **Scope-based Authorization**: Role and permission-based access control

### 2. Security Monitoring & Logging
- **Audit Logging**: All authentication events logged with timestamps
- **Rate Limiting**: Per-IP request rate limiting
- **Failed Attempt Tracking**: Suspicious activity detection
- **Token Blacklisting**: Immediate token revocation capability
- **Security Events**: Real-time security event monitoring

### 3. Production Security Controls
- **Environment-based Configuration**: Secure secret management
- **IP-based Rate Limiting**: DDoS protection
- **Comprehensive Error Handling**: Secure error responses
- **Request Validation**: Input sanitization and validation

## Environment Configuration

### Required Environment Variables

```bash
# JWT Configuration (REQUIRED)
JWT_SECRET_KEY=your_super_secure_jwt_secret_key_minimum_32_characters
SESSION_TIMEOUT_MINUTES=30

# Security Configuration
RATE_LIMIT_REQUESTS_PER_MINUTE=60
AUDIT_LOG_ENABLED=true
DATA_ENCRYPTION_ENABLED=true

# Production Security Headers
ALLOWED_ISSUERS=["bfsi-grc-platform", "bfsi-auth-service"]
ALLOWED_AUDIENCES=["bfsi-api", "bfsi-policy-service"]
REQUIRED_SCOPES=["policy:read", "policy:write"]
```

### Security Best Practices

1. **JWT Secret Key**:
   - Minimum 32 characters
   - Use cryptographically secure random generation
   - Store in secure environment variables or key management system
   - Rotate regularly (quarterly recommended)

2. **Token Configuration**:
   - Set appropriate expiration times (30 minutes for access tokens)
   - Use refresh tokens for longer sessions
   - Implement token rotation

3. **Rate Limiting**:
   - Configure based on expected traffic patterns
   - Monitor for abuse patterns
   - Adjust limits based on user behavior

## API Endpoints

### Authentication Endpoints

#### `POST /security/logout`
- **Purpose**: Logout and blacklist current token
- **Authentication**: Required (Bearer token)
- **Response**: Success confirmation

#### `GET /security/events`
- **Purpose**: Retrieve security audit events
- **Authentication**: Required (Admin role)
- **Parameters**: `limit` (optional, default: 100)

#### `GET /security/status`
- **Purpose**: Get current security metrics
- **Authentication**: Required (Admin or Security Officer role)
- **Response**: Security statistics and configuration

### Policy Endpoints (All require authentication)

All existing policy endpoints now include:
- JWT token validation
- Rate limiting
- Audit logging
- Permission checking

## JWT Token Structure

### Required Claims
```json
{
  "sub": "user-123",                    // User ID (required)
  "organization_id": "org-123",         // Organization ID (required)
  "role": "ADMIN",                      // User role
  "scope": "policy:read policy:write",  // Required scopes
  "iss": "bfsi-grc-platform",          // Issuer (required)
  "aud": "bfsi-policy-service",        // Audience (required)
  "exp": 1640995200,                   // Expiration time
  "iat": 1640991600,                   // Issued at
  "nbf": 1640991600,                   // Not before (optional)
  "jti": "token-id-123"                // JWT ID (recommended)
}
```

### Optional Claims
```json
{
  "email": "user@example.com",
  "username": "john.doe",
  "session_id": "session-123",
  "department": "Compliance",
  "permissions": ["policy:create", "policy:approve"]
}
```

## Security Monitoring

### Security Events Logged
- `SUCCESSFUL_AUTHENTICATION`: Successful login
- `EXPIRED_TOKEN_ACCESS`: Attempted access with expired token
- `INVALID_TOKEN_CLAIMS`: Token validation failures
- `RATE_LIMIT_EXCEEDED`: Rate limit violations
- `BLACKLISTED_TOKEN_ACCESS`: Attempted access with revoked token
- `SUSPICIOUS_ACTIVITY`: Multiple failed attempts
- `USER_LOGOUT`: User logout events

### Monitoring Recommendations
1. Set up alerts for:
   - Multiple failed authentication attempts
   - Rate limit violations
   - Token blacklist access attempts
   - Unusual authentication patterns

2. Regular Security Reviews:
   - Review security events weekly
   - Analyze failed authentication patterns
   - Monitor token usage patterns
   - Audit user permissions quarterly

## Production Deployment Steps

### 1. Environment Setup
```bash
# Set required environment variables
export JWT_SECRET_KEY="$(openssl rand -base64 32)"
export SESSION_TIMEOUT_MINUTES="30"
export RATE_LIMIT_REQUESTS_PER_MINUTE="60"
export AUDIT_LOG_ENABLED="true"
```

### 2. Security Configuration
- Configure firewall rules
- Set up SSL/TLS certificates
- Configure reverse proxy (nginx/Apache)
- Set up monitoring and alerting

### 3. Database Security
- Use encrypted connections
- Implement database access controls
- Regular security updates
- Backup encryption

### 4. Network Security
- Use HTTPS only
- Configure CORS properly
- Implement IP whitelisting if needed
- Use load balancer with SSL termination

## Compliance Considerations

### GDPR Compliance
- Audit logging for data access
- User consent tracking
- Data retention policies
- Right to be forgotten implementation

### SOX Compliance
- Comprehensive audit trails
- Access control monitoring
- Change management tracking
- Regular security assessments

### PCI DSS Compliance
- Secure token storage
- Encryption in transit and at rest
- Access control monitoring
- Regular vulnerability assessments

## Troubleshooting

### Common Issues

1. **"JWT_SECRET_KEY environment variable is required"**
   - Solution: Set the JWT_SECRET_KEY environment variable

2. **"Invalid token claims: insufficient permissions"**
   - Solution: Ensure token includes required scopes

3. **"Rate limit exceeded"**
   - Solution: Wait or increase rate limit configuration

4. **"Token has been revoked"**
   - Solution: Obtain new token after logout

### Security Incident Response

1. **Immediate Actions**:
   - Blacklist compromised tokens
   - Review security events
   - Notify security team

2. **Investigation**:
   - Analyze security logs
   - Identify attack vectors
   - Document incident

3. **Recovery**:
   - Rotate secrets if compromised
   - Update security configurations
   - Implement additional controls

## Performance Considerations

- JWT validation adds ~1-2ms per request
- Rate limiting uses in-memory storage (consider Redis for distributed deployments)
- Security event logging has minimal performance impact
- Token blacklisting uses SHA256 hashing for fast lookups

## Scaling Considerations

For high-traffic deployments:
- Use Redis for distributed rate limiting
- Implement token caching
- Consider JWT token pre-validation
- Use connection pooling for database operations
- Implement horizontal scaling with load balancers

## Maintenance

### Regular Tasks
- Monitor security events daily
- Review rate limiting effectiveness weekly
- Rotate JWT secrets quarterly
- Update dependencies monthly
- Conduct security assessments annually

### Security Updates
- Keep dependencies updated
- Monitor security advisories
- Implement security patches promptly
- Regular penetration testing

## Support

For production issues or security concerns:
1. Check security event logs
2. Review rate limiting metrics
3. Validate JWT token configuration
4. Contact security team for incidents

---

**Note**: This implementation is production-ready but should be reviewed by your security team before deployment. Consider additional security measures based on your specific compliance requirements and threat model.
