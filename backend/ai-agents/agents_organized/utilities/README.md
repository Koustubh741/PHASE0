# 🛠️ Utilities - Helper Tools & Testing

## Overview
This directory contains utility scripts, testing tools, and helper functions for the GRC Platform AI Agents.

## Utility Files

### Vector Store Utilities
- **`simple_vector_store.py`**: Simple vector database implementation for testing and development

### Testing Utilities
- **`test_ai_agents.py`**: Comprehensive test suite for AI agents
- **`test_optimization_components.py`**: Tests for optimization components

## Utility Categories

### Vector Database
- **Simple Implementation**: Lightweight vector store for development
- **Testing Support**: Vector operations for testing scenarios
- **Development Tools**: Helper functions for vector operations

### Testing Framework
- **Agent Testing**: Comprehensive agent functionality tests
- **Performance Testing**: Performance benchmark tests
- **Integration Testing**: Cross-component integration tests
- **Optimization Testing**: Enhancement feature validation

## Usage Examples

### Vector Store Testing
```python
from utilities.simple_vector_store import SimpleVectorStore

# Initialize vector store
vector_store = SimpleVectorStore()

# Add documents
vector_store.add_document("doc1", "This is a test document")
vector_store.add_document("doc2", "Another test document")

# Search documents
results = vector_store.search("test document", top_k=5)
```

### Agent Testing
```python
from utilities.test_ai_agents import TestAIAgents

# Initialize test suite
test_suite = TestAIAgents()

# Run comprehensive tests
test_suite.run_all_tests()

# Run specific test categories
test_suite.test_bfsi_agent()
test_suite.test_telecom_agent()
test_suite.test_manufacturing_agent()
test_suite.test_healthcare_agent()
test_suite.test_compliance_agent()
```

### Optimization Testing
```python
from utilities.test_optimization_components import TestOptimizationComponents

# Initialize optimization tests
opt_tests = TestOptimizationComponents()

# Test Ollama integration
opt_tests.test_ollama_integration()

# Test Chroma integration
opt_tests.test_chroma_integration()

# Test performance improvements
opt_tests.test_performance_improvements()
```

## Key Features

### Vector Store Utilities
- **Document Management**: Add, update, delete documents
- **Semantic Search**: Vector-based similarity search
- **Batch Operations**: Efficient batch processing
- **Memory Management**: Optimized memory usage

### Testing Utilities
- **Comprehensive Coverage**: Full system testing
- **Performance Benchmarks**: Speed and accuracy testing
- **Integration Validation**: Cross-component testing
- **Regression Testing**: Change impact validation

### Development Support
- **Mock Services**: Simulated external services
- **Test Data**: Sample data for testing
- **Debugging Tools**: Development debugging utilities
- **Performance Profiling**: Performance analysis tools

## Testing Strategy

### Unit Testing
- **Individual Components**: Test each component in isolation
- **Function Testing**: Test individual functions and methods
- **Edge Cases**: Test boundary conditions and error cases
- **Mock Dependencies**: Use mocks for external dependencies

### Integration Testing
- **Component Integration**: Test component interactions
- **API Testing**: Test API endpoints and responses
- **Data Flow Testing**: Test data flow through the system
- **End-to-End Testing**: Test complete user workflows

### Performance Testing
- **Load Testing**: Test under various load conditions
- **Stress Testing**: Test system limits and breaking points
- **Benchmark Testing**: Compare performance metrics
- **Optimization Validation**: Validate performance improvements

## Best Practices

### Testing
- **Automated Testing**: Run tests automatically in CI/CD
- **Test Coverage**: Maintain high test coverage
- **Test Data**: Use consistent test data sets
- **Test Isolation**: Ensure tests don't interfere with each other

### Development
- **Code Quality**: Maintain high code quality standards
- **Documentation**: Document utility functions and usage
- **Error Handling**: Implement proper error handling
- **Performance**: Optimize for performance and efficiency
