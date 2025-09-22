"""
API Gateway Configuration
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ServiceConfig:
    """Configuration for a microservice"""
    name: str
    host: str
    port: int
    health_check_path: str = "/health"
    timeout: int = 30
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 300  # 5 minutes


@dataclass
class GatewayConfig:
    """API Gateway configuration"""
    services: List[ServiceConfig]
    health_check_interval: int = 30
    request_timeout: int = 30
    max_retries: int = 3
    cors_origins: List[str] = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]


# Default service configurations
DEFAULT_SERVICES = [
    ServiceConfig(
        name="policy",
        host="localhost",
        port=8001,
        health_check_path="/health"
    ),
    ServiceConfig(
        name="risk",
        host="localhost", 
        port=8002,
        health_check_path="/health"
    ),
    ServiceConfig(
        name="compliance",
        host="localhost",
        port=8003,
        health_check_path="/health"
    ),
    ServiceConfig(
        name="workflow",
        host="localhost",
        port=8004,
        health_check_path="/health"
    ),
    ServiceConfig(
        name="ai-agents",
        host="localhost",
        port=8005,
        health_check_path="/health"
    ),
]

# Default gateway configuration
DEFAULT_GATEWAY_CONFIG = GatewayConfig(
    services=DEFAULT_SERVICES,
    health_check_interval=30,
    request_timeout=30,
    max_retries=3,
    cors_origins=["*"]
)
