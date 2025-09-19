"""
Advanced MCP Protocol Implementation
Enhanced communication protocol for multi-agent GRC systems
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import uuid
from dataclasses import dataclass, asdict
import hashlib
import hmac
import base64
from cryptography.fernet import Fernet
import redis
import numpy as np

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """MCP Message Types"""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    TASK_DELEGATION = "task_delegation"
    COLLABORATION_REQUEST = "collaboration_request"
    COLLABORATION_RESPONSE = "collaboration_response"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"
    PERFORMANCE_UPDATE = "performance_update"
    CAPABILITY_ANNOUNCEMENT = "capability_announcement"
    FAILOVER_REQUEST = "failover_request"
    FAILOVER_RESPONSE = "failover_response"
    CONSENSUS_REQUEST = "consensus_request"
    CONSENSUS_RESPONSE = "consensus_response"

class MessagePriority(Enum):
    """Message Priority Levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class MessageStatus(Enum):
    """Message Status"""
    SENT = "sent"
    DELIVERED = "delivered"
    PROCESSED = "processed"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class MCPHeader:
    """MCP Message Header"""
    message_id: str
    timestamp: datetime
    source_agent: str
    destination_agent: Optional[str]
    message_type: MessageType
    priority: MessagePriority
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    ttl: int = 3600  # Time to live in seconds
    encryption_required: bool = False
    signature: Optional[str] = None

@dataclass
class MCPPayload:
    """MCP Message Payload"""
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    attachments: List[Dict[str, Any]] = None
    validation_hash: Optional[str] = None

@dataclass
class MCPMessage:
    """Complete MCP Message"""
    header: MCPHeader
    payload: MCPPayload
    status: MessageStatus = MessageStatus.SENT
    retry_count: int = 0
    max_retries: int = 3

class AdvancedMCPBroker:
    """
    Advanced MCP Broker with enhanced features
    Superior to traditional Archer communication
    """
    
    def __init__(self, encryption_key: Optional[str] = None):
        self.redis_client = None
        self.agents = {}
        self.message_handlers = {}
        self.encryption_key = encryption_key
        self.cipher_suite = None
        self.is_running = False
        self.message_queue = asyncio.Queue()
        self.performance_metrics = {}
        self.circuit_breakers = {}
        self.rate_limiters = {}
        
        # Initialize encryption if key provided
        if encryption_key:
            self.cipher_suite = Fernet(encryption_key.encode())
    
    async def initialize(self):
        """Initialize the advanced MCP broker"""
        try:
            # Initialize Redis connection with advanced configuration
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            self.redis_client = redis.from_url(
                redis_url, 
                decode_responses=True,
                socket_keepalive=True,
                socket_keepalive_options={},
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            await self.redis_client.ping()
            
            # Initialize performance tracking
            await self._initialize_performance_tracking()
            
            # Start background services
            await self._start_background_services()
            
            logger.info("Advanced MCP Broker initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Advanced MCP Broker: {e}")
            raise
    
    async def _initialize_performance_tracking(self):
        """Initialize performance tracking for agents"""
        # Initialize performance metrics for each agent
        for agent_id in self.agents.keys():
            self.performance_metrics[agent_id] = {
                "message_count": 0,
                "success_rate": 1.0,
                "avg_response_time": 0.0,
                "error_count": 0,
                "last_activity": datetime.now()
            }
            
            # Initialize circuit breaker
            self.circuit_breakers[agent_id] = {
                "failure_count": 0,
                "last_failure": None,
                "state": "closed",  # closed, open, half-open
                "threshold": 5
            }
            
            # Initialize rate limiter
            self.rate_limiters[agent_id] = {
                "request_count": 0,
                "window_start": datetime.now(),
                "limit": 100,  # requests per minute
                "window_size": 60  # seconds
            }
    
    async def _start_background_services(self):
        """Start background services"""
        # Start message processing
        asyncio.create_task(self._process_message_queue())
        
        # Start performance monitoring
        asyncio.create_task(self._monitor_performance())
        
        # Start circuit breaker monitoring
        asyncio.create_task(self._monitor_circuit_breakers())
        
        # Start cleanup service
        asyncio.create_task(self._cleanup_expired_messages())
    
    async def register_agent(self, agent_id: str, agent, capabilities: List[str] = None):
        """Register an agent with enhanced capabilities"""
        try:
            self.agents[agent_id] = agent
            agent.set_mcp_broker(self)
            
            # Store agent capabilities
            if capabilities:
                await self.redis_client.hset(
                    f"agent:{agent_id}:capabilities",
                    mapping={cap: "true" for cap in capabilities}
                )
            
            # Add to registered agents set
            await self.redis_client.sadd("registered_agents", agent_id)
            
            # Announce agent registration
            await self._announce_agent_registration(agent_id, capabilities)
            
            logger.info(f"Agent {agent_id} registered with capabilities: {capabilities}")
            
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            raise
    
    async def send_message(self, message: MCPMessage) -> str:
        """Send message with advanced features"""
        try:
            # Validate message
            if not self._validate_message(message):
                raise ValueError("Invalid message format")
            
            # Check circuit breaker
            if self._is_circuit_breaker_open(message.header.destination_agent):
                raise Exception(f"Circuit breaker open for agent {message.header.destination_agent}")
            
            # Check rate limiting
            if not self._check_rate_limit(message.header.source_agent):
                raise Exception(f"Rate limit exceeded for agent {message.header.source_agent}")
            
            # Encrypt message if required
            if message.header.encryption_required:
                message = await self._encrypt_message(message)
            
            # Add signature
            message.header.signature = self._generate_signature(message)
            
            # Store message with TTL
            message_key = f"message:{message.header.message_id}"
            message_data = self._serialize_message(message)
            
            await self.redis_client.setex(
                message_key,
                message.header.ttl,
                message_data
            )
            
            # Publish to destination
            if message.header.destination_agent:
                # Direct message
                await self.redis_client.publish(
                    f"agent:{message.header.destination_agent}",
                    message_data
                )
            else:
                # Broadcast message
                await self._broadcast_message(message)
            
            # Update performance metrics
            await self._update_performance_metrics(message.header.source_agent, success=True)
            
            # Add to message queue for processing
            await self.message_queue.put(message)
            
            logger.debug(f"Message {message.header.message_id} sent successfully")
            return message.header.message_id
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            await self._update_performance_metrics(message.header.source_agent, success=False)
            raise
    
    async def send_task_request(self, 
                              source_agent: str,
                              destination_agent: str,
                              task_data: Dict[str, Any],
                              priority: MessagePriority = MessagePriority.MEDIUM,
                              timeout: int = 300) -> str:
        """Send task request with advanced features"""
        try:
            message = MCPMessage(
                header=MCPHeader(
                    message_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source_agent=source_agent,
                    destination_agent=destination_agent,
                    message_type=MessageType.TASK_REQUEST,
                    priority=priority,
                    ttl=timeout
                ),
                payload=MCPPayload(
                    data=task_data,
                    metadata={
                        "task_type": task_data.get("type", "unknown"),
                        "complexity": task_data.get("complexity", 0.5),
                        "deadline": task_data.get("deadline"),
                        "required_capabilities": task_data.get("capabilities", [])
                    }
                )
            )
            
            return await self.send_message(message)
            
        except Exception as e:
            logger.error(f"Failed to send task request: {e}")
            raise
    
    async def send_collaboration_request(self,
                                       source_agent: str,
                                       target_agents: List[str],
                                       collaboration_data: Dict[str, Any],
                                       consensus_required: bool = False) -> str:
        """Send collaboration request to multiple agents"""
        try:
            correlation_id = str(uuid.uuid4())
            responses = []
            
            for target_agent in target_agents:
                message = MCPMessage(
                    header=MCPHeader(
                        message_id=str(uuid.uuid4()),
                        timestamp=datetime.now(),
                        source_agent=source_agent,
                        destination_agent=target_agent,
                        message_type=MessageType.COLLABORATION_REQUEST,
                        priority=MessagePriority.HIGH,
                        correlation_id=correlation_id
                    ),
                    payload=MCPPayload(
                        data=collaboration_data,
                        metadata={
                            "consensus_required": consensus_required,
                            "target_agents": target_agents,
                            "collaboration_type": collaboration_data.get("type", "general")
                        }
                    )
                )
                
                message_id = await self.send_message(message)
                responses.append(message_id)
            
            return correlation_id
            
        except Exception as e:
            logger.error(f"Failed to send collaboration request: {e}")
            raise
    
    async def request_consensus(self,
                              source_agent: str,
                              target_agents: List[str],
                              consensus_data: Dict[str, Any],
                              timeout: int = 60) -> Dict[str, Any]:
        """Request consensus from multiple agents"""
        try:
            correlation_id = str(uuid.uuid4())
            consensus_responses = {}
            
            # Send consensus request to all target agents
            for target_agent in target_agents:
                message = MCPMessage(
                    header=MCPHeader(
                        message_id=str(uuid.uuid4()),
                        timestamp=datetime.now(),
                        source_agent=source_agent,
                        destination_agent=target_agent,
                        message_type=MessageType.CONSENSUS_REQUEST,
                        priority=MessagePriority.HIGH,
                        correlation_id=correlation_id
                    ),
                    payload=MCPPayload(
                        data=consensus_data,
                        metadata={
                            "consensus_type": consensus_data.get("type", "general"),
                            "timeout": timeout,
                            "required_agents": len(target_agents)
                        }
                    )
                )
                
                await self.send_message(message)
            
            # Wait for consensus responses
            start_time = datetime.now()
            while (datetime.now() - start_time).seconds < timeout:
                # Check for responses
                responses = await self._get_consensus_responses(correlation_id)
                if len(responses) >= len(target_agents):
                    break
                await asyncio.sleep(1)
            
            # Calculate consensus
            consensus_result = await self._calculate_consensus(responses)
            
            return {
                "consensus_id": correlation_id,
                "consensus_reached": consensus_result["consensus_reached"],
                "consensus_value": consensus_result["consensus_value"],
                "participating_agents": list(responses.keys()),
                "confidence_score": consensus_result["confidence_score"]
            }
            
        except Exception as e:
            logger.error(f"Failed to request consensus: {e}")
            raise
    
    async def _process_message_queue(self):
        """Process message queue for monitoring and analytics"""
        while self.is_running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                
                # Process message for analytics
                await self._process_message_for_analytics(message)
                
                # Check for message patterns
                await self._analyze_message_patterns(message)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing message queue: {e}")
                await asyncio.sleep(1)
    
    async def _monitor_performance(self):
        """Monitor agent performance continuously"""
        while self.is_running:
            try:
                # Update performance metrics
                await self._update_all_performance_metrics()
                
                # Check for performance anomalies
                await self._detect_performance_anomalies()
                
                # Adjust circuit breakers
                await self._adjust_circuit_breakers()
                
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in performance monitoring: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_circuit_breakers(self):
        """Monitor and manage circuit breakers"""
        while self.is_running:
            try:
                for agent_id, breaker in self.circuit_breakers.items():
                    if breaker["state"] == "open":
                        # Check if enough time has passed to try half-open
                        if breaker["last_failure"] and \
                           (datetime.now() - breaker["last_failure"]).seconds > 300:  # 5 minutes
                            breaker["state"] = "half-open"
                            logger.info(f"Circuit breaker for {agent_id} moved to half-open")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error monitoring circuit breakers: {e}")
                await asyncio.sleep(120)
    
    async def _cleanup_expired_messages(self):
        """Clean up expired messages"""
        while self.is_running:
            try:
                # Get all message keys
                message_keys = await self.redis_client.keys("message:*")
                
                for key in message_keys:
                    ttl = await self.redis_client.ttl(key)
                    if ttl == -1:  # No TTL set, set one
                        await self.redis_client.expire(key, 3600)
                    elif ttl == -2:  # Key doesn't exist
                        continue
                
                await asyncio.sleep(300)  # Cleanup every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in message cleanup: {e}")
                await asyncio.sleep(600)
    
    def _validate_message(self, message: MCPMessage) -> bool:
        """Validate message format and content"""
        if not message.header.message_id:
            return False
        
        if not message.header.source_agent:
            return False
        
        if not message.payload.data:
            return False
        
        return True
    
    def _is_circuit_breaker_open(self, agent_id: str) -> bool:
        """Check if circuit breaker is open for agent"""
        if agent_id not in self.circuit_breakers:
            return False
        
        return self.circuit_breakers[agent_id]["state"] == "open"
    
    def _check_rate_limit(self, agent_id: str) -> bool:
        """Check if agent is within rate limits"""
        if agent_id not in self.rate_limiters:
            return True
        
        limiter = self.rate_limiters[agent_id]
        now = datetime.now()
        
        # Reset window if needed
        if (now - limiter["window_start"]).seconds >= limiter["window_size"]:
            limiter["request_count"] = 0
            limiter["window_start"] = now
        
        # Check limit
        if limiter["request_count"] >= limiter["limit"]:
            return False
        
        limiter["request_count"] += 1
        return True
    
    async def _encrypt_message(self, message: MCPMessage) -> MCPMessage:
        """Encrypt message payload"""
        if not self.cipher_suite:
            return message
        
        try:
            # Encrypt payload data
            encrypted_data = self.cipher_suite.encrypt(
                json.dumps(message.payload.data).encode()
            )
            
            message.payload.data = {
                "encrypted": True,
                "data": base64.b64encode(encrypted_data).decode()
            }
            
            return message
            
        except Exception as e:
            logger.error(f"Failed to encrypt message: {e}")
            raise
    
    def _generate_signature(self, message: MCPMessage) -> str:
        """Generate message signature for integrity"""
        try:
            # Create signature data
            signature_data = f"{message.header.message_id}:{message.header.timestamp}:{json.dumps(message.payload.data)}"
            
            # Generate HMAC signature
            signature = hmac.new(
                self.encryption_key.encode() if self.encryption_key else b"default",
                signature_data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return signature
            
        except Exception as e:
            logger.error(f"Failed to generate signature: {e}")
            return ""
    
    def _serialize_message(self, message: MCPMessage) -> str:
        """Serialize message for storage/transmission"""
        try:
            # Convert to dict
            message_dict = {
                "header": asdict(message.header),
                "payload": asdict(message.payload),
                "status": message.status.value,
                "retry_count": message.retry_count,
                "max_retries": message.max_retries
            }
            
            # Convert datetime to string
            message_dict["header"]["timestamp"] = message.header.timestamp.isoformat()
            
            return json.dumps(message_dict)
            
        except Exception as e:
            logger.error(f"Failed to serialize message: {e}")
            raise
    
    async def _broadcast_message(self, message: MCPMessage):
        """Broadcast message to all agents"""
        try:
            # Publish to broadcast channel
            await self.redis_client.publish("broadcast", self._serialize_message(message))
            
        except Exception as e:
            logger.error(f"Failed to broadcast message: {e}")
            raise
    
    async def _announce_agent_registration(self, agent_id: str, capabilities: List[str]):
        """Announce agent registration to other agents"""
        try:
            announcement = MCPMessage(
                header=MCPHeader(
                    message_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source_agent="mcp_broker",
                    destination_agent=None,  # Broadcast
                    message_type=MessageType.CAPABILITY_ANNOUNCEMENT,
                    priority=MessagePriority.MEDIUM
                ),
                payload=MCPPayload(
                    data={
                        "agent_id": agent_id,
                        "capabilities": capabilities or [],
                        "registration_time": datetime.now().isoformat()
                    },
                    metadata={
                        "announcement_type": "agent_registration"
                    }
                )
            )
            
            await self._broadcast_message(announcement)
            
        except Exception as e:
            logger.error(f"Failed to announce agent registration: {e}")
    
    async def _update_performance_metrics(self, agent_id: str, success: bool):
        """Update performance metrics for agent"""
        if agent_id not in self.performance_metrics:
            self.performance_metrics[agent_id] = {
                "message_count": 0,
                "success_rate": 1.0,
                "avg_response_time": 0.0,
                "error_count": 0,
                "last_activity": datetime.now()
            }
        
        metrics = self.performance_metrics[agent_id]
        metrics["message_count"] += 1
        metrics["last_activity"] = datetime.now()
        
        if not success:
            metrics["error_count"] += 1
        
        # Update success rate
        metrics["success_rate"] = 1.0 - (metrics["error_count"] / metrics["message_count"])
        
        # Update circuit breaker
        if not success:
            breaker = self.circuit_breakers.get(agent_id, {})
            breaker["failure_count"] = breaker.get("failure_count", 0) + 1
            breaker["last_failure"] = datetime.now()
            
            if breaker["failure_count"] >= breaker.get("threshold", 5):
                breaker["state"] = "open"
                logger.warning(f"Circuit breaker opened for agent {agent_id}")
    
    async def _update_all_performance_metrics(self):
        """Update performance metrics for all agents"""
        # This would typically involve querying Redis for message statistics
        # and updating the in-memory metrics
        pass
    
    async def _detect_performance_anomalies(self):
        """Detect performance anomalies across agents"""
        try:
            for agent_id, metrics in self.performance_metrics.items():
                # Check for high error rate
                if metrics["success_rate"] < 0.8:
                    logger.warning(f"High error rate detected for agent {agent_id}: {1 - metrics['success_rate']:.2%}")
                
                # Check for inactivity
                if (datetime.now() - metrics["last_activity"]).seconds > 300:  # 5 minutes
                    logger.warning(f"Agent {agent_id} inactive for {(datetime.now() - metrics['last_activity']).seconds} seconds")
        
        except Exception as e:
            logger.error(f"Error detecting performance anomalies: {e}")
    
    async def _adjust_circuit_breakers(self):
        """Adjust circuit breaker thresholds based on performance"""
        try:
            for agent_id, metrics in self.performance_metrics.items():
                breaker = self.circuit_breakers.get(agent_id, {})
                
                # Adjust threshold based on success rate
                if metrics["success_rate"] > 0.95:
                    breaker["threshold"] = max(3, breaker.get("threshold", 5) - 1)
                elif metrics["success_rate"] < 0.8:
                    breaker["threshold"] = min(10, breaker.get("threshold", 5) + 1)
        
        except Exception as e:
            logger.error(f"Error adjusting circuit breakers: {e}")
    
    async def _process_message_for_analytics(self, message: MCPMessage):
        """Process message for analytics and insights"""
        try:
            # Store message analytics in Redis
            analytics_key = f"analytics:message:{message.header.message_id}"
            analytics_data = {
                "timestamp": message.header.timestamp.isoformat(),
                "source": message.header.source_agent,
                "destination": message.header.destination_agent,
                "type": message.header.message_type.value,
                "priority": message.header.priority.value,
                "size": len(self._serialize_message(message))
            }
            
            await self.redis_client.hset(analytics_key, mapping=analytics_data)
            await self.redis_client.expire(analytics_key, 86400)  # 24 hours TTL
        
        except Exception as e:
            logger.error(f"Error processing message for analytics: {e}")
    
    async def _analyze_message_patterns(self, message: MCPMessage):
        """Analyze message patterns for insights"""
        try:
            # This would implement pattern analysis for:
            # - Communication patterns between agents
            # - Message frequency analysis
            # - Performance correlation analysis
            # - Anomaly detection in communication
            pass
        
        except Exception as e:
            logger.error(f"Error analyzing message patterns: {e}")
    
    async def _get_consensus_responses(self, correlation_id: str) -> Dict[str, Any]:
        """Get consensus responses for correlation ID"""
        try:
            # Query Redis for responses with matching correlation ID
            response_keys = await self.redis_client.keys(f"consensus_response:{correlation_id}:*")
            responses = {}
            
            for key in response_keys:
                response_data = await self.redis_client.hgetall(key)
                if response_data:
                    agent_id = key.split(":")[-1]
                    responses[agent_id] = json.loads(response_data.get("data", "{}"))
            
            return responses
        
        except Exception as e:
            logger.error(f"Error getting consensus responses: {e}")
            return {}
    
    async def _calculate_consensus(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate consensus from multiple responses"""
        try:
            if not responses:
                return {
                    "consensus_reached": False,
                    "consensus_value": None,
                    "confidence_score": 0.0
                }
            
            # Simple consensus calculation (can be made more sophisticated)
            values = [resp.get("value") for resp in responses.values() if "value" in resp]
            
            if not values:
                return {
                    "consensus_reached": False,
                    "consensus_value": None,
                    "confidence_score": 0.0
                }
            
            # Calculate consensus (simplified - could use more sophisticated algorithms)
            consensus_value = max(set(values), key=values.count) if values else None
            consensus_count = values.count(consensus_value) if consensus_value else 0
            consensus_reached = consensus_count > len(values) / 2
            
            confidence_score = consensus_count / len(values) if values else 0.0
            
            return {
                "consensus_reached": consensus_reached,
                "consensus_value": consensus_value,
                "confidence_score": confidence_score
            }
        
        except Exception as e:
            logger.error(f"Error calculating consensus: {e}")
            return {
                "consensus_reached": False,
                "consensus_value": None,
                "confidence_score": 0.0
            }
    
    async def get_system_analytics(self) -> Dict[str, Any]:
        """Get comprehensive system analytics"""
        try:
            return {
                "total_agents": len(self.agents),
                "performance_metrics": self.performance_metrics,
                "circuit_breaker_status": {
                    agent_id: breaker["state"] 
                    for agent_id, breaker in self.circuit_breakers.items()
                },
                "rate_limiter_status": {
                    agent_id: {
                        "current_requests": limiter["request_count"],
                        "limit": limiter["limit"],
                        "window_remaining": limiter["window_size"] - (datetime.now() - limiter["window_start"]).seconds
                    }
                    for agent_id, limiter in self.rate_limiters.items()
                },
                "message_queue_size": self.message_queue.qsize(),
                "system_health": self._calculate_system_health()
            }
        
        except Exception as e:
            logger.error(f"Error getting system analytics: {e}")
            return {}
    
    def _calculate_system_health(self) -> float:
        """Calculate overall system health score"""
        try:
            if not self.performance_metrics:
                return 1.0
            
            health_scores = []
            for metrics in self.performance_metrics.values():
                health = metrics["success_rate"]
                health_scores.append(health)
            
            return np.mean(health_scores) if health_scores else 1.0
        
        except Exception as e:
            logger.error(f"Error calculating system health: {e}")
            return 0.0
    
    async def cleanup(self):
        """Cleanup broker resources"""
        self.is_running = False
        
        if self.redis_client:
            await self.redis_client.close()
        
        logger.info("Advanced MCP Broker cleaned up")

# Import os for environment variables
import os
