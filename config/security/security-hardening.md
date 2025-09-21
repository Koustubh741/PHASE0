# BFSI API Security Hardening Guide

## Production Security Configuration

This guide provides comprehensive security hardening for the BFSI API in production environments.

## 1. Server Configuration Security

### Environment Variables
Set the following environment variables for production:

```bash
# Production environment
ENVIRONMENT=production
HOST=127.0.0.1  # Never use 0.0.0.0 in production
PORT=8009
WORKERS=4

# Request limits
LIMIT_REQUEST_BODY=10485760  # 10MB
LIMIT_CONCURRENCY=1000
LIMIT_MAX_REQUESTS=10000

# Security settings
DATA_ENCRYPTION_ENABLED=true
AUDIT_LOG_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
```

### TLS/SSL Configuration
For direct TLS termination (not recommended for production):

```bash
SSL_KEYFILE=/etc/ssl/private/bfsi-api.key
SSL_CERTFILE=/etc/ssl/certs/bfsi-api.crt
SSL_CA_CERTS=/etc/ssl/certs/ca-bundle.crt
SSL_CIPHERS=ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS
SSL_MINIMUM_VERSION=TLSv1.2
```

## 2. Reverse Proxy Configuration

### Nginx (Recommended)
Use the provided `config/nginx/bfsi-api.conf` with the following security features:

- TLS termination with modern ciphers
- Rate limiting (10 req/s general, 5 req/s sensitive endpoints)
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Request size limits (10MB)
- WebSocket support with proper timeouts
- Blocking of sensitive file access

### Apache
Use the provided `config/apache/bfsi-api.conf` with similar security features.

## 3. Docker Security

### Production Docker Compose
Use `config/docker/docker-compose.production.yml` with:

- Non-root user execution
- Read-only filesystems
- Dropped capabilities
- Resource limits
- Health checks
- Security options

### Security Features:
```yaml
security_opt:
  - no-new-privileges:true
read_only: true
user: "1000:1000"
cap_drop:
  - ALL
cap_add:
  - NET_BIND_SERVICE
```

## 4. Network Security

### Firewall Rules
```bash
# Allow only necessary ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp  # SSH
ufw deny 8009/tcp  # Block direct access to API
ufw enable
```

### Network Segmentation
- Place API behind reverse proxy
- Use internal networks for database connections
- Implement network policies for container communication

## 5. Database Security

### PostgreSQL Configuration
```sql
-- Enable SSL
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'

-- Connection limits
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB

-- Security settings
password_encryption = scram-sha-256
log_connections = on
log_disconnections = on
log_statement = 'all'
```

### Redis Security
```bash
# Require authentication
requirepass secure_redis_password

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
rename-command CONFIG ""

# Enable SSL
tls-port 6380
tls-cert-file /etc/ssl/certs/redis.crt
tls-key-file /etc/ssl/private/redis.key
```

## 6. Application Security

### Security Headers
The application includes comprehensive security headers:

- `Strict-Transport-Security`: HSTS with 1-year max-age
- `X-Frame-Options`: DENY
- `X-Content-Type-Options`: nosniff
- `X-XSS-Protection`: 1; mode=block
- `Content-Security-Policy`: Restrictive CSP
- `Referrer-Policy`: strict-origin-when-cross-origin
- `Permissions-Policy`: Restrictive permissions

### Rate Limiting
- General endpoints: 10 requests/second
- Sensitive endpoints: 5 requests/second
- Burst handling with nodelay
- IP-based rate limiting

### Request Validation
- Maximum request body: 10MB
- Maximum request line: 4094 bytes
- Maximum request fields: 100
- Maximum field size: 8190 bytes

## 7. Monitoring and Logging

### Security Monitoring
- Failed authentication attempts
- Rate limit violations
- Suspicious request patterns
- Database access anomalies

### Log Aggregation
- Centralized logging with Fluentd
- Log rotation and retention
- Security event correlation
- Real-time alerting

### Metrics Collection
- Prometheus for metrics collection
- Grafana for visualization
- Custom security metrics
- Performance monitoring

## 8. Compliance Requirements

### PCI-DSS Compliance
- Data encryption at rest and in transit
- Access controls and authentication
- Network security and monitoring
- Regular security testing
- Incident response procedures

### GDPR Compliance
- Data anonymization capabilities
- Consent tracking
- Right to be forgotten
- Data portability
- Privacy by design

## 9. Backup and Recovery

### Backup Strategy
- Daily automated backups
- Encrypted backup storage
- Off-site backup replication
- Regular restore testing
- Point-in-time recovery

### Disaster Recovery
- Multi-region deployment
- Automated failover
- Data replication
- Recovery time objectives
- Business continuity planning

## 10. Security Testing

### Regular Security Assessments
- Vulnerability scanning
- Penetration testing
- Code security reviews
- Dependency updates
- Security training

### Automated Security Testing
- SAST (Static Application Security Testing)
- DAST (Dynamic Application Security Testing)
- Dependency vulnerability scanning
- Container security scanning
- Infrastructure as Code security

## 11. Incident Response

### Security Incident Procedures
- Incident detection and classification
- Response team activation
- Evidence collection and preservation
- Communication and notification
- Recovery and lessons learned

### Security Monitoring
- Real-time threat detection
- Automated response systems
- Security information and event management (SIEM)
- Threat intelligence integration
- Continuous monitoring

## 12. Access Control

### Authentication
- Multi-factor authentication (MFA)
- Strong password policies
- Account lockout mechanisms
- Session management
- Token-based authentication

### Authorization
- Role-based access control (RBAC)
- Principle of least privilege
- Resource-based permissions
- API key management
- Audit trail maintenance

## 13. Data Protection

### Encryption
- AES-256-GCM for data at rest
- TLS 1.3 for data in transit
- Key rotation policies
- Hardware security modules (HSM)
- End-to-end encryption

### Data Classification
- Public, internal, confidential, restricted
- Automated data classification
- Data loss prevention (DLP)
- Data retention policies
- Secure data disposal

## 14. Security Updates

### Patch Management
- Regular security updates
- Vulnerability management
- Dependency updates
- Security patch testing
- Rollback procedures

### Change Management
- Security review process
- Change approval workflow
- Impact assessment
- Testing requirements
- Documentation updates

This security hardening guide provides a comprehensive approach to securing the BFSI API in production environments. Regular reviews and updates of security measures are essential to maintain a strong security posture.
