"""
BFSI Agent Demo Components
==========================

This module contains demonstration scripts and examples for the BFSI agent,
showcasing various capabilities and use cases.

Components:
- basic_demo: Basic functionality demonstration
- enhanced_demo: Enhanced features demonstration
- ml_demo: Machine learning capabilities demonstration
- integration_demo: Integration and workflow demonstration
"""

from .basic_demo import BFSIBasicDemo
from .enhanced_demo import BFSIEnhancedDemo
from .ml_demo import BFSIMLDemo
from .integration_demo import BFSIIntegrationDemo

__all__ = [
    'BFSIBasicDemo',
    'BFSIEnhancedDemo', 
    'BFSIMLDemo',
    'BFSIIntegrationDemo'
]
