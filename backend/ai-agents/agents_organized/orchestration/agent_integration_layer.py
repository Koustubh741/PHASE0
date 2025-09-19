"""
Agent Integration Layer - Central hub for connecting existing agents with new multi-agent strategy
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class IntegrationManager:
    """Manages integration between old and new agent systems"""
    
    def __init__(self):
        self.old_agents = {}
        self.new_agents = {}
        self.integration_status = {}
        
    async def register_old_agent(self, agent_id: str, agent_instance: Any):
        """Register an old agent for integration"""
        self.old_agents[agent_id] = agent_instance
        self.integration_status[agent_id] = "registered"
        logger.info(f"Registered old agent: {agent_id}")
        
    async def register_new_agent(self, agent_id: str, agent_instance: Any):
        """Register a new agent for integration"""
        self.new_agents[agent_id] = agent_instance
        self.integration_status[agent_id] = "registered"
        logger.info(f"Registered new agent: {agent_id}")
        
    async def get_integration_status(self) -> Dict[str, str]:
        """Get current integration status"""
        return self.integration_status.copy()

# Global integration manager instance
integration_manager = IntegrationManager()



