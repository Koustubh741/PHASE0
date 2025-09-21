"""
Database configuration and connection management

This module handles database connections and initialization for the API Gateway.
It manages connection pooling and database migrations.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import redis
from typing import AsyncGenerator
import logging

from src.core.config import settings

logger = logging.getLogger(__name__)

# Database engine configuration
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Redis connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def init_db():
    """Initialize database connections"""
    try:
        # Test database connection
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Database connection established")
        
        # Test Redis connection
        redis_client.ping()
        logger.info("Redis connection established")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def get_db() -> AsyncGenerator:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    """Get Redis client"""
    return redis_client
