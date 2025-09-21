# Login Rate Limiting Implementation

## Overview

This implementation adds comprehensive Redis-based login rate limiting to the BFSI API service, protecting against brute force attacks with exponential backoff and account lockout mechanisms.

## Features Implemented

### 1. Redis-Based Rate Limiting Service
- **Location**: `realtime_bfsi_api.py` (lines 55-231)
- **Class**: `LoginRateLimitService`
- **Features**:
  - Redis-based storage for attempt tracking
  - Exponential backoff algorithm
  - Account lockout after repeated failures
  - Per-IP and per-username tracking
  - Configurable time windows and limits

### 2. Configuration Options
- **Location**: `security_config.py` (lines 35-41)
- **New Settings**:
  ```python
  login_max_attempts: int = 5          # Max attempts per window
  login_window_minutes: int = 15       # Time window for attempts
  login_lockout_minutes: int = 30       # Account lockout duration
  login_exponential_backoff_base: int = 2  # Exponential backoff base
  login_max_backoff_minutes: int = 60   # Maximum backoff time
  login_rate_limit_enabled: bool = True # Enable/disable feature
  ```

### 3. Enhanced Login Endpoint
- **Location**: `realtime_bfsi_api.py` (lines 1058-1128)
- **Protection Features**:
  - Rate limiting check before authentication
  - Failed attempt tracking for both IP and username
  - Successful login clears rate limiting data
  - Comprehensive error handling and logging
  - Proper HTTP status codes and headers

### 4. Rate Limiting Algorithm

#### Sliding Window with Exponential Backoff
1. **Initial Attempts**: Allow up to 5 attempts within 15-minute window
2. **Rate Limit Exceeded**: Apply exponential backoff (2^attempts minutes)
3. **Account Lockout**: After 10+ attempts, lock account for 30 minutes
4. **Success**: Clear all rate limiting data

#### Redis Key Structure
```
login_attempts:ip:{client_ip}     # IP-based attempt tracking
login_attempts:user:{username}    # Username-based attempt tracking
account_lockout:ip:{client_ip}    # IP lockout status
account_lockout:user:{username}   # Username lockout status
login_backoff:ip:{client_ip}      # IP exponential backoff
login_backoff:user:{username}     # Username exponential backoff
```

### 5. HTTP Response Headers
When rate limited, the API returns:
- `429 Too Many Requests` status code
- `Retry-After`: Seconds until next attempt allowed
- `X-RateLimit-Limit`: Maximum attempts allowed
- `X-RateLimit-Remaining`: Attempts remaining (0 when limited)
- `X-RateLimit-Reset`: Timestamp when limit resets

### 6. Security Features

#### Multi-Layer Protection
- **IP-based limiting**: Prevents attacks from single IP
- **Username-based limiting**: Prevents targeted account attacks
- **Exponential backoff**: Increases delay with each attempt
- **Account lockout**: Temporary account suspension
- **Redis persistence**: Survives application restarts

#### Fail-Safe Design
- **Fail-open**: If Redis unavailable, allows login (with warning)
- **Graceful degradation**: Continues operation if rate limiting fails
- **Comprehensive logging**: All attempts and violations logged
- **Error handling**: Proper exception handling throughout

### 7. Integration Points

#### Startup/Shutdown
- **Startup**: Initializes Redis connections for rate limiting
- **Shutdown**: Properly closes Redis connections
- **Configuration**: Uses centralized security configuration

#### Middleware Integration
- **Dependency injection**: `check_login_rate_limit` dependency
- **Request processing**: Rate limiting checked before authentication
- **Response handling**: Proper headers and status codes

## Usage Examples

### Basic Rate Limiting Test
```python
# Test script: test_login_rate_limiting.py
async with LoginRateLimitTester() as tester:
    # This will trigger rate limiting after 5 failed attempts
    await tester.test_rate_limiting("testuser", "wrongpassword")
```

### Configuration
```python
# In security_config.py
login_max_attempts = 5          # Allow 5 attempts
login_window_minutes = 15       # Within 15 minutes
login_lockout_minutes = 30      # Lock for 30 minutes
login_exponential_backoff_base = 2  # 2^attempts backoff
```

## Security Benefits

### 1. Brute Force Protection
- Prevents automated password guessing
- Exponential backoff makes attacks increasingly difficult
- Account lockout prevents persistent attacks

### 2. DDoS Mitigation
- IP-based limiting prevents distributed attacks
- Rate limiting reduces server load
- Redis-based storage is efficient and scalable

### 3. Compliance
- Meets BFSI security requirements
- Provides audit trail for failed attempts
- Configurable for different security policies

### 4. User Experience
- Legitimate users rarely hit limits
- Clear error messages with retry information
- Automatic reset after successful login

## Monitoring and Alerting

### Log Messages
- Failed login attempts: `WARNING` level
- Rate limit violations: `WARNING` level with IP/username
- Successful logins: `INFO` level
- Rate limiting errors: `ERROR` level

### Metrics to Monitor
- Failed login attempts per IP/username
- Rate limit violations
- Account lockouts
- Redis connection health
- Rate limiting service availability

## Deployment Considerations

### Redis Requirements
- Redis server running on `localhost:6379`
- Database 1 used for login rate limiting (separate from CSRF)
- Persistent storage recommended for production

### Configuration
- Adjust limits based on security requirements
- Consider different limits for different user roles
- Monitor and tune based on usage patterns

### Scaling
- Redis can handle high concurrent load
- Consider Redis clustering for high availability
- Monitor Redis memory usage and performance

## Testing

### Manual Testing
1. Start the API server
2. Run `python test_login_rate_limiting.py`
3. Observe rate limiting behavior
4. Check Redis keys and expiration

### Automated Testing
- Unit tests for rate limiting logic
- Integration tests with Redis
- Load testing for performance
- Security testing for bypass attempts

## Future Enhancements

### Potential Improvements
1. **Geolocation-based limiting**: Different limits by country
2. **Device fingerprinting**: Track by device characteristics
3. **Machine learning**: Detect unusual login patterns
4. **Integration**: Connect with SIEM systems
5. **Analytics**: Detailed reporting and dashboards

### Configuration Options
1. **Per-role limits**: Different limits for different user types
2. **Time-based limits**: Different limits by time of day
3. **Location-based limits**: Different limits by IP geolocation
4. **Dynamic limits**: Adjust limits based on threat level

This implementation provides robust protection against brute force attacks while maintaining usability for legitimate users and meeting BFSI compliance requirements.
