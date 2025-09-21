"""
Integration tests for User API endpoints
Tests complete user management workflows with database interactions
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import json
from datetime import datetime

from src.core.presentation.api.main import app
from src.core.domain.entities.user import User, UserStatus, UserRole
from src.core.application.dto.user_dto import UserCreateRequest, UserUpdateRequest


@pytest.fixture
def client():
    """Test client for API testing"""
    return TestClient(app)


@pytest.fixture
def async_client():
    """Async test client for API testing"""
    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "admin",
        "organization_id": "org-123",
        "department": "IT",
        "job_title": "Developer",
        "phone": "+1234567890",
        "password": "TestPassword123!"
    }


@pytest.fixture
def mock_jwt_token():
    """Mock JWT token for authentication"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXItaWQiLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIiwicm9sZSI6ImFkbWluIiwib3JnYW5pemF0aW9uX2lkIjoib3JnLTEyMyJ9.test-signature"


class TestUserAPIIntegration:
    """Integration tests for User API"""
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, async_client, sample_user_data, mock_jwt_token):
        """Test successful user creation"""
        # Arrange
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            # Mock the controller and its methods
            mock_controller.return_value.create_user = AsyncMock()
            mock_controller.return_value.create_user.return_value = {
                "id": "user-123",
                "username": "testuser",
                "email": "test@example.com",
                "status": "pending_activation"
            }
            
            # Act
            response = await async_client.post(
                "/api/v1/users",
                json=sample_user_data,
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_create_user_unauthorized(self, async_client, sample_user_data):
        """Test user creation without authentication"""
        # Act
        response = await async_client.post("/api/v1/users", json=sample_user_data)
        
        # Assert
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_create_user_invalid_data(self, async_client, mock_jwt_token):
        """Test user creation with invalid data"""
        # Arrange
        invalid_data = {
            "username": "ab",  # Too short
            "email": "invalid-email",
            "first_name": "",
            "role": "invalid_role"
        }
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        # Act
        response = await async_client.post(
            "/api/v1/users",
            json=invalid_data,
            headers=headers
        )
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, async_client, mock_jwt_token):
        """Test successful user retrieval"""
        # Arrange
        user_id = "user-123"
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.get_user = AsyncMock()
            mock_controller.return_value.get_user.return_value = {
                "id": user_id,
                "username": "testuser",
                "email": "test@example.com",
                "role": "admin",
                "status": "active"
            }
            
            # Act
            response = await async_client.get(
                f"/api/v1/users/{user_id}",
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "testuser"
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, async_client, mock_jwt_token):
        """Test user retrieval when user doesn't exist"""
        # Arrange
        user_id = "nonexistent-user"
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.get_user = AsyncMock()
            mock_controller.return_value.get_user.side_effect = Exception("User not found")
            
            # Act
            response = await async_client.get(
                f"/api/v1/users/{user_id}",
                headers=headers
            )
        
        # Assert
        assert response.status_code == 500  # Internal server error
    
    @pytest.mark.asyncio
    async def test_update_user_success(self, async_client, mock_jwt_token):
        """Test successful user update"""
        # Arrange
        user_id = "user-123"
        update_data = {
            "first_name": "Updated",
            "department": "Engineering"
        }
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.update_user = AsyncMock()
            mock_controller.return_value.update_user.return_value = {
                "id": user_id,
                "username": "testuser",
                "first_name": "Updated",
                "department": "Engineering"
            }
            
            # Act
            response = await async_client.put(
                f"/api/v1/users/{user_id}",
                json=update_data,
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["department"] == "Engineering"
    
    @pytest.mark.asyncio
    async def test_delete_user_success(self, async_client, mock_jwt_token):
        """Test successful user deletion"""
        # Arrange
        user_id = "user-123"
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.delete_user = AsyncMock()
            mock_controller.return_value.delete_user.return_value = {
                "message": "User deleted successfully"
            }
            
            # Act
            response = await async_client.delete(
                f"/api/v1/users/{user_id}",
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data["message"]
    
    @pytest.mark.asyncio
    async def test_list_users_success(self, async_client, mock_jwt_token):
        """Test successful user listing"""
        # Arrange
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.list_users = AsyncMock()
            mock_controller.return_value.list_users.return_value = {
                "users": [
                    {
                        "id": "user-1",
                        "username": "user1",
                        "email": "user1@example.com",
                        "role": "admin"
                    },
                    {
                        "id": "user-2",
                        "username": "user2",
                        "email": "user2@example.com",
                        "role": "viewer"
                    }
                ],
                "total": 2,
                "skip": 0,
                "limit": 100
            }
            
            # Act
            response = await async_client.get(
                "/api/v1/users",
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) == 2
        assert data["total"] == 2
    
    @pytest.mark.asyncio
    async def test_list_users_with_filters(self, async_client, mock_jwt_token):
        """Test user listing with filters"""
        # Arrange
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        params = {
            "role": "admin",
            "status": "active",
            "skip": 0,
            "limit": 10
        }
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.list_users = AsyncMock()
            mock_controller.return_value.list_users.return_value = {
                "users": [],
                "total": 0,
                "skip": 0,
                "limit": 10
            }
            
            # Act
            response = await async_client.get(
                "/api/v1/users",
                params=params,
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
    
    @pytest.mark.asyncio
    async def test_search_users_success(self, async_client, mock_jwt_token):
        """Test successful user search"""
        # Arrange
        search_data = {
            "query": "test",
            "skip": 0,
            "limit": 10
        }
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.search_users = AsyncMock()
            mock_controller.return_value.search_users.return_value = {
                "users": [
                    {
                        "id": "user-1",
                        "username": "testuser",
                        "email": "test@example.com"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 10
            }
            
            # Act
            response = await async_client.post(
                "/api/v1/users/search",
                json=search_data,
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) == 1
        assert data["users"][0]["username"] == "testuser"
    
    @pytest.mark.asyncio
    async def test_change_user_role_success(self, async_client, mock_jwt_token):
        """Test successful user role change"""
        # Arrange
        user_id = "user-123"
        role_change_data = {
            "role": "viewer",
            "reason": "Role downgrade for security"
        }
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.change_user_role = AsyncMock()
            mock_controller.return_value.change_user_role.return_value = {
                "id": user_id,
                "username": "testuser",
                "role": "viewer"
            }
            
            # Act
            response = await async_client.patch(
                f"/api/v1/users/{user_id}/role",
                json=role_change_data,
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "viewer"
    
    @pytest.mark.asyncio
    async def test_change_user_status_success(self, async_client, mock_jwt_token):
        """Test successful user status change"""
        # Arrange
        user_id = "user-123"
        status_change_data = {
            "status": "suspended",
            "reason": "Security violation"
        }
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.change_user_status = AsyncMock()
            mock_controller.return_value.change_user_status.return_value = {
                "id": user_id,
                "username": "testuser",
                "status": "suspended"
            }
            
            # Act
            response = await async_client.patch(
                f"/api/v1/users/{user_id}/status",
                json=status_change_data,
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "suspended"
    
    @pytest.mark.asyncio
    async def test_bulk_update_users_success(self, async_client, mock_jwt_token):
        """Test successful bulk user update"""
        # Arrange
        bulk_update_data = {
            "user_ids": ["user-1", "user-2"],
            "updates": {
                "department": "Engineering"
            }
        }
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.bulk_update_users = AsyncMock()
            mock_controller.return_value.bulk_update_users.return_value = {
                "successful": 2,
                "failed": 0,
                "errors": [],
                "total": 2
            }
            
            # Act
            response = await async_client.post(
                "/api/v1/users/bulk-update",
                json=bulk_update_data,
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] == 2
        assert data["failed"] == 0
    
    @pytest.mark.asyncio
    async def test_get_user_statistics_success(self, async_client, mock_jwt_token):
        """Test successful user statistics retrieval"""
        # Arrange
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
            mock_controller.return_value.get_user_statistics = AsyncMock()
            mock_controller.return_value.get_user_statistics.return_value = {
                "total_users": 100,
                "active_users": 95,
                "inactive_users": 3,
                "suspended_users": 2,
                "users_by_role": {
                    "admin": 5,
                    "auditor": 10,
                    "risk_owner": 20,
                    "control_owner": 30,
                    "viewer": 35
                }
            }
            
            # Act
            response = await async_client.get(
                "/api/v1/users/statistics",
                headers=headers
            )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_users"] == 100
        assert data["active_users"] == 95


class TestUserAPIErrorHandling:
    """Test error handling in User API"""
    
    @pytest.mark.asyncio
    async def test_invalid_user_id_format(self, async_client, mock_jwt_token):
        """Test API with invalid user ID format"""
        # Arrange
        invalid_user_id = "invalid-uuid"
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        # Act
        response = await async_client.get(
            f"/api/v1/users/{invalid_user_id}",
            headers=headers
        )
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_missing_required_fields(self, async_client, mock_jwt_token):
        """Test API with missing required fields"""
        # Arrange
        incomplete_data = {
            "username": "testuser"
            # Missing required fields
        }
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        # Act
        response = await async_client.post(
            "/api/v1/users",
            json=incomplete_data,
            headers=headers
        )
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, async_client, mock_jwt_token):
        """Test API rate limiting"""
        # Arrange
        headers = {"Authorization": f"Bearer {mock_jwt_token}"}
        
        # Act - Make multiple requests quickly
        responses = []
        for _ in range(15):  # Exceed rate limit
            response = await async_client.get("/api/v1/users", headers=headers)
            responses.append(response)
        
        # Assert - Some requests should be rate limited
        rate_limited_responses = [r for r in responses if r.status_code == 429]
        assert len(rate_limited_responses) > 0


@pytest.mark.asyncio
async def test_user_api_performance(async_client, mock_jwt_token):
    """Test User API performance with multiple concurrent requests"""
    # Arrange
    headers = {"Authorization": f"Bearer {mock_jwt_token}"}
    
    with patch('src.api.v1.endpoints.users.get_user_controller') as mock_controller:
        mock_controller.return_value.list_users = AsyncMock()
        mock_controller.return_value.list_users.return_value = {
            "users": [],
            "total": 0,
            "skip": 0,
            "limit": 100
        }
        
        # Act - Make concurrent requests
        import asyncio
        
        async def make_request():
            response = await async_client.get("/api/v1/users", headers=headers)
            return response.status_code
        
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        # Assert - All requests should succeed
        assert all(status == 200 for status in results)
