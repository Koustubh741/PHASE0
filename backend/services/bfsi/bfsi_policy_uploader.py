#!/usr/bin/env python3
"""
BFSI Policy Uploader and Processor
Upload, process, and prepare BFSI policies for LLM training
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib
import sqlite3
from dataclasses import dataclass, asdict
from database_connection_manager import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BFSIPolicy:
    """BFSI Policy data structure"""
    policy_id: str
    title: str
    policy_type: str  # compliance, risk, fraud, operational
    content: str
    framework: str  # SOX, PCI DSS, Basel III, GDPR, etc.
    version: str
    upload_date: datetime
    file_path: str
    file_hash: str
    status: str = "uploaded"  # uploaded, processed, training_ready
    metadata: Dict[str, Any] = None

@dataclass
class TrainingDataset:
    """Training dataset structure"""
    dataset_id: str
    name: str
    description: str
    policies: List[str]  # policy IDs
    created_date: datetime
    total_tokens: int
    total_policies: int
    framework_coverage: List[str]
    status: str = "created"  # created, processing, ready, training

class BFSIPolicyManager:
    """
    BFSI Policy Manager
    Handles policy uploads, processing, and training dataset creation
    """
    
    def __init__(self):
        self.db_path = "bfsi_policies.db"
        self.policies_dir = Path("bfsi_policies")
        self.training_dir = Path("bfsi_training_data")
        
        # Create directories
        self.policies_dir.mkdir(exist_ok=True)
        self.training_dir.mkdir(exist_ok=True)
        
        self.setup_database()
        
        logger.info("BFSI Policy Manager initialized")
    
    def setup_database(self):
        """Setup SQLite database for policy management with connection pooling"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                cursor = conn.cursor()
                
                # Create policies table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS policies (
                        policy_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        policy_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        framework TEXT NOT NULL,
                        version TEXT NOT NULL,
                        upload_date DATETIME NOT NULL,
                        file_path TEXT NOT NULL,
                        file_hash TEXT UNIQUE NOT NULL,
                        status TEXT DEFAULT 'uploaded',
                        metadata TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create training datasets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS training_datasets (
                        dataset_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        policies TEXT NOT NULL,
                        created_date DATETIME NOT NULL,
                        total_tokens INTEGER DEFAULT 0,
                        total_policies INTEGER DEFAULT 0,
                        framework_coverage TEXT NOT NULL,
                        status TEXT DEFAULT 'created',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create training chunks table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS training_chunks (
                        chunk_id TEXT PRIMARY KEY,
                        dataset_id TEXT NOT NULL,
                        policy_id TEXT NOT NULL,
                        chunk_index INTEGER NOT NULL,
                        content TEXT NOT NULL,
                        tokens INTEGER NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (dataset_id) REFERENCES training_datasets (dataset_id),
                        FOREIGN KEY (policy_id) REFERENCES policies (policy_id)
                    )
                ''')
                
                conn.commit()
                logger.info("Database setup completed with connection pooling")
        except sqlite3.Error as e:
            logger.error(f"Database setup failed: {e}")
            raise
    
    def _safe_json_loads(self, json_string: str) -> Dict[str, Any]:
        """Safely parse JSON string with error handling"""
        try:
            return json.loads(json_string) if json_string else {}
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Failed to parse JSON: {e}")
            return {}
    
    def upload_policy_file(self, file_path: str, policy_type: str, framework: str, 
                          version: str = "1.0", metadata: Dict[str, Any] = None) -> str:
        """Upload a policy file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate file hash
            file_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Check if already uploaded
            if self.policy_exists_by_hash(file_hash):
                logger.warning(f"Policy already uploaded: {file_hash}")
                return self.get_policy_id_by_hash(file_hash)
            
            # Generate policy ID
            policy_id = f"policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_hash[:8]}"
            
            # Copy file to policies directory
            target_path = self.policies_dir / f"{policy_id}.txt"
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Create policy object
            # Use title from metadata if provided, otherwise use filename
            title = (metadata or {}).get('title', file_path.stem)
            policy = BFSIPolicy(
                policy_id=policy_id,
                title=title,
                policy_type=policy_type,
                content=content,
                framework=framework,
                version=version,
                upload_date=datetime.now(),
                file_path=str(target_path),
                file_hash=file_hash,
                metadata=metadata or {}
            )
            
            # Save to database
            self.save_policy(policy)
            
            logger.info(f"Policy uploaded successfully: {policy_id}")
            return policy_id
            
        except Exception as e:
            logger.error(f"Error uploading policy: {e}")
            raise
    
    def upload_policy_text(self, title: str, content: str, policy_type: str, 
                          framework: str, version: str = "1.0", 
                          metadata: Dict[str, Any] = None) -> str:
        """Upload policy content directly as text"""
        try:
            # Generate content hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Check if already uploaded
            if self.policy_exists_by_hash(content_hash):
                logger.warning(f"Policy already uploaded: {content_hash}")
                return self.get_policy_id_by_hash(content_hash)
            
            # Generate policy ID
            policy_id = f"policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{content_hash[:8]}"
            
            # Save to file
            target_path = self.policies_dir / f"{policy_id}.txt"
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Create policy object
            policy = BFSIPolicy(
                policy_id=policy_id,
                title=title,
                policy_type=policy_type,
                content=content,
                framework=framework,
                version=version,
                upload_date=datetime.now(),
                file_path=str(target_path),
                file_hash=content_hash,
                metadata=metadata or {}
            )
            
            # Save to database
            self.save_policy(policy)
            
            logger.info(f"Policy uploaded successfully: {policy_id}")
            return policy_id
            
        except Exception as e:
            logger.error(f"Error uploading policy: {e}")
            raise
    
    def save_policy(self, policy: BFSIPolicy):
        """Save policy to database with connection pooling"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO policies (policy_id, title, policy_type, content, framework, 
                                        version, upload_date, file_path, file_hash, status, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    policy.policy_id,
                    policy.title,
                    policy.policy_type,
                    policy.content,
                    policy.framework,
                    policy.version,
                    policy.upload_date.isoformat(),
                    policy.file_path,
                    policy.file_hash,
                    policy.status,
                    json.dumps(policy.metadata)
                ))
                
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error saving policy: {e}")
            raise
        except Exception as e:
            logger.error(f"Error saving policy: {e}")
            raise
    
    def policy_exists_by_hash(self, file_hash: str) -> bool:
        """Check if policy exists by hash with connection pooling"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT 1 FROM policies WHERE file_hash = ?", (file_hash,))
                exists = cursor.fetchone() is not None
                
                return exists
        except sqlite3.Error as e:
            logger.error(f"Database error checking policy existence: {e}")
            return False
    
    def get_policy_id_by_hash(self, file_hash: str) -> str:
        """Get policy ID by hash with connection pooling"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT policy_id FROM policies WHERE file_hash = ?", (file_hash,))
                result = cursor.fetchone()
                
                return result[0] if result else None
        except sqlite3.Error as e:
            logger.error(f"Database error getting policy ID: {e}")
            return None
    
    def get_all_policies(self) -> List[BFSIPolicy]:
        """Get all policies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT policy_id, title, policy_type, content, framework, version, 
                   upload_date, file_path, file_hash, status, metadata
            FROM policies
            ORDER BY upload_date DESC
        """)
        
        policies = []
        for row in cursor.fetchall():
            policy = BFSIPolicy(
                policy_id=row[0],
                title=row[1],
                policy_type=row[2],
                content=row[3],
                framework=row[4],
                version=row[5],
                upload_date=datetime.fromisoformat(row[6]),
                file_path=row[7],
                file_hash=row[8],
                status=row[9],
                metadata=self._safe_json_loads(row[10]) if row[10] else {}
            )
            policies.append(policy)
        
        conn.close()
        return policies
    
    def delete_policy(self, policy_id: str) -> bool:
        """Delete a policy by ID with connection pooling and context management"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                with conn.cursor() as cursor:
                    # Check if policy exists
                    cursor.execute("SELECT policy_id FROM policies WHERE policy_id = ?", (policy_id,))
                    if not cursor.fetchone():
                        return False
                    
                    # Delete the policy
                    cursor.execute("DELETE FROM policies WHERE policy_id = ?", (policy_id,))
                    conn.commit()
                    
                    # Check if deletion was successful
                    rows_affected = cursor.rowcount
                    return rows_affected > 0
                    
        except sqlite3.Error as e:
            logger.error(f"Database error deleting policy {policy_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error deleting policy {policy_id}: {e}")
            return False
    
    def create_training_dataset(self, name: str, description: str, 
                               policy_ids: List[str], framework_filter: List[str] = None) -> str:
        """Create a training dataset from policies"""
        try:
            # Get policies
            policies = self.get_all_policies()
            
            if policy_ids:
                # Filter by specific policy IDs
                selected_policies = [p for p in policies if p.policy_id in policy_ids]
            else:
                # Filter by framework if specified
                if framework_filter:
                    selected_policies = [p for p in policies if p.framework in framework_filter]
                else:
                    selected_policies = policies
            
            if not selected_policies:
                raise ValueError("No policies found for training dataset")
            
            # Generate dataset ID
            dataset_id = f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Calculate metrics
            total_tokens = sum(len(p.content.split()) for p in selected_policies)
            framework_coverage = list(set(p.framework for p in selected_policies))
            
            # Create training dataset
            dataset = TrainingDataset(
                dataset_id=dataset_id,
                name=name,
                description=description,
                policies=[p.policy_id for p in selected_policies],
                created_date=datetime.now(),
                total_tokens=total_tokens,
                total_policies=len(selected_policies),
                framework_coverage=framework_coverage
            )
            
            # Save to database
            self.save_training_dataset(dataset)
            
            # Create training chunks
            self.create_training_chunks(dataset, selected_policies)
            
            logger.info(f"Training dataset created: {dataset_id}")
            return dataset_id
            
        except Exception as e:
            logger.error(f"Error creating training dataset: {e}")
            raise
    
    def save_training_dataset(self, dataset: TrainingDataset):
        """Save training dataset to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO training_datasets (dataset_id, name, description, policies, 
                                         created_date, total_tokens, total_policies, 
                                         framework_coverage, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dataset.dataset_id,
            dataset.name,
            dataset.description,
            json.dumps(dataset.policies),
            dataset.created_date.isoformat(),
            dataset.total_tokens,
            dataset.total_policies,
            json.dumps(dataset.framework_coverage),
            dataset.status
        ))
        
        conn.commit()
        conn.close()
    
    def create_training_chunks(self, dataset: TrainingDataset, policies: List[BFSIPolicy]):
        """Create training chunks from policies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for policy in policies:
            # Split content into chunks (e.g., 512 tokens per chunk)
            chunks = self.split_into_chunks(policy.content, max_tokens=512)
            
            for i, chunk_content in enumerate(chunks):
                chunk_id = f"chunk_{dataset.dataset_id}_{policy.policy_id}_{i}"
                tokens = len(chunk_content.split())
                
                cursor.execute('''
                    INSERT INTO training_chunks (chunk_id, dataset_id, policy_id, 
                                               chunk_index, content, tokens)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    chunk_id,
                    dataset.dataset_id,
                    policy.policy_id,
                    i,
                    chunk_content,
                    tokens
                ))
        
        conn.commit()
        conn.close()
        logger.info(f"Created training chunks for dataset: {dataset.dataset_id}")
    
    def split_into_chunks(self, content: str, max_tokens: int = 512) -> List[str]:
        """Split content into chunks"""
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), max_tokens):
            chunk = ' '.join(words[i:i + max_tokens])
            chunks.append(chunk)
        
        return chunks
    
    def get_training_chunks(self, dataset_id: str) -> List[Dict[str, Any]]:
        """Get training chunks for a dataset"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT chunk_id, policy_id, chunk_index, content, tokens
            FROM training_chunks
            WHERE dataset_id = ?
            ORDER BY policy_id, chunk_index
        """, (dataset_id,))
        
        chunks = []
        for row in cursor.fetchall():
            chunks.append({
                "chunk_id": row[0],
                "policy_id": row[1],
                "chunk_index": row[2],
                "content": row[3],
                "tokens": row[4]
            })
        
        conn.close()
        return chunks
    
    def export_training_data(self, dataset_id: str, format: str = "json") -> str:
        """Export training data in specified format"""
        try:
            chunks = self.get_training_chunks(dataset_id)
            
            if format == "json":
                output_file = self.training_dir / f"{dataset_id}_training_data.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks, f, indent=2, ensure_ascii=False)
            
            elif format == "txt":
                output_file = self.training_dir / f"{dataset_id}_training_data.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    for chunk in chunks:
                        f.write(f"=== Chunk {chunk['chunk_index']} (Policy: {chunk['policy_id']}) ===\n")
                        f.write(chunk['content'])
                        f.write("\n\n")
            
            elif format == "jsonl":
                output_file = self.training_dir / f"{dataset_id}_training_data.jsonl"
                with open(output_file, 'w', encoding='utf-8') as f:
                    for chunk in chunks:
                        json.dump({
                            "text": chunk['content'],
                            "metadata": {
                                "chunk_id": chunk['chunk_id'],
                                "policy_id": chunk['policy_id'],
                                "chunk_index": chunk['chunk_index'],
                                "tokens": chunk['tokens']
                            }
                        }, f, ensure_ascii=False)
                        f.write("\n")
            
            logger.info(f"Training data exported: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error exporting training data: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get policy and training statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Policy statistics
        cursor.execute("SELECT COUNT(*) FROM policies")
        total_policies = cursor.fetchone()[0]
        
        cursor.execute("SELECT policy_type, COUNT(*) FROM policies GROUP BY policy_type")
        policies_by_type = dict(cursor.fetchall())
        
        cursor.execute("SELECT framework, COUNT(*) FROM policies GROUP BY framework")
        policies_by_framework = dict(cursor.fetchall())
        
        # Training dataset statistics
        cursor.execute("SELECT COUNT(*) FROM training_datasets")
        total_datasets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM training_chunks")
        total_chunks = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_policies": total_policies,
            "policies_by_type": policies_by_type,
            "policies_by_framework": policies_by_framework,
            "total_datasets": total_datasets,
            "total_chunks": total_chunks
        }

# Global instance
policy_manager = BFSIPolicyManager()

# Convenience functions
def upload_policy_file(file_path: str, policy_type: str, framework: str, 
                      version: str = "1.0", metadata: Dict[str, Any] = None) -> str:
    """Upload a policy file"""
    return policy_manager.upload_policy_file(file_path, policy_type, framework, version, metadata)

def upload_policy_text(title: str, content: str, policy_type: str, 
                      framework: str, version: str = "1.0", 
                      metadata: Dict[str, Any] = None) -> str:
    """Upload policy content as text"""
    return policy_manager.upload_policy_text(title, content, policy_type, framework, version, metadata)

def create_training_dataset(name: str, description: str, 
                           policy_ids: List[str] = None, 
                           framework_filter: List[str] = None) -> str:
    """Create a training dataset"""
    return policy_manager.create_training_dataset(name, description, policy_ids, framework_filter)

def get_policy_statistics() -> Dict[str, Any]:
    """Get policy statistics"""
    return policy_manager.get_statistics()

# Example usage
if __name__ == "__main__":
    # Example: Upload a sample policy
    sample_policy = """
    BFSI COMPLIANCE POLICY
    
    This policy outlines the compliance requirements for Banking, Financial Services, and Insurance (BFSI) operations.
    
    Key Requirements:
    1. All financial transactions must be recorded and auditable
    2. Customer data must be protected according to GDPR and local regulations
    3. Risk assessments must be conducted quarterly
    4. Fraud detection systems must be operational 24/7
    
    Implementation:
    - Automated monitoring systems
    - Regular compliance training
    - Quarterly audits
    - Incident reporting procedures
    
    This policy is effective immediately and supersedes all previous versions.
    """
    
    print("🚀 BFSI Policy Uploader")
    print("=" * 50)
    
    # Upload sample policy
    policy_id = upload_policy_text(
        title="BFSI Compliance Policy",
        content=sample_policy,
        policy_type="compliance",
        framework="SOX",
        version="1.0",
        metadata={"department": "Risk Management", "approver": "Chief Risk Officer"}
    )
    
    print(f"✅ Sample policy uploaded: {policy_id}")
    
    # Get statistics
    stats = get_policy_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total Policies: {stats['total_policies']}")
    print(f"   By Type: {stats['policies_by_type']}")
    print(f"   By Framework: {stats['policies_by_framework']}")
    
    print("\n🎯 Ready to upload your BFSI policies!")

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        