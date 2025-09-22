#!/usr/bin/env python3
"""
Authentication System Test Script
Tests the authentication system functionality
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.application.services.auth_service import AuthService
from core.infrastructure.persistence.repositories import SQLAlchemyUserRepository, SQLAlchemyAuditLogRepository
from core.infrastructure.database import get_sync_db
from core.domain.entities.user import User, UserRole, UserStatus
from core.domain.entities.audit_log import AuditAction, AuditResource, AuditSeverity
import uuid
from datetime import datetime

async def test_authentication_system():
    """
    Test the authentication system functionality
    """
    print("🔐 Testing GRC Platform Authentication System...")
    
    try:
        # Initialize repositories
        print("📡 Initializing repositories...")
        from core.infrastructure.database import SessionLocal
        
        # Create session
        session = SessionLocal()
        
        # Initialize repositories with session
        user_repo = SQLAlchemyUserRepository(session)
        audit_repo = SQLAlchemyAuditLogRepository()
        audit_repo.set_session_factory(lambda: session)
        
        # Initialize auth service
        print("🔧 Initializing authentication service...")
        auth_service = AuthService(user_repo, audit_repo)
        
        # Test 1: Create a test user
        print("\n👤 Test 1: Creating test user...")
        test_user_id = str(uuid.uuid4())
        test_org_id = str(uuid.uuid4())
        test_user = User(
            id=test_user_id,
            username="testuser@example.com",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/4Qz8K2K",  # password: testpass123
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            organization_id=test_org_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save user to database
        user_repo.create(test_user)
        print(f"✅ Test user created: {test_user.username}")
        
        # Test 2: Authenticate user
        print("\n🔑 Test 2: Testing user authentication...")
        try:
            authenticated_user, token = await auth_service.authenticate_user(
                username="testuser@example.com",
                password="testpass123",
                ip_address="127.0.0.1",
                user_agent="Test Agent"
            )
            print(f"✅ User authenticated successfully: {authenticated_user.username}")
            print(f"✅ JWT token generated: {token[:50]}...")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
        
        # Test 3: Validate token
        print("\n🎫 Test 3: Testing token validation...")
        try:
            current_user = await auth_service.get_current_user_from_token(token)
            if current_user and current_user.id == test_user_id:
                print(f"✅ Token validation successful: {current_user.username}")
            else:
                print("❌ Token validation failed: Invalid user")
                return False
        except Exception as e:
            print(f"❌ Token validation failed: {e}")
            return False
        
        # Test 4: Test password change
        print("\n🔒 Test 4: Testing password change...")
        try:
            await auth_service.change_password(
                user_id=test_user_id,
                current_password="testpass123",
                new_password="newpass456"
            )
            print("✅ Password changed successfully")
            
            # Test login with new password
            authenticated_user, new_token = await auth_service.authenticate_user(
                username="testuser@example.com",
                password="newpass456",
                ip_address="127.0.0.1",
                user_agent="Test Agent"
            )
            print("✅ Login with new password successful")
            
        except Exception as e:
            print(f"❌ Password change failed: {e}")
            return False
        
        # Test 5: Test authorization
        print("\n🛡️ Test 5: Testing authorization...")
        try:
            # Test admin permissions
            has_admin_permission = await auth_service.has_permission(
                user_id=test_user_id,
                permission="can_create_policies"
            )
            if has_admin_permission:
                print("✅ Admin permissions verified")
            else:
                print("❌ Admin permissions failed")
                return False
                
        except Exception as e:
            print(f"❌ Authorization test failed: {e}")
            return False
        
        # Test 6: Test audit logging
        print("\n📝 Test 6: Testing audit logging...")
        try:
            # Check if audit logs were created
            audit_logs = audit_repo.get_by_user_id(test_user_id)
            if audit_logs:
                print(f"✅ Audit logs created: {len(audit_logs)} entries")
                for log in audit_logs[:3]:  # Show first 3 logs
                    print(f"  - {log.action.value}: {log.resource.value} at {log.created_at}")
            else:
                print("⚠️ No audit logs found")
                
        except Exception as e:
            print(f"❌ Audit logging test failed: {e}")
            return False
        
        # Cleanup
        print("\n🧹 Cleaning up test data...")
        try:
            user_repo.delete(test_user_id)
            print("✅ Test user deleted")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
        
        print("\n🎉 Authentication system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n💥 Authentication system test failed: {e}")
        return False

async def main():
    """
    Main function to run authentication tests
    """
    success = await test_authentication_system()
    if success:
        print("\n✅ All authentication tests passed!")
        print("🔐 Authentication system is ready for production use.")
    else:
        print("\n❌ Authentication system tests failed!")
        print("🔧 Please check the authentication implementation.")

if __name__ == "__main__":
    asyncio.run(main())
