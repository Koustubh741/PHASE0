"""
Base Agent Class
Abstract base class for all AI agents in the GRC platform
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio
import json
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.status = "inactive"
        self.last_activity = None
        self.mcp_broker = None
        
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages"""
        pass
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific tasks"""
        pass
    
    async def send_message(self, target_agent: str, message: Dict[str, Any]):
        """Send message to another agent via MCP"""
        if not self.mcp_broker:
            logger.warning(f"Agent {self.agent_id} has no MCP broker connection")
            return
            
        mcp_message = {
            "header": {
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "source": self.agent_id,
                "destination": target_agent,
                "message_type": message.get("type", "general")
            },
            "payload": message
        }
        
        try:
            await self.mcp_broker.send_message(mcp_message)
            logger.info(f"Message sent from {self.agent_id} to {target_agent}")
        except Exception as e:
            logger.error(f"Failed to send message from {self.agent_id} to {target_agent}: {e}")
    
    def update_status(self, status: str):
        """Update agent status"""
        self.status = status
        self.last_activity = datetime.utcnow()
        logger.info(f"Agent {self.agent_id} status updated to: {status}")
    
    def set_mcp_broker(self, broker):
        """Set MCP broker reference"""
        self.mcp_broker = broker
    
    async def start(self):
        """Start the agent"""
        self.update_status("active")
        logger.info(f"Agent {self.agent_id} started")
    
    async def stop(self):
        """Stop the agent"""
        self.update_status("inactive")
        logger.info(f"Agent {self.agent_id} stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }
