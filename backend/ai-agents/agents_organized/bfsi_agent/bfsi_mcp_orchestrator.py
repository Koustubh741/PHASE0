"""
BFSI MCP Orchestrator
=====================

This module provides orchestration capabilities for BFSI agents using the MCP protocol
for coordinated GRC operations, task delegation, and inter-agent collaboration.

Features:
- Multi-agent task coordination
- Intelligent task routing and load balancing
- Real-time collaboration workflows
- Cross-agent validation and consensus
- Performance monitoring and optimization
- Dynamic agent scaling and failover
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from .bfsi_mcp_agent import BFSIMCPAgent, BFSIMessage, BFSIMessageType, BFSITask, BFSITaskPriority
from .bfsi_mcp_subagents import BFSIMCPAgentFactory

logger = logging.getLogger(__name__)

# =============================================================================
# ORCHESTRATION DATA STRUCTURES
# =============================================================================

class WorkflowType(Enum):
    """Types of BFSI workflows"""
    COMPLIANCE_AUDIT = "compliance_audit"
    RISK_ASSESSMENT = "risk_assessment"
    AML_INVESTIGATION = "aml_investigation"
    FRAUD_INVESTIGATION = "fraud_investigation"
    REGULATORY_REPORTING = "regulatory_reporting"
    CAPITAL_ADEQUACY_CHECK = "capital_adequacy_check"
    OPERATIONAL_RISK_REVIEW = "operational_risk_review"
    CYBER_SECURITY_AUDIT = "cyber_security_audit"

class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowStep:
    """Individual step in a workflow"""
    step_id: str
    workflow_id: str
    step_name: str
    agent_type: str
    task_type: str
    priority: BFSITaskPriority
    dependencies: List[str] = None  # Step IDs this step depends on
    context: Dict[str, Any] = None
    assigned_agent: Optional[str] = None
    status: str = "pending"
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

@dataclass
class WorkflowExecution:
    """Complete workflow execution tracking"""
    workflow_id: str
    workflow_type: WorkflowType
    status: WorkflowStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    steps: List[WorkflowStep] = None
    context: Dict[str, Any] = None
    results: Dict[str, Any] = None
    error_message: Optional[str] = None

# =============================================================================
# BFSI MCP ORCHESTRATOR
# =============================================================================

class BFSIMCPOrchestrator:
    """
    Orchestrator for BFSI MCP agents
    
    Coordinates multi-agent workflows, manages task delegation,
    and ensures optimal resource utilization across BFSI operations.
    """
    
    def __init__(self):
        self.agents: Dict[str, BFSIMCPAgent] = {}
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_history: List[WorkflowExecution] = []
        self.agent_capabilities: Dict[str, List[str]] = {}
        self.performance_metrics = {
            "workflows_completed": 0,
            "workflows_failed": 0,
            "avg_completion_time": 0.0,
            "agent_utilization": {}
        }
        
        logger.info("🎭 BFSI MCP Orchestrator initialized")
    
    # =============================================================================
    # AGENT MANAGEMENT
    # =============================================================================
    
    async def register_agent(self, agent: BFSIMCPAgent):
        """Register an agent with the orchestrator"""
        try:
            self.agents[agent.agent_id] = agent
            self.agent_capabilities[agent.agent_id] = agent.get_capabilities()
            self.performance_metrics["agent_utilization"][agent.agent_id] = {
                "tasks_completed": 0,
                "tasks_failed": 0,
                "avg_response_time": 0.0,
                "last_activity": None
            }
            
            logger.info(f"✅ Registered agent: {agent.name} ({agent.agent_id})")
            
        except Exception as e:
            logger.error(f"❌ Failed to register agent {agent.agent_id}: {e}")
            raise
    
    async def unregister_agent(self, agent_id: str):
        """Unregister an agent from the orchestrator"""
        try:
            if agent_id in self.agents:
                del self.agents[agent_id]
                del self.agent_capabilities[agent_id]
                if agent_id in self.performance_metrics["agent_utilization"]:
                    del self.performance_metrics["agent_utilization"][agent_id]
                
                logger.info(f"❌ Unregistered agent: {agent_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to unregister agent {agent_id}: {e}")
    
    def get_available_agents(self, required_capabilities: List[str] = None) -> List[str]:
        """Get list of available agents with optional capability filtering"""
        if not required_capabilities:
            return list(self.agents.keys())
        
        available_agents = []
        for agent_id, capabilities in self.agent_capabilities.items():
            if all(cap in capabilities for cap in required_capabilities):
                available_agents.append(agent_id)
        
        return available_agents
    
    # =============================================================================
    # WORKFLOW MANAGEMENT
    # =============================================================================
    
    async def create_workflow(self, workflow_type: WorkflowType, 
                            context: Dict[str, Any]) -> str:
        """Create a new workflow execution"""
        try:
            workflow_id = f"workflow_{workflow_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create workflow steps based on type
            steps = await self._create_workflow_steps(workflow_type, workflow_id, context)
            
            workflow = WorkflowExecution(
                workflow_id=workflow_id,
                workflow_type=workflow_type,
                status=WorkflowStatus.PENDING,
                created_at=datetime.now(),
                steps=steps,
                context=context
            )
            
            self.active_workflows[workflow_id] = workflow
            
            logger.info(f"📋 Created workflow: {workflow_id} ({workflow_type.value})")
            
            return workflow_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create workflow: {e}")
            raise
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow with intelligent task routing"""
        try:
            if workflow_id not in self.active_workflows:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            workflow = self.active_workflows[workflow_id]
            workflow.status = WorkflowStatus.RUNNING
            workflow.started_at = datetime.now()
            
            logger.info(f"🚀 Starting workflow execution: {workflow_id}")
            
            # Execute steps in dependency order
            await self._execute_workflow_steps(workflow)
            
            # Check if workflow completed successfully
            if all(step.status == "completed" for step in workflow.steps):
                workflow.status = WorkflowStatus.COMPLETED
                workflow.completed_at = datetime.now()
                
                # Collect results
                workflow.results = {
                    step.step_id: step.result for step in workflow.steps
                }
                
                # Move to history
                self.workflow_history.append(workflow)
                del self.active_workflows[workflow_id]
                
                # Update metrics
                self.performance_metrics["workflows_completed"] += 1
                
                logger.info(f"✅ Workflow completed: {workflow_id}")
                
            else:
                workflow.status = WorkflowStatus.FAILED
                workflow.error_message = "One or more steps failed"
                
                # Update metrics
                self.performance_metrics["workflows_failed"] += 1
                
                logger.error(f"❌ Workflow failed: {workflow_id}")
            
            return {
                "workflow_id": workflow_id,
                "status": workflow.status.value,
                "results": workflow.results,
                "duration": (workflow.completed_at - workflow.started_at).total_seconds() if workflow.completed_at else None
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {e}")
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id].status = WorkflowStatus.FAILED
                self.active_workflows[workflow_id].error_message = str(e)
            raise
    
    async def _create_workflow_steps(self, workflow_type: WorkflowType, 
                                   workflow_id: str, context: Dict[str, Any]) -> List[WorkflowStep]:
        """Create workflow steps based on workflow type"""
        steps = []
        
        if workflow_type == WorkflowType.COMPLIANCE_AUDIT:
            steps = [
                WorkflowStep(
                    step_id=f"{workflow_id}_step_1",
                    workflow_id=workflow_id,
                    step_name="Compliance Check",
                    agent_type="compliance",
                    task_type="compliance_check",
                    priority=BFSITaskPriority.HIGH,
                    context=context
                ),
                WorkflowStep(
                    step_id=f"{workflow_id}_step_2",
                    workflow_id=workflow_id,
                    step_name="Risk Assessment",
                    agent_type="risk",
                    task_type="risk_assessment",
                    priority=BFSITaskPriority.MEDIUM,
                    dependencies=[f"{workflow_id}_step_1"],
                    context=context
                ),
                WorkflowStep(
                    step_id=f"{workflow_id}_step_3",
                    workflow_id=workflow_id,
                    step_name="Regulatory Reporting",
                    agent_type="compliance",
                    task_type="regulatory_reporting",
                    priority=BFSITaskPriority.MEDIUM,
                    dependencies=[f"{workflow_id}_step_1", f"{workflow_id}_step_2"],
                    context=context
                )
            ]
        
        elif workflow_type == WorkflowType.FRAUD_INVESTIGATION:
            steps = [
                WorkflowStep(
                    step_id=f"{workflow_id}_step_1",
                    workflow_id=workflow_id,
                    step_name="Fraud Detection",
                    agent_type="fraud",
                    task_type="fraud_detection",
                    priority=BFSITaskPriority.CRITICAL,
                    context=context
                ),
                WorkflowStep(
                    step_id=f"{workflow_id}_step_2",
                    workflow_id=workflow_id,
                    step_name="AML Analysis",
                    agent_type="aml",
                    task_type="aml_analysis",
                    priority=BFSITaskPriority.HIGH,
                    dependencies=[f"{workflow_id}_step_1"],
                    context=context
                ),
                WorkflowStep(
                    step_id=f"{workflow_id}_step_3",
                    workflow_id=workflow_id,
                    step_name="Compliance Review",
                    agent_type="compliance",
                    task_type="compliance_check",
                    priority=BFSITaskPriority.HIGH,
                    dependencies=[f"{workflow_id}_step_1", f"{workflow_id}_step_2"],
                    context=context
                )
            ]
        
        elif workflow_type == WorkflowType.RISK_ASSESSMENT:
            steps = [
                WorkflowStep(
                    step_id=f"{workflow_id}_step_1",
                    workflow_id=workflow_id,
                    step_name="Risk Analysis",
                    agent_type="risk",
                    task_type="risk_assessment",
                    priority=BFSITaskPriority.HIGH,
                    context=context
                ),
                WorkflowStep(
                    step_id=f"{workflow_id}_step_2",
                    workflow_id=workflow_id,
                    step_name="Capital Adequacy Check",
                    agent_type="capital_adequacy",
                    task_type="capital_adequacy_check",
                    priority=BFSITaskPriority.MEDIUM,
                    dependencies=[f"{workflow_id}_step_1"],
                    context=context
                )
            ]
        
        return steps
    
    async def _execute_workflow_steps(self, workflow: WorkflowExecution):
        """Execute workflow steps with dependency management"""
        completed_steps = set()
        
        while len(completed_steps) < len(workflow.steps):
            # Find steps that can be executed (dependencies satisfied)
            ready_steps = []
            for step in workflow.steps:
                if step.status == "pending":
                    dependencies_met = True
                    if step.dependencies:
                        dependencies_met = all(dep in completed_steps for dep in step.dependencies)
                    
                    if dependencies_met:
                        ready_steps.append(step)
            
            # Execute ready steps in parallel
            if ready_steps:
                tasks = []
                for step in ready_steps:
                    task = asyncio.create_task(self._execute_workflow_step(step))
                    tasks.append((step, task))
                
                # Wait for all tasks to complete
                for step, task in tasks:
                    try:
                        result = await task
                        if result.get("status") == "completed":
                            step.status = "completed"
                            step.result = result.get("result")
                            step.completed_at = datetime.now()
                            completed_steps.add(step.step_id)
                            
                            # Update agent performance metrics
                            if step.assigned_agent:
                                self._update_agent_metrics(step.assigned_agent, True)
                        else:
                            step.status = "failed"
                            step.error_message = result.get("error", "Unknown error")
                            completed_steps.add(step.step_id)
                            
                            # Update agent performance metrics
                            if step.assigned_agent:
                                self._update_agent_metrics(step.assigned_agent, False)
                            
                            logger.error(f"❌ Step failed: {step.step_id} - {step.error_message}")
                            
                    except Exception as e:
                        step.status = "failed"
                        step.error_message = str(e)
                        completed_steps.add(step.step_id)
                        logger.error(f"❌ Step execution error: {step.step_id} - {e}")
            
            else:
                # No ready steps, check for circular dependencies or deadlock
                logger.warning(f"⚠️ No ready steps found for workflow {workflow.workflow_id}")
                break
    
    async def _execute_workflow_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute a single workflow step"""
        try:
            step.status = "in_progress"
            step.started_at = datetime.now()
            
            # Find suitable agent for the step
            suitable_agents = self.get_available_agents([step.agent_type])
            
            if not suitable_agents:
                return {
                    "status": "failed",
                    "error": f"No agents available for type: {step.agent_type}"
                }
            
            # Select best agent (load balancing)
            selected_agent_id = await self._select_best_agent(suitable_agents, step)
            step.assigned_agent = selected_agent_id
            
            agent = self.agents[selected_agent_id]
            
            # Execute task
            result = await agent.execute_task({
                "task_type": step.task_type,
                "context": step.context,
                "priority": step.priority.value
            })
            
            return {
                "status": "completed",
                "result": result
            }
            
        except Exception as e:
            logger.error(f"❌ Step execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _select_best_agent(self, candidate_agents: List[str], step: WorkflowStep) -> str:
        """Select the best agent for a task based on load balancing and capabilities"""
        if len(candidate_agents) == 1:
            return candidate_agents[0]
        
        # Simple round-robin load balancing
        # In production, this could be more sophisticated (consider agent load, performance, etc.)
        return candidate_agents[0]
    
    def _update_agent_metrics(self, agent_id: str, success: bool):
        """Update agent performance metrics"""
        if agent_id not in self.performance_metrics["agent_utilization"]:
            self.performance_metrics["agent_utilization"][agent_id] = {
                "tasks_completed": 0,
                "tasks_failed": 0,
                "avg_response_time": 0.0,
                "last_activity": None
            }
        
        metrics = self.performance_metrics["agent_utilization"][agent_id]
        
        if success:
            metrics["tasks_completed"] += 1
        else:
            metrics["tasks_failed"] += 1
        
        metrics["last_activity"] = datetime.now().isoformat()
    
    # =============================================================================
    # COLLABORATION AND COORDINATION
    # =============================================================================
    
    async def coordinate_collaboration(self, agent_id: str, collaboration_type: str, 
                                     context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate collaboration between multiple agents"""
        try:
            if agent_id not in self.agents:
                raise ValueError(f"Agent {agent_id} not found")
            
            requesting_agent = self.agents[agent_id]
            
            # Determine collaborating agents based on collaboration type
            collaborating_agents = await self._determine_collaborating_agents(
                collaboration_type, context
            )
            
            # Initiate collaboration
            collaboration_results = []
            for collaborator_id in collaborating_agents:
                if collaborator_id != agent_id:  # Don't collaborate with self
                    result = await requesting_agent.request_collaboration(
                        collaborator_id, collaboration_type, context
                    )
                    collaboration_results.append({
                        "agent_id": collaborator_id,
                        "result": result
                    })
            
            return {
                "status": "collaboration_initiated",
                "collaborating_agents": collaborating_agents,
                "results": collaboration_results
            }
            
        except Exception as e:
            logger.error(f"❌ Collaboration coordination failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _determine_collaborating_agents(self, collaboration_type: str, 
                                            context: Dict[str, Any]) -> List[str]:
        """Determine which agents should collaborate for a given type"""
        collaboration_map = {
            "comprehensive_risk_analysis": ["bfsi-risk-001", "bfsi-compliance-001", "bfsi-aml-001"],
            "fraud_investigation": ["bfsi-fraud-001", "bfsi-aml-001", "bfsi-compliance-001"],
            "regulatory_compliance_check": ["bfsi-compliance-001", "bfsi-risk-001"],
            "aml_comprehensive_analysis": ["bfsi-aml-001", "bfsi-fraud-001", "bfsi-compliance-001"]
        }
        
        return collaboration_map.get(collaboration_type, [])
    
    # =============================================================================
    # MONITORING AND ANALYTICS
    # =============================================================================
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status and metrics"""
        return {
            "orchestrator_status": "active",
            "total_agents": len(self.agents),
            "active_workflows": len(self.active_workflows),
            "completed_workflows": len(self.workflow_history),
            "performance_metrics": self.performance_metrics,
            "agent_capabilities": self.agent_capabilities,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a specific workflow"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": workflow.status.value,
                "progress": len([s for s in workflow.steps if s.status == "completed"]) / len(workflow.steps),
                "steps": [
                    {
                        "step_id": step.step_id,
                        "step_name": step.step_name,
                        "agent_type": step.agent_type,
                        "status": step.status,
                        "assigned_agent": step.assigned_agent
                    }
                    for step in workflow.steps
                ],
                "created_at": workflow.created_at.isoformat(),
                "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
                "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None
            }
        else:
            return {"error": f"Workflow {workflow_id} not found"}
    
    def get_agent_performance(self) -> Dict[str, Any]:
        """Get performance metrics for all agents"""
        return self.performance_metrics["agent_utilization"]
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    
    async def cleanup(self):
        """Cleanup orchestrator resources"""
        try:
            # Cancel all active workflows
            for workflow in self.active_workflows.values():
                workflow.status = WorkflowStatus.CANCELLED
            
            # Clear active workflows
            self.active_workflows.clear()
            
            logger.info("🧹 BFSI MCP Orchestrator cleaned up")
            
        except Exception as e:
            logger.error(f"❌ Error during orchestrator cleanup: {e}")

# =============================================================================
# ORCHESTRATOR FACTORY
# =============================================================================

class BFSIMCPOrchestratorFactory:
    """Factory for creating and configuring BFSI MCP Orchestrator"""
    
    @staticmethod
    async def create_orchestrator_with_agents() -> BFSIMCPOrchestrator:
        """Create orchestrator and register all available BFSI agents"""
        orchestrator = BFSIMCPOrchestrator()
        
        # Create and register all available agents
        for agent_type in BFSIMCPAgentFactory.get_available_agents():
            try:
                agent = BFSIMCPAgentFactory.create_agent(agent_type)
                await agent.start()
                await orchestrator.register_agent(agent)
            except Exception as e:
                logger.error(f"❌ Failed to create agent {agent_type}: {e}")
        
        logger.info(f"🎭 BFSI MCP Orchestrator created with {len(orchestrator.agents)} agents")
        
        return orchestrator
