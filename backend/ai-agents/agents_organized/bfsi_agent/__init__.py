"""
BFSI Agent Package
Banking, Financial Services, and Insurance GRC Agent
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from .bfsi_grc_agent import BFSIGRCAgent
    from .bfsi_config import BFSI_CONFIG
except ImportError:
    # Fallback for standalone execution
    from bfsi_grc_agent import BFSIGRCAgent
    from bfsi_config import BFSI_CONFIG

__all__ = ['BFSIGRCAgent', 'BFSI_CONFIG']



