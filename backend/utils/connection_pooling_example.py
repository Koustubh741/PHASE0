#!/usr/bin/env python3
"""
Connection Pooling Example
Demonstrates the usage of the database connection manager with pooling
"""

import asyncio
import logging
from database_connection_manager import get_db_connection, get_connection_pool, close_all_pools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_basic_usage():
    """Example of basic connection pooling usage"""
    logger.info("=== Basic Connection Pooling Example ===")
    
    # Example 1: Simple database operations with pooling
    try:
        with get_db_connection("example.db", max_connections=3, timeout=10) as conn:
            cursor = conn.cursor()
            
            # Create a simple table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT
                )
            ''')
            
            # Insert some data
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("John Doe", "john@example.com"))
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Jane Smith", "jane@example.com"))
            
            conn.commit()
            
            # Query data
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            
            logger.info(f"Found {len(users)} users:")
            for user in users:
                logger.info(f"  - {user[1]} ({user[2]})")
                
    except Exception as e:
        logger.error(f"Database operation failed: {e}")

def example_pool_monitoring():
    """Example of monitoring connection pool status"""
    logger.info("=== Connection Pool Monitoring Example ===")
    
    try:
        # Get connection pool instance
        pool = get_connection_pool("example.db", max_connections=5, timeout=10)
        
        # Perform multiple operations to see pool in action
        for i in range(10):
            with get_db_connection("example.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                logger.info(f"Operation {i+1}: Found {count} users")
        
        # Get pool status
        status = pool.get_pool_status()
        logger.info("Pool Status:")
        for key, value in status.items():
            logger.info(f"  {key}: {value}")
            
    except Exception as e:
        logger.error(f"Pool monitoring failed: {e}")

async def example_concurrent_operations():
    """Example of concurrent database operations with pooling"""
    logger.info("=== Concurrent Operations Example ===")
    
    def _sync_database_operation(operation_id: int):
        """Synchronous database operation that will run in thread pool"""
        with get_db_connection("example.db", max_connections=5, timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            return count

    async def database_operation(operation_id: int):
        """Simulate a database operation"""
        try:
            # Simulate some work
            await asyncio.sleep(0.1)
            
            # Run synchronous database operation in thread pool
            count = await asyncio.to_thread(_sync_database_operation, operation_id)
            
            logger.info(f"Operation {operation_id}: Found {count} users")
                
        except Exception as e:
            logger.error(f"Operation {operation_id} failed: {e}")
    
    try:
        # Run multiple concurrent operations
        tasks = [database_operation(i) for i in range(20)]
        await asyncio.gather(*tasks)
        
        # Check final pool status
        pool = get_connection_pool("example.db")
        status = pool.get_pool_status()
        logger.info("Final Pool Status:")
        for key, value in status.items():
            logger.info(f"  {key}: {value}")
            
    except Exception as e:
        logger.error(f"Concurrent operations failed: {e}")

def example_error_handling():
    """Example of error handling with connection pooling"""
    logger.info("=== Error Handling Example ===")
    
    try:
        # This will fail due to invalid SQL
        with get_db_connection("example.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INVALID SQL STATEMENT")
            
    except Exception as e:
        logger.info(f"Expected error caught: {e}")
    
    # Pool should still be functional after error
    try:
        with get_db_connection("example.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            logger.info(f"Pool still functional after error: {count} users found")
            
    except Exception as e:
        logger.error(f"Pool recovery failed: {e}")

async def main():
    """Main function demonstrating connection pooling"""
    logger.info("Starting Connection Pooling Examples")
    
    try:
        # Basic usage
        example_basic_usage()
        
        # Pool monitoring
        example_pool_monitoring()
        
        # Concurrent operations
        await example_concurrent_operations()
        
        # Error handling
        example_error_handling()
        
    finally:
        # Clean up - ensure pools are always closed regardless of exceptions
        close_all_pools()
        logger.info("All connection pools closed")

if __name__ == "__main__":
    asyncio.run(main())
