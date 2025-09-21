# GRC Platform Backend

A production-ready Governance, Risk, and Compliance (GRC) platform backend built with FastAPI, PostgreSQL, and Redis. This platform provides comprehensive GRC functionality with enterprise-grade security, audit capabilities, and compliance features.

## 🚀 Features

### Core GRC Functionality
- **User Management** - Complete user lifecycle with RBAC
- **Policy Management** - Policy creation, versioning, and compliance tracking
- **Risk Management** - Risk assessment, treatment, and monitoring
- **Control Management** - Control implementation, testing, and effectiveness
- **Issue Management** - Issue tracking, resolution, and escalation
- **Audit & Compliance** - Comprehensive audit trails and reporting

### Security Features
- JWT-based authentication with role-based access control
- Two-factor authentication support
- Comprehensive audit logging for all operations
- Input validation and sanitization
- Rate limiting and security headers
- OWASP security best practices

### Enterprise Features
- Horizontal scaling with Docker containers
- PostgreSQL with connection pooling
- Redis caching and session management
- Nginx reverse proxy with SSL termination
- Database migrations with Alembic
- Comprehensive API documentation

## 🏗️ Architecture

The backend follows Clean Architecture principles with clear separation of concerns:

```
backend/
├── src/
│   ├── core/
│   │   ├── domain/           # Domain entities and business logic
│   │   ├── application/      # Use cases and services
│   │   └── infrastructure/   # Database and external services
│   └── api/
│       ├── v1/              # API version 1 endpoints
│       └── middleware/      # Authentication and security middleware
├── alembic/                 # Database migrations
├── nginx/                   # Nginx configuration
├── docker-compose.yml       # Container orchestration
└── Dockerfile              # Container definition
```

### Domain Entities
- **User** - User accounts with roles and permissions
- **Policy** - Policies with versioning and approval workflows
- **Risk** - Risk assessments and treatment plans
- **Control** - Control implementation and testing
- **Issue** - Issue tracking and resolution
- **AuditLog** - Immutable audit trail for compliance

### Roles and Permissions
- **Admin** - Full system access and user management
- **Auditor** - Read-only access with audit log viewing
- **Risk Owner** - Risk management and assessment
- **Control Owner** - Control implementation and testing
- **Compliance Manager** - Policy and compliance management
- **Policy Owner** - Policy creation and management
- **Viewer** - Read-only access to assigned resources

## 🛠️ Technology Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Authentication**: JWT with bcrypt password hashing
- **API Documentation**: OpenAPI/Swagger
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx
- **Database Migrations**: Alembic
- **Testing**: pytest with async support
- **Code Quality**: Black, Flake8, MyPy

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)
- Redis 7+ (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   createdb grc_platform
   ```

3. **Run migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start Redis**
   ```bash
   redis-server
   ```

5. **Run the application**
   ```bash
   uvicorn src.core.presentation.api.main:app --reload
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=grc_platform
POSTGRES_USER=grc_user
POSTGRES_PASSWORD=your_secure_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_DB=0

# Security
SECRET_KEY=your_super_secret_key_change_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=GRC Platform
DEBUG=false
VERSION=1.0.0

# Vector Store
VECTOR_STORE_DIR=./vector_store
VECTOR_COLLECTION=compliance-policies
```

### Security Configuration

For production deployment, ensure you:

1. **Change default passwords** in environment variables
2. **Use strong JWT secret keys** (minimum 32 characters)
3. **Enable SSL/TLS** with valid certificates
4. **Configure firewall rules** to restrict access
5. **Set up monitoring and logging**
6. **Regular security updates** of dependencies

## 📚 API Documentation

### Authentication

All API endpoints (except public ones) require JWT authentication:

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Use token in subsequent requests
curl -X GET "http://localhost:8000/api/v1/users" \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Core Endpoints

#### User Management
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{user_id}` - Get user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

#### Policy Management
- `POST /api/v1/policies` - Create policy
- `GET /api/v1/policies` - List policies
- `GET /api/v1/policies/{policy_id}` - Get policy
- `PUT /api/v1/policies/{policy_id}` - Update policy
- `POST /api/v1/policies/{policy_id}/versions` - Create policy version

#### Risk Management
- `POST /api/v1/risks` - Create risk
- `GET /api/v1/risks` - List risks
- `POST /api/v1/risks/{risk_id}/assess` - Assess risk
- `POST /api/v1/risks/{risk_id}/treatments` - Add treatment

#### Control Management
- `POST /api/v1/controls` - Create control
- `GET /api/v1/controls` - List controls
- `POST /api/v1/controls/{control_id}/tests` - Add control test
- `PUT /api/v1/controls/{control_id}/effectiveness` - Assess effectiveness

#### Issue Management
- `POST /api/v1/issues` - Create issue
- `GET /api/v1/issues` - List issues
- `POST /api/v1/issues/{issue_id}/actions` - Add action
- `POST /api/v1/issues/{issue_id}/comments` - Add comment

### Response Format

All API responses follow a consistent format:

```json
{
  "data": {...},
  "message": "Success",
  "status_code": 200,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Error Handling

Errors are returned with appropriate HTTP status codes:

```json
{
  "error": "Validation Error",
  "message": "Invalid input data",
  "details": {...},
  "status_code": 400
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for API endpoints
├── e2e/           # End-to-end tests
└── fixtures/      # Test fixtures and data
```

### Test Categories

1. **Unit Tests** - Test individual functions and classes
2. **Integration Tests** - Test API endpoints and database interactions
3. **Security Tests** - Test authentication, authorization, and security features
4. **Performance Tests** - Test API performance and scalability

## 🔍 Monitoring and Logging

### Logging

The application uses structured logging with the following levels:
- **INFO** - General application flow
- **WARNING** - Potential issues
- **ERROR** - Error conditions
- **CRITICAL** - Critical system failures

Logs are written to:
- Console (for development)
- `/app/logs/grc_platform.log` (in containers)
- Structured JSON format for production

### Health Checks

The application provides health check endpoints:

- `GET /health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed system health

### Metrics

Key metrics to monitor:
- API response times
- Database connection pool status
- Redis cache hit rates
- Authentication success/failure rates
- Audit log volume

## 🚀 Deployment

### Production Deployment

1. **Prepare production environment**
   ```bash
   # Set production environment variables
   export DEBUG=false
   export SECRET_KEY="your-production-secret-key"
   export POSTGRES_PASSWORD="your-secure-password"
   ```

2. **Build and deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Run migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

4. **Verify deployment**
   ```bash
   curl http://your-domain.com/health
   ```

### Scaling

The application supports horizontal scaling:

1. **Database scaling** - Use PostgreSQL read replicas
2. **Application scaling** - Scale backend containers
3. **Cache scaling** - Use Redis cluster
4. **Load balancing** - Use Nginx or external load balancer

### Backup and Recovery

1. **Database backups**
   ```bash
   pg_dump grc_platform > backup.sql
   ```

2. **Redis persistence** - Configure Redis persistence
3. **Application data** - Backup uploaded files and logs

## 🔒 Security Considerations

### Authentication Security
- Use strong passwords (minimum 8 characters with complexity)
- Implement account lockout policies
- Regular password rotation
- Two-factor authentication for admin accounts

### API Security
- Rate limiting to prevent abuse
- Input validation and sanitization
- SQL injection prevention with parameterized queries
- XSS protection with security headers

### Data Security
- Encryption at rest for sensitive data
- Encryption in transit with TLS
- Regular security audits
- Access logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Use type hints
- Follow security best practices

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the API documentation at `/docs`

## 🔄 Version History

- **v1.0.0** - Initial release with core GRC functionality
- **v1.1.0** - Added advanced risk assessment features
- **v1.2.0** - Enhanced audit and compliance reporting

## 🎯 Roadmap

- [ ] Advanced workflow automation
- [ ] Machine learning for risk prediction
- [ ] Mobile application support
- [ ] Advanced reporting and analytics
- [ ] Third-party integrations
- [ ] Multi-tenant support

---

Built with ❤️ for enterprise governance, risk, and compliance management.