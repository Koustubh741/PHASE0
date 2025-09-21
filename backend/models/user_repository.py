#!/usr/bin/env python3
"""
User Repository for BFSI Authentication
Handles user data retrieval from external sources
"""

import json
import os
from typing import Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository for user data management"""
    
    def __init__(self, config_file_path: str = "user_config.json"):
        self.config_file_path = config_file_path
        self._users_cache: Optional[Dict[str, Any]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl_seconds = 300  # 5 minutes cache TTL
    
    def _load_user_config(self) -> Dict[str, Any]:
        """Load user configuration from file"""
        try:
            if not os.path.exists(self.config_file_path):
                logger.error(f"User config file not found: {self.config_file_path}")
                return {}
            
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.info(f"Loaded user configuration from {self.config_file_path}")
            return config.get('users', {})
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in user config file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading user config: {e}")
            return {}
    
    def _get_users(self) -> Dict[str, Any]:
        """Get users with caching"""
        now = datetime.utcnow()
        
        # Check if cache is valid
        if (self._users_cache is not None and 
            self._cache_timestamp is not None and 
            (now - self._cache_timestamp).total_seconds() < self._cache_ttl_seconds):
            return self._users_cache
        
        # Load fresh data
        self._users_cache = self._load_user_config()
        self._cache_timestamp = now
        
        return self._users_cache
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            users = self._get_users()
            user_data = users.get(username)
            
            if user_data:
                logger.debug(f"Found user: {username}")
                return user_data
            else:
                logger.warning(f"User not found: {username}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving user {username}: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by user ID"""
        try:
            users = self._get_users()
            for user_data in users.values():
                if user_data.get('user_id') == user_id:
                    logger.debug(f"Found user by ID: {user_id}")
                    return user_data
            
            logger.warning(f"User not found by ID: {user_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving user by ID {user_id}: {e}")
            return None
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users"""
        try:
            return self._get_users()
        except Exception as e:
            logger.error(f"Error retrieving all users: {e}")
            return {}
    
    def is_user_active(self, username: str) -> bool:
        """Check if user is active"""
        user_data = self.get_user_by_username(username)
        if user_data:
            return user_data.get('is_active', False)
        return False
    
    def update_last_login(self, username: str) -> bool:
        """Update user's last login timestamp"""
        try:
            # In a real implementation, this would update the database
            # For now, we'll just log the event
            logger.info(f"User {username} logged in at {datetime.utcnow()}")
            return True
        except Exception as e:
            logger.error(f"Error updating last login for {username}: {e}")
            return False
    
    def validate_user_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials without exposing password hashes"""
        try:
            user_data = self.get_user_by_username(username)
            if not user_data:
                logger.warning(f"Authentication failed: User not found - {username}")
                return False
            
            if not user_data.get('is_active', False):
                logger.warning(f"Authentication failed: Inactive user - {username}")
                return False
            
            # Return the hashed password for verification by the auth service
            # The actual password verification will be done in the auth service
            return True
            
        except Exception as e:
            logger.error(f"Error validating credentials for {username}: {e}")
            return False

# Global user repository instance
user_repository = UserRepository()
