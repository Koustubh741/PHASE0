#!/usr/bin/env python3
"""
Simple BFSI Sample Data Loader
Loads BFSI sample data into the GRC Platform database
"""

import os
import sys
import psycopg2
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'grc_platform',
    'user': 'grc_user',
    'password': 'grc_password'
}

def load_bfsi_sample_data():
    """Load BFSI sample data into database"""
    try:
        # Connect to database
        logger.info("Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Read and execute SQL file
        sql_file_path = os.path.join('database', 'bfsi_sample_data_clean.sql')
        
        if not os.path.exists(sql_file_path):
            logger.error(f"SQL file not found: {sql_file_path}")
            return False
        
        logger.info(f"Loading BFSI sample data from: {sql_file_path}")
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Execute SQL content
        cursor.execute(sql_content)
        conn.commit()
        
        # Verify data loaded
        cursor.execute("SELECT COUNT(*) FROM policies WHERE organization_id = 'org-123'")
        policies_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM risks WHERE organization_id = 'org-123'")
        risks_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM compliance_assessments WHERE organization_id = 'org-123'")
        compliance_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM workflows WHERE organization_id = 'org-123'")
        workflows_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ai_agent_records WHERE organization_id = 'org-123'")
        agents_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        # Print results
        logger.info("=== BFSI Sample Data Loaded Successfully ===")
        logger.info(f"✅ Policies: {policies_count}")
        logger.info(f"✅ Risks: {risks_count}")
        logger.info(f"✅ Compliance Assessments: {compliance_count}")
        logger.info(f"✅ Workflows: {workflows_count}")
        logger.info(f"✅ AI Agent Records: {agents_count}")
        logger.info("=============================================")
        
        return True
        
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error loading BFSI sample data: {e}")
        return False

def main():
    """Main function"""
    logger.info("🚀 Starting BFSI Sample Data Loading...")
    
    if load_bfsi_sample_data():
        logger.info("🎉 BFSI sample data loaded successfully!")
        logger.info("📊 Dashboard should now show BFSI data")
        logger.info("🌐 Access your platform at: http://localhost:3000")
    else:
        logger.error("❌ Failed to load BFSI sample data")
        sys.exit(1)

if __name__ == "__main__":
    main()
