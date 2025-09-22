"""
Comprehensive API Documentation
Swagger/OpenAPI documentation for the GRC Platform
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from typing import Dict, Any
import json

def create_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """Create comprehensive OpenAPI schema for GRC Platform"""
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="GRC Platform API",
        version="2.0.0",
        description="""
        # GRC Platform API Documentation
        
        ## Overview
        The GRC (Governance, Risk, and Compliance) Platform provides a comprehensive suite of APIs for managing governance, risk assessment, compliance monitoring, and regulatory reporting in financial services organizations.
        
        ## Key Features
        
        ### 🏛️ Governance & Policy Management
        - Policy lifecycle management
        - Document version control
        - Approval workflows
        - Policy compliance tracking
        
        ### ⚠️ Risk Management
        - Risk assessment and analysis
        - Risk scoring and categorization
        - Risk mitigation planning
        - Risk monitoring and reporting
        
        ### 📋 Compliance Management
        - Multi-framework compliance (SOX, GDPR, PCI-DSS, HIPAA, ISO27001, NIST, COSO, COBIT)
        - Compliance assessment workflows
        - Gap analysis and remediation
        - Evidence collection and verification
        
        ### 🤖 AI & Machine Learning
        - BFSI-specific AI agents
        - Machine learning models for risk prediction
        - Automated compliance checking
        - Predictive analytics and insights
        
        ### 📊 Analytics & Reporting
        - Real-time dashboards
        - Executive reporting
        - Trend analysis
        - Performance metrics
        
        ### 🔄 Workflow Automation
        - Automated workflow triggers
        - AI-powered decision making
        - Process automation
        - Integration capabilities
        
        ### 📈 Real-time Monitoring
        - System health monitoring
        - Performance metrics
        - Alert management
        - Service monitoring
        
        ## Authentication
        All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:
        ```
        Authorization: Bearer <your-jwt-token>
        ```
        
        ## Rate Limiting
        API requests are rate-limited to ensure fair usage:
        - Standard endpoints: 1000 requests per hour
        - AI/ML endpoints: 100 requests per hour
        - Analytics endpoints: 500 requests per hour
        
        ## Error Handling
        The API uses standard HTTP status codes and returns detailed error information in JSON format.
        
        ## Support
        For API support and questions, contact the GRC Platform team.
        """,
        routes=app.routes,
    )
    
    # Add custom OpenAPI extensions
    openapi_schema["info"]["contact"] = {
        "name": "GRC Platform Team",
        "email": "support@grcplatform.com",
        "url": "https://grcplatform.com/support"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "https://api.grcplatform.com",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.grcplatform.com",
            "description": "Staging server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token authentication"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key authentication"
        }
    }
    
    # Add global security
    openapi_schema["security"] = [
        {"BearerAuth": []},
        {"ApiKeyAuth": []}
    ]
    
    # Add tags for better organization
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication and authorization endpoints"
        },
        {
            "name": "Users",
            "description": "User management and profile operations"
        },
        {
            "name": "Policies",
            "description": "Policy management and compliance tracking"
        },
        {
            "name": "Workflows",
            "description": "Workflow management and process automation"
        },
        {
            "name": "BFSI AI",
            "description": "BFSI-specific AI agents and analysis"
        },
        {
            "name": "Analytics",
            "description": "Analytics, reporting, and dashboard data"
        },
        {
            "name": "Real-time Monitoring",
            "description": "System monitoring and alerting"
        },
        {
            "name": "Workflow Automation",
            "description": "Advanced workflow automation and triggers"
        },
        {
            "name": "Compliance Frameworks",
            "description": "Multi-framework compliance management"
        },
        {
            "name": "ML-Enhanced AI",
            "description": "Machine learning enhanced AI capabilities"
        }
    ]
    
    # Add examples for common use cases
    openapi_schema["components"]["examples"] = {
        "RiskAssessment": {
            "summary": "Risk Assessment Example",
            "value": {
                "risk_type": "credit_risk",
                "portfolio_data": {
                    "total_exposure": 1000000000,
                    "number_of_borrowers": 1000,
                    "average_credit_score": 720,
                    "default_rate": 0.02,
                    "recovery_rate": 0.4
                },
                "context": {
                    "economic_conditions": "stable",
                    "regulatory_environment": "evolving"
                }
            }
        },
        "ComplianceAssessment": {
            "summary": "Compliance Assessment Example",
            "value": {
                "framework": "sox",
                "organization_id": "org-123",
                "assessor_id": "user-456",
                "scope": ["finance", "accounting", "audit"],
                "methodology": "standard"
            }
        },
        "WorkflowTrigger": {
            "summary": "Workflow Trigger Example",
            "value": {
                "name": "High Risk Alert",
                "description": "Triggered when risk score exceeds threshold",
                "trigger_type": "threshold",
                "conditions": {"risk_score": "> 0.8", "risk_type": "credit"},
                "actions": ["send_alert", "escalate_to_manager"],
                "priority": 1,
                "enabled": True,
                "ai_powered": False
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def create_api_documentation_html() -> str:
    """Create comprehensive HTML documentation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GRC Platform API Documentation</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                border-radius: 10px;
                margin-bottom: 30px;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
                font-weight: 300;
            }
            .header p {
                margin: 10px 0 0 0;
                font-size: 1.2em;
                opacity: 0.9;
            }
            .section {
                background: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .section h2 {
                color: #667eea;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .feature-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .feature-card h3 {
                margin: 0 0 10px 0;
                color: #667eea;
            }
            .code-block {
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                margin: 20px 0;
            }
            .endpoint {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
            }
            .method {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 0.8em;
                margin-right: 10px;
            }
            .get { background: #48bb78; color: white; }
            .post { background: #ed8936; color: white; }
            .put { background: #4299e1; color: white; }
            .delete { background: #f56565; color: white; }
            .nav {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .nav a {
                color: #667eea;
                text-decoration: none;
                margin-right: 20px;
                font-weight: 500;
            }
            .nav a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏛️ GRC Platform API</h1>
            <p>Comprehensive Governance, Risk & Compliance Management</p>
        </div>
        
        <div class="nav">
            <a href="#overview">Overview</a>
            <a href="#features">Features</a>
            <a href="#authentication">Authentication</a>
            <a href="#endpoints">Endpoints</a>
            <a href="#examples">Examples</a>
            <a href="/docs">Interactive API Docs</a>
            <a href="/redoc">ReDoc Documentation</a>
        </div>
        
        <div class="section" id="overview">
            <h2>📋 Overview</h2>
            <p>The GRC Platform API provides a comprehensive suite of endpoints for managing governance, risk assessment, compliance monitoring, and regulatory reporting in financial services organizations.</p>
            
            <h3>🎯 Key Capabilities</h3>
            <ul>
                <li><strong>Multi-Framework Compliance:</strong> Support for SOX, GDPR, PCI-DSS, HIPAA, ISO27001, NIST, COSO, COBIT</li>
                <li><strong>AI-Powered Analysis:</strong> BFSI-specific AI agents with machine learning capabilities</li>
                <li><strong>Real-time Monitoring:</strong> System health, performance metrics, and alerting</li>
                <li><strong>Workflow Automation:</strong> Advanced triggers and automated processes</li>
                <li><strong>Analytics & Reporting:</strong> Executive dashboards and trend analysis</li>
            </ul>
        </div>
        
        <div class="section" id="features">
            <h2>🚀 Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>🏛️ Governance & Policy Management</h3>
                    <ul>
                        <li>Policy lifecycle management</li>
                        <li>Document version control</li>
                        <li>Approval workflows</li>
                        <li>Compliance tracking</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>⚠️ Risk Management</h3>
                    <ul>
                        <li>Risk assessment and analysis</li>
                        <li>Risk scoring and categorization</li>
                        <li>Mitigation planning</li>
                        <li>Risk monitoring</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>📋 Compliance Management</h3>
                    <ul>
                        <li>Multi-framework support</li>
                        <li>Assessment workflows</li>
                        <li>Gap analysis</li>
                        <li>Evidence collection</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>🤖 AI & Machine Learning</h3>
                    <ul>
                        <li>BFSI AI agents</li>
                        <li>ML risk prediction</li>
                        <li>Automated compliance</li>
                        <li>Predictive analytics</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>📊 Analytics & Reporting</h3>
                    <ul>
                        <li>Real-time dashboards</li>
                        <li>Executive reporting</li>
                        <li>Trend analysis</li>
                        <li>Performance metrics</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <h3>🔄 Workflow Automation</h3>
                    <ul>
                        <li>Automated triggers</li>
                        <li>AI decision making</li>
                        <li>Process automation</li>
                        <li>Integration capabilities</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="section" id="authentication">
            <h2>🔐 Authentication</h2>
            <p>All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:</p>
            
            <div class="code-block">
Authorization: Bearer &lt;your-jwt-token&gt;
            </div>
            
            <h3>Rate Limiting</h3>
            <ul>
                <li><strong>Standard endpoints:</strong> 1000 requests per hour</li>
                <li><strong>AI/ML endpoints:</strong> 100 requests per hour</li>
                <li><strong>Analytics endpoints:</strong> 500 requests per hour</li>
            </ul>
        </div>
        
        <div class="section" id="endpoints">
            <h2>🔗 API Endpoints</h2>
            
            <h3>Authentication</h3>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/auth/login</strong> - User login
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/auth/register</strong> - User registration
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/auth/refresh</strong> - Refresh token
            </div>
            
            <h3>User Management</h3>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/users</strong> - Get all users
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/users/{user_id}</strong> - Get user by ID
            </div>
            <div class="endpoint">
                <span class="method put">PUT</span>
                <strong>/api/v1/users/{user_id}</strong> - Update user
            </div>
            
            <h3>Policy Management</h3>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/policies</strong> - Get all policies
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/policies</strong> - Create policy
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/policies/{policy_id}</strong> - Get policy by ID
            </div>
            
            <h3>BFSI AI Services</h3>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/bfsi-ai/risk-assessment</strong> - Risk assessment
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/bfsi-ai/compliance-check</strong> - Compliance check
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/bfsi-ai/policy-review</strong> - Policy review
            </div>
            
            <h3>Analytics & Reporting</h3>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/analytics/dashboard</strong> - Get dashboard data
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/analytics/metrics</strong> - Get analytics metrics
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/analytics/reports</strong> - Generate report
            </div>
            
            <h3>Real-time Monitoring</h3>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/monitoring/metrics</strong> - Get system metrics
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/monitoring/alerts</strong> - Get alerts
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/monitoring/health</strong> - Health checks
            </div>
            
            <h3>Workflow Automation</h3>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/workflow-automation/templates</strong> - Get workflow templates
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/workflow-automation/workflows</strong> - Create workflow
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/workflow-automation/triggers</strong> - Create trigger
            </div>
            
            <h3>Compliance Frameworks</h3>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/compliance-frameworks/frameworks</strong> - Get frameworks
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/compliance-frameworks/assessments</strong> - Create assessment
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/compliance-frameworks/dashboard</strong> - Compliance dashboard
            </div>
            
            <h3>ML-Enhanced AI</h3>
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/ml-ai/models</strong> - Get ML models
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/ml-ai/models/train</strong> - Train model
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/ml-ai/models/{model_id}/predict</strong> - Make prediction
            </div>
        </div>
        
        <div class="section" id="examples">
            <h2>💡 Usage Examples</h2>
            
            <h3>Risk Assessment</h3>
            <div class="code-block">
POST /api/v1/bfsi-ai/risk-assessment
Content-Type: application/json
Authorization: Bearer &lt;token&gt;

{
  "risk_type": "credit_risk",
  "portfolio_data": {
    "total_exposure": 1000000000,
    "number_of_borrowers": 1000,
    "average_credit_score": 720,
    "default_rate": 0.02,
    "recovery_rate": 0.4
  }
}
            </div>
            
            <h3>Compliance Assessment</h3>
            <div class="code-block">
POST /api/v1/compliance-frameworks/assessments
Content-Type: application/json
Authorization: Bearer &lt;token&gt;

{
  "framework": "sox",
  "organization_id": "org-123",
  "assessor_id": "user-456",
  "scope": ["finance", "accounting", "audit"],
  "methodology": "standard"
}
            </div>
            
            <h3>ML Prediction</h3>
            <div class="code-block">
POST /api/v1/ml-ai/models/{model_id}/predict
Content-Type: application/json
Authorization: Bearer &lt;token&gt;

{
  "input_data": {
    "credit_score": 750,
    "debt_ratio": 0.3,
    "income_stability": 0.8,
    "employment_history": 5
  }
}
            </div>
        </div>
        
        <div class="section">
            <h2>📚 Additional Resources</h2>
            <ul>
                <li><a href="/docs">Interactive API Documentation (Swagger UI)</a></li>
                <li><a href="/redoc">ReDoc Documentation</a></li>
                <li><a href="/openapi.json">OpenAPI Schema (JSON)</a></li>
                <li><a href="https://grcplatform.com/support">Support Documentation</a></li>
                <li><a href="https://grcplatform.com/examples">Code Examples</a></li>
            </ul>
        </div>
    </body>
    </html>
    """

def setup_api_documentation(app: FastAPI):
    """Setup comprehensive API documentation"""
    
    # Custom OpenAPI schema
    app.openapi = lambda: create_openapi_schema(app)
    
    # HTML documentation endpoint
    @app.get("/api-docs", response_class=HTMLResponse)
    async def get_api_docs():
        """Get comprehensive HTML API documentation"""
        return create_api_documentation_html()
    
    # API overview endpoint
    @app.get("/api/overview")
    async def get_api_overview():
        """Get API overview and statistics"""
        return {
            "title": "GRC Platform API",
            "version": "2.0.0",
            "description": "Comprehensive Governance, Risk & Compliance Management API",
            "features": [
                "Multi-Framework Compliance Management",
                "AI-Powered Risk Assessment",
                "Real-time Monitoring & Alerting",
                "Workflow Automation",
                "Advanced Analytics & Reporting",
                "Machine Learning Enhanced AI"
            ],
            "endpoints": {
                "authentication": "/api/v1/auth/",
                "users": "/api/v1/users/",
                "policies": "/api/v1/policies/",
                "workflows": "/api/v1/workflows/",
                "bfsi_ai": "/api/v1/bfsi-ai/",
                "analytics": "/api/v1/analytics/",
                "monitoring": "/api/v1/monitoring/",
                "workflow_automation": "/api/v1/workflow-automation/",
                "compliance_frameworks": "/api/v1/compliance-frameworks/",
                "ml_ai": "/api/v1/ml-ai/"
            },
            "documentation": {
                "swagger_ui": "/docs",
                "redoc": "/redoc",
                "openapi_json": "/openapi.json",
                "html_docs": "/api-docs"
            },
            "authentication": {
                "type": "JWT Bearer Token",
                "header": "Authorization: Bearer <token>"
            },
            "rate_limits": {
                "standard": "1000 requests/hour",
                "ai_ml": "100 requests/hour",
                "analytics": "500 requests/hour"
            }
        }
    
    logger.info("API documentation setup completed")
