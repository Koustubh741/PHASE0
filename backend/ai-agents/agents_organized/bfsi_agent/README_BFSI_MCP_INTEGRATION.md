# BFSI MCP Integration Documentation

## Overview

This documentation provides a comprehensive guide to the BFSI (Banking, Financial Services, Insurance) MCP (Management Communication Protocol) integration system. The system enables coordinated multi-agent GRC (Governance, Risk, and Compliance) operations through intelligent agent communication, task delegation, and workflow orchestration.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Quick Start Guide](#quick-start-guide)
3. [Agent Types and Capabilities](#agent-types-and-capabilities)
4. [MCP Protocol Details](#mcp-protocol-details)
5. [Workflow Orchestration](#workflow-orchestration)
6. [API Endpoints](#api-endpoints)
7. [Usage Examples](#usage-examples)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)
10. [Performance Optimization](#performance-optimization)

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    BFSI MCP Integration System                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  MCP Broker     │  │  Orchestrator   │  │  API Gateway    │  │
│  │  (Communication)│  │  (Coordination) │  │  (REST API)     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ Compliance  │ │ Risk        │ │ AML         │ │ Fraud       │ │
│  │ Coordinator │ │ Analyzer    │ │ Analyzer    │ │ Detection   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Enhanced Hugging Face Service                  │ │
│  │           (Multi-LLM Support & Local Processing)           │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Key Features

- **Multi-Agent Coordination**: Seamless communication between specialized BFSI agents
- **Intelligent Task Routing**: Automatic task delegation based on agent capabilities
- **Real-time Collaboration**: Live inter-agent collaboration for complex workflows
- **Workflow Orchestration**: Structured multi-step GRC processes
- **Performance Monitoring**: Comprehensive metrics and health tracking
- **Fault Tolerance**: Error handling and recovery mechanisms
- **Scalability**: Dynamic agent registration and load balancing

## Quick Start Guide

### 1. Prerequisites

```bash
# Ensure Redis is running (optional, system works without Redis)
redis-server

# Install required dependencies
pip install -r requirements_huggingface_local.txt
```

### 2. Start the Enhanced Service

```bash
# Start the enhanced Hugging Face service with multi-LLM support
python backend/ai-agents/agents_organized/applications/enhanced_huggingface_service.py

# Start the main application with MCP integration
python backend/ai-agents/agents_organized/applications/main.py
```

### 3. Verify Installation

```bash
# Check MCP status
curl http://localhost:8000/mcp/status

# Check agent status
curl http://localhost:8000/agents/status
```

### Expected Response

```json
{
  "mcp_broker_status": "active",
  "registered_agents": [
    "bfsi-compliance-001",
    "bfsi-risk-001", 
    "bfsi-aml-001",
    "bfsi-fraud-001"
  ],
  "is_listening": true,
  "total_agents": 4,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Agent Types and Capabilities

### 1. Compliance Coordinator (`bfsi-compliance-001`)

**Capabilities:**
- Regulatory compliance monitoring
- Policy management
- Compliance reporting
- Audit coordination

**Message Types:**
- `compliance_check`
- `regulatory_update`
- `policy_review`
- `audit_preparation`

**Example Usage:**
```python
# Send compliance check request
message = {
    "message_id": "comp_check_001",
    "timestamp": "2024-01-15T10:30:00Z",
    "source_agent": "api_client",
    "message_type": "compliance_check",
    "priority": "high",
    "payload": {
        "context": {
            "regulation": "GDPR",
            "entity": "customer_data_processing",
            "scope": "data_protection"
        }
    }
}

response = await compliance_agent.process_message(message)
```

### 2. Risk Analyzer (`bfsi-risk-001`)

**Capabilities:**
- Risk assessment
- Stress testing
- Risk modeling
- Portfolio analysis

**Message Types:**
- `risk_assessment`
- `stress_test`
- `portfolio_analysis`
- `risk_monitoring`

**Example Usage:**
```python
# Perform risk assessment
task = {
    "task_type": "risk_assessment",
    "context": {
        "portfolio_id": "port_001",
        "risk_categories": ["market", "credit", "operational"],
        "time_horizon": "1_year"
    },
    "priority": "high"
}

result = await risk_agent.execute_task(task)
```

### 3. AML Analyzer (`bfsi-aml-001`)

**Capabilities:**
- AML screening
- Transaction monitoring
- Suspicious activity reporting
- Sanctions screening

**Message Types:**
- `aml_analysis`
- `transaction_monitoring`
- `suspicious_activity_analysis`
- `sanctions_check`

**Example Usage:**
```python
# AML screening request
message = {
    "message_id": "aml_001",
    "timestamp": "2024-01-15T10:30:00Z",
    "source_agent": "transaction_system",
    "message_type": "aml_analysis",
    "priority": "high",
    "payload": {
        "context": {
            "customer_id": "cust_001",
            "transaction_amount": 50000,
            "transaction_type": "wire_transfer",
            "destination_country": "high_risk_jurisdiction"
        }
    }
}

response = await aml_agent.process_message(message)
```

### 4. Fraud Detection (`bfsi-fraud-001`)

**Capabilities:**
- Pattern recognition
- Anomaly detection
- Behavioral analysis
- Real-time monitoring

**Message Types:**
- `fraud_detection`
- `pattern_analysis`
- `anomaly_detection`
- `behavioral_analysis`

**Example Usage:**
```python
# Fraud detection request
task = {
    "task_type": "fraud_detection",
    "context": {
        "transaction_id": "txn_001",
        "behavioral_data": {
            "login_time": "03:00",
            "location": "unusual_country",
            "device_fingerprint": "new_device"
        },
        "risk_indicators": ["unusual_pattern", "high_velocity"]
    },
    "priority": "critical"
}

result = await fraud_agent.execute_task(task)
```

## MCP Protocol Details

### Message Structure

```json
{
  "header": {
    "message_id": "uuid4",
    "timestamp": "ISO 8601",
    "source_agent": "agent_id",
    "destination_agent": "target_agent_id",
    "message_type": "message_type",
    "priority": "critical|high|medium|low",
    "correlation_id": "optional_correlation_id",
    "reply_to": "optional_reply_agent",
    "ttl": 3600,
    "encryption_required": false,
    "signature": "optional_signature"
  },
  "payload": {
    "data": {},
    "metadata": {}
  }
}
```

### Message Types

| Message Type | Description | Priority | Use Case |
|-------------|-------------|----------|----------|
| `compliance_check` | Compliance verification | High | Regulatory compliance |
| `risk_assessment` | Risk evaluation | Medium-High | Portfolio analysis |
| `aml_analysis` | AML screening | High | Transaction monitoring |
| `fraud_detection` | Fraud identification | Critical | Real-time fraud detection |
| `task_delegation` | Task assignment | Medium | Workflow coordination |
| `collaboration_request` | Inter-agent collaboration | Medium | Complex analysis |
| `heartbeat` | Health monitoring | Low | System health |
| `alert_notification` | System alerts | High-Critical | Incident response |

### Priority Levels

- **Critical**: Immediate attention required (fraud detection, security breaches)
- **High**: Urgent but not immediate (compliance violations, high-risk transactions)
- **Medium**: Standard priority (routine assessments, regular monitoring)
- **Low**: Can be deferred (maintenance, reporting)

## Workflow Orchestration

### Workflow Types

#### 1. Compliance Audit Workflow

```python
# Create compliance audit workflow
workflow_id = await orchestrator.create_workflow(
    WorkflowType.COMPLIANCE_AUDIT,
    {
        "entity": "financial_institution",
        "regulation": "GDPR",
        "scope": "data_protection"
    }
)

# Execute workflow
result = await orchestrator.execute_workflow(workflow_id)
```

**Workflow Steps:**
1. **Compliance Check** (Compliance Coordinator)
2. **Risk Assessment** (Risk Analyzer) - depends on step 1
3. **Regulatory Reporting** (Compliance Coordinator) - depends on steps 1, 2

#### 2. Fraud Investigation Workflow

```python
# Create fraud investigation workflow
workflow_id = await orchestrator.create_workflow(
    WorkflowType.FRAUD_INVESTIGATION,
    {
        "transaction_id": "suspicious_txn_001",
        "customer_id": "cust_001",
        "amount": 100000,
        "flags": ["unusual_pattern", "high_risk_location"]
    }
)

# Execute workflow
result = await orchestrator.execute_workflow(workflow_id)
```

**Workflow Steps:**
1. **Fraud Detection** (Fraud Detection) - Critical priority
2. **AML Analysis** (AML Analyzer) - depends on step 1
3. **Compliance Review** (Compliance Coordinator) - depends on steps 1, 2

#### 3. Risk Assessment Workflow

```python
# Create risk assessment workflow
workflow_id = await orchestrator.create_workflow(
    WorkflowType.RISK_ASSESSMENT,
    {
        "portfolio_id": "port_001",
        "risk_categories": ["market", "credit", "operational"]
    }
)

# Execute workflow
result = await orchestrator.execute_workflow(workflow_id)
```

**Workflow Steps:**
1. **Risk Analysis** (Risk Analyzer)
2. **Capital Adequacy Check** (Capital Adequacy) - depends on step 1

### Workflow Execution Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Create        │───▶│   Execute       │───▶│   Monitor       │
│   Workflow      │    │   Steps         │    │   Progress      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Define        │    │   Route Tasks   │    │   Collect       │
│   Dependencies  │    │   to Agents     │    │   Results       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## API Endpoints

### MCP Status Endpoints

#### GET `/mcp/status`
Get MCP broker and agent communication status.

**Response:**
```json
{
  "mcp_broker_status": "active",
  "registered_agents": ["bfsi-compliance-001", "bfsi-risk-001", "bfsi-aml-001", "bfsi-fraud-001"],
  "is_listening": true,
  "total_agents": 4,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### GET `/mcp/agents`
Get detailed information about all MCP-enabled agents.

**Response:**
```json
{
  "agents": [
    {
      "agent_id": "bfsi-compliance-001",
      "name": "MCP Compliance Coordinator",
      "agent_type": "compliance",
      "status": "active",
      "health_status": "healthy",
      "capabilities": ["regulatory_compliance_monitoring", "policy_management"],
      "performance_metrics": {
        "tasks_completed": 25,
        "tasks_failed": 1,
        "avg_response_time": 2.5
      }
    }
  ],
  "total": 4,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Message Endpoints

#### POST `/mcp/message`
Send a message via MCP protocol.

**Request:**
```json
{
  "message_id": "msg_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "source_agent": "api_client",
  "destination_agent": "bfsi-compliance-001",
  "message_type": "compliance_check",
  "priority": "high",
  "payload": {
    "context": {
      "regulation": "GDPR",
      "entity": "customer_data"
    }
  }
}
```

**Response:**
```json
{
  "status": "sent",
  "message_id": "msg_001",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### POST `/mcp/broadcast`
Broadcast a message to all MCP agents.

**Request:**
```json
{
  "message_type": "alert_notification",
  "priority": "critical",
  "payload": {
    "alert_type": "security_breach",
    "message": "Unauthorized access detected",
    "context": {
      "system": "core_banking",
      "severity": "critical"
    }
  }
}
```

**Response:**
```json
{
  "status": "broadcasted",
  "message_id": "broadcast_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "target_agents": ["bfsi-compliance-001", "bfsi-risk-001", "bfsi-aml-001", "bfsi-fraud-001"]
}
```

### Agent Management Endpoints

#### GET `/mcp/agent/{agent_id}/health`
Get detailed health status of a specific MCP agent.

**Response:**
```json
{
  "agent_id": "bfsi-compliance-001",
  "name": "MCP Compliance Coordinator",
  "agent_type": "compliance",
  "status": "active",
  "health_status": "healthy",
  "last_heartbeat": "2024-01-15T10:30:00Z",
  "last_activity": "2024-01-15T10:29:45Z",
  "capabilities": ["regulatory_compliance_monitoring", "policy_management"],
  "current_tasks_count": 2,
  "collaboration_partners": ["bfsi-risk-001", "bfsi-aml-001"],
  "performance_metrics": {
    "tasks_completed": 25,
    "tasks_failed": 1,
    "avg_response_time": 2.5
  }
}
```

#### POST `/mcp/agent/{agent_id}/task`
Delegate a task to a specific MCP agent.

**Request:**
```json
{
  "task_type": "compliance_check",
  "context": {
    "regulation": "SOX",
    "entity": "financial_reporting"
  },
  "priority": "high"
}
```

**Response:**
```json
{
  "status": "completed",
  "agent_id": "bfsi-compliance-001",
  "result": {
    "compliance_score": 92,
    "violations_found": 1,
    "recommendations": ["update_policy_doc_001"]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Usage Examples

### Example 1: Simple Compliance Check

```python
import httpx
import asyncio

async def perform_compliance_check():
    async with httpx.AsyncClient() as client:
        # Send compliance check message
        message = {
            "message_id": "comp_check_001",
            "timestamp": "2024-01-15T10:30:00Z",
            "source_agent": "external_system",
            "destination_agent": "bfsi-compliance-001",
            "message_type": "compliance_check",
            "priority": "high",
            "payload": {
                "context": {
                    "regulation": "GDPR",
                    "entity": "customer_data_processing",
                    "scope": "data_protection_compliance"
                }
            }
        }
        
        response = await client.post(
            "http://localhost:8000/mcp/message",
            json=message
        )
        
        print(f"Compliance check response: {response.json()}")

# Run the example
asyncio.run(perform_compliance_check())
```

### Example 2: Complex Fraud Investigation Workflow

```python
import httpx
import asyncio
import uuid

async def run_fraud_investigation():
    async with httpx.AsyncClient() as client:
        # Create fraud investigation workflow
        workflow_context = {
            "transaction_id": "txn_001",
            "customer_id": "cust_001",
            "amount": 100000,
            "flags": ["unusual_pattern", "high_risk_location"],
            "timestamp": "2024-01-15T10:30:00Z"
        }
        
        # Create workflow via orchestrator
        workflow_response = await client.post(
            "http://localhost:8000/orchestrator/workflow/create",
            json={
                "workflow_type": "fraud_investigation",
                "context": workflow_context
            }
        )
        
        workflow_id = workflow_response.json()["workflow_id"]
        print(f"Created workflow: {workflow_id}")
        
        # Execute workflow
        execution_response = await client.post(
            f"http://localhost:8000/orchestrator/workflow/{workflow_id}/execute"
        )
        
        result = execution_response.json()
        print(f"Workflow execution result: {result}")
        
        # Monitor workflow progress
        status_response = await client.get(
            f"http://localhost:8000/orchestrator/workflow/{workflow_id}/status"
        )
        
        status = status_response.json()
        print(f"Workflow status: {status}")

# Run the example
asyncio.run(run_fraud_investigation())
```

### Example 3: Inter-Agent Collaboration

```python
import httpx
import asyncio

async def coordinate_risk_analysis():
    async with httpx.AsyncClient() as client:
        # Request collaboration between agents
        collaboration_request = {
            "collaboration_type": "comprehensive_risk_analysis",
            "context": {
                "portfolio_id": "port_001",
                "analysis_scope": "full_portfolio",
                "risk_categories": ["market", "credit", "operational", "liquidity"]
            }
        }
        
        response = await client.post(
            "http://localhost:8000/orchestrator/collaborate",
            json={
                "requesting_agent": "bfsi-risk-001",
                **collaboration_request
            }
        )
        
        result = response.json()
        print(f"Collaboration initiated: {result}")
        
        # Wait for collaboration results
        await asyncio.sleep(5)
        
        # Check collaboration status
        status_response = await client.get(
            "http://localhost:8000/orchestrator/collaboration/status"
        )
        
        status = status_response.json()
        print(f"Collaboration status: {status}")

# Run the example
asyncio.run(coordinate_risk_analysis())
```

### Example 4: Real-time Monitoring

```python
import httpx
import asyncio
import time

async def monitor_agents():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                # Get agent status
                response = await client.get("http://localhost:8000/agents/status")
                status = response.json()
                
                print(f"Agent Status at {time.strftime('%H:%M:%S')}:")
                for agent_id, agent_status in status["agents"].items():
                    print(f"  {agent_id}: {agent_status['status']} - {agent_status.get('health_status', 'unknown')}")
                
                # Get MCP broker status
                mcp_response = await client.get("http://localhost:8000/mcp/status")
                mcp_status = mcp_response.json()
                print(f"  MCP Broker: {mcp_status['mcp_broker_status']} - {len(mcp_status['registered_agents'])} agents")
                
                print("-" * 50)
                
                # Wait 30 seconds before next check
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(10)

# Run the example
asyncio.run(monitor_agents())
```

## Testing

### Running Tests

```bash
# Run all BFSI MCP integration tests
python -m pytest backend/ai-agents/agents_organized/bfsi_agent/test_bfsi_mcp_integration.py -v

# Run specific test categories
python -m pytest backend/ai-agents/agents_organized/bfsi_agent/test_bfsi_mcp_integration.py::TestAgentRegistration -v
python -m pytest backend/ai-agents/agents_organized/bfsi_agent/test_bfsi_mcp_integration.py::TestMessageHandling -v
python -m pytest backend/ai-agents/agents_organized/bfsi_agent/test_bfsi_mcp_integration.py::TestOrchestrator -v

# Run integration tests
python backend/ai-agents/agents_organized/bfsi_agent/test_bfsi_mcp_integration.py
```

### Test Coverage

The test suite covers:

- **Agent Registration**: Agent creation, initialization, and capabilities
- **Message Handling**: MCP message processing and routing
- **Task Execution**: Individual agent task processing
- **Collaboration**: Inter-agent collaboration and coordination
- **Workflow Orchestration**: Multi-step workflow execution
- **Performance Monitoring**: Health checks and metrics tracking
- **Error Handling**: Failure scenarios and recovery
- **Integration**: End-to-end workflow testing

### Manual Testing

```bash
# Test MCP status
curl http://localhost:8000/mcp/status

# Test agent health
curl http://localhost:8000/mcp/agent/bfsi-compliance-001/health

# Test message sending
curl -X POST http://localhost:8000/mcp/message \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "test_001",
    "timestamp": "2024-01-15T10:30:00Z",
    "source_agent": "test_client",
    "destination_agent": "bfsi-compliance-001",
    "message_type": "compliance_check",
    "priority": "medium",
    "payload": {
      "context": {
        "regulation": "GDPR",
        "entity": "test_entity"
      }
    }
  }'

# Test task delegation
curl -X POST http://localhost:8000/mcp/agent/bfsi-risk-001/task \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "risk_assessment",
    "context": {
      "portfolio_id": "test_portfolio",
      "risk_categories": ["market", "credit"]
    },
    "priority": "high"
  }'
```

## Troubleshooting

### Common Issues

#### 1. Agent Registration Failed

**Error:** `❌ Failed to register BFSI Agent bfsi-compliance-001`

**Solution:**
```bash
# Check if Redis is running (optional)
redis-cli ping

# Check agent logs
tail -f logs/bfsi_agents.log

# Restart the service
python backend/ai-agents/agents_organized/applications/main.py
```

#### 2. MCP Broker Not Available

**Error:** `MCP broker not available`

**Solution:**
```bash
# Check if main application is running
curl http://localhost:8000/health

# Check MCP broker status
curl http://localhost:8000/mcp/status

# Restart with proper initialization
python backend/ai-agents/agents_organized/applications/main.py
```

#### 3. Agent Communication Timeout

**Error:** `Message timeout or agent not responding`

**Solution:**
```bash
# Check agent health status
curl http://localhost:8000/mcp/agent/bfsi-compliance-001/health

# Check agent logs
tail -f logs/bfsi_agents.log

# Restart specific agent
curl -X POST http://localhost:8000/mcp/agent/bfsi-compliance-001/restart
```

#### 4. Workflow Execution Failed

**Error:** `Workflow execution failed`

**Solution:**
```bash
# Check workflow status
curl http://localhost:8000/orchestrator/workflow/{workflow_id}/status

# Check agent capabilities
curl http://localhost:8000/mcp/agents

# Check orchestrator logs
tail -f logs/orchestrator.log
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug output
python backend/ai-agents/agents_organized/applications/main.py --debug
```

### Health Checks

```bash
# Comprehensive health check
curl http://localhost:8000/health

# Agent-specific health check
curl http://localhost:8000/mcp/agent/bfsi-compliance-001/health

# System-wide status
curl http://localhost:8000/agents/status
```

## Performance Optimization

### Agent Performance

1. **Resource Allocation:**
   - Ensure adequate CPU and memory for each agent
   - Monitor agent response times
   - Implement agent-specific resource limits

2. **Message Optimization:**
   - Use appropriate message priorities
   - Implement message batching for bulk operations
   - Optimize message payload sizes

3. **Workflow Optimization:**
   - Minimize workflow dependencies
   - Use parallel execution where possible
   - Implement workflow caching for repeated operations

### System Scaling

1. **Horizontal Scaling:**
   - Add more agent instances
   - Implement load balancing
   - Use distributed MCP brokers

2. **Vertical Scaling:**
   - Increase server resources
   - Optimize database connections
   - Implement connection pooling

### Monitoring and Metrics

```python
# Custom performance monitoring
import time
import asyncio

async def monitor_performance():
    while True:
        # Get performance metrics
        response = await httpx.get("http://localhost:8000/mcp/agents")
        agents = response.json()["agents"]
        
        for agent in agents:
            metrics = agent.get("performance_metrics", {})
            print(f"{agent['agent_id']}: {metrics.get('avg_response_time', 0):.2f}s avg response time")
        
        await asyncio.sleep(60)  # Monitor every minute
```

## Conclusion

The BFSI MCP Integration system provides a robust, scalable solution for coordinated multi-agent GRC operations. With its comprehensive agent capabilities, intelligent workflow orchestration, and real-time monitoring, it enables financial institutions to maintain compliance, manage risks, and detect fraud more effectively than ever before.

For additional support or questions, please refer to the system logs or contact the development team.
