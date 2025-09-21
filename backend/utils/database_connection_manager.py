#!/usr/bin/env python3
"""
Database Connection Manager with Connection Pooling
Provides efficient database connection management for SQLite with pooling capabilities
"""

import sqlite3
import threading
import logging
from contextlib import contextmanager
from typing import Optional, Dict, Any
from queue import Queue, Empty
import time

logger = logging.getLogger(__name__)

class DatabaseConnectionPool:
    """
    SQLite Connection Pool for efficient database access
    Provides connection pooling with WAL mode for better concurrency
    """
    
    def __init__(self, db_path: str, max_connections: int = 10, timeout: int = 30):
        """
        Initialize connection pool
        
        Args:
            db_path: Path to SQLite database file
            max_connections: Maximum number of connections in pool
            timeout: Connection timeout in seconds
        """
        self.db_path = db_path
        self.max_connections = max_connections
        self.timeout = timeout
        self._pool = Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        self._created_connections = 0
        self._active_connections = 0
        
        # Thread-local storage for thread-safe connection management
        self._thread_local = threading.local()
        
        # Initialize database with WAL mode for better concurrency
        self._initialize_database()
        
        logger.info(f"Database connection pool initialized: {db_path}, max_connections={max_connections}")
    
    def _initialize_database(self):
        """Initialize database with WAL mode for better concurrency"""
        try:
            with sqlite3.connect(self.db_path, timeout=self.timeout) as conn:
                # Enable WAL mode for better concurrency
                conn.execute("PRAGMA journal_mode=WAL")
                # Set other performance optimizations
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=10000")
                conn.execute("PRAGMA temp_store=MEMORY")
                conn.execute("PRAGMA mmap_size=268435456")  # 256MB
                conn.commit()
                logger.info("Database initialized with WAL mode and performance optimizations")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _create_connection(self) -> sqlite3.Connection:
        """Create a new database connection with optimizations"""
        # Hold lock during entire connection creation process to prevent race conditions
        with self._lock:
            try:
                conn = sqlite3.connect(
                    self.db_path,
                    timeout=self.timeout,
                    check_same_thread=True  # Ensure thread safety - connections only used by creating thread
                )
                
                # Set connection-specific optimizations
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=10000")
                conn.execute("PRAGMA temp_store=MEMORY")
                
                # Atomically increment counters after successful connection creation
                self._created_connections += 1
                self._active_connections += 1
                
                logger.debug(f"Created new database connection (total: {self._created_connections}, active: {self._active_connections})")
                return conn
                
            except sqlite3.Error as e:
                logger.error(f"Failed to create database connection: {e}")
                raise
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a connection from the pool or create a new one"""
        try:
            # Try to get existing connection from pool
            conn = self._pool.get_nowait()
            
            # Test if connection is still valid
            try:
                conn.execute("SELECT 1")
                return conn
            except sqlite3.Error:
                # Connection is stale, decrement counter and create a new one
                logger.debug("Stale connection detected, creating new one")
                with self._lock:
                    self._active_connections -= 1
                    logger.debug(f"Decremented active connections due to stale connection (active: {self._active_connections})")
                return self._create_connection()
                
        except Empty:
            # Pool is empty, create new connection if under limit
            with self._lock:
                if self._active_connections < self.max_connections:
                    # Release lock before calling _create_connection since it will acquire it
                    pass
                else:
                    # Wait for a connection to become available
                    # Release lock before waiting to avoid deadlock
                    pass
            
            # Check again outside the lock to avoid race condition
            with self._lock:
                if self._active_connections < self.max_connections:
                    return self._create_connection()
                else:
                    # Wait for a connection to become available
                    # Release lock before waiting to avoid deadlock
                    pass
            
            # Wait for a connection to become available (outside of lock)
            try:
                conn = self._pool.get(timeout=self.timeout)
                # Test connection
                conn.execute("SELECT 1")
                return conn
            except Empty:
                raise sqlite3.Error("Connection pool timeout - no connections available")
            except sqlite3.Error:
                # Connection is stale, decrement counter and create new one
                logger.debug("Stale connection from pool timeout detected")
                with self._lock:
                    self._active_connections -= 1
                    logger.debug(f"Decremented active connections due to stale connection (active: {self._active_connections})")
                return self._create_connection()
    
    def _return_connection(self, conn: sqlite3.Connection):
        """Return a connection to the pool"""
        try:
            # Reset connection state
            conn.rollback()  # Clear any pending transactions
            
            # Test connection is still valid
            conn.execute("SELECT 1")
            
            # Return to pool
            self._pool.put_nowait(conn)
            
        except sqlite3.Error:
            # Connection is stale, close it
            try:
                conn.close()
            except:
                pass
            
            with self._lock:
                self._active_connections -= 1
            
            logger.debug("Closed stale connection")
        except Exception as e:
            logger.error(f"Error returning connection to pool: {e}")
            try:
                conn.close()
            except:
                pass
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        Automatically handles connection acquisition and return
        """
        conn = None
        try:
            conn = self._get_connection()
            yield conn
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise
        finally:
            if conn:
                self._return_connection(conn)
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get current pool status for monitoring"""
        with self._lock:
            return {
                "max_connections": self.max_connections,
                "active_connections": self._active_connections,
                "available_connections": self._pool.qsize(),
                "created_connections": self._created_connections,
                "pool_utilization": f"{(self._active_connections / self.max_connections) * 100:.1f}%"
            }
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        with self._lock:
            while not self._pool.empty():
                try:
                    conn = self._pool.get_nowait()
                    conn.close()
                except:
                    pass
            self._active_connections = 0
            logger.info("All database connections closed")

# Global connection pool instances
_connection_pools: Dict[str, DatabaseConnectionPool] = {}
_pools_lock = threading.Lock()  # Lock for thread-safe access to _connection_pools

def get_connection_pool(db_path: str, max_connections: int = 10, timeout: int = 30) -> DatabaseConnectionPool:
    """
    Get or create a connection pool for the specified database
    
    Args:
        db_path: Path to SQLite database file
        max_connections: Maximum number of connections in pool
        timeout: Connection timeout in seconds
    
    Returns:
        DatabaseConnectionPool instance
    """
    # Use double-checked locking pattern to prevent race conditions
    # First check without lock for performance
    if db_path not in _connection_pools:
        with _pools_lock:
            # Check again inside lock to prevent race condition
            if db_path not in _connection_pools:
                _connection_pools[db_path] = DatabaseConnectionPool(
                    db_path=db_path,
                    max_connections=max_connections,
                    timeout=timeout
                )
    
    return _connection_pools[db_path]

def close_all_pools():
    """Close all connection pools"""
    for pool in _connection_pools.values():
        pool.close_all_connections()
    _connection_pools.clear()
    logger.info("All connection pools closed")

# Convenience function for easy database access
@contextmanager
def get_db_connection(db_path: str, max_connections: int = 10, timeout: int = 30):
    """
    Convenience function for getting database connections with pooling
    
    Usage:
        with get_db_connection("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table")
            result = cursor.fetchall()
    """
    pool = get_connection_pool(db_path, max_connections, timeout)
    with pool.get_connection() as conn:
        yield conn
