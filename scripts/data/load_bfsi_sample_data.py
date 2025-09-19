#!/usr/bin/env python3
"""
Load BFSI Sample Data Script
Loads sample data for BFSI domain into the GRC Platform database
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'grc_platform'),
    'user': os.getenv('DB_USER', 'grc_user'),
    'password': os.getenv('DB_PASSWORD', 'grc_password')
}

def connect_to_database():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        logger.info("Successfully connected to database")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None

def execute_sql_file(conn, sql_file_path):
    """Execute SQL file"""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_content)
        conn.commit()
        cursor.close()
        
        logger.info(f"Successfully executed SQL file: {sql_file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to execute SQL file {sql_file_path}: {e}")
        conn.rollback()
        return False

def verify_sample_data(conn):
    """Verify that sample data was loaded correctly"""
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check policies
        cursor.execute("SELECT COUNT(*) as count FROM policies WHERE organization_id = 'org-123'")
        policies_count = cursor.fetchone()['count']
        
        # Check risks
        cursor.execute("SELECT COUNT(*) as count FROM risks WHERE organization_id = 'org-123'")
        risks_count = cursor.fetchone()['count']
        
        # Check compliance assessments
        cursor.execute("SELECT COUNT(*) as count FROM compliance_assessments WHERE organization_id = 'org-123'")
        compliance_count = cursor.fetchone()['count']
        
        # Check workflows
        cursor.execute("SELECT COUNT(*) as count FROM workflows WHERE organization_id = 'org-123'")
        workflows_count = cursor.fetchone()['count']
        
        # Check AI agent records
        cursor.execute("SELECT COUNT(*) as count FROM ai_agent_records WHERE organization_id = 'org-123'")
        agents_count = cursor.fetchone()['count']
        
        cursor.close()
        
        logger.info("=== BFSI Sample Data Verification ===")
        logger.info(f"Policies loaded: {policies_count}")
        logger.info(f"Risks loaded: {risks_count}")
        logger.info(f"Compliance Assessments loaded: {compliance_count}")
        logger.info(f"Workflows loaded: {workflows_count}")
        logger.info(f"AI Agent Records loaded: {agents_count}")
        logger.info("=====================================")
        
        return True
    except Exception as e:
        logger.error(f"Failed to verify sample data: {e}")
        return False

def main():
    """Main function to load BFSI sample data"""
    logger.info("Starting BFSI Sample Data Loading Process")
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        logger.error("Failed to connect to database. Exiting.")
        sys.exit(1)
    
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sql_file_path = os.path.join(script_dir, '..', 'database', 'bfsi_sample_data.sql')
        
        # Execute SQL file
        if execute_sql_file(conn, sql_file_path):
            logger.info("BFSI sample data loaded successfully")
            
            # Verify data
            if verify_sample_data(conn):
                logger.info("BFSI sample data verification completed successfully")
            else:
                logger.warning("BFSI sample data verification failed")
        else:
            logger.error("Failed to load BFSI sample data")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error during BFSI sample data loading: {e}")
        sys.exit(1)
    finally:
        conn.close()
        logger.info("Database connection closed")

if __name__ == "__main__":
    main()
