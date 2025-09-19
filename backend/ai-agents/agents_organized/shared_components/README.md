# 🔧 Shared Components - Common Utilities & Base Classes

## Overview
The Shared Components folder contains common utilities, base classes, and shared functionality used across all industry-specific agents. This ensures consistency and reduces code duplication.

## Components

### Base Classes
- **BaseAgent**: Abstract base class for all agents
- **IndustryAgent**: Base class for industry-specific agents
- **MCPBroker**: Management Communication Protocol broker

### Utilities
- **SimpleVectorStore**: Vector database interface for document storage
- **Configuration**: Shared configuration management
- **Logging**: Centralized logging utilities
- **Data Models**: Common data structures and models

### Industry Types & Enums
- **IndustryType**: Enumeration of supported industries
- **GRCOperationType**: Types of GRC operations
- **RiskLevel**: Risk severity levels
- **ComplianceStatus**: Compliance status types

## Files Structure
```
shared_components/
├── README.md                    # This file
├── base_agent.py               # Abstract base agent class
├── industry_agent.py           # Industry-specific agent base class
├── mcp_broker.py              # MCP protocol broker
├── simple_vector_store.py     # Vector database interface
├── config.py                  # Configuration management
├── logging_utils.py           # Logging utilities
├── data_models.py             # Common data structures
├── enums.py                   # Industry types and enums
└── utils.py                   # Common utility functions
```

## Usage Example
```python
from shared_components.industry_agent import IndustryAgent, IndustryType, GRCOperationType
from shared_components.simple_vector_store import SimpleVectorStore

# Create industry-specific agent
class MyIndustryAgent(IndustryAgent):
    def __init__(self):
        super().__init__(IndustryType.MANUFACTURING, "my-agent", "My Agent")
    
    # Implement required methods...

# Use vector store
vector_store = SimpleVectorStore("my-collection", "./data")
vector_store.add_documents([{"content": "document", "metadata": {}}])
```

## Key Features
- **Consistent Interface**: All agents implement the same base interface
- **Shared Functionality**: Common utilities reduce code duplication
- **Type Safety**: Strong typing with enums and data models
- **Extensibility**: Easy to add new industries and operations
- **Configuration**: Centralized configuration management
- **Logging**: Standardized logging across all agents
