# GRC Platform API Documentation

## Overview

The GRC Platform provides a comprehensive API for Governance, Risk, and Compliance management. This documentation covers all API endpoints, request/response schemas, and integration examples.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require authentication using JWT tokens.

### Getting a Token

```bash
POST /auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Using the Token

Include the token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

## Services

### Policy Service (Port 8001)

#### Create Policy
```bash
POST /policies
Content-Type: application/json

{
  "title": "Security Policy",
  "content": "Policy content here...",
  "category": "security",
  "status": "active"
}
```

#### Get Policy
```bash
GET /policies/{policy_id}
```

#### Update Policy
```bash
PUT /policies/{policy_id}
Content-Type: application/json

{
  "title": "Updated Security Policy",
  "content": "Updated content...",
  "status": "active"
}
```

#### Delete Policy
```bash
DELETE /policies/{policy_id}
```

### Risk Service (Port 8002)

#### Create Risk Assessment
```bash
POST /risks
Content-Type: application/json

{
  "title": "Data Breach Risk",
  "description": "Risk of unauthorized data access",
  "category": "security",
  "score": 0.75,
  "mitigation": "Implement access controls"
}
```

#### Get Risk Assessment
```bash
GET /risks/{risk_id}
```

#### Update Risk Assessment
```bash
PUT /risks/{risk_id}
Content-Type: application/json

{
  "score": 0.5,
  "mitigation": "Enhanced access controls implemented"
}
```

### Compliance Service (Port 8003)

#### Check Compliance
```bash
POST /compliance/check
Content-Type: application/json

{
  "policy_id": "policy_123",
  "entity_id": "entity_456",
  "check_type": "automated"
}
```

#### Get Compliance Status
```bash
GET /compliance/status/{entity_id}
```

#### Generate Compliance Report
```bash
POST /compliance/reports
Content-Type: application/json

{
  "entity_id": "entity_456",
  "report_type": "full",
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  }
}
```

## AI Agents Integration

### BFSI Agent

The Banking, Financial Services, and Insurance (BFSI) agent provides specialized compliance monitoring for financial institutions.

```bash
POST /ai-agents/bfsi/analyze
Content-Type: application/json

{
  "document_type": "policy",
  "content": "Financial policy content...",
  "regulations": ["SOX", "PCI-DSS"]
}
```

### Healthcare Agent

The Healthcare agent provides compliance monitoring for healthcare organizations.

```bash
POST /ai-agents/healthcare/analyze
Content-Type: application/json

{
  "document_type": "policy",
  "content": "Healthcare policy content...",
  "regulations": ["HIPAA", "HITECH"]
}
```

## Error Handling

All API endpoints return standardized error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "title",
      "issue": "Title is required"
    }
  }
}
```

### Common Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_ERROR`: Invalid or missing authentication
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `INTERNAL_ERROR`: Server error

## Rate Limiting

API requests are rate-limited to prevent abuse:

- **Authenticated users**: 1000 requests per hour
- **Unauthenticated users**: 100 requests per hour

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Pagination

List endpoints support pagination:

```bash
GET /policies?page=1&limit=10&sort=created_at&order=desc
```

Response includes pagination metadata:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}
```

## Webhooks

The platform supports webhooks for real-time notifications:

### Register Webhook

```bash
POST /webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["policy.created", "risk.updated"],
  "secret": "your_webhook_secret"
}
```

### Webhook Payload

```json
{
  "event": "policy.created",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "policy_id": "policy_123",
    "title": "New Policy"
  }
}
```

## SDKs and Libraries

### Python SDK

```python
from grc_platform import GRCClient

client = GRCClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Create a policy
policy = client.policies.create({
    "title": "Security Policy",
    "content": "Policy content...",
    "category": "security"
})

# Get compliance status
status = client.compliance.get_status("entity_123")
```

### JavaScript SDK

```javascript
import { GRCClient } from '@grc/platform-sdk';

const client = new GRCClient({
  baseUrl: 'http://localhost:8000',
  apiKey: 'your_api_key'
});

// Create a policy
const policy = await client.policies.create({
  title: 'Security Policy',
  content: 'Policy content...',
  category: 'security'
});

// Get compliance status
const status = await client.compliance.getStatus('entity_123');
```

## Testing

### Test Environment

Use the test environment for development and testing:

```
https://test-api.grc-platform.com/api/v1
```

### Test Data

The test environment includes sample data for testing:

- **Policies**: 10 sample policies
- **Risks**: 15 sample risk assessments
- **Compliance**: 5 sample compliance checks

## Support

For API support and questions:

- **Documentation**: [docs.grc-platform.com](https://docs.grc-platform.com)
- **Support Email**: api-support@grc-platform.com
- **Status Page**: [status.grc-platform.com](https://status.grc-platform.com)
