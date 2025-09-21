# Database Configuration

This module provides secure database configuration management for the GRC platform.

## Environment Variables

### Production (Recommended)
```bash
DATABASE_URL=postgresql://username:password@hostname:port/database_name
ENVIRONMENT=production
```

### Development (Fallback)
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=grc_platform
DB_USER=grc_user
DB_PASSWORD=grc_password
ENVIRONMENT=development
```

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** or secret management systems in production
3. **DATABASE_URL is preferred** for production deployments
4. **Validate configuration** before application startup
5. **Use connection pooling** for high-traffic applications

## Usage

```python
from backend.src.core.infrastructure.config.database_config import get_database_url, is_secure_config

# Get database URL
database_url = get_database_url()

# Check if using secure configuration
if is_secure_config():
    print("Using secure configuration")
```

## Configuration Validation

The configuration module automatically:
- Validates DATABASE_URL format
- Checks for required environment variables in production
- Provides fallback values for development
- Logs security warnings for development configurations
