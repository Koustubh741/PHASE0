"""
Integration tests for GRC services.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class TestServiceIntegration:
    """Integration tests for service interactions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_data = {
            "policy_id": "test_policy_123",
            "risk_score": 0.75,
            "compliance_status": "compliant"
        }
    
    @patch('backend.src.core.infrastructure.external_services.compliance_service.SimpleVectorStore')
    def test_compliance_service_integration(self, mock_vector_store):
        """Test compliance service integration."""
        # Mock the vector store
        mock_store = MagicMock()
        mock_vector_store.return_value = mock_store
        
        # Import and test the service
        from backend.src.core.infrastructure.external_services.compliance_service import ComplianceService
        
        service = ComplianceService()
        assert service is not None
    
    @patch('backend.src.core.infrastructure.external_services.risk_service.SimpleVectorStore')
    def test_risk_service_integration(self, mock_vector_store):
        """Test risk service integration."""
        # Mock the vector store
        mock_store = MagicMock()
        mock_vector_store.return_value = mock_store
        
        # Import and test the service
        from backend.src.core.infrastructure.external_services.risk_service import RiskService
        
        service = RiskService()
        assert service is not None
    
    @patch('backend.src.core.infrastructure.external_services.policy_service.SimpleVectorStore')
    def test_policy_service_integration(self, mock_vector_store):
        """Test policy service integration."""
        # Mock the vector store
        mock_store = MagicMock()
        mock_vector_store.return_value = mock_store
        
        # Import and test the service
        from backend.src.core.infrastructure.external_services.policy_service import PolicyService
        
        service = PolicyService()
        assert service is not None
    
    def test_shared_utilities_integration(self):
        """Test shared utilities integration."""
        # Test vector store
        from backend.src.shared.utils.vector_store import SimpleVectorStore
        store = SimpleVectorStore("test_collection")
        assert store is not None
        
        # Test security manager
        from backend.src.shared.utils.security import SecurityManager
        security = SecurityManager()
        assert security is not None
        
        # Test database manager
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


if __name__ == "__main__":
    pytest.main([__file__])
