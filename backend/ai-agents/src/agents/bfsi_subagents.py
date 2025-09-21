"""
BFSI Sub-Agents and Orchestrator
Specialized sub-agents for BFSI GRC operations
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BFSIAgentType(Enum):
    """BFSI Agent Types"""
    COMPLIANCE = "compliance"
    RISK_ANALYZER = "risk_analyzer"
    REGULATORY_MONITOR = "regulatory_monitor"
    AML_ANALYZER = "aml_analyzer"
    CAPITAL_ADEQUACY = "capital_adequacy"
    OPERATIONAL_RISK = "operational_risk"
    CYBER_SECURITY = "cyber_security"
    FRAUD_DETECTION = "fraud_detection"


@dataclass
class BFSIOperationContext:
    """Context for BFSI operations"""
    operation_id: str
    operation_type: str
    business_unit: str
    risk_level: str
    compliance_requirements: List[str]
    regulatory_frameworks: List[str]
    data_sources: List[str]
    stakeholders: List[str]
    priority: int = 1
    deadline: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BFSISubAgent(ABC):
    """Abstract base class for BFSI sub-agents"""
    
    def __init__(self, agent_type: BFSIAgentType, name: str):
        self.agent_type = agent_type
        self.name = name
        self.status = "active"
        self.last_activity = datetime.now()
        self.operation_count = 0
        self.error_count = 0
        self.performance_metrics: Dict[str, Any] = {}
    
    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process requests specific to this sub-agent"""
        pass
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task specific to this sub-agent"""
        start_time = datetime.now()
        self.status = "working"
        
        try:
            result = await self.process_request(task_data)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update performance metrics
            self.performance_metrics.update({
                "last_execution_time": execution_time,
                "total_operations": self.operation_count,
                "error_rate": (self.error_count / self.operation_count) * 100 if self.operation_count > 0 else 0
            })
            
            return result
        except Exception as e:
            self.status = "error"
            logger.error(f"Task execution failed in {self.name}: {e}")
            raise
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the sub-agent"""
        return {
            "agent_type": self.agent_type.value,
            "name": self.name,
            "status": self.status,
            "operation_count": self.operation_count,
            "error_count": self.error_count,
            "error_rate": (self.error_count / self.operation_count) * 100 if self.operation_count > 0 else 0,
            "last_activity": self.last_activity.isoformat(),
            "performance_metrics": self.performance_metrics
        }


class BFSIOrchestrator:
    """
    BFSI Orchestrator for coordinating sub-agents
    Manages the execution of complex BFSI operations across multiple sub-agents
    """
    
    def __init__(self):
        self.sub_agents: Dict[BFSIAgentType, BFSISubAgent] = {}
        self.operation_history: List[Dict[str, Any]] = []
        self.status = "active"
        self.last_activity = datetime.now()
        
    def register_sub_agent(self, agent_type: BFSIAgentType, sub_agent: BFSISubAgent):
        """Register a sub-agent with the orchestrator"""
        self.sub_agents[agent_type] = sub_agent
        logger.info(f"Registered sub-agent: {agent_type.value}")
    
    async def execute_bfsi_operation(self, operation_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute BFSI operations using appropriate sub-agents"""
        start_time = datetime.now()
        operation_id = f"bfsi_op_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Route operation to appropriate sub-agents
            result = await self._route_operation(operation_type, context)
            
            # Record operation
            self.operation_history.append({
                "operation_id": operation_id,
                "operation_type": operation_type,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "status": "success",
                "result": result
            })
            
            return result
            
        except Exception as e:
            logger.error(f"BFSI operation failed: {e}")
            
            # Record failed operation
            self.operation_history.append({
                "operation_id": operation_id,
                "operation_type": operation_type,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e)
            })
            
            raise
    
    async def _route_operation(self, operation_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Route operations to appropriate sub-agents"""
        if operation_type == "risk_assessment":
            return await self._execute_risk_assessment(context)
        elif operation_type == "compliance_check":
            return await self._execute_compliance_check(context)
        elif operation_type == "regulatory_monitoring":
            return await self._execute_regulatory_monitoring(context)
        elif operation_type == "aml_analysis":
            return await self._execute_aml_analysis(context)
        elif operation_type == "capital_adequacy_check":
            return await self._execute_capital_adequacy_check(context)
        elif operation_type == "operational_risk_assessment":
            return await self._execute_operational_risk_assessment(context)
        elif operation_type == "cyber_security_check":
            return await self._execute_cyber_security_check(context)
        elif operation_type == "fraud_detection":
            return await self._execute_fraud_detection(context)
        else:
            return await self._execute_general_operation(operation_type, context)
    
    async def _execute_risk_assessment(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute risk assessment using risk analyzer"""
        if BFSIAgentType.RISK_ANALYZER in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.RISK_ANALYZER].process_request(context)
        else:
            return {"error": "Risk analyzer not available"}
    
    async def _execute_compliance_check(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute compliance check using compliance coordinator"""
        if BFSIAgentType.COMPLIANCE in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.COMPLIANCE].process_request(context)
        else:
            return {"error": "Compliance coordinator not available"}
    
    async def _execute_regulatory_monitoring(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute regulatory monitoring"""
        if BFSIAgentType.REGULATORY_MONITOR in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.REGULATORY_MONITOR].process_request(context)
        else:
            return {"error": "Regulatory monitor not available"}
    
    async def _execute_aml_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AML analysis"""
        if BFSIAgentType.AML_ANALYZER in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.AML_ANALYZER].process_request(context)
        else:
            return {"error": "AML analyzer not available"}
    
    async def _execute_capital_adequacy_check(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute capital adequacy check"""
        if BFSIAgentType.CAPITAL_ADEQUACY in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.CAPITAL_ADEQUACY].process_request(context)
        else:
            return {"error": "Capital adequacy monitor not available"}
    
    async def _execute_operational_risk_assessment(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute operational risk assessment"""
        if BFSIAgentType.OPERATIONAL_RISK in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.OPERATIONAL_RISK].process_request(context)
        else:
            return {"error": "Operational risk manager not available"}
    
    async def _execute_cyber_security_check(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute cyber security check"""
        if BFSIAgentType.CYBER_SECURITY in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.CYBER_SECURITY].process_request(context)
        else:
            return {"error": "Cyber security monitor not available"}
    
    async def _execute_fraud_detection(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute fraud detection"""
        if BFSIAgentType.FRAUD_DETECTION in self.sub_agents:
            return await self.sub_agents[BFSIAgentType.FRAUD_DETECTION].process_request(context)
        else:
            return {"error": "Fraud detection system not available"}
    
    async def _execute_general_operation(self, operation_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute general operations"""
        return {
            "operation_type": operation_type,
            "status": "executed",
            "message": f"General operation {operation_type} executed",
            "context": context
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents"""
        status = {
            "orchestrator_status": self.status,
            "last_activity": self.last_activity.isoformat(),
            "total_operations": len(self.operation_history),
            "sub_agents": {}
        }
        
        for agent_type, agent in self.sub_agents.items():
            status["sub_agents"][agent_type.value] = agent.get_health_status()
        
        return status
    
    def get_operation_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent operation history"""
        return self.operation_history[-limit:] if self.operation_history else []

