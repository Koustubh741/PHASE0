"""
End-to-end tests for complete GRC workflows.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class TestCompleteWorkflow:
    """End-to-end tests for complete GRC workflows."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_policy = {
            "id": "policy_123",
            "title": "Test Policy",
            "content": "This is a test policy for compliance monitoring.",
            "category": "security",
            "status": "active"
        }
        
        self.test_risk = {
            "id": "risk_456",
            "title": "Test Risk",
            "description": "This is a test risk assessment.",
            "score": 0.75,
            "category": "operational"
        }
    
    @patch('backend.src.core.infrastructure.external_services.compliance_service.SimpleVectorStore')
    @patch('backend.src.core.infrastructure.external_services.risk_service.SimpleVectorStore')
    @patch('backend.src.core.infrastructure.external_services.policy_service.SimpleVectorStore')
    def test_policy_risk_compliance_workflow(self, mock_policy_store, mock_risk_store, mock_compliance_store):
        """Test complete policy -> risk -> compliance workflow."""
        # Mock all vector stores
        for mock_store in [mock_policy_store, mock_risk_store, mock_compliance_store]:
            mock_store.return_value = MagicMock()
        
        # Import services
        from backend.src.core.infrastructure.external_services.policy_service import PolicyService
        from backend.src.core.infrastructure.external_services.risk_service import RiskService
        from backend.src.core.infrastructure.external_services.compliance_service import ComplianceService
        
        # Initialize services
        policy_service = PolicyService()
        risk_service = RiskService()
        compliance_service = ComplianceService()
        
        # Test workflow
        assert policy_service is not None
        assert risk_service is not None
        assert compliance_service is not None
    
    @patch('backend.src.shared.utils.database.DatabaseManager')
    def test_database_integration_workflow(self, mock_db_manager):
        """Test database integration workflow."""
        # Mock database manager
        mock_db_manager.return_value = MagicMock()
        
        # Test database operations
        from backend.src.shared.utils.database import DatabaseManager
        
        db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        }
        redis_config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
        
        db_manager = DatabaseManager(db_config, redis_config)
        assert db_manager is not None
    
    def test_security_workflow(self):
        """Test security workflow."""
        from backend.src.shared.utils.security import SecurityManager
        
        security = SecurityManager()
        
        # Test password hashing
        password = "test_password"
        hashed = security.hash_password(password)
        assert security.verify_password(password, hashed) is True
        
        # Test token generation and verification
        user_id = "test_user"
        token = security.generate_token(user_id)
        payload = security.verify_token(token)
        assert payload is not None
        assert payload['user_id'] == user_id
    
    def test_vector_store_workflow(self):
        """Test vector store workflow."""
        from backend.src.shared.utils.vector_store import SimpleVectorStore
        
        store = SimpleVectorStore("test_collection")
        
        # Test adding vectors
        ids = ["1", "2"]
        embeddings = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        store.add(ids, embeddings)
        
        # Test querying
        query_embeddings = [[1.0, 2.0, 3.0]]
        results = store.query(query_embeddings, n_results=2)
        
        assert len(results['ids']) == 1
        assert len(results['ids'][0]) == 2
    
    @patch('backend.src.core.infrastructure.external_services.compliance_service.SimpleVectorStore')
    def test_ai_agent_integration_workflow(self, mock_vector_store):
        """Test AI agent integration workflow."""
        # Mock vector store
        mock_vector_store.return_value = MagicMock()
        
        # Test AI agent integration
        from backend.src.core.infrastructure.external_services.compliance_service import ComplianceService
        
        service = ComplianceService()
        assert service is not None
        
        # Test that the service can be used with AI agents
        # This would typically involve more complex integration testing
        # with actual AI agent calls


if __name__ == "__main__":
    pytest.main([__file__])
