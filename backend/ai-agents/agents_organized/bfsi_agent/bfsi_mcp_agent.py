"""
BFSI MCP-Enabled Agent
======================

This module provides MCP-enabled BFSI agents that can communicate with each other
through the Management Communication Protocol (MCP) for coordinated GRC operations.

Features:
- MCP protocol integration for inter-agent communication
- BFSI-specific message handling and task delegation
- Real-time collaboration between BFSI sub-agents
- Advanced error handling and retry mechanisms
- Performance monitoring and health checks
- Dynamic task routing and load balancing
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# Import base classes and MCP components
from ..shared_components.base_agent import BaseAgent
from ..shared_components.mcp_broker import MCPBroker

logger = logging.getLogger(__name__)

# =============================================================================
# BFSI MCP MESSAGE TYPES AND DATA STRUCTURES
# =============================================================================

class BFSIMessageType(Enum):
    """BFSI-specific message types for MCP communication"""
    COMPLIANCE_CHECK = "compliance_check"
    RISK_ASSESSMENT = "risk_assessment"
    AML_ANALYSIS = "aml_analysis"
    REGULATORY_UPDATE = "regulatory_update"
    FRAUD_DETECTION = "fraud_detection"
    CAPITAL_ADEQUACY_CHECK = "capital_adequacy_check"
    OPERATIONAL_RISK_ASSESSMENT = "operational_risk_assessment"
    CYBER_SECURITY_SCAN = "cyber_security_scan"
    TASK_DELEGATION = "task_delegation"
    COLLABORATION_REQUEST = "collaboration_request"
    COLLABORATION_RESPONSE = "collaboration_response"
    HEARTBEAT = "heartbeat"
    PERFORMANCE_UPDATE = "performance_update"
    ALERT_NOTIFICATION = "alert_notification"

class BFSITaskPriority(Enum):
    """Task priority levels for BFSI operations"""
    CRITICAL = "critical"      # Immediate attention required
    HIGH = "high"             # Urgent but not immediate
    MEDIUM = "medium"         # Standard priority
    LOW = "low"              # Can be deferred

@dataclass
class BFSIMessage:
    """BFSI-specific message structure for MCP communication"""
    message_id: str
    timestamp: datetime
    source_agent: str
    destination_agent: Optional[str]
    message_type: BFSIMessageType
    priority: BFSITaskPriority
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    ttl: int = 3600  # Time to live in seconds
    payload: Dict[str, Any] = None
    metadata: Dict[str, Any] = None

@dataclass
class BFSITask:
    """BFSI task structure for delegation and processing"""
    task_id: str
    task_type: str
    priority: BFSITaskPriority
    description: str
    context: Dict[str, Any]
    assigned_agent: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

# =============================================================================
# BFSI MCP-ENABLED AGENT BASE CLASS
# =============================================================================

class BFSIMCPAgent(BaseAgent):
    """
    Base class for all MCP-enabled BFSI agents
    
    Provides MCP communication capabilities, task management, and BFSI-specific
    functionality for coordinated GRC operations.
    """
    
    def __init__(self, agent_id: str, name: str, agent_type: str):
        super().__init__(agent_id, name)
        self.agent_type = agent_type
        self.capabilities = []
        self.current_tasks = {}
        self.task_history = []
        self.message_handlers = {}
        self.collaboration_partners = set()
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "avg_response_time": 0.0,
            "last_activity": None
        }
        self.health_status = "healthy"
        self.last_heartbeat = datetime.now()
        
        # Initialize default message handlers
        self._initialize_message_handlers()
        
        logger.info(f"🏦 Initialized BFSI MCP Agent: {name} ({agent_id})")
    
    def _initialize_message_handlers(self):
        """Initialize default message handlers for BFSI operations"""
        self.message_handlers = {
            BFSIMessageType.COMPLIANCE_CHECK: self._handle_compliance_check,
            BFSIMessageType.RISK_ASSESSMENT: self._handle_risk_assessment,
            BFSIMessageType.AML_ANALYSIS: self._handle_aml_analysis,
            BFSIMessageType.REGULATORY_UPDATE: self._handle_regulatory_update,
            BFSIMessageType.FRAUD_DETECTION: self._handle_fraud_detection,
            BFSIMessageType.CAPITAL_ADEQUACY_CHECK: self._handle_capital_adequacy_check,
            BFSIMessageType.OPERATIONAL_RISK_ASSESSMENT: self._handle_operational_risk_assessment,
            BFSIMessageType.CYBER_SECURITY_SCAN: self._handle_cyber_security_scan,
            BFSIMessageType.TASK_DELEGATION: self._handle_task_delegation,
            BFSIMessageType.COLLABORATION_REQUEST: self._handle_collaboration_request,
            BFSIMessageType.COLLABORATION_RESPONSE: self._handle_collaboration_response,
            BFSIMessageType.HEARTBEAT: self._handle_heartbeat,
            BFSIMessageType.PERFORMANCE_UPDATE: self._handle_performance_update,
            BFSIMessageType.ALERT_NOTIFICATION: self._handle_alert_notification,
        }
    
    # =============================================================================
    # MESSAGE PROCESSING METHODS
    # =============================================================================
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming MCP messages for BFSI operations
        
        Args:
            message: MCP message payload
            
        Returns:
            Response message or None
        """
        try:
            # Parse BFSI message
            bfsi_msg = self._parse_bfsi_message(message)
            if not bfsi_msg:
                return {"error": "Invalid BFSI message format"}
            
            # Update last activity
            self.last_activity = datetime.now()
            
            # Route message to appropriate handler
            handler = self.message_handlers.get(bfsi_msg.message_type)
            if handler:
                response = await handler(bfsi_msg)
                logger.info(f"✅ Processed {bfsi_msg.message_type.value} message from {bfsi_msg.source_agent}")
                return response
            else:
                logger.warning(f"⚠️ No handler for message type: {bfsi_msg.message_type}")
                return {"error": f"No handler for message type: {bfsi_msg.message_type}"}
                
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            return {"error": str(e)}
    
    def _parse_bfsi_message(self, message: Dict[str, Any]) -> Optional[BFSIMessage]:
        """Parse raw message into BFSI message structure"""
        try:
            return BFSIMessage(
                message_id=message.get("message_id", str(uuid.uuid4())),
                timestamp=datetime.fromisoformat(message.get("timestamp", datetime.now().isoformat())),
                source_agent=message.get("source_agent", "unknown"),
                destination_agent=message.get("destination_agent"),
                message_type=BFSIMessageType(message.get("message_type", "general")),
                priority=BFSITaskPriority(message.get("priority", "medium")),
                correlation_id=message.get("correlation_id"),
                reply_to=message.get("reply_to"),
                ttl=message.get("ttl", 3600),
                payload=message.get("payload", {}),
                metadata=message.get("metadata", {})
            )
        except Exception as e:
            logger.error(f"Failed to parse BFSI message: {e}")
            return None
    
    # =============================================================================
    # BFSI MESSAGE HANDLERS (Override in subclasses)
    # =============================================================================
    
    async def _handle_compliance_check(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle compliance check requests"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_risk_assessment(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle risk assessment requests"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_aml_analysis(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle AML analysis requests"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_regulatory_update(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle regulatory update notifications"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_fraud_detection(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle fraud detection requests"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_capital_adequacy_check(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle capital adequacy check requests"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_operational_risk_assessment(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle operational risk assessment requests"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_cyber_security_scan(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle cyber security scan requests"""
        return {"status": "not_implemented", "message": "Override in subclass"}
    
    async def _handle_task_delegation(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle task delegation requests"""
        try:
            task_data = message.payload
            task = BFSITask(
                task_id=task_data.get("task_id", str(uuid.uuid4())),
                task_type=task_data.get("task_type"),
                priority=BFSITaskPriority(task_data.get("priority", "medium")),
                description=task_data.get("description"),
                context=task_data.get("context", {}),
                assigned_agent=self.agent_id,
                status="pending",
                created_at=datetime.now()
            )
            
            # Add to current tasks
            self.current_tasks[task.task_id] = task
            
            # Process task asynchronously
            asyncio.create_task(self._process_delegated_task(task))
            
            return {
                "status": "accepted",
                "task_id": task.task_id,
                "message": f"Task {task.task_id} accepted and queued for processing"
            }
            
        except Exception as e:
            logger.error(f"Error handling task delegation: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _handle_collaboration_request(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle collaboration requests from other agents"""
        try:
            request_data = message.payload
            collaboration_type = request_data.get("collaboration_type")
            context = request_data.get("context", {})
            
            # Add to collaboration partners
            self.collaboration_partners.add(message.source_agent)
            
            # Process collaboration request
            response = await self._process_collaboration_request(collaboration_type, context)
            
            return {
                "status": "collaboration_accepted",
                "response": response,
                "collaboration_partner": self.agent_id
            }
            
        except Exception as e:
            logger.error(f"Error handling collaboration request: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _handle_collaboration_response(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle collaboration responses from other agents"""
        try:
            response_data = message.payload
            correlation_id = message.correlation_id
            
            # Process collaboration response
            await self._process_collaboration_response(correlation_id, response_data)
            
            return {"status": "response_processed"}
            
        except Exception as e:
            logger.error(f"Error handling collaboration response: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _handle_heartbeat(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle heartbeat messages"""
        self.last_heartbeat = datetime.now()
        return {
            "status": "alive",
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "health_status": self.health_status,
            "performance_metrics": self.performance_metrics
        }
    
    async def _handle_performance_update(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle performance update messages"""
        try:
            update_data = message.payload
            # Update performance metrics
            self.performance_metrics.update(update_data.get("metrics", {}))
            return {"status": "updated"}
        except Exception as e:
            logger.error(f"Error handling performance update: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _handle_alert_notification(self, message: BFSIMessage) -> Dict[str, Any]:
        """Handle alert notifications"""
        try:
            alert_data = message.payload
            await self._process_alert(alert_data)
            return {"status": "alert_processed"}
        except Exception as e:
            logger.error(f"Error handling alert notification: {e}")
            return {"status": "error", "message": str(e)}
    
    # =============================================================================
    # TASK MANAGEMENT METHODS
    # =============================================================================
    
    async def _process_delegated_task(self, task: BFSITask):
        """Process a delegated task asynchronously"""
        try:
            task.status = "in_progress"
            task.started_at = datetime.now()
            
            logger.info(f"🔄 Processing task: {task.task_id} - {task.description}")
            
            # Execute task based on type
            result = await self.execute_task({
                "task_type": task.task_type,
                "context": task.context,
                "priority": task.priority.value
            })
            
            # Update task with result
            task.status = "completed"
            task.completed_at = datetime.now()
            task.result = result
            
            # Update performance metrics
            self.performance_metrics["tasks_completed"] += 1
            
            # Add to task history
            self.task_history.append(task)
            
            # Remove from current tasks
            if task.task_id in self.current_tasks:
                del self.current_tasks[task.task_id]
            
            logger.info(f"✅ Task completed: {task.task_id}")
            
        except Exception as e:
            # Handle task failure
            task.status = "failed"
            task.error_message = str(e)
            task.completed_at = datetime.now()
            
            self.performance_metrics["tasks_failed"] += 1
            
            logger.error(f"❌ Task failed: {task.task_id} - {e}")
    
    # =============================================================================
    # COLLABORATION METHODS
    # =============================================================================
    
    async def request_collaboration(self, target_agent: str, collaboration_type: str, 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Request collaboration from another agent"""
        try:
            message = {
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "source_agent": self.agent_id,
                "destination_agent": target_agent,
                "message_type": BFSIMessageType.COLLABORATION_REQUEST.value,
                "priority": BFSITaskPriority.MEDIUM.value,
                "payload": {
                    "collaboration_type": collaboration_type,
                    "context": context
                },
                "metadata": {
                    "requesting_agent": self.agent_id
                }
            }
            
            await self.send_message(target_agent, message)
            
            logger.info(f"🤝 Collaboration requested from {target_agent}")
            
            return {"status": "request_sent", "target_agent": target_agent}
            
        except Exception as e:
            logger.error(f"Error requesting collaboration: {e}")
            return {"status": "error", "message": str(e)}
    
    async def delegate_task(self, target_agent: str, task: BFSITask) -> Dict[str, Any]:
        """Delegate a task to another agent"""
        try:
            message = {
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "source_agent": self.agent_id,
                "destination_agent": target_agent,
                "message_type": BFSIMessageType.TASK_DELEGATION.value,
                "priority": task.priority.value,
                "payload": asdict(task),
                "metadata": {
                    "delegating_agent": self.agent_id
                }
            }
            
            await self.send_message(target_agent, message)
            
            logger.info(f"📋 Task delegated to {target_agent}: {task.task_id}")
            
            return {"status": "delegated", "task_id": task.task_id, "target_agent": target_agent}
            
        except Exception as e:
            logger.error(f"Error delegating task: {e}")
            return {"status": "error", "message": str(e)}
    
    async def broadcast_alert(self, alert_type: str, severity: str, message: str, 
                            context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Broadcast an alert to all agents"""
        try:
            alert_message = {
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "source_agent": self.agent_id,
                "destination_agent": None,  # Broadcast to all
                "message_type": BFSIMessageType.ALERT_NOTIFICATION.value,
                "priority": BFSITaskPriority.HIGH.value,
                "payload": {
                    "alert_type": alert_type,
                    "severity": severity,
                    "message": message,
                    "context": context or {}
                },
                "metadata": {
                    "broadcasting_agent": self.agent_id
                }
            }
            
            # Send to MCP broker for broadcasting
            if self.mcp_broker:
                await self.mcp_broker.broadcast_message(alert_message)
            
            logger.warning(f"🚨 Alert broadcasted: {alert_type} - {severity}")
            
            return {"status": "broadcasted", "alert_type": alert_type}
            
        except Exception as e:
            logger.error(f"Error broadcasting alert: {e}")
            return {"status": "error", "message": str(e)}
    
    # =============================================================================
    # ABSTRACT METHODS (Must be implemented by subclasses)
    # =============================================================================
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific task - Must be implemented by subclasses
        
        Args:
            task: Task details including type and context
            
        Returns:
            Task execution result
        """
        raise NotImplementedError("execute_task must be implemented by subclass")
    
    async def _process_collaboration_request(self, collaboration_type: str, 
                                           context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process collaboration request - Must be implemented by subclasses
        
        Args:
            collaboration_type: Type of collaboration requested
            context: Collaboration context
            
        Returns:
            Collaboration response
        """
        raise NotImplementedError("_process_collaboration_request must be implemented by subclass")
    
    async def _process_collaboration_response(self, correlation_id: str, 
                                            response_data: Dict[str, Any]):
        """
        Process collaboration response - Must be implemented by subclasses
        
        Args:
            correlation_id: Correlation ID for the collaboration
            response_data: Response data from collaborating agent
        """
        raise NotImplementedError("_process_collaboration_response must be implemented by subclass")
    
    async def _process_alert(self, alert_data: Dict[str, Any]):
        """
        Process alert notification - Must be implemented by subclasses
        
        Args:
            alert_data: Alert data including type, severity, and message
        """
        raise NotImplementedError("_process_alert must be implemented by subclass")
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    
    def add_capability(self, capability: str):
        """Add a capability to the agent"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            logger.info(f"✅ Added capability: {capability}")
    
    def remove_capability(self, capability: str):
        """Remove a capability from the agent"""
        if capability in self.capabilities:
            self.capabilities.remove(capability)
            logger.info(f"❌ Removed capability: {capability}")
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return self.capabilities.copy()
    
    def get_current_tasks(self) -> Dict[str, BFSITask]:
        """Get current active tasks"""
        return self.current_tasks.copy()
    
    def get_task_history(self) -> List[BFSITask]:
        """Get task history"""
        return self.task_history.copy()
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.performance_metrics.copy()
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "agent_type": self.agent_type,
            "status": self.status,
            "health_status": self.health_status,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "capabilities": self.capabilities,
            "current_tasks_count": len(self.current_tasks),
            "collaboration_partners": list(self.collaboration_partners),
            "performance_metrics": self.performance_metrics
        }
    
    async def start_heartbeat(self, interval: int = 30):
        """Start periodic heartbeat to maintain agent status"""
        while self.status == "active":
            try:
                # Send heartbeat to MCP broker
                if self.mcp_broker:
                    heartbeat_message = {
                        "message_id": str(uuid.uuid4()),
                        "timestamp": datetime.now().isoformat(),
                        "source_agent": self.agent_id,
                        "destination_agent": None,
                        "message_type": BFSIMessageType.HEARTBEAT.value,
                        "priority": BFSITaskPriority.LOW.value,
                        "payload": {
                            "agent_id": self.agent_id,
                            "health_status": self.health_status,
                            "performance_metrics": self.performance_metrics
                        }
                    }
                    
                    await self.mcp_broker.broadcast_message(heartbeat_message)
                
                self.last_heartbeat = datetime.now()
                
                # Wait for next heartbeat
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in heartbeat: {e}")
                await asyncio.sleep(interval)
    
    async def start(self):
        """Start the BFSI MCP agent"""
        await super().start()
        
        # Start heartbeat in background
        asyncio.create_task(self.start_heartbeat())
        
        logger.info(f"🚀 BFSI MCP Agent started: {self.name}")
    
    async def stop(self):
        """Stop the BFSI MCP agent"""
        await super().stop()
        
        # Cancel all current tasks
        for task in self.current_tasks.values():
            task.status = "cancelled"
        
        logger.info(f"🛑 BFSI MCP Agent stopped: {self.name}")
