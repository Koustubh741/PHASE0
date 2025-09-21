"""
Communication Agent - Inter-Agent Communication and Coordination
Provides centralized communication management for the GRC platform multi-agent system
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from shared_components.industry_agent import IndustryAgent, IndustryType, GRCOperationType
except ImportError:
    # Fallback for demo purposes
    class IndustryAgent:
        def __init__(self, industry_type, agent_id, name):
            self.industry_type = industry_type
            self.agent_id = agent_id
            self.name = name
    
    class IndustryType:
        BFSI = "BFSI"
        HEALTHCARE = "HEALTHCARE"
        MANUFACTURING = "MANUFACTURING"
        TELECOM = "TELECOM"
    
    class GRCOperationType:
        RISK_ASSESSMENT = "risk_assessment"
        COMPLIANCE_CHECK = "compliance_check"
        POLICY_REVIEW = "policy_review"

class MessageType(Enum):
    """Message types for inter-agent communication"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"
    REGISTRATION = "registration"
    DISCOVERY = "discovery"

class AgentStatus(Enum):
    """Agent status for communication management"""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class CommunicationProtocol(Enum):
    """Supported communication protocols"""
    MCP = "mcp"
    REST = "rest"
    WEBSOCKET = "websocket"
    MESSAGE_QUEUE = "message_queue"

class CommunicationAgent(IndustryAgent):
    """
    Communication Agent for inter-agent communication and coordination
    Provides centralized communication management for all agents
    """
    
    def __init__(self, agent_id: str = "communication-agent", name: str = "Communication Management Agent"):
        # Initialize with a generic industry type since this is cross-industry
        super().__init__(IndustryType.BFSI, agent_id, name)  # Using BFSI as base, but will be cross-industry
        self.registered_agents = {}  # Agent registry
        self.message_queues = {}  # Message queues for each agent
        self.communication_protocols = [protocol.value for protocol in CommunicationProtocol]
        self.message_router = self._initialize_message_router()
        self.protocol_handlers = self._initialize_protocol_handlers()
        self.health_monitor = self._initialize_health_monitor()
        
        logging.info(f"Communication Agent initialized with {len(self.communication_protocols)} protocols")

    def _initialize_message_router(self) -> Dict[str, Any]:
        """Initialize message routing system"""
        return {
            "routing_rules": {
                "by_agent_type": True,
                "by_industry": True,
                "by_capability": True,
                "load_balancing": True
            },
            "routing_algorithms": {
                "round_robin": True,
                "least_connections": True,
                "weighted_round_robin": True,
                "random": True
            },
            "timeout_settings": {
                "default_timeout": 30,  # seconds
                "max_retries": 3,
                "retry_delay": 1  # seconds
            }
        }

    def _initialize_protocol_handlers(self) -> Dict[str, Any]:
        """Initialize communication protocol handlers"""
        return {
            "mcp": {
                "enabled": True,
                "port": 8001,
                "features": ["agent_registration", "service_invocation", "health_checks"]
            },
            "rest": {
                "enabled": True,
                "port": 8002,
                "features": ["http_communication", "json_payloads", "authentication"]
            },
            "websocket": {
                "enabled": True,
                "port": 8003,
                "features": ["real_time_communication", "event_streaming", "heartbeat"]
            },
            "message_queue": {
                "enabled": True,
                "features": ["async_processing", "priority_queues", "dead_letter_queues"]
            }
        }

    def _initialize_health_monitor(self) -> Dict[str, Any]:
        """Initialize health monitoring system"""
        return {
            "health_check_interval": 30,  # seconds
            "health_check_timeout": 10,  # seconds
            "failure_threshold": 3,
            "recovery_threshold": 2,
            "monitored_metrics": [
                "response_time",
                "success_rate",
                "error_rate",
                "throughput"
            ]
        }

    async def register_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Register an agent for communication services"""
        try:
            agent_id = context.get("agent_id")
            agent_type = context.get("agent_type", "unknown")
            industry = context.get("industry", "general")
            capabilities = context.get("capabilities", [])
            endpoints = context.get("endpoints", {})
            
            if not agent_id:
                return {
                    "success": False,
                    "error": "Agent ID is required for registration",
                    "agent": self.name
                }
            
            # Create agent record
            agent_record = {
                "agent_id": agent_id,
                "agent_type": agent_type,
                "industry": industry,
                "capabilities": capabilities,
                "endpoints": endpoints,
                "status": AgentStatus.ONLINE.value,
                "registered_at": datetime.now().isoformat(),
                "last_heartbeat": datetime.now().isoformat(),
                "message_count": 0,
                "error_count": 0
            }
            
            # Register agent
            self.registered_agents[agent_id] = agent_record
            
            # Initialize message queue for agent
            self.message_queues[agent_id] = []
            
            # Start health monitoring for agent
            await self._start_health_monitoring(agent_id)
            
            logging.info(f"Agent {agent_id} registered successfully")
            
            return {
                "success": True,
                "operation": "agent_registration",
                "agent_id": agent_id,
                "agent_type": agent_type,
                "industry": industry,
                "capabilities": capabilities,
                "endpoints": endpoints,
                "registered_at": datetime.now().isoformat(),
                "agent": self.name
            }
            
        except Exception as e:
            logging.error(f"Agent registration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def route_message(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Route message between agents"""
        try:
            from_agent = context.get("from_agent")
            to_agent = context.get("to_agent")
            message_type = context.get("message_type", MessageType.REQUEST.value)
            payload = context.get("payload", {})
            priority = context.get("priority", "normal")
            
            if not from_agent or not to_agent:
                return {
                    "success": False,
                    "error": "Both from_agent and to_agent are required",
                    "agent": self.name
                }
            
            # Check if target agent is registered
            if to_agent not in self.registered_agents:
                return {
                    "success": False,
                    "error": f"Target agent {to_agent} is not registered",
                    "agent": self.name
                }
            
            # Create message
            message = {
                "message_id": f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(context)) % 10000}",
                "from_agent": from_agent,
                "to_agent": to_agent,
                "message_type": message_type,
                "payload": payload,
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "status": "pending"
            }
            
            # Route message based on protocol
            routing_result = await self._route_message_by_protocol(message)
            
            # Update agent message count
            if to_agent in self.registered_agents:
                self.registered_agents[to_agent]["message_count"] += 1
            
            return {
                "success": True,
                "operation": "message_routing",
                "message_id": message["message_id"],
                "from_agent": from_agent,
                "to_agent": to_agent,
                "message_type": message_type,
                "routing_result": routing_result,
                "routed_at": datetime.now().isoformat(),
                "agent": self.name
            }
            
        except Exception as e:
            logging.error(f"Message routing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def _route_message_by_protocol(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Route message using appropriate protocol"""
        try:
            to_agent = message["to_agent"]
            agent_record = self.registered_agents.get(to_agent, {})
            endpoints = agent_record.get("endpoints", {})
            
            # Determine best protocol to use
            protocol = self._select_protocol(endpoints)
            
            # Route message using selected protocol
            if protocol == CommunicationProtocol.MCP.value:
                return await self._route_via_mcp(message, endpoints.get("mcp"))
            elif protocol == CommunicationProtocol.REST.value:
                return await self._route_via_rest(message, endpoints.get("rest"))
            elif protocol == CommunicationProtocol.WEBSOCKET.value:
                return await self._route_via_websocket(message, endpoints.get("websocket"))
            else:
                # Default to message queue
                return await self._route_via_message_queue(message)
                
        except Exception as e:
            logging.error(f"Protocol routing failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "protocol": "unknown"
            }

    def _select_protocol(self, endpoints: Dict[str, str]) -> str:
        """Select best communication protocol based on available endpoints"""
        if "mcp" in endpoints:
            return CommunicationProtocol.MCP.value
        elif "rest" in endpoints:
            return CommunicationProtocol.REST.value
        elif "websocket" in endpoints:
            return CommunicationProtocol.WEBSOCKET.value
        else:
            return CommunicationProtocol.MESSAGE_QUEUE.value

    async def _route_via_mcp(self, message: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Route message via MCP protocol"""
        # Simulate MCP routing
        return {
            "status": "routed",
            "protocol": "mcp",
            "endpoint": endpoint,
            "routing_time": 0.05  # seconds
        }

    async def _route_via_rest(self, message: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Route message via REST API"""
        # Simulate REST routing
        return {
            "status": "routed",
            "protocol": "rest",
            "endpoint": endpoint,
            "routing_time": 0.1  # seconds
        }

    async def _route_via_websocket(self, message: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Route message via WebSocket"""
        # Simulate WebSocket routing
        return {
            "status": "routed",
            "protocol": "websocket",
            "endpoint": endpoint,
            "routing_time": 0.02  # seconds
        }

    async def _route_via_message_queue(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Route message via message queue"""
        try:
            to_agent = message["to_agent"]
            
            # Add message to agent's queue
            if to_agent in self.message_queues:
                self.message_queues[to_agent].append(message)
            
            return {
                "status": "queued",
                "protocol": "message_queue",
                "queue_length": len(self.message_queues.get(to_agent, [])),
                "routing_time": 0.01  # seconds
            }
            
        except Exception as e:
            logging.error(f"Message queue routing failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "protocol": "message_queue"
            }

    async def broadcast_message(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Broadcast message to multiple agents"""
        try:
            message_type = context.get("message_type", MessageType.BROADCAST.value)
            payload = context.get("payload", {})
            target_agents = context.get("target_agents", [])
            target_agent_types = context.get("target_agent_types", [])
            target_industries = context.get("target_industries", [])
            
            # Determine target agents
            if target_agents:
                agents_to_notify = target_agents
            else:
                agents_to_notify = self._select_agents_by_criteria(target_agent_types, target_industries)
            
            # Create broadcast message
            broadcast_message = {
                "message_id": f"broadcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(context)) % 10000}",
                "message_type": message_type,
                "payload": payload,
                "broadcast_type": "targeted" if target_agents else "filtered",
                "created_at": datetime.now().isoformat()
            }
            
            # Broadcast to selected agents
            broadcast_results = []
            for agent_id in agents_to_notify:
                if agent_id in self.registered_agents:
                    result = await self.route_message({
                        "from_agent": self.agent_id,
                        "to_agent": agent_id,
                        "message_type": message_type,
                        "payload": payload
                    })
                    broadcast_results.append({
                        "agent_id": agent_id,
                        "result": result
                    })
            
            return {
                "success": True,
                "operation": "message_broadcast",
                "broadcast_message_id": broadcast_message["message_id"],
                "target_agents": agents_to_notify,
                "broadcast_results": broadcast_results,
                "total_agents_notified": len(broadcast_results),
                "broadcast_at": datetime.now().isoformat(),
                "agent": self.name
            }
            
        except Exception as e:
            logging.error(f"Message broadcast failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    def _select_agents_by_criteria(self, agent_types: List[str], industries: List[str]) -> List[str]:
        """Select agents based on type and industry criteria"""
        selected_agents = []
        
        for agent_id, agent_record in self.registered_agents.items():
            agent_type = agent_record.get("agent_type", "")
            industry = agent_record.get("industry", "")
            
            # Check if agent matches criteria
            type_match = not agent_types or agent_type in agent_types
            industry_match = not industries or industry in industries
            
            if type_match and industry_match:
                selected_agents.append(agent_id)
        
        return selected_agents

    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of specific agent"""
        try:
            if agent_id not in self.registered_agents:
                return {
                    "success": False,
                    "error": f"Agent {agent_id} is not registered",
                    "agent": self.name
                }
            
            agent_record = self.registered_agents[agent_id]
            queue_length = len(self.message_queues.get(agent_id, []))
            
            return {
                "success": True,
                "agent_id": agent_id,
                "status": agent_record["status"],
                "agent_type": agent_record["agent_type"],
                "industry": agent_record["industry"],
                "capabilities": agent_record["capabilities"],
                "endpoints": agent_record["endpoints"],
                "registered_at": agent_record["registered_at"],
                "last_heartbeat": agent_record["last_heartbeat"],
                "message_count": agent_record["message_count"],
                "error_count": agent_record["error_count"],
                "queue_length": queue_length,
                "agent": self.name
            }
            
        except Exception as e:
            logging.error(f"Agent status retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system communication status"""
        try:
            total_agents = len(self.registered_agents)
            online_agents = sum(1 for agent in self.registered_agents.values() 
                              if agent["status"] == AgentStatus.ONLINE.value)
            
            total_messages = sum(agent["message_count"] for agent in self.registered_agents.values())
            total_errors = sum(agent["error_count"] for agent in self.registered_agents.values())
            
            # Calculate system health
            system_health = "healthy"
            if online_agents / total_agents < 0.8:
                system_health = "degraded"
            if online_agents / total_agents < 0.5:
                system_health = "critical"
            
            return {
                "success": True,
                "system_health": system_health,
                "total_agents": total_agents,
                "online_agents": online_agents,
                "offline_agents": total_agents - online_agents,
                "total_messages": total_messages,
                "total_errors": total_errors,
                "error_rate": total_errors / max(total_messages, 1),
                "protocols_available": self.communication_protocols,
                "last_updated": datetime.now().isoformat(),
                "agent": self.name
            }
            
        except Exception as e:
            logging.error(f"System status retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def _start_health_monitoring(self, agent_id: str):
        """Start health monitoring for an agent"""
        try:
            # Simulate health monitoring start
            logging.info(f"Started health monitoring for agent {agent_id}")
            
            # In a real implementation, this would start a background task
            # to periodically check agent health
            
        except Exception as e:
            logging.error(f"Failed to start health monitoring for agent {agent_id}: {e}")

    async def unregister_agent(self, agent_id: str) -> Dict[str, Any]:
        """Unregister an agent from communication services"""
        try:
            if agent_id not in self.registered_agents:
                return {
                    "success": False,
                    "error": f"Agent {agent_id} is not registered",
                    "agent": self.name
                }
            
            # Remove agent from registry
            del self.registered_agents[agent_id]
            
            # Clear agent's message queue
            if agent_id in self.message_queues:
                del self.message_queues[agent_id]
            
            logging.info(f"Agent {agent_id} unregistered successfully")
            
            return {
                "success": True,
                "operation": "agent_unregistration",
                "agent_id": agent_id,
                "unregistered_at": datetime.now().isoformat(),
                "agent": self.name
            }
            
        except Exception as e:
            logging.error(f"Agent unregistration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    # Abstract methods from IndustryAgent (simplified implementations)
    def _load_industry_regulations(self) -> Dict[str, Any]:
        return {"communication_regulations": "Cross-industry communication regulations"}

    def _load_risk_frameworks(self) -> Dict[str, Any]:
        return {"communication_risk_frameworks": "Communication risk management frameworks"}

    def _load_compliance_frameworks(self) -> Dict[str, Any]:
        return {"communication_compliance_frameworks": "Communication compliance frameworks"}

    def _get_industry_risk_categories(self) -> List[str]:
        return ["communication_risk", "protocol_risk", "security_risk", "availability_risk"]

    def _get_industry_compliance_requirements(self) -> List[Dict[str, Any]]:
        return [{"requirement": "Communication compliance", "category": "general"}]

    def _get_industry_kpis(self) -> Dict[str, Any]:
        return {"communication_kpis": ["message_throughput", "response_time", "availability", "error_rate"]}

    async def _assess_industry_risks(self, business_unit: str, risk_scope: str) -> List[Dict[str, Any]]:
        return [{"risk": "Communication failure risk", "category": "operational", "score": 0.2}]

    async def _calculate_risk_scores(self, risks: List[Dict[str, Any]]) -> Dict[str, float]:
        return {"overall": 0.2}

    async def _generate_risk_recommendations(self, risks: List[Dict[str, Any]], risk_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        return [{"recommendation": "Communication reliability recommendation", "priority": "low"}]

    # Additional abstract methods (simplified implementations)
    async def _get_compliance_requirements(self, framework: str, business_unit: str) -> List[Dict[str, Any]]:
        return [{"requirement": "Communication compliance", "framework": framework}]

    async def _check_compliance_status(self, requirements: List[Dict[str, Any]], check_scope: str) -> Dict[str, Any]:
        return {"status": "compliant", "score": 0.9}

    async def _calculate_compliance_score(self, compliance_results: Dict[str, Any]) -> float:
        return 0.9

    async def _generate_compliance_report(self, compliance_results: Dict[str, Any], compliance_score: float) -> Dict[str, Any]:
        return {"report": "Communication compliance report", "score": compliance_score}

    async def _get_policy_details(self, policy_id: str) -> Dict[str, Any]:
        return {"policy": "Communication policy", "id": policy_id}

    async def _analyze_policy(self, policy: Dict[str, Any], review_type: str) -> Dict[str, Any]:
        return {"analysis": "Communication policy analysis", "type": review_type}

    async def _check_policy_compliance_alignment(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        return {"alignment": "Good", "score": 0.9}

    async def _generate_policy_review_report(self, analysis: Dict[str, Any], alignment: Dict[str, Any]) -> Dict[str, Any]:
        return {"report": "Communication policy review report"}

    async def _create_audit_plan(self, audit_scope: str, audit_type: str, business_units: List[str]) -> Dict[str, Any]:
        return {"plan": "Communication audit plan", "scope": audit_scope}

    async def _schedule_audit_activities(self, audit_plan: Dict[str, Any]) -> Dict[str, Any]:
        return {"schedule": "Communication audit schedule"}

    async def _assign_audit_resources(self, audit_plan: Dict[str, Any]) -> Dict[str, Any]:
        return {"resources": "Communication audit resources"}

    async def _assess_incident_impact(self, incident_type: str, severity: str, description: str) -> Dict[str, Any]:
        return {"impact": "Communication incident impact assessment"}

    async def _generate_incident_response_plan(self, impact_assessment: Dict[str, Any]) -> Dict[str, Any]:
        return {"plan": "Communication incident response plan"}

    async def _execute_incident_response_actions(self, response_plan: Dict[str, Any]) -> Dict[str, Any]:
        return {"actions": "Communication response actions executed"}

    async def _generate_regulatory_report(self, report_type: str, reporting_period: str, regulatory_body: str) -> Dict[str, Any]:
        return {"report": "Communication regulatory report"}

    async def _validate_regulatory_report(self, report: Dict[str, Any]) -> Dict[str, Any]:
        return {"validation": "Communication report validated"}

    async def _submit_regulatory_report(self, report: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        return {"submission": "Communication report submitted"}

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages from MCP broker"""
        try:
            message_type = message.get("type", "unknown")
            
            if message_type == "agent_registration_request":
                return await self.register_agent(message.get("context", {}))
            elif message_type == "message_routing_request":
                return await self.route_message(message.get("context", {}))
            elif message_type == "broadcast_request":
                return await self.broadcast_message(message.get("context", {}))
            elif message_type == "agent_status_request":
                return await self.get_agent_status(message.get("agent_id", ""))
            elif message_type == "system_status_request":
                return await self.get_system_status()
            else:
                return {
                    "success": False,
                    "error": f"Unknown message type: {message_type}",
                    "agent": self.name
                }
                
        except Exception as e:
            logging.error(f"Message processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific communication tasks"""
        try:
            task_type = task.get("type", "unknown")
            
            if task_type == "agent_registration":
                return await self.register_agent(task.get("context", {}))
            elif task_type == "message_routing":
                return await self.route_message(task.get("context", {}))
            elif task_type == "broadcast":
                return await self.broadcast_message(task.get("context", {}))
            elif task_type == "system_monitoring":
                return await self.get_system_status()
            else:
                return {
                    "success": False,
                    "error": f"Unknown task type: {task_type}",
                    "agent": self.name
                }
                
        except Exception as e:
            logging.error(f"Task execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
