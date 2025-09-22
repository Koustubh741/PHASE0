# GRC Platform Docker Deployment Guide

This guide provides comprehensive instructions for deploying the GRC Platform using Docker containers.

## 🏗️ Architecture Overview

The GRC Platform consists of the following services:

- **PostgreSQL**: Primary database
- **Redis**: Caching and session management
- **Backend API**: FastAPI-based REST API
- **Frontend**: React-based web application
- **API Gateway**: Request routing and load balancing
- **BFSI AI Agents**: AI-powered analysis services
- **Nginx**: Reverse proxy and load balancer

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB+ RAM recommended
- 20GB+ disk space

## 🚀 Quick Start

### Development Environment

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd phase0
   ```

2. **Start development environment**:
   ```bash
   python scripts/docker-manager.py dev
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Gateway: http://localhost:8080
   - BFSI AI Agents: http://localhost:8001

### Production Environment

1. **Configure environment variables**:
   ```bash
   cp docker.env .env.production
   # Edit .env.production with production values
   ```

2. **Start production environment**:
   ```bash
   python scripts/docker-manager.py prod
   ```

## 🔧 Docker Management

### Using the Docker Manager Script

```bash
# Check Docker installation
python scripts/docker-manager.py check

# Build all services
python scripts/docker-manager.py build

# Start all services
python scripts/docker-manager.py start

# Stop all services
python scripts/docker-manager.py stop

# Restart specific services
python scripts/docker-manager.py restart --services backend frontend

# View logs
python scripts/docker-manager.py logs --follow

# Check service status
python scripts/docker-manager.py status

# Health check
python scripts/docker-manager.py health

# Clean up resources
python scripts/docker-manager.py clean
```

### Using Docker Compose Directly

#### Development
```bash
# Start all services
docker-compose up -d

# Start specific services
docker-compose up -d postgres redis backend

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

#### Production
```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop production services
docker-compose -f docker-compose.prod.yml down
```

## 🏥 Health Checks

All services include health checks:

- **PostgreSQL**: `pg_isready` command
- **Redis**: `redis-cli ping` command
- **Backend**: HTTP health endpoint
- **Frontend**: HTTP health check
- **API Gateway**: HTTP health endpoint
- **BFSI AI Agents**: HTTP health endpoint
- **Nginx**: HTTP health endpoint

## 📊 Monitoring

### Service Status
```bash
# Check all service status
python scripts/docker-manager.py status

# Check service health
python scripts/docker-manager.py health
```

### Logs
```bash
# View all logs
python scripts/docker-manager.py logs

# Follow specific service logs
python scripts/docker-manager.py logs --services backend --follow

# View production logs
python scripts/docker-manager.py logs --production
```

## 🔒 Security Configuration

### Environment Variables

Create a `.env.production` file with secure values:

```bash
# Database
POSTGRES_PASSWORD=your-secure-password
SECRET_KEY=your-jwt-secret-key

# API Configuration
REACT_APP_API_URL=https://your-domain.com/api
```

### SSL/TLS Configuration

1. **Generate SSL certificates**:
   ```bash
   mkdir -p infrastructure/nginx/ssl
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout infrastructure/nginx/ssl/key.pem \
     -out infrastructure/nginx/ssl/cert.pem
   ```

2. **Update Nginx configuration** for HTTPS (uncomment HTTPS server block)

## 🗄️ Database Management

### Backup
```bash
# Manual backup
docker exec grc-postgres pg_dump -U grc_user grc_platform > backup.sql

# Automated backup (production)
# Backups are automatically created daily and stored in ./backups/
```

### Restore
```bash
# Restore from backup
docker exec -i grc-postgres psql -U grc_user grc_platform < backup.sql
```

### Database Initialization
```bash
# Initialize database with schema
docker-compose exec backend python scripts/init_db.py

# Seed with demo data
docker-compose exec backend python scripts/seed_demo_data.py
```

## 🔄 Updates and Maintenance

### Update Services
```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

### Clean Up
```bash
# Remove unused resources
python scripts/docker-manager.py clean

# Remove all containers and volumes
docker-compose down -v
docker system prune -a
```

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**:
   ```bash
   # Check port usage
   netstat -tulpn | grep :8000
   
   # Change ports in docker-compose.yml
   ```

2. **Database connection issues**:
   ```bash
   # Check database logs
   docker-compose logs postgres
   
   # Test database connection
   docker-compose exec backend python -c "from core.infrastructure.database import db_manager; print(db_manager.check_connection())"
   ```

3. **Service not starting**:
   ```bash
   # Check service logs
   docker-compose logs <service-name>
   
   # Check service status
   docker-compose ps
   ```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set debug environment variable
export DEBUG=true

# Restart services
docker-compose restart
```

## 📈 Performance Optimization

### Resource Limits

Add resource limits to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### Scaling Services

```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Scale with load balancer
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## 🔐 Production Deployment

### Security Checklist

- [ ] Change default passwords
- [ ] Use strong JWT secret keys
- [ ] Enable SSL/TLS
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Backup strategy implementation

### Environment Configuration

1. **Create production environment file**:
   ```bash
   cp docker.env .env.production
   ```

2. **Update with production values**:
   - Strong passwords
   - Production database URLs
   - SSL certificates
   - Monitoring endpoints

3. **Deploy**:
   ```bash
   python scripts/docker-manager.py prod
   ```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Redis Docker Image](https://hub.docker.com/_/redis)

## 🆘 Support

For issues and support:

1. Check the troubleshooting section
2. Review service logs
3. Check Docker and Docker Compose versions
4. Verify system requirements
5. Contact the development team

---

**Note**: This deployment guide is for the GRC Platform demo environment. For production deployments, additional security, monitoring, and backup configurations should be implemented.
