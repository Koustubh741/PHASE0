#!/usr/bin/env python3
"""
Database initialization script for GRC Platform
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from core.infrastructure.database import db_manager
from core.infrastructure.database.sqlalchemy_models import Base


async def init_database():
    """
    Initialize the database with tables
    """
    print("🔧 Initializing GRC Platform database...")
    
    # Check database connection
    print("📡 Checking database connection...")
    if not await db_manager.check_connection():
        print("❌ Database connection failed!")
        return False
    
    print("✅ Database connection successful!")
    
    # Create tables
    print("🏗️  Creating database tables...")
    try:
        await db_manager.create_tables()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        return False


async def main():
    """
    Main function to initialize the database
    """
    success = await init_database()
    if success:
        print("\n🎉 Database initialization completed successfully!")
        print("You can now run the GRC Platform application.")
    else:
        print("\n💥 Database initialization failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
