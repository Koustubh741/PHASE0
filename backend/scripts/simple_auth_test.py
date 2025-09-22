#!/usr/bin/env python3
"""
Simple Authentication System Test
Tests basic authentication functionality without async complexity
"""

import sys
import os
import uuid
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.infrastructure.database import SessionLocal
from core.infrastructure.persistence.repositories import SQLAlchemyUserRepository
from core.domain.entities.user import User, UserRole, UserStatus
from core.application.services.auth_service import AuthService
import bcrypt

def test_basic_auth():
    """
    Test basic authentication functionality
    """
    print("🔐 Testing Basic Authentication System...")
    
    try:
        # Initialize database session
        print("📡 Initializing database session...")
        session = SessionLocal()
        
        # Initialize user repository
        print("🔧 Initializing user repository...")
        user_repo = SQLAlchemyUserRepository(session)
        
        # Test 1: Create a test user
        print("\n👤 Test 1: Creating test user...")
        test_user_id = str(uuid.uuid4())
        test_org_id = str(uuid.uuid4())
        unique_username = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        
        # Hash password
        password = "testpass123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        test_user = User(
            id=test_user_id,
            username=unique_username,
            email=unique_username,
            first_name="Test",
            last_name="User",
            password_hash=password_hash,
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            organization_id=test_org_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save user to database
        user_repo.create(test_user)
        print(f"✅ Test user created: {test_user.username}")
        
        # Test 2: Retrieve user
        print("\n🔍 Test 2: Testing user retrieval...")
        retrieved_user = user_repo.get_by_username(unique_username)
        if retrieved_user:
            print(f"✅ User retrieved: {retrieved_user.username}")
        else:
            print("❌ User retrieval failed")
            return False
        
        # Test 3: Test password verification
        print("\n🔒 Test 3: Testing password verification...")
        if bcrypt.checkpw(password.encode('utf-8'), retrieved_user.password_hash.encode('utf-8')):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
            return False
        
        # Test 4: Test user roles and permissions
        print("\n🛡️ Test 4: Testing user roles...")
        if retrieved_user.role == UserRole.ADMIN or retrieved_user.role == "admin":
            print("✅ Admin role verified")
        else:
            print(f"❌ Admin role verification failed. Role: {retrieved_user.role}")
            return False
        
        if retrieved_user.status == UserStatus.ACTIVE or retrieved_user.status == "active":
            print("✅ Active status verified")
        else:
            print(f"❌ Active status verification failed. Status: {retrieved_user.status}")
            return False
        
        # Test 5: Test user ID retrieval
        print("\n🆔 Test 5: Testing user retrieval by ID...")
        id_user = user_repo.get_by_id(test_user_id)
        if id_user and id_user.username == unique_username:
            print("✅ User retrieval by ID successful")
        else:
            print("❌ User retrieval by ID failed")
            return False
        
        # Cleanup - just close session
        print("\n🧹 Test completed successfully")
        
        session.close()
        
        print("\n🎉 Basic authentication system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n💥 Basic authentication test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    Main function to run basic authentication tests
    """
    success = test_basic_auth()
    if success:
        print("\n✅ All basic authentication tests passed!")
        print("🔐 Basic authentication system is working correctly.")
    else:
        print("\n❌ Basic authentication tests failed!")
        print("🔧 Please check the authentication implementation.")

if __name__ == "__main__":
    main()
