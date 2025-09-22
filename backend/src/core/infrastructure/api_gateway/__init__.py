"""
API Gateway module for GRC Platform
"""

from .gateway import APIGateway, ServiceRegistry, get_api_gateway
from .main import app as gateway_app

__all__ = [
    "APIGateway",
    "ServiceRegistry", 
    "get_api_gateway",
    "gateway_app"
]
