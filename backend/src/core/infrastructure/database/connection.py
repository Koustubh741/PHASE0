"""
Database connection and session management for GRC Platform
"""

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from config.settings import settings

# Create the base class for all models
Base = declarative_base()

# Database URL from settings
DATABASE_URL = settings.database.url

# Create async engine for async operations
async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create sync engine for sync operations (migrations, etc.)
sync_engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False,
)

# Create sync session factory
SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_sync_session() -> Generator[Session, None, None]:
    """
    Dependency to get a synchronous database session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_async_session() -> AsyncSession:
    """
    Dependency to get an asynchronous database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class DatabaseManager:
    """
    Database manager for handling connections and operations
    """
    
    def __init__(self):
        self.async_engine = async_engine
        self.sync_engine = sync_engine
        self.async_session_factory = AsyncSessionLocal
        self.sync_session_factory = SessionLocal
    
    async def create_tables(self):
        """
        Create all tables in the database
        """
        async with self.async_engine.begin() as conn:
            # Import models to ensure they are registered
            from .sqlalchemy_models import Base
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self):
        """
        Drop all tables in the database
        """
        async with self.async_engine.begin() as conn:
            # Import models to ensure they are registered
            from .sqlalchemy_models import Base
            # Use CASCADE to drop dependent objects
            await conn.execute(text("DROP SCHEMA public CASCADE"))
            await conn.execute(text("CREATE SCHEMA public"))
            await conn.run_sync(Base.metadata.create_all)
    
    async def check_connection(self) -> bool:
        """
        Check if database connection is working
        """
        try:
            async with self.async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def get_sync_session(self) -> Session:
        """
        Get a synchronous database session
        """
        return self.sync_session_factory()
    
    def get_async_session(self) -> AsyncSession:
        """
        Get an asynchronous database session
        """
        return self.async_session_factory()


# Global database manager instance
db_manager = DatabaseManager()


# Dependency functions for FastAPI
async def get_db() -> AsyncSession:
    """
    FastAPI dependency for getting database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for getting synchronous database session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
