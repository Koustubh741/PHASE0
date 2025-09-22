# GRC Platform API Gateway

The API Gateway serves as the single entry point for all client requests to the GRC Platform microservices. It provides routing, load balancing, authentication, circuit breaking, and service discovery capabilities.

## Features

- **Service Routing**: Routes requests to appropriate microservices based on URL patterns
- **Load Balancing**: Distributes requests across healthy service instances
- **Circuit Breaking**: Prevents cascading failures by temporarily disabling unhealthy services
- **Health Monitoring**: Continuous health checks for all microservices
- **Authentication**: JWT token validation and user context propagation
- **Request Logging**: Comprehensive logging of all requests and responses
- **CORS Support**: Configurable Cross-Origin Resource Sharing

## Architecture

```
Client Request
     ↓
API Gateway (Port 8000)
     ↓
Route to Microservice:
- /api/v1/policies → Policy Service (Port 8001)
- /api/v1/risks → Risk Service (Port 8002)
- /api/v1/compliance → Compliance Service (Port 8003)
- /api/v1/workflows → Workflow Service (Port 8004)
- /api/v1/ai-agents → AI Agents Service (Port 8005)
```

## Service Registry

The gateway maintains a registry of all microservices:

| Service | Port | Health Check | Description |
|---------|------|--------------|-------------|
| Policy | 8001 | `/health` | Policy management operations |
| Risk | 8002 | `/health` | Risk assessment and management |
| Compliance | 8003 | `/health` | Compliance monitoring and reporting |
| Workflow | 8004 | `/health` | Workflow orchestration |
| AI Agents | 8005 | `/health` | AI-powered analysis and insights |

## Circuit Breaker

The gateway implements circuit breaker patterns to handle service failures:

- **Closed**: Normal operation, requests are forwarded
- **Open**: Service is failing, requests are rejected immediately
- **Half-Open**: Testing if service has recovered

Circuit breaker opens after 5 consecutive failures and stays open for 5 minutes.

## Running the Gateway

### Development Mode

```bash
cd backend/src/core/infrastructure/api_gateway
python start_gateway.py
```

### Production Mode

```bash
cd backend/src/core/infrastructure/api_gateway
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
cd backend/src/core/infrastructure/api_gateway
docker-compose up
```

## API Endpoints

### Gateway Endpoints

- `GET /health` - Gateway health check
- `GET /services/status` - Status of all microservices
- `GET /` - Gateway information

### Proxied Endpoints

All requests to `/api/v1/*` are automatically routed to the appropriate microservice.

## Configuration

The gateway can be configured through environment variables:

- `DEBUG`: Enable debug mode (default: false)
- `CORS_ORIGINS`: Allowed CORS origins (default: ["*"])
- `REQUEST_TIMEOUT`: Request timeout in seconds (default: 30)
- `HEALTH_CHECK_INTERVAL`: Health check interval in seconds (default: 30)

## Authentication

The gateway validates JWT tokens for protected endpoints:

1. Extracts `Authorization: Bearer <token>` header
2. Validates token with auth service
3. Adds user context to request headers:
   - `X-User-ID`: User identifier
   - `X-User-Email`: User email
   - `X-User-Role`: User role
   - `X-Organization-ID`: Organization identifier

## Monitoring

### Health Checks

- Gateway health: `GET /health`
- Service status: `GET /services/status`

### Logging

All requests are logged with:
- Client IP address
- Request method and path
- Target service
- Response status code
- Processing time

### Metrics

The gateway tracks:
- Request count per service
- Response times
- Error rates
- Circuit breaker states

## Development

### Adding New Services

1. Add service configuration to `config.py`
2. Update route mappings in `gateway.py`
3. Add authentication requirements if needed
4. Update docker-compose.yml

### Testing

```bash
# Test gateway health
curl http://localhost:8000/health

# Test service routing
curl http://localhost:8000/api/v1/policies

# Test service status
curl http://localhost:8000/services/status
```

## Troubleshooting

### Common Issues

1. **Service Unavailable**: Check if target microservice is running
2. **Authentication Errors**: Verify JWT token format and validity
3. **Timeout Errors**: Increase request timeout in configuration
4. **Circuit Breaker Open**: Wait for service recovery or manually reset

### Logs

Check gateway logs for detailed error information:

```bash
# View logs
docker-compose logs api-gateway

# Follow logs
docker-compose logs -f api-gateway
```
