"""
Database utilities for the GRC platform.
"""

import psycopg2
import redis
from typing import Dict, Any, Optional, List
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database manager for PostgreSQL and Redis connections"""
    
    def __init__(self, postgres_config: Dict[str, Any], redis_config: Dict[str, Any]):
        self.postgres_config = postgres_config
        self.redis_config = redis_config
        self._redis_pool = None
    
    @contextmanager
    def get_postgres_connection(self):
        """Get a PostgreSQL connection"""
        conn = None
        try:
            conn = psycopg2.connect(**self.postgres_config)
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def get_redis_connection(self):
        """Get a Redis connection"""
        if not self._redis_pool:
            self._redis_pool = redis.ConnectionPool(**self.redis_config)
        return redis.Redis(connection_pool=self._redis_pool)
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a PostgreSQL query and return results"""
        with self.get_postgres_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    results = []
                    for row in cursor.fetchall():
                        results.append(dict(zip(columns, row)))
                    return results
                return []
    
    def cache_set(self, key: str, value: Any, expire: int = 3600):
        """Set a value in Redis cache"""
        try:
            redis_conn = self.get_redis_connection()
            redis_conn.setex(key, expire, str(value))
        except Exception as e:
            logger.error(f"Redis cache set error: {e}")
    
    def cache_get(self, key: str) -> Optional[str]:
        """Get a value from Redis cache"""
        try:
            redis_conn = self.get_redis_connection()
            return redis_conn.get(key)
        except Exception as e:
            logger.error(f"Redis cache get error: {e}")
            return None

