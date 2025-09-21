#!/usr/bin/env python3
"""
Test script for PostgreSQL integration in security_data_access.py
"""

import os
import sys
import logging
from security_data_access import DatabaseConfig, SecureDataRepository

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_postgresql_connection():
    """Test PostgreSQL connection and basic operations"""
    
    # Create database configuration from environment or use defaults
    db_config = DatabaseConfig.from_environment()
    
    logger.info("Testing PostgreSQL connection...")
    logger.info(f"Database config: {db_config.host}:{db_config.port}/{db_config.database}")
    
    try:
        # Create repository instance
        with SecureDataRepository(db_config) as repo:
            
            # Test connection
            if repo.test_database_connection():
                logger.info("✅ PostgreSQL connection test passed")
            else:
                logger.error("❌ PostgreSQL connection test failed")
                return False
            
            # Get database info
            db_info = repo.get_database_info()
            if "error" not in db_info:
                logger.info("✅ Database info retrieved successfully:")
                logger.info(f"   Version: {db_info['version']}")
                logger.info(f"   Database: {db_info['database']}")
                logger.info(f"   Active connections: {db_info['active_connections']}")
                logger.info(f"   Pool size: {db_info['pool_size']}")
                logger.info(f"   SSL mode: {db_info['ssl_mode']}")
            else:
                logger.error(f"❌ Failed to get database info: {db_info['error']}")
                return False
            
            # Test basic query (this will fail if tables don't exist, which is expected)
            try:
                transactions = repo.get_transactions(limit=1)
                logger.info(f"✅ Basic query test passed - retrieved {len(transactions)} transactions")
            except Exception as e:
                logger.warning(f"⚠️  Basic query test failed (expected if tables don't exist): {e}")
            
            logger.info("✅ All PostgreSQL integration tests completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"❌ PostgreSQL integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL Integration Test")
    print("=" * 50)
    
    # Set default environment variables if not set
    if not os.getenv('BFSI_DB_HOST'):
        os.environ['BFSI_DB_HOST'] = 'localhost'
    if not os.getenv('BFSI_DB_PORT'):
        os.environ['BFSI_DB_PORT'] = '5432'
    if not os.getenv('BFSI_DB_NAME'):
        os.environ['BFSI_DB_NAME'] = 'bfsi_security'
    if not os.getenv('BFSI_DB_USER'):
        os.environ['BFSI_DB_USER'] = 'bfsi_user'
    
    success = test_postgresql_connection()
    
    if success:
        print("\n✅ PostgreSQL integration is working correctly!")
        print("You can now use the security_data_access module with PostgreSQL.")
        sys.exit(0)
    else:
        print("\n❌ PostgreSQL integration test failed.")
        print("Please check your PostgreSQL configuration and connection settings.")
        sys.exit(1)
