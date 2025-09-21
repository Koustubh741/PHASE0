"""
BFSI Agent Configuration Components
===================================

This module contains all configuration, constants, and settings for the BFSI agent,
providing centralized configuration management.

Components:
- settings: Main configuration settings and constants
- regulations: Regulatory framework definitions and constants
- prompts: AI prompts and templates for reasoning
- categories: Document categories and classification
"""

from .settings import *
from .regulations import *
from .prompts import *
from .categories import *

__all__ = [
    # Settings
    'BFSI_CONFIG', 'BFSI_SETTINGS',
    
    # Regulations
    'BFSI_REGULATION_TYPES', 'BFSI_REGULATORY_BODIES',
    
    # Prompts
    'BFSI_PROMPTS', 'AnalysisPrompt',
    
    # Categories
    'BFSI_DOCUMENT_CATEGORIES', 'BFSI_CATEGORY_MAPPING'
]
