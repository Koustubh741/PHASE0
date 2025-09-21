"""
Unit tests for Authentication Service
Tests user authentication, JWT token management, and security features
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from uuid import uuid4

from src.core.application.services.auth_service import AuthService, AuthenticationError, AuthorizationError
from src.core.domain.entities.user import User, UserStatus, UserRole
from src.core.domain.entities.audit_log import AuditAction, AuditResource, AuditSeverity


@pytest.fixture
def mock_user_repository():
    """Mock user repository"""
    return AsyncMock()


@pytest.fixture
def mock_audit_log_repository():
    """Mock audit log repository"""
    return AsyncMock()


@pytest.fixture
def auth_service(mock_user_repository, mock_audit_log_repository):
    """Authentication service with mocked dependencies"""
    return AuthService(mock_user_repository, mock_audit_log_repository)


@pytest.fixture
def sample_user():
    """Sample user for testing"""
    user = User.create_new(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        role=UserRole.ADMIN,
        organization_id="org-123"
    )
    user.set_password("TestPassword123!")
    user.activate()
    return user


class TestAuthenticationService:
    """Test cases for authentication service"""
    
    @pytest.mark.asyncio
    async def test_successful_login(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test successful user login"""
        # Arrange
        mock_user_repository.get_by_username.return_value = sample_user
        
        # Act
        user, token = await auth_service.authenticate_user(
            username="testuser",
            password="TestPassword123!",
            ip_address="192.168.1.1"
        )
        
        # Assert
        assert user == sample_user
        assert token is not None
        assert user.failed_login_attempts == 0
        assert user.last_login is not None
        
        # Verify audit log was created
        mock_audit_log_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_failed_login_invalid_credentials(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test login failure with invalid credentials"""
        # Arrange
        mock_user_repository.get_by_username.return_value = sample_user
        
        # Act & Assert
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await auth_service.authenticate_user(
                username="testuser",
                password="WrongPassword",
                ip_address="192.168.1.1"
            )
        
        # Verify failed login attempt was recorded
        assert sample_user.failed_login_attempts == 1
        mock_user_repository.update.assert_called_once_with(sample_user)
    
    @pytest.mark.asyncio
    async def test_failed_login_user_not_found(self, auth_service, mock_user_repository, mock_audit_log_repository):
        """Test login failure when user is not found"""
        # Arrange
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.get_by_email.return_value = None
        
        # Act & Assert
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await auth_service.authenticate_user(
                username="nonexistent",
                password="password",
                ip_address="192.168.1.1"
            )
        
        # Verify audit log was created for failed attempt
        mock_audit_log_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_login_with_locked_account(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test login attempt with locked account"""
        # Arrange
        sample_user.lock_account()
        mock_user_repository.get_by_username.return_value = sample_user
        
        # Act & Assert
        with pytest.raises(AuthenticationError, match="Account is locked"):
            await auth_service.authenticate_user(
                username="testuser",
                password="TestPassword123!",
                ip_address="192.168.1.1"
            )
    
    @pytest.mark.asyncio
    async def test_login_with_inactive_account(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test login attempt with inactive account"""
        # Arrange
        sample_user.status = UserStatus.INACTIVE
        mock_user_repository.get_by_username.return_value = sample_user
        
        # Act & Assert
        with pytest.raises(AuthenticationError, match="Account is not active"):
            await auth_service.authenticate_user(
                username="testuser",
                password="TestPassword123!",
                ip_address="192.168.1.1"
            )
    
    @pytest.mark.asyncio
    async def test_account_lockout_after_multiple_failures(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test account lockout after multiple failed login attempts"""
        # Arrange
        mock_user_repository.get_by_username.return_value = sample_user
        
        # Act - Simulate 5 failed login attempts
        for _ in range(5):
            with pytest.raises(AuthenticationError):
                await auth_service.authenticate_user(
                    username="testuser",
                    password="WrongPassword",
                    ip_address="192.168.1.1"
                )
        
        # Assert
        assert sample_user.status == UserStatus.LOCKED
        assert sample_user.locked_until is not None
        assert sample_user.failed_login_attempts == 5
    
    @pytest.mark.asyncio
    async def test_two_factor_authentication(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test two-factor authentication flow"""
        # Arrange
        sample_user.enable_two_factor()
        mock_user_repository.get_by_username.return_value = sample_user
        
        # Mock 2FA token verification
        with patch.object(sample_user, 'verify_two_factor_token', return_value=True):
            # Act
            user, token = await auth_service.authenticate_with_two_factor(
                username="testuser",
                password="TestPassword123!",
                two_factor_token="123456",
                ip_address="192.168.1.1"
            )
        
        # Assert
        assert user == sample_user
        assert token is not None
        mock_audit_log_repository.create.assert_called()
    
    @pytest.mark.asyncio
    async def test_two_factor_authentication_invalid_token(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test two-factor authentication with invalid token"""
        # Arrange
        sample_user.enable_two_factor()
        mock_user_repository.get_by_username.return_value = sample_user
        
        # Mock 2FA token verification failure
        with patch.object(sample_user, 'verify_two_factor_token', return_value=False):
            # Act & Assert
            with pytest.raises(AuthenticationError, match="Invalid two-factor authentication token"):
                await auth_service.authenticate_with_two_factor(
                    username="testuser",
                    password="TestPassword123!",
                    two_factor_token="invalid",
                    ip_address="192.168.1.1"
                )
    
    @pytest.mark.asyncio
    async def test_password_change_success(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test successful password change"""
        # Arrange
        mock_user_repository.update = AsyncMock()
        
        # Act
        await auth_service.change_password(
            user=sample_user,
            old_password="TestPassword123!",
            new_password="NewPassword123!",
            ip_address="192.168.1.1"
        )
        
        # Assert
        assert sample_user.verify_password("NewPassword123!")
        mock_user_repository.update.assert_called_once_with(sample_user)
        mock_audit_log_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_password_change_wrong_old_password(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test password change with wrong old password"""
        # Act & Assert
        with pytest.raises(AuthenticationError, match="Current password is incorrect"):
            await auth_service.change_password(
                user=sample_user,
                old_password="WrongPassword",
                new_password="NewPassword123!",
                ip_address="192.168.1.1"
            )
    
    def test_password_validation(self, auth_service):
        """Test password strength validation"""
        # Test weak passwords
        weak_passwords = [
            "12345678",  # No letters
            "password",  # No uppercase, numbers, or special chars
            "Password",  # No numbers or special chars
            "Password1",  # No special chars
            "P@ssword",  # No numbers
        ]
        
        for password in weak_passwords:
            with pytest.raises(AuthenticationError):
                auth_service._validate_password(password)
        
        # Test strong password
        try:
            auth_service._validate_password("StrongPass123!")
        except AuthenticationError:
            pytest.fail("Strong password should not raise AuthenticationError")
    
    @pytest.mark.asyncio
    async def test_password_reset_initiation(self, auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
        """Test password reset initiation"""
        # Arrange
        mock_user_repository.get_by_email.return_value = sample_user
        mock_user_repository.update = AsyncMock()
        
        # Act
        result = await auth_service.initiate_password_reset(
            email="test@example.com",
            ip_address="192.168.1.1"
        )
        
        # Assert
        assert result is True
        assert sample_user.password_reset_token is not None
        assert sample_user.password_reset_expires is not None
        mock_user_repository.update.assert_called_once_with(sample_user)
        mock_audit_log_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_password_reset_nonexistent_user(self, auth_service, mock_user_repository, mock_audit_log_repository):
        """Test password reset for non-existent user"""
        # Arrange
        mock_user_repository.get_by_email.return_value = None
        
        # Act
        result = await auth_service.initiate_password_reset(
            email="nonexistent@example.com",
            ip_address="192.168.1.1"
        )
        
        # Assert
        assert result is False
        mock_audit_log_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_jwt_token_verification(self, auth_service, sample_user):
        """Test JWT token verification"""
        # Arrange
        token = auth_service._generate_jwt_token(sample_user)
        
        # Act
        payload = auth_service.verify_jwt_token(token)
        
        # Assert
        assert payload["sub"] == str(sample_user.id)
        assert payload["username"] == sample_user.username
        assert payload["role"] == sample_user.role.value
        assert payload["organization_id"] == sample_user.organization_id
    
    def test_jwt_token_expiration(self, auth_service, sample_user):
        """Test JWT token expiration"""
        # Arrange
        with patch('src.core.application.services.auth_service.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.utcnow() - timedelta(hours=1)
            expired_token = auth_service._generate_jwt_token(sample_user)
        
        # Act & Assert
        with pytest.raises(AuthenticationError, match="Token has expired"):
            auth_service.verify_jwt_token(expired_token)
    
    def test_permission_checking(self, auth_service, sample_user):
        """Test user permission checking"""
        # Test admin permissions
        assert auth_service.check_permission(sample_user, "can_manage_users") is True
        assert auth_service.check_permission(sample_user, "can_view_audit_logs") is True
        
        # Test require_permission
        try:
            auth_service.require_permission(sample_user, "can_manage_users")
        except AuthorizationError:
            pytest.fail("Admin user should have can_manage_users permission")
    
    def test_permission_denied(self, auth_service, sample_user):
        """Test permission denied scenario"""
        # Change user to viewer role
        sample_user.role = UserRole.VIEWER
        
        # Test permission check
        assert auth_service.check_permission(sample_user, "can_manage_users") is False
        
        # Test require_permission raises exception
        with pytest.raises(AuthorizationError):
            auth_service.require_permission(sample_user, "can_manage_users")
    
    @pytest.mark.asyncio
    async def test_user_logout(self, auth_service, mock_audit_log_repository, sample_user):
        """Test user logout"""
        # Act
        await auth_service.logout_user(sample_user, ip_address="192.168.1.1")
        
        # Assert
        mock_audit_log_repository.create.assert_called_once()
        audit_log = mock_audit_log_repository.create.call_args[0][0]
        assert audit_log.action == AuditAction.LOGOUT
        assert audit_log.user_id == str(sample_user.id)


class TestAuthenticationErrors:
    """Test authentication error handling"""
    
    def test_authentication_error_inheritance(self):
        """Test AuthenticationError inheritance"""
        error = AuthenticationError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
    
    def test_authorization_error_inheritance(self):
        """Test AuthorizationError inheritance"""
        error = AuthorizationError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"


@pytest.mark.asyncio
async def test_concurrent_login_attempts(auth_service, mock_user_repository, mock_audit_log_repository, sample_user):
    """Test handling of concurrent login attempts"""
    # Arrange
    mock_user_repository.get_by_username.return_value = sample_user
    
    # Act - Simulate concurrent failed login attempts
    import asyncio
    
    async def failed_login():
        with pytest.raises(AuthenticationError):
            await auth_service.authenticate_user(
                username="testuser",
                password="WrongPassword",
                ip_address="192.168.1.1"
            )
    
    # Run multiple concurrent failed logins
    tasks = [failed_login() for _ in range(3)]
    await asyncio.gather(*tasks)
    
    # Assert
    assert sample_user.failed_login_attempts == 3
    mock_user_repository.update.assert_called()


@pytest.mark.asyncio
async def test_token_refresh(auth_service, mock_user_repository, sample_user):
    """Test JWT token refresh"""
    # Arrange
    token = auth_service._generate_jwt_token(sample_user)
    mock_user_repository.get_by_id.return_value = sample_user
    
    # Act
    new_token = await auth_service.refresh_token(token)
    
    # Assert
    assert new_token != token
    assert new_token is not None
    
    # Verify new token is valid
    payload = auth_service.verify_jwt_token(new_token)
    assert payload["sub"] == str(sample_user.id)
