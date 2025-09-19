"""
MCP (Management Communication Protocol) Broker
Handles communication between AI agents
"""

import asyncio
import json
import logging
import os
import redis
from typing import Dict, Any, Callable, Optional, List
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class MCPBroker:
    """MCP Broker for inter-agent communication"""
    
    def __init__(self):
        self.redis_client = None
        self.agents = {}
        self.message_handlers = {}
        self.is_running = False
        
    async def initialize(self):
        """Initialize the MCP broker"""
        try:
            # Initialize Redis connection (optional)
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            
            # Test connection
            await self.redis_client.ping()
            
            logger.info("MCP Broker initialized successfully with Redis")
            
        except Exception as e:
            logger.warning(f"Redis not available, MCP broker running in memory mode: {e}")
            self.redis_client = None
            # Don't raise exception, allow the system to work without Redis
    
    async def register_agent(self, agent_id: str, agent):
        """Register an agent with the MCP broker"""
        self.agents[agent_id] = agent
        agent.set_mcp_broker(self)
        
        # Add agent to Redis set
        await self.redis_client.sadd("registered_agents", agent_id)
        
        logger.info(f"Agent {agent_id} registered successfully")
    
    async def send_message(self, message: Dict[str, Any]):
        """Send message via MCP protocol"""
        try:
            message_id = message["header"]["message_id"]
            destination = message["header"]["destination"]
            
            # Store message in Redis with TTL
            await self.redis_client.setex(
                f"message:{message_id}",
                3600,  # 1 hour TTL
                json.dumps(message)
            )
            
            # Publish to destination channel
            await self.redis_client.publish(
                f"agent:{destination}",
                json.dumps(message)
            )
            
            logger.debug(f"Message {message_id} sent to {destination}")
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise
    
    async def start_listening(self):
        """Start listening for incoming messages"""
        self.is_running = True
        
        # Create pubsub for each registered agent
        pubsubs = {}
        for agent_id in self.agents.keys():
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe(f"agent:{agent_id}")
            pubsubs[agent_id] = pubsub
        
        logger.info("MCP Broker started listening for messages")
        
        # Listen for messages
        while self.is_running:
            try:
                for agent_id, pubsub in pubsubs.items():
                    message = await pubsub.get_message(timeout=1.0)
                    if message and message["type"] == "message":
                        await self.handle_incoming_message(agent_id, json.loads(message["data"]))
                
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logger.error(f"Error in message listening loop: {e}")
                await asyncio.sleep(1)
    
    async def handle_incoming_message(self, agent_id: str, message: Dict[str, Any]):
        """Handle incoming message for specific agent"""
        try:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                
                # Process message with agent
                response = await agent.process_message(message["payload"])
                
                # Send response back if needed
                if response and message["header"].get("expects_response"):
                    response_message = {
                        "header": {
                            "message_id": str(uuid.uuid4()),
                            "timestamp": datetime.utcnow().isoformat(),
                            "source": agent_id,
                            "destination": message["header"]["source"],
                            "message_type": "response"
                        },
                        "payload": response
                    }
                    await self.send_message(response_message)
                
                logger.debug(f"Message processed by agent {agent_id}")
                
        except Exception as e:
            logger.error(f"Failed to handle message for agent {agent_id}: {e}")
    
    async def cleanup(self):
        """Cleanup MCP broker resources"""
        self.is_running = False
        
        if self.redis_client:
            await self.redis_client.close()
        
        logger.info("MCP Broker cleaned up")
    
    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent IDs"""
        return list(self.agents.keys())
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast message to all registered agents"""
        for agent_id in self.agents.keys():
            broadcast_msg = {
                "header": {
                    "message_id": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "mcp_broker",
                    "destination": agent_id,
                    "message_type": "broadcast"
                },
                "payload": message
            }
            await self.send_message(broadcast_msg)
