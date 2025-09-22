#!/usr/bin/env python3
"""
Simple BFSI Policy Upload Tool
Upload your BFSI policies directly for model training
"""

import os
import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path

# PDF processing imports
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ PyPDF2 not available. Install with: pip install PyPDF2")

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
                source_file TEXT,
                file_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add new columns if they don't exist (for existing databases)
        try:
            cursor.execute('ALTER TABLE policies ADD COLUMN source_file TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute('ALTER TABLE policies ADD COLUMN file_type TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def upload_policy_text(self, title, content, policy_type, framework, source_file=None, file_type=None):
        """Upload policy from text"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert policy
            cursor.execute('''
                INSERT INTO policies (title, content, policy_type, framework, source_file, file_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, policy_type, framework, source_file, file_type))
            
            policy_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Policy uploaded successfully: {title} (ID: {policy_id})")
            return {"success": True, "policy_id": policy_id}
            
        except Exception as e:
            logger.error(f"Error uploading policy: {e}")
            return {"success": False, "error": str(e)}
    
    def upload_policy_interactive(self):
        """Interactive policy upload"""
        print("🚀 BFSI Policy Upload Tool")
        print("=" * 50)
        
        # Show current statistics
        stats = self.get_policy_statistics()
        if stats:
            print(f"📊 Current Policy Database:")
            print(f"   Total Policies: {stats['total_policies']}")
            print(f"   By Type: {stats['by_type']}")
            print(f"   By Framework: {stats['by_framework']}")
            print()
        
        while True:
            print("\n📋 Policy Upload Options:")
            print("1. Upload policy from text input")
            print("2. Upload policy from file")
            print("3. Upload PDF documents")
            print("4. View existing policies")
            print("5. Create training dataset")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                self.upload_from_text()
            elif choice == "2":
                self.upload_from_file()
            elif choice == "3":
                self.upload_pdf_documents()
            elif choice == "4":
                self.view_policies()
            elif choice == "5":
                self.create_training_data()
            elif choice == "6":
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
        result = self.upload_policy_text(title, content, policy_type, framework)
        if result["success"]:
            print(f"✅ Policy uploaded successfully!")
            print(f"   Policy ID: {result['policy_id']}")
            print(f"   Title: {title}")
            print(f"   Type: {policy_type}")
            print(f"   Framework: {framework}")
        else:
            print(f"❌ Upload failed: {result['error']}")
    
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
        result = self.upload_policy_text(title, content, policy_type, framework)
        if result["success"]:
            print(f"✅ Policy uploaded successfully!")
            print(f"   Policy ID: {result['policy_id']}")
            print(f"   Title: {title}")
            print(f"   Type: {policy_type}")
            print(f"   Framework: {framework}")
        else:
            print(f"❌ Upload failed: {result['error']}")
    
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
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all policies
            cursor.execute("SELECT title, content, policy_type, framework FROM policies")
            policies = cursor.fetchall()
            conn.close()
            
            if not policies:
                print("📭 No policies found to create training data.")
                return None
            
            # Create training examples
            training_data = []
            
            for title, content, policy_type, framework in policies:
                # Create multiple training examples for each policy
                examples = self._create_training_examples(title, content, policy_type, framework)
                training_data.extend(examples)
            
            # Create datasets directory
            datasets_dir = Path("../../data/training_datasets/training_datasets")
            datasets_dir.mkdir(parents=True, exist_ok=True)
            
            # Save dataset
            dataset_path = datasets_dir / f"enhanced_bfsi_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(dataset_path, 'w', encoding='utf-8') as f:
                json.dump(training_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Training dataset created successfully!")
            print(f"   Dataset path: {dataset_path}")
            print(f"   Total policies: {len(policies)}")
            print(f"   Total examples: {len(training_data)}")
            
            # Show sample
            if training_data:
                print(f"\n📝 Sample training example:")
                sample = training_data[0]
                print(f"   Instruction: {sample['instruction'][:100]}...")
                print(f"   Input: {sample['input'][:100]}...")
                print(f"   Output: {sample['output'][:100]}...")
            
            print(f"\n🚀 Ready for model training!")
            return str(dataset_path)
            
        except Exception as e:
            print(f"❌ Error creating training dataset: {e}")
            return None
    
    def _create_training_examples(self, title, content, policy_type, framework):
        """Create training examples from policy"""
        examples = []
        
        # Policy summary example
        examples.append({
            "instruction": f"Summarize this {policy_type} policy under {framework} framework:",
            "input": content[:500] + "..." if len(content) > 500 else content,
            "output": f"Policy Summary: {title}\nType: {policy_type}\nFramework: {framework}\n\nThis policy outlines key requirements for {policy_type} management under {framework} framework. It includes specific procedures for compliance monitoring, risk assessment, and implementation guidelines. The policy ensures adherence to regulatory standards and provides clear guidance for stakeholders."
        })
        
        # Policy analysis example
        examples.append({
            "instruction": f"Analyze the compliance requirements in this {policy_type} policy:",
            "input": content,
            "output": f"Compliance Analysis for {title}:\n\nKey Requirements:\n1. Establish governance structures with clear roles and responsibilities\n2. Implement monitoring systems for {policy_type} activities\n3. Develop reporting mechanisms for regulatory compliance\n4. Create incident response procedures\n5. Ensure regular training and awareness programs\n\nFramework: {framework}\nType: {policy_type}\n\nThis policy ensures comprehensive compliance with {framework} requirements through structured implementation and ongoing monitoring."
        })
        
        # Risk assessment example (for risk-related policies)
        if policy_type in ['risk', 'compliance', 'security']:
            examples.append({
                "instruction": "Identify potential risks and mitigation strategies:",
                "input": content,
                "output": f"Risk Assessment for {title}:\n\nIdentified Risks:\n1. Regulatory non-compliance leading to penalties\n2. Operational failures affecting business continuity\n3. Security breaches compromising sensitive data\n4. Inadequate monitoring and reporting\n5. Insufficient staff training and awareness\n\nMitigation Strategies:\n1. Implement robust monitoring and audit procedures\n2. Establish clear escalation and incident response protocols\n3. Conduct regular risk assessments and reviews\n4. Provide comprehensive staff training programs\n5. Maintain detailed documentation and reporting systems\n\nFramework: {framework}"
            })
        
        # Implementation guidance example
        examples.append({
            "instruction": f"Provide implementation guidance for this {policy_type} policy:",
            "input": content,
            "output": f"Implementation Guidance for {title}:\n\nStep 1: Policy Review and Understanding\n- Conduct thorough review of policy requirements\n- Identify key stakeholders and responsibilities\n- Assess current state vs. policy requirements\n\nStep 2: Gap Analysis\n- Compare existing procedures with policy requirements\n- Identify areas requiring improvement or implementation\n- Prioritize implementation activities\n\nStep 3: Implementation Planning\n- Develop detailed implementation timeline\n- Assign responsibilities to appropriate teams\n- Establish success metrics and monitoring procedures\n\nStep 4: Training and Communication\n- Develop training materials for all stakeholders\n- Conduct awareness sessions and training programs\n- Establish communication channels for ongoing support\n\nStep 5: Monitoring and Review\n- Implement monitoring systems for policy compliance\n- Conduct regular reviews and assessments\n- Update procedures based on lessons learned\n\nFramework: {framework}\nPolicy Type: {policy_type}"
        })
        
        return examples
    
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

    def upload_pdf_documents(self):
        """Upload PDF documents and extract text"""
        if not PDF_AVAILABLE:
            print("❌ PDF processing not available. Please install PyPDF2:")
            print("   pip install PyPDF2")
            return
        
        print("\n📄 Upload PDF Documents")
        print("-" * 30)
        
        # Get PDF file path
        pdf_path = input("Enter path to PDF file: ").strip()
        if not pdf_path:
            print("❌ No file path provided")
            return
        
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return
        
        if not pdf_path.lower().endswith('.pdf'):
            print("❌ File must be a PDF document")
            return
        
        try:
            # Extract text from PDF
            print("📖 Extracting text from PDF...")
            content = self._extract_pdf_text(pdf_path)
            
            if not content.strip():
                print("❌ No text content found in PDF")
                return
            
            print(f"✅ Extracted {len(content)} characters from PDF")
            
            # Get policy details
            title = input("Enter policy title: ").strip()
            if not title:
                title = os.path.basename(pdf_path).replace('.pdf', '')
            
            print("\nPolicy Types:")
            print("1. Risk Management")
            print("2. Compliance")
            print("3. Security")
            print("4. Governance")
            print("5. Operational")
            print("6. Financial")
            print("7. Other")
            
            type_choice = input("Select policy type (1-7): ").strip()
            type_map = {
                "1": "risk", "2": "compliance", "3": "security", 
                "4": "governance", "5": "operational", "6": "financial", "7": "other"
            }
            policy_type = type_map.get(type_choice, "other")
            
            print("\nFrameworks:")
            print("1. Basel III")
            print("2. SOX")
            print("3. GDPR")
            print("4. PCI DSS")
            print("5. ISO 27001")
            print("6. COSO")
            print("7. Other")
            
            framework_choice = input("Select framework (1-7): ").strip()
            framework_map = {
                "1": "basel_iii", "2": "sox", "3": "gdpr", 
                "4": "pci_dss", "5": "iso_27001", "6": "coso", "7": "other"
            }
            framework = framework_map.get(framework_choice, "other")
            
            # Upload the policy
            result = self.upload_policy_text(
                title, content, policy_type, framework, 
                os.path.basename(pdf_path), "pdf"
            )
            
            if result["success"]:
                print(f"✅ PDF policy uploaded successfully!")
                print(f"   Policy ID: {result['policy_id']}")
                print(f"   Title: {title}")
                print(f"   Type: {policy_type}")
                print(f"   Framework: {framework}")
                print(f"   Source: {os.path.basename(pdf_path)}")
                print(f"   Content Length: {len(content)} characters")
            else:
                print(f"❌ Upload failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
    
    def _extract_pdf_text(self, pdf_path):
        """Extract text content from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {e}")

def main():
    """Main function"""
    uploader = SimplePolicyUploader()
    uploader.upload_policy_interactive()

if __name__ == "__main__":
    main()
