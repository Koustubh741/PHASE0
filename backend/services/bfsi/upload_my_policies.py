#!/usr/bin/env python3
"""
Simple BFSI Policy Upload Tool
Upload your BFSI policies directly for model training
"""

import os
import sys
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# Add the current directory to the path to import bfsi_policy_uploader
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bfsi_policy_uploader import policy_manager, upload_policy_text, create_training_dataset

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimplePolicyUploader:
    """Simple policy uploader for BFSI training"""
    
    def __init__(self):
        self.db_path = "bfsi_policies.db"
        self.ensure_database()
    
    def ensure_database(self):
        """Ensure the database exists and is properly initialized"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create policies table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                policy_type TEXT NOT NULL,
                framework TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def upload_policy_interactive(self):
        """Interactive policy upload"""
        print("🚀 BFSI Policy Upload Tool")
        print("=" * 50)
        
        while True:
            print("\n📋 Policy Upload Options:")
            print("1. Upload policy from text input")
            print("2. Upload policy from file")
            print("3. View existing policies")
            print("4. Create training dataset")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                self.upload_from_text()
            elif choice == "2":
                self.upload_from_file()
            elif choice == "3":
                self.view_policies()
            elif choice == "4":
                self.create_training_data()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def upload_from_text(self):
        """Upload policy from text input"""
        print("\n📝 Upload Policy from Text")
        print("-" * 30)
        
        # Get policy details
        title = input("Policy Title: ").strip()
        if not title:
            print("❌ Title is required!")
            return
        
        policy_type = input("Policy Type (compliance/risk/fraud/operational/security/audit): ").strip().lower()
        if policy_type not in ["compliance", "risk", "fraud", "operational", "security", "audit"]:
            print("❌ Invalid policy type!")
            return
        
        framework = input("Framework (SOX/Basel III/PCI DSS/GDPR/IFRS/FATCA/Other): ").strip()
        if not framework:
            framework = "Other"
        
        print(f"\n📄 Enter Policy Content for '{title}':")
        print("(Type 'END' on a new line when finished)")
        
        content_lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines)
        if not content.strip():
            print("❌ Policy content is required!")
            return
        
        # Upload the policy
        try:
            result = upload_policy_text(title, content, policy_type, framework)
            if result["success"]:
                print(f"✅ Policy uploaded successfully!")
                print(f"   Policy ID: {result['policy_id']}")
                print(f"   Title: {title}")
                print(f"   Type: {policy_type}")
                print(f"   Framework: {framework}")
            else:
                print(f"❌ Upload failed: {result['error']}")
        except Exception as e:
            print(f"❌ Error uploading policy: {e}")
    
    def upload_from_file(self):
        """Upload policy from file"""
        print("\n📁 Upload Policy from File")
        print("-" * 30)
        
        file_path = input("Enter file path: ").strip().strip('"')
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        # Get policy details
        title = input("Policy Title (or press Enter to use filename): ").strip()
        if not title:
            title = Path(file_path).stem
        
        policy_type = input("Policy Type (compliance/risk/fraud/operational/security/audit): ").strip().lower()
        if policy_type not in ["compliance", "risk", "fraud", "operational", "security", "audit"]:
            print("❌ Invalid policy type!")
            return
        
        framework = input("Framework (SOX/Basel III/PCI DSS/GDPR/IFRS/FATCA/Other): ").strip()
        if not framework:
            framework = "Other"
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
        
        if not content.strip():
            print("❌ File is empty!")
            return
        
        # Upload the policy
        try:
            result = upload_policy_text(title, content, policy_type, framework)
            if result["success"]:
                print(f"✅ Policy uploaded successfully!")
                print(f"   Policy ID: {result['policy_id']}")
                print(f"   Title: {title}")
                print(f"   Type: {policy_type}")
                print(f"   Framework: {framework}")
            else:
                print(f"❌ Upload failed: {result['error']}")
        except Exception as e:
            print(f"❌ Error uploading policy: {e}")
    
    def view_policies(self):
        """View existing policies"""
        print("\n📋 Existing Policies")
        print("-" * 30)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, policy_type, framework, created_at
                FROM policies
                ORDER BY created_at DESC
                LIMIT 20
            ''')
            
            policies = cursor.fetchall()
            conn.close()
            
            if not policies:
                print("📭 No policies found.")
                return
            
            print(f"Found {len(policies)} policies:")
            print()
            
            for policy_id, title, policy_type, framework, created_at in policies:
                print(f"ID: {policy_id}")
                print(f"Title: {title}")
                print(f"Type: {policy_type}")
                print(f"Framework: {framework}")
                print(f"Created: {created_at}")
                print("-" * 40)
            
        except Exception as e:
            print(f"❌ Error viewing policies: {e}")
    
    def create_training_data(self):
        """Create training dataset from uploaded policies"""
        print("\n🎯 Create Training Dataset")
        print("-" * 30)
        
        try:
            # Create training dataset
            dataset_path = create_training_dataset()
            
            if dataset_path:
                print(f"✅ Training dataset created successfully!")
                print(f"   Dataset path: {dataset_path}")
                
                # Show dataset info
                with open(dataset_path, 'r', encoding='utf-8') as f:
                    dataset = json.load(f)
                
                print(f"   Total examples: {len(dataset)}")
                
                # Show sample
                if dataset:
                    print(f"\n📝 Sample training example:")
                    sample = dataset[0]
                    print(f"   Instruction: {sample['instruction'][:100]}...")
                    print(f"   Input: {sample['input'][:100]}...")
                    print(f"   Output: {sample['output'][:100]}...")
                
                print(f"\n🚀 Ready for model training!")
                return dataset_path
            else:
                print("❌ Failed to create training dataset")
                return None
                
        except Exception as e:
            print(f"❌ Error creating training dataset: {e}")
            return None
    
    def get_policy_statistics(self):
        """Get policy statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total policies
            cursor.execute("SELECT COUNT(*) FROM policies")
            total_policies = cursor.fetchone()[0]
            
            # By type
            cursor.execute("SELECT policy_type, COUNT(*) FROM policies GROUP BY policy_type")
            by_type = dict(cursor.fetchall())
            
            # By framework
            cursor.execute("SELECT framework, COUNT(*) FROM policies GROUP BY framework")
            by_framework = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                "total_policies": total_policies,
                "by_type": by_type,
                "by_framework": by_framework
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return None

def main():
    """Main function"""
    uploader = SimplePolicyUploader()
    
    # Show current statistics
    stats = uploader.get_policy_statistics()
    if stats:
        print(f"📊 Current Policy Database:")
        print(f"   Total Policies: {stats['total_policies']}")
        print(f"   By Type: {stats['by_type']}")
        print(f"   By Framework: {stats['by_framework']}")
        print()
    
    # Start interactive upload
    uploader.upload_policy_interactive()

if __name__ == "__main__":
    main()
