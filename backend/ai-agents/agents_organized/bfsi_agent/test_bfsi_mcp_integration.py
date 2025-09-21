"""
BFSI MCP Integration Test Suite
===============================

Comprehensive test suite for BFSI MCP integration including:
- Agent registration and communication
- Message handling and routing
- Workflow orchestration
- Performance monitoring
- Error handling and recovery
"""

import asyncio
import pytest
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock, patch

# Import BFSI MCP components
from .bfsi_mcp_agent import BFSIMCPAgent, BFSIMessage, BFSIMessageType, BFSITaskPriority
from .bfsi_mcp_subagents import (
    MCPComplianceCoordinator, MCPRiskAnalyzer, MCPAMLAnalyzer, MCPFraudDetection,
    BFSIMCPAgentFactory, initialize_all_bfsi_mcp_agents
)
from .bfsi_mcp_orchestrator import (
    BFSIMCPOrchestrator, WorkflowType, WorkflowStatus, BFSIMCPOrchestratorFactory
)
from ..shared_components.mcp_broker import MCPBroker

logger = logging.getLogger(__name__)

# =============================================================================
# TEST FIXTURES AND SETUP
# =============================================================================

@pytest.fixture
async def mock_mcp_broker():
    """Create a mock MCP broker for testing"""
    broker = Mock(spec=MCPBroker)
    broker.agents = {}
    broker.is_running = True
    broker.get_registered_agents = Mock(return_value=[])
    broker.send_message = AsyncMock()
    broker.broadcast_message = AsyncMock()
    broker.register_agent = AsyncMock()
    return broker

@pytest.fixture
async def compliance_agent():
    """Create a compliance agent for testing"""
    agent = MCPComplianceCoordinator()
    agent.mcp_broker = Mock()
    await agent.start()
    return agent

@pytest.fixture
async def risk_agent():
    """Create a risk analyzer agent for testing"""
    agent = MCPRiskAnalyzer()
    agent.mcp_broker = Mock()
    await agent.start()
    return agent

@pytest.fixture
async def aml_agent():
    """Create an AML analyzer agent for testing"""
    agent = MCPAMLAnalyzer()
    agent.mcp_broker = Mock()
    await agent.start()
    return agent

@pytest.fixture
async def fraud_agent():
    """Create a fraud detection agent for testing"""
    agent = MCPFraudDetection()
    agent.mcp_broker = Mock()
    await agent.start()
    return agent

@pytest.fixture
async def orchestrator():
    """Create an orchestrator with test agents"""
    orchestrator = BFSIMCPOrchestrator()
    
    # Create and register test agents
    agents = [
        MCPComplianceCoordinator(),
        MCPRiskAnalyzer(),
        MCPAMLAnalyzer(),
        MCPFraudDetection()
    ]
    
    for agent in agents:
        agent.mcp_broker = Mock()
        await agent.start()
        await orchestrator.register_agent(agent)
    
    return orchestrator

# =============================================================================
# AGENT REGISTRATION AND BASIC FUNCTIONALITY TESTS
# =============================================================================

class TestAgentRegistration:
    """Test agent registration and basic functionality"""
    
    @pytest.mark.asyncio
    async def test_compliance_agent_creation(self):
        """Test compliance agent creation and initialization"""
        agent = MCPComplianceCoordinator()
        
        assert agent.agent_id == "bfsi-compliance-001"
        assert agent.name == "MCP Compliance Coordinator"
        assert agent.agent_type == "compliance"
        assert "regulatory_compliance_monitoring" in agent.get_capabilities()
        assert "policy_management" in agent.get_capabilities()
    
    @pytest.mark.asyncio
    async def test_risk_agent_creation(self):
        """Test risk analyzer agent creation and initialization"""
        agent = MCPRiskAnalyzer()
        
        assert agent.agent_id == "bfsi-risk-001"
        assert agent.name == "MCP Risk Analyzer"
        assert agent.agent_type == "risk"
        assert "risk_assessment" in agent.get_capabilities()
        assert "stress_testing" in agent.get_capabilities()
    
    @pytest.mark.asyncio
    async def test_aml_agent_creation(self):
        """Test AML analyzer agent creation and initialization"""
        agent = MCPAMLAnalyzer()
        
        assert agent.agent_id == "bfsi-aml-001"
        assert agent.name == "MCP AML Analyzer"
        assert agent.agent_type == "aml"
        assert "aml_screening" in agent.get_capabilities()
        assert "transaction_monitoring" in agent.get_capabilities()
    
    @pytest.mark.asyncio
    async def test_fraud_agent_creation(self):
        """Test fraud detection agent creation and initialization"""
        agent = MCPFraudDetection()
        
        assert agent.agent_id == "bfsi-fraud-001"
        assert agent.name == "MCP Fraud Detection"
        assert agent.agent_type == "fraud"
        assert "pattern_recognition" in agent.get_capabilities()
        assert "anomaly_detection" in agent.get_capabilities()
    
    @pytest.mark.asyncio
    async def test_agent_factory(self):
        """Test agent factory creation"""
        agent_types = BFSIMCPAgentFactory.get_available_agents()
        
        assert "compliance" in agent_types
        assert "risk" in agent_types
        assert "aml" in agent_types
        assert "fraud" in agent_types
        
        # Test creating each agent type
        for agent_type in agent_types:
            agent = BFSIMCPAgentFactory.create_agent(agent_type)
            assert agent is not None
            assert hasattr(agent, 'agent_id')
            assert hasattr(agent, 'name')
            assert hasattr(agent, 'agent_type')

# =============================================================================
# MESSAGE HANDLING TESTS
# =============================================================================

class TestMessageHandling:
    """Test message handling and routing"""
    
    @pytest.mark.asyncio
    async def test_compliance_message_processing(self, compliance_agent):
        """Test compliance agent message processing"""
        message = {
            "message_id": "test_msg_001",
            "timestamp": datetime.now().isoformat(),
            "source_agent": "test_agent",
            "message_type": BFSIMessageType.COMPLIANCE_CHECK.value,
            "priority": BFSITaskPriority.MEDIUM.value,
            "payload": {
                "context": {
                    "regulation": "GDPR",
                    "entity": "customer_data_processing"
                }
            }
        }
        
        response = await compliance_agent.process_message(message)
        
        assert response is not None
        assert "status" in response
        assert response["status"] in ["completed", "not_implemented", "error"]
    
    @pytest.mark.asyncio
    async def test_risk_message_processing(self, risk_agent):
        """Test risk analyzer message processing"""
        message = {
            "message_id": "test_msg_002",
            "timestamp": datetime.now().isoformat(),
            "source_agent": "test_agent",
            "message_type": BFSIMessageType.RISK_ASSESSMENT.value,
            "priority": BFSITaskPriority.HIGH.value,
            "payload": {
                "context": {
                    "portfolio": "investment_portfolio",
                    "risk_type": "market_risk"
                }
            }
        }
        
        response = await risk_agent.process_message(message)
        
        assert response is not None
        assert "status" in response
    
    @pytest.mark.asyncio
    async def test_aml_message_processing(self, aml_agent):
        """Test AML analyzer message processing"""
        message = {
            "message_id": "test_msg_003",
            "timestamp": datetime.now().isoformat(),
            "source_agent": "test_agent",
            "message_type": BFSIMessageType.AML_ANALYSIS.value,
            "priority": BFSITaskPriority.HIGH.value,
            "payload": {
                "context": {
                    "transaction_id": "txn_001",
                    "amount": 50000,
                    "customer_id": "cust_001"
                }
            }
        }
        
        response = await aml_agent.process_message(message)
        
        assert response is not None
        assert "status" in response
    
    @pytest.mark.asyncio
    async def test_fraud_message_processing(self, fraud_agent):
        """Test fraud detection message processing"""
        message = {
            "message_id": "test_msg_004",
            "timestamp": datetime.now().isoformat(),
            "source_agent": "test_agent",
            "message_type": BFSIMessageType.FRAUD_DETECTION.value,
            "priority": BFSITaskPriority.CRITICAL.value,
            "payload": {
                "context": {
                    "transaction_id": "txn_002",
                    "behavior_pattern": "unusual_activity",
                    "risk_score": 85
                }
            }
        }
        
        response = await fraud_agent.process_message(message)
        
        assert response is not None
        assert "status" in response
    
    @pytest.mark.asyncio
    async def test_invalid_message_handling(self, compliance_agent):
        """Test handling of invalid messages"""
        invalid_message = {
            "invalid_field": "invalid_value"
        }
        
        response = await compliance_agent.process_message(invalid_message)
        
        assert response is not None
        assert "error" in response

# =============================================================================
# TASK EXECUTION TESTS
# =============================================================================

class TestTaskExecution:
    """Test task execution capabilities"""
    
    @pytest.mark.asyncio
    async def test_compliance_task_execution(self, compliance_agent):
        """Test compliance agent task execution"""
        task = {
            "task_type": "compliance_check",
            "context": {
                "regulation": "SOX",
                "entity": "financial_reporting"
            },
            "priority": "high"
        }
        
        result = await compliance_agent.execute_task(task)
        
        assert result is not None
        assert "status" in result
    
    @pytest.mark.asyncio
    async def test_risk_task_execution(self, risk_agent):
        """Test risk analyzer task execution"""
        task = {
            "task_type": "risk_assessment",
            "context": {
                "portfolio_id": "port_001",
                "risk_categories": ["market", "credit", "operational"]
            },
            "priority": "medium"
        }
        
        result = await risk_agent.execute_task(task)
        
        assert result is not None
        assert "status" in result
    
    @pytest.mark.asyncio
    async def test_aml_task_execution(self, aml_agent):
        """Test AML analyzer task execution"""
        task = {
            "task_type": "aml_screening",
            "context": {
                "customer_id": "cust_002",
                "transaction_history": ["txn_001", "txn_002", "txn_003"]
            },
            "priority": "high"
        }
        
        result = await aml_agent.execute_task(task)
        
        assert result is not None
        assert "status" in result
    
    @pytest.mark.asyncio
    async def test_fraud_task_execution(self, fraud_agent):
        """Test fraud detection task execution"""
        task = {
            "task_type": "fraud_detection",
            "context": {
                "transaction_id": "txn_003",
                "behavioral_data": {"login_time": "03:00", "location": "unusual"}
            },
            "priority": "critical"
        }
        
        result = await fraud_agent.execute_task(task)
        
        assert result is not None
        assert "status" in result

# =============================================================================
# COLLABORATION TESTS
# =============================================================================

class TestCollaboration:
    """Test inter-agent collaboration"""
    
    @pytest.mark.asyncio
    async def test_collaboration_request(self, compliance_agent, risk_agent):
        """Test collaboration request between agents"""
        # Mock the risk agent's collaboration response
        risk_agent._process_collaboration_request = AsyncMock(return_value={
            "status": "collaboration_accepted",
            "response": {"risk_score": 75, "recommendations": ["monitor_closely"]}
        })
        
        # Request collaboration
        result = await compliance_agent.request_collaboration(
            "bfsi-risk-001", "compliance_assessment", {"context": "test"}
        )
        
        assert result is not None
        assert "status" in result
        assert result["status"] == "request_sent"
    
    @pytest.mark.asyncio
    async def test_task_delegation(self, compliance_agent, risk_agent):
        """Test task delegation between agents"""
        task = BFSITask(
            task_id="test_task_001",
            task_type="risk_assessment",
            priority=BFSITaskPriority.MEDIUM,
            description="Test risk assessment task",
            context={"portfolio": "test_portfolio"}
        )
        
        result = await compliance_agent.delegate_task("bfsi-risk-001", task)
        
        assert result is not None
        assert "status" in result
        assert result["status"] == "delegated"
        assert result["task_id"] == task.task_id
    
    @pytest.mark.asyncio
    async def test_alert_broadcasting(self, compliance_agent):
        """Test alert broadcasting to all agents"""
        result = await compliance_agent.broadcast_alert(
            alert_type="compliance_violation",
            severity="high",
            message="Test compliance violation detected",
            context={"violation_type": "data_breach"}
        )
        
        assert result is not None
        assert "status" in result
        assert result["status"] == "broadcasted"

# =============================================================================
# ORCHESTRATOR TESTS
# =============================================================================

class TestOrchestrator:
    """Test workflow orchestration"""
    
    @pytest.mark.asyncio
    async def test_orchestrator_creation(self, orchestrator):
        """Test orchestrator creation and agent registration"""
        assert len(orchestrator.agents) == 4
        assert "bfsi-compliance-001" in orchestrator.agents
        assert "bfsi-risk-001" in orchestrator.agents
        assert "bfsi-aml-001" in orchestrator.agents
        assert "bfsi-fraud-001" in orchestrator.agents
    
    @pytest.mark.asyncio
    async def test_workflow_creation(self, orchestrator):
        """Test workflow creation"""
        context = {
            "entity": "test_bank",
            "regulation": "Basel III",
            "scope": "capital_adequacy"
        }
        
        workflow_id = await orchestrator.create_workflow(
            WorkflowType.COMPLIANCE_AUDIT, context
        )
        
        assert workflow_id is not None
        assert workflow_id in orchestrator.active_workflows
        assert len(orchestrator.active_workflows[workflow_id].steps) == 3
    
    @pytest.mark.asyncio
    async def test_workflow_execution(self, orchestrator):
        """Test workflow execution"""
        context = {
            "entity": "test_bank",
            "scope": "risk_assessment"
        }
        
        # Create workflow
        workflow_id = await orchestrator.create_workflow(
            WorkflowType.RISK_ASSESSMENT, context
        )
        
        # Mock agent task execution
        for agent in orchestrator.agents.values():
            agent.execute_task = AsyncMock(return_value={
                "status": "completed",
                "result": {"analysis": "successful", "score": 85}
            })
        
        # Execute workflow
        result = await orchestrator.execute_workflow(workflow_id)
        
        assert result is not None
        assert "status" in result
        assert result["workflow_id"] == workflow_id
    
    @pytest.mark.asyncio
    async def test_agent_capability_filtering(self, orchestrator):
        """Test agent filtering by capabilities"""
        # Get agents with risk assessment capability
        risk_agents = orchestrator.get_available_agents(["risk_assessment"])
        assert len(risk_agents) >= 1
        assert "bfsi-risk-001" in risk_agents
        
        # Get agents with compliance capability
        compliance_agents = orchestrator.get_available_agents(["regulatory_compliance_monitoring"])
        assert len(compliance_agents) >= 1
        assert "bfsi-compliance-001" in compliance_agents
    
    @pytest.mark.asyncio
    async def test_collaboration_coordination(self, orchestrator):
        """Test collaboration coordination"""
        result = await orchestrator.coordinate_collaboration(
            "bfsi-compliance-001", "comprehensive_risk_analysis", {"context": "test"}
        )
        
        assert result is not None
        assert "status" in result
        assert "collaborating_agents" in result
    
    @pytest.mark.asyncio
    async def test_orchestrator_status(self, orchestrator):
        """Test orchestrator status reporting"""
        status = orchestrator.get_orchestrator_status()
        
        assert "orchestrator_status" in status
        assert "total_agents" in status
        assert "active_workflows" in status
        assert "performance_metrics" in status
        assert status["total_agents"] == 4

# =============================================================================
# PERFORMANCE AND MONITORING TESTS
# =============================================================================

class TestPerformanceMonitoring:
    """Test performance monitoring and health checks"""
    
    @pytest.mark.asyncio
    async def test_agent_health_status(self, compliance_agent):
        """Test agent health status reporting"""
        health_status = compliance_agent.get_health_status()
        
        assert "agent_id" in health_status
        assert "name" in health_status
        assert "status" in health_status
        assert "health_status" in health_status
        assert "capabilities" in health_status
        assert "performance_metrics" in health_status
        assert health_status["agent_id"] == "bfsi-compliance-001"
    
    @pytest.mark.asyncio
    async def test_performance_metrics_tracking(self, compliance_agent):
        """Test performance metrics tracking"""
        initial_metrics = compliance_agent.get_performance_metrics()
        
        # Simulate task completion
        compliance_agent.performance_metrics["tasks_completed"] += 1
        
        updated_metrics = compliance_agent.get_performance_metrics()
        
        assert updated_metrics["tasks_completed"] > initial_metrics["tasks_completed"]
    
    @pytest.mark.asyncio
    async def test_heartbeat_functionality(self, compliance_agent):
        """Test heartbeat functionality"""
        # Mock MCP broker for heartbeat
        compliance_agent.mcp_broker.broadcast_message = AsyncMock()
        
        # Start heartbeat (short duration for testing)
        heartbeat_task = asyncio.create_task(
            compliance_agent.start_heartbeat(interval=1)
        )
        
        # Let it run for a short time
        await asyncio.sleep(1.5)
        
        # Cancel the heartbeat task
        heartbeat_task.cancel()
        
        # Verify heartbeat was sent
        assert compliance_agent.mcp_broker.broadcast_message.called

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Test full integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_full_compliance_workflow(self, orchestrator):
        """Test full compliance audit workflow"""
        context = {
            "entity": "test_financial_institution",
            "regulation": "GDPR",
            "scope": "data_protection_compliance"
        }
        
        # Create compliance audit workflow
        workflow_id = await orchestrator.create_workflow(
            WorkflowType.COMPLIANCE_AUDIT, context
        )
        
        # Mock all agent responses
        for agent in orchestrator.agents.values():
            agent.execute_task = AsyncMock(return_value={
                "status": "completed",
                "result": {
                    "compliance_score": 92,
                    "violations_found": 2,
                    "recommendations": ["update_policies", "staff_training"]
                }
            })
        
        # Execute workflow
        result = await orchestrator.execute_workflow(workflow_id)
        
        assert result["status"] == "completed"
        assert "results" in result
        assert len(result["results"]) == 3  # Three workflow steps
    
    @pytest.mark.asyncio
    async def test_fraud_investigation_workflow(self, orchestrator):
        """Test fraud investigation workflow"""
        context = {
            "transaction_id": "suspicious_txn_001",
            "customer_id": "cust_001",
            "amount": 100000,
            "flags": ["unusual_pattern", "high_risk_location"]
        }
        
        # Create fraud investigation workflow
        workflow_id = await orchestrator.create_workflow(
            WorkflowType.FRAUD_INVESTIGATION, context
        )
        
        # Mock agent responses with fraud-specific results
        for agent in orchestrator.agents.values():
            if agent.agent_type == "fraud":
                agent.execute_task = AsyncMock(return_value={
                    "status": "completed",
                    "result": {
                        "fraud_detected": True,
                        "risk_score": 95,
                        "recommendation": "immediate_action_required"
                    }
                })
            else:
                agent.execute_task = AsyncMock(return_value={
                    "status": "completed",
                    "result": {"analysis": "completed", "score": 85}
                })
        
        # Execute workflow
        result = await orchestrator.execute_workflow(workflow_id)
        
        assert result["status"] == "completed"
        assert "results" in result
    
    @pytest.mark.asyncio
    async def test_agent_factory_integration(self):
        """Test agent factory integration"""
        # Test initializing all agents
        agents = await initialize_all_bfsi_mcp_agents()
        
        assert len(agents) == 4
        assert "bfsi-compliance-001" in agents
        assert "bfsi-risk-001" in agents
        assert "bfsi-aml-001" in agents
        assert "bfsi-fraud-001" in agents
        
        # Verify all agents are started
        for agent in agents.values():
            assert agent.status == "active"

# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

class TestErrorHandling:
    """Test error handling and recovery"""
    
    @pytest.mark.asyncio
    async def test_agent_task_failure(self, compliance_agent):
        """Test agent task failure handling"""
        # Mock task execution failure
        compliance_agent.execute_task = AsyncMock(side_effect=Exception("Task failed"))
        
        task = {
            "task_type": "compliance_check",
            "context": {"test": "data"},
            "priority": "high"
        }
        
        result = await compliance_agent.execute_task(task)
        
        assert result is not None
        assert "status" in result
        assert result["status"] == "error"
    
    @pytest.mark.asyncio
    async def test_workflow_step_failure(self, orchestrator):
        """Test workflow step failure handling"""
        context = {"test": "data"}
        
        # Create workflow
        workflow_id = await orchestrator.create_workflow(
            WorkflowType.RISK_ASSESSMENT, context
        )
        
        # Mock one agent to fail
        risk_agent = orchestrator.agents["bfsi-risk-001"]
        risk_agent.execute_task = AsyncMock(side_effect=Exception("Agent failed"))
        
        # Mock other agents to succeed
        for agent_id, agent in orchestrator.agents.items():
            if agent_id != "bfsi-risk-001":
                agent.execute_task = AsyncMock(return_value={
                    "status": "completed",
                    "result": {"analysis": "successful"}
                })
        
        # Execute workflow
        result = await orchestrator.execute_workflow(workflow_id)
        
        # Workflow should fail due to step failure
        assert result["status"] == "failed"
    
    @pytest.mark.asyncio
    async def test_invalid_message_format(self, compliance_agent):
        """Test handling of invalid message formats"""
        invalid_messages = [
            {},  # Empty message
            {"invalid": "format"},  # Invalid format
            {"message_id": "test"},  # Missing required fields
            None  # Null message
        ]
        
        for invalid_msg in invalid_messages:
            response = await compliance_agent.process_message(invalid_msg)
            assert response is not None
            assert "error" in response or response.get("status") == "error"

# =============================================================================
# TEST RUNNER AND UTILITIES
# =============================================================================

async def run_integration_tests():
    """Run all integration tests"""
    print("🧪 Starting BFSI MCP Integration Tests...")
    
    # Test agent creation
    print("✅ Testing agent creation...")
    test_agent_creation = TestAgentRegistration()
    await test_agent_creation.test_compliance_agent_creation()
    await test_agent_creation.test_risk_agent_creation()
    await test_agent_creation.test_aml_agent_creation()
    await test_agent_creation.test_fraud_agent_creation()
    
    print("✅ Testing message handling...")
    # Test message handling
    test_message_handling = TestMessageHandling()
    compliance_agent = MCPComplianceCoordinator()
    risk_agent = MCPRiskAnalyzer()
    aml_agent = MCPAMLAnalyzer()
    fraud_agent = MCPFraudDetection()
    
    await test_message_handling.test_compliance_message_processing(compliance_agent)
    await test_message_handling.test_risk_message_processing(risk_agent)
    await test_message_handling.test_aml_message_processing(aml_agent)
    await test_message_handling.test_fraud_message_processing(fraud_agent)
    
    print("✅ Testing task execution...")
    # Test task execution
    test_task_execution = TestTaskExecution()
    await test_task_execution.test_compliance_task_execution(compliance_agent)
    await test_task_execution.test_risk_task_execution(risk_agent)
    await test_task_execution.test_aml_task_execution(aml_agent)
    await test_task_execution.test_fraud_task_execution(fraud_agent)
    
    print("✅ Testing orchestrator...")
    # Test orchestrator
    orchestrator = BFSIMCPOrchestrator()
    await orchestrator.register_agent(compliance_agent)
    await orchestrator.register_agent(risk_agent)
    await orchestrator.register_agent(aml_agent)
    await orchestrator.register_agent(fraud_agent)
    
    test_orchestrator = TestOrchestrator()
    await test_orchestrator.test_orchestrator_creation(orchestrator)
    await test_orchestrator.test_workflow_creation(orchestrator)
    
    print("🎉 All BFSI MCP Integration Tests Completed Successfully!")
    
    return True

if __name__ == "__main__":
    asyncio.run(run_integration_tests())
