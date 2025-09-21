#!/usr/bin/env python3
"""
Real-Time BFSI Data Integration
Connects to real BFSI data sources and processes live operations
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
import sqlite3
from pathlib import Path
from database_connection_manager import get_db_connection

from bfsi_local_ai_integration import bfsi_agent, process_bfsi_compliance_check, process_bfsi_risk_assessment, process_bfsi_fraud_detection, process_bfsi_document_analysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RealTimeBFSIEvent:
    """Real-time BFSI event data structure"""
    event_id: str
    event_type: str
    timestamp: datetime
    source_system: str
    data: Dict[str, Any]
    priority: str = "medium"
    processed: bool = False

@dataclass
class BFSIDataSource:
    """BFSI data source configuration"""
    name: str
    type: str  # database, api, file, stream
    connection_config: Dict[str, Any]
    refresh_interval: int = 60  # seconds
    enabled: bool = True

class RealTimeBFSIDataManager:
    """
    Real-Time BFSI Data Manager
    Manages connections to real BFSI data sources and processes live events
    """
    
    def __init__(self, max_queue_size: int = 1000):
        self.data_sources: List[BFSIDataSource] = []
        # Use asyncio.Queue for thread-safe operations with size limit
        self.event_queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.processing_active = False
        self.db_path = "bfsi_realtime_data.db"
        self.max_queue_size = max_queue_size
        self.setup_database()
        self.load_data_sources()
        
        logger.info("Real-Time BFSI Data Manager initialized with queue size limit: %d", max_queue_size)
    
    async def safe_queue_put(self, event: RealTimeBFSIEvent) -> bool:
        """
        Safely add event to queue with atomic overflow handling.
        If queue is full, atomically removes oldest event and adds new one.
        Returns True if event was added successfully, False otherwise.
        """
        try:
            self.event_queue.put_nowait(event)
            logger.debug(f"Event {event.event_id} added to queue")
            return True
        except asyncio.QueueFull:
            logger.warning(f"Event queue is full, replacing oldest event with {event.event_id}")
            try:
                # Atomic operation: remove oldest and add new in one step
                oldest_event = self.event_queue.get_nowait()
                self.event_queue.put_nowait(event)
                logger.info(f"Replaced oldest event {oldest_event.event_id} with {event.event_id}")
                return True
            except asyncio.QueueEmpty:
                # This should not happen, but handle gracefully
                logger.error(f"Queue became empty unexpectedly while trying to replace event {event.event_id}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error during queue replacement for event {event.event_id}: {e}")
                return False
    
    def setup_database(self):
        """Setup SQLite database for real-time data storage with connection pooling"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                cursor = conn.cursor()
                
                # Create tables for different BFSI data types
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS transactions (
                        id TEXT PRIMARY KEY,
                        transaction_id TEXT,
                        amount REAL,
                        customer_id TEXT,
                        transaction_type TEXT,
                        location TEXT,
                        timestamp DATETIME,
                        risk_score REAL,
                        processed BOOLEAN DEFAULT FALSE
                    )
                ''')
                
                # Create indices for transactions table
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_processed ON transactions(processed)')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS compliance_checks (
                        id TEXT PRIMARY KEY,
                        regulation TEXT,
                        process TEXT,
                        controls TEXT,
                        documents TEXT,
                        timestamp DATETIME,
                        compliance_score REAL,
                        processed BOOLEAN DEFAULT FALSE
                    )
                ''')
                
                # Create indices for compliance_checks table
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_compliance_checks_timestamp ON compliance_checks(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_compliance_checks_processed ON compliance_checks(processed)')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS risk_assessments (
                        id TEXT PRIMARY KEY,
                        risk_type TEXT,
                        portfolio TEXT,
                        exposure REAL,
                        probability TEXT,
                        impact TEXT,
                        timestamp DATETIME,
                        risk_score REAL,
                        processed BOOLEAN DEFAULT FALSE
                    )
                ''')
                
                # Create indices for risk_assessments table
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_risk_assessments_timestamp ON risk_assessments(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_risk_assessments_processed ON risk_assessments(processed)')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS documents (
                        id TEXT PRIMARY KEY,
                        document_type TEXT,
                        content TEXT,
                        classification TEXT,
                        compliance_framework TEXT,
                        timestamp DATETIME,
                        processed BOOLEAN DEFAULT FALSE
                    )
                ''')
                
                # Create indices for documents table
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_timestamp ON documents(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_processed ON documents(processed)')
                
                conn.commit()
                logger.info("Database setup completed with connection pooling")
        except sqlite3.Error as e:
            logger.error(f"Database setup failed: {e}")
            raise
    
    def load_data_sources(self):
        """Load configured data sources from environment variables"""
        # Load configuration from environment variables with sensible defaults
        db_host = os.getenv('BFSI_DB_HOST', 'localhost')
        db_name = os.getenv('BFSI_DB_NAME', 'bfsi_transactions')
        db_table = os.getenv('BFSI_DB_TABLE', 'transactions')
        
        compliance_api_url = os.getenv('BFSI_COMPLIANCE_API_URL', 'http://localhost:8080/api/compliance')
        compliance_auth_token = os.getenv('BFSI_COMPLIANCE_AUTH_TOKEN', '')
        
        risk_api_url = os.getenv('BFSI_RISK_API_URL', 'http://localhost:8080/api/risk')
        risk_auth_token = os.getenv('BFSI_RISK_AUTH_TOKEN', '')
        
        document_path = os.getenv('BFSI_DOCUMENT_PATH', './bfsi_documents')
        document_file_types = os.getenv('BFSI_DOCUMENT_FILE_TYPES', '.pdf,.docx,.txt').split(',')
        
        # Refresh intervals from environment with defaults
        db_refresh_interval = int(os.getenv('BFSI_DB_REFRESH_INTERVAL', '30'))
        compliance_refresh_interval = int(os.getenv('BFSI_COMPLIANCE_REFRESH_INTERVAL', '60'))
        risk_refresh_interval = int(os.getenv('BFSI_RISK_REFRESH_INTERVAL', '120'))
        document_refresh_interval = int(os.getenv('BFSI_DOCUMENT_REFRESH_INTERVAL', '300'))
        
        self.data_sources = [
            BFSIDataSource(
                name="Transaction Database",
                type="database",
                connection_config={
                    "host": db_host,
                    "database": db_name,
                    "table": db_table
                },
                refresh_interval=db_refresh_interval
            ),
            BFSIDataSource(
                name="Compliance API",
                type="api",
                connection_config={
                    "url": compliance_api_url,
                    "auth_token": compliance_auth_token
                },
                refresh_interval=compliance_refresh_interval
            ),
            BFSIDataSource(
                name="Risk Management System",
                type="api",
                connection_config={
                    "url": risk_api_url,
                    "auth_token": risk_auth_token
                },
                refresh_interval=risk_refresh_interval
            ),
            BFSIDataSource(
                name="Document Repository",
                type="file",
                connection_config={
                    "path": document_path,
                    "file_types": document_file_types
                },
                refresh_interval=document_refresh_interval
            )
        ]
        logger.info(f"Loaded {len(self.data_sources)} data sources from environment configuration")
    
    async def start_real_time_processing(self):
        """Start real-time data processing"""
        self.processing_active = True
        logger.info("Starting real-time BFSI data processing...")
        
        # Start background tasks and store as instance variables for lifecycle management
        self.monitor_task = asyncio.create_task(self.monitor_data_sources())
        self.process_task = asyncio.create_task(self.process_event_queue())
        self.generate_task = asyncio.create_task(self.generate_sample_real_data())
        
        await asyncio.gather(self.monitor_task, self.process_task, self.generate_task)
    
    async def monitor_data_sources(self):
        """Monitor data sources for new data"""
        while self.processing_active:
            for source in self.data_sources:
                if source.enabled:
                    try:
                        await self.check_data_source(source)
                    except Exception as e:
                        logger.error(f"Error monitoring {source.name}: {e}")
            
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def check_data_source(self, source: BFSIDataSource):
        """Check a specific data source for new data"""
        if source.type == "database":
            await self.check_database_source(source)
        elif source.type == "api":
            await self.check_api_source(source)
        elif source.type == "file":
            await self.check_file_source(source)
    
    async def check_database_source(self, source: BFSIDataSource):
        """Check database source for new transactions"""
        # Simulate checking database for new transactions
        # In real implementation, connect to your actual database
        
        # Generate sample real-time transaction
        if datetime.now().second % 30 == 0:  # Every 30 seconds
            transaction = {
                "transaction_id": f"TXN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "amount": round(1000 + (datetime.now().microsecond % 100000), 2),
                "customer_id": f"CUST-{1000 + (datetime.now().microsecond % 100)}",
                "transaction_type": ["Wire Transfer", "Credit Card", "ACH", "Check"][datetime.now().microsecond % 4],
                "location": ["Domestic", "International"][datetime.now().microsecond % 2],
                "timestamp": datetime.now().isoformat()
            }
            
            event = RealTimeBFSIEvent(
                event_id=f"event_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                event_type="fraud_detection",
                timestamp=datetime.now(),
                source_system=source.name,
                data=transaction,
                priority="high" if transaction["amount"] > 50000 else "medium"
            )
            
            await self.safe_queue_put(event)
            logger.info(f"New transaction detected: {transaction['transaction_id']}")
    
    async def check_api_source(self, source: BFSIDataSource):
        """Check API source for new data"""
        # Simulate API calls to compliance and risk systems
        if "compliance" in source.name.lower():
            await self.check_compliance_api(source)
        elif "risk" in source.name.lower():
            await self.check_risk_api(source)
    
    async def check_compliance_api(self, source: BFSIDataSource):
        """Check compliance API for new checks"""
        # Simulate compliance check every 2 minutes
        if datetime.now().minute % 2 == 0 and datetime.now().second < 10:
            compliance_data = {
                "regulation": ["SOX", "PCI DSS", "Basel III", "GDPR"][datetime.now().minute % 4],
                "process": ["Financial Reporting", "Data Protection", "Risk Management", "Audit Trail"][datetime.now().minute % 4],
                "controls": [
                    ["Access Control", "Data Integrity"],
                    ["Encryption", "Backup"],
                    ["Monitoring", "Alerting"],
                    ["Documentation", "Training"]
                ][datetime.now().minute % 4],
                "documents": [f"Document_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"],
                "priority": "high"
            }
            
            event = RealTimeBFSIEvent(
                event_id=f"compliance_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                event_type="compliance_check",
                timestamp=datetime.now(),
                source_system=source.name,
                data=compliance_data,
                priority=compliance_data["priority"]
            )
            
            await self.safe_queue_put(event)
            logger.info(f"New compliance check: {compliance_data['regulation']}")
    
    async def check_risk_api(self, source: BFSIDataSource):
        """Check risk API for new assessments"""
        # Simulate risk assessment every 3 minutes
        if datetime.now().minute % 3 == 0 and datetime.now().second < 10:
            risk_data = {
                "risk_type": ["Credit Risk", "Market Risk", "Operational Risk", "Liquidity Risk"][datetime.now().minute % 4],
                "portfolio": ["Corporate Loans", "Retail Banking", "Investment Portfolio", "Trading Desk"][datetime.now().minute % 4],
                "exposure": round(1000000 + (datetime.now().microsecond % 50000000), 2),
                "probability": ["low", "medium", "high"][datetime.now().microsecond % 3],
                "impact": ["low", "medium", "high"][datetime.now().microsecond % 3],
                "controls": ["Credit Scoring", "Collateral Management", "Regular Reviews"]
            }
            
            event = RealTimeBFSIEvent(
                event_id=f"risk_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                event_type="risk_assessment",
                timestamp=datetime.now(),
                source_system=source.name,
                data=risk_data,
                priority="high" if risk_data["exposure"] > 10000000 else "medium"
            )
            
            await self.safe_queue_put(event)
            logger.info(f"New risk assessment: {risk_data['risk_type']}")
    
    async def check_file_source(self, source: BFSIDataSource):
        """Check file source for new documents"""
        # Simulate document processing every 5 minutes
        if datetime.now().minute % 5 == 0 and datetime.now().second < 10:
            # Extract document type to a separate variable first
            document_type = ["Loan Agreement", "Compliance Report", "Risk Assessment", "Audit Report"][datetime.now().minute % 4]
            
            document_data = {
                "document_type": document_type,
                "content": f"""
                {document_type} - {datetime.now().strftime('%Y-%m-%d')}
                
                This is a real-time generated document for BFSI processing.
                Document contains critical information requiring AI analysis.
                
                Key points:
                - Document ID: DOC-{datetime.now().strftime('%Y%m%d_%H%M%S')}
                - Generated: {datetime.now().isoformat()}
                - Priority: High
                - Requires immediate review
                """,
                "classification": ["Credit Documentation", "Compliance", "Risk Management", "Audit"][datetime.now().minute % 4],
                "compliance_framework": ["Basel III", "SOX", "PCI DSS", "GDPR"][datetime.now().minute % 4]
            }
            
            event = RealTimeBFSIEvent(
                event_id=f"document_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                event_type="document_analysis",
                timestamp=datetime.now(),
                source_system=source.name,
                data=document_data,
                priority="high"
            )
            
            await self.safe_queue_put(event)
            logger.info(f"New document: {document_data['document_type']}")
    
    async def generate_sample_real_data(self):
        """Generate sample real-time data for demonstration"""
        while self.processing_active:
            # Generate random real-time events
            await asyncio.sleep(45)  # Every 45 seconds
            
            if self.event_queue.empty():  # Only if queue is empty
                # Generate a random event type
                event_types = ["fraud_detection", "compliance_check", "risk_assessment", "document_analysis"]
                event_type = event_types[datetime.now().second % 4]
                
                if event_type == "fraud_detection":
                    data = {
                        "transaction_id": f"TXN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                        "amount": round(50000 + (datetime.now().microsecond % 200000), 2),
                        "customer_id": f"CUST-{2000 + (datetime.now().microsecond % 50)}",
                        "transaction_type": "Wire Transfer",
                        "location": "International",
                        "timestamp": datetime.now().isoformat()
                    }
                elif event_type == "compliance_check":
                    data = {
                        "regulation": "SOX",
                        "process": "Financial Reporting",
                        "controls": ["Access Control", "Data Integrity", "Audit Trail"],
                        "documents": [f"SOX_Report_{datetime.now().strftime('%Y%m%d')}.pdf"],
                        "priority": "high"
                    }
                elif event_type == "risk_assessment":
                    data = {
                        "risk_type": "Credit Risk",
                        "portfolio": "Corporate Loans",
                        "exposure": round(5000000 + (datetime.now().microsecond % 20000000), 2),
                        "probability": "medium",
                        "impact": "high",
                        "controls": ["Credit Scoring", "Collateral Management"]
                    }
                else:  # document_analysis
                    amount = round(1000000 + (datetime.now().microsecond % 5000000), 2)
                    data = {
                        "document_type": "Loan Agreement",
                        "content": f"Loan Agreement for {amount} - Generated {datetime.now().isoformat()}",
                        "classification": "Credit Documentation",
                        "compliance_framework": "Basel III"
                    }
                
                event = RealTimeBFSIEvent(
                    event_id=f"auto_{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                    event_type=event_type,
                    timestamp=datetime.now(),
                    source_system="Auto Generator",
                    data=data,
                    priority="high" if event_type in ["fraud_detection", "compliance_check"] else "medium"
                )
                
                await self.safe_queue_put(event)
                logger.info(f"Generated {event_type} event")
    
    async def process_event_queue(self):
        """Process events in the queue"""
        while self.processing_active:
            try:
                # Wait for event with timeout to allow checking processing_active
                try:
                    event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                    await self.process_bfsi_event(event)
                    self.event_queue.task_done()
                except asyncio.TimeoutError:
                    # No events in queue, continue loop to check processing_active
                    continue
            except Exception as e:
                logger.error(f"Error processing event queue: {e}")
                await asyncio.sleep(1)
    
    async def process_bfsi_event(self, event: RealTimeBFSIEvent):
        """Process a single BFSI event"""
        try:
            logger.info(f"Processing {event.event_type} event: {event.event_id}")
            
            # Route to appropriate BFSI processing function
            if event.event_type == "compliance_check":
                result = await process_bfsi_compliance_check(event.data)
            elif event.event_type == "risk_assessment":
                result = await process_bfsi_risk_assessment(event.data)
            elif event.event_type == "fraud_detection":
                result = await process_bfsi_fraud_detection(event.data)
            elif event.event_type == "document_analysis":
                result = await process_bfsi_document_analysis(event.data)
            else:
                logger.warning(f"Unknown event type: {event.event_type}")
                return
            
            # Store result in database
            await self.store_processing_result(event, result)
            
            # Mark event as processed
            event.processed = True
            
            logger.info(f"✅ Processed {event.event_type}: Risk={result.get('risk_score', 0)}, Compliance={result.get('compliance_score', 0)}")
            
        except Exception as e:
            logger.error(f"Error processing event {event.event_id}: {e}")
    
    async def store_processing_result(self, event: RealTimeBFSIEvent, result: Dict[str, Any]):
        """Store processing result in database with connection pooling"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                cursor = conn.cursor()
                
                if event.event_type == "fraud_detection":
                    cursor.execute('''
                        INSERT INTO transactions (id, transaction_id, amount, customer_id, transaction_type, location, timestamp, risk_score, processed)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        event.event_id,
                        event.data.get("transaction_id"),
                        event.data.get("amount"),
                        event.data.get("customer_id"),
                        event.data.get("transaction_type"),
                        event.data.get("location"),
                        event.timestamp.isoformat(),
                        result.get("risk_score", 0),
                        True
                    ))
                
                elif event.event_type == "compliance_check":
                    cursor.execute('''
                        INSERT INTO compliance_checks (id, regulation, process, controls, documents, timestamp, compliance_score, processed)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        event.event_id,
                        event.data.get("regulation"),
                        event.data.get("process"),
                        json.dumps(event.data.get("controls", [])),
                        json.dumps(event.data.get("documents", [])),
                        event.timestamp.isoformat(),
                        result.get("compliance_score", 0),
                        True
                    ))
                
                elif event.event_type == "risk_assessment":
                    cursor.execute('''
                        INSERT INTO risk_assessments (id, risk_type, portfolio, exposure, probability, impact, timestamp, risk_score, processed)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        event.event_id,
                        event.data.get("risk_type"),
                        event.data.get("portfolio"),
                        event.data.get("exposure"),
                        event.data.get("probability"),
                        event.data.get("impact"),
                        event.timestamp.isoformat(),
                        result.get("risk_score", 0),
                        True
                    ))
                
                elif event.event_type == "document_analysis":
                    cursor.execute('''
                        INSERT INTO documents (id, document_type, content, classification, compliance_framework, timestamp, processed)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        event.event_id,
                        event.data.get("document_type"),
                        event.data.get("content"),
                        event.data.get("classification"),
                        event.data.get("compliance_framework"),
                        event.timestamp.isoformat(),
                        True
                    ))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Database error storing result: {e}")
            raise
        except Exception as e:
            logger.error(f"Error storing result: {e}")
            raise
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time processing metrics with connection pooling"""
        try:
            with get_db_connection(self.db_path, max_connections=5, timeout=30) as conn:
                cursor = conn.cursor()
                
                # Get counts by type
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE processed = 1")
                transaction_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM compliance_checks WHERE processed = 1")
                compliance_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM risk_assessments WHERE processed = 1")
                risk_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM documents WHERE processed = 1")
                document_count = cursor.fetchone()[0]
                
                # Get recent activity (last hour)
                one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
                
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE timestamp > ?", (one_hour_ago,))
                recent_transactions = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM compliance_checks WHERE timestamp > ?", (one_hour_ago,))
                recent_compliance = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM risk_assessments WHERE timestamp > ?", (one_hour_ago,))
                recent_risk = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM documents WHERE timestamp > ?", (one_hour_ago,))
                recent_documents = cursor.fetchone()[0]
                
                return {
                    "total_processed": {
                        "transactions": transaction_count,
                        "compliance_checks": compliance_count,
                        "risk_assessments": risk_count,
                        "documents": document_count
                    },
                    "recent_activity_1h": {
                        "transactions": recent_transactions,
                        "compliance_checks": recent_compliance,
                        "risk_assessments": recent_risk,
                        "documents": recent_documents
                    },
                    "queue_status": {
                        "pending_events": self.event_queue.qsize(),
                        "processing_active": self.processing_active,
                        "data_sources_active": len([s for s in self.data_sources if s.enabled])
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
        except sqlite3.Error as e:
            logger.error(f"Database error getting metrics: {e}")
            return {"error": f"Database error: {str(e)}"}
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {"error": str(e)}
    
    def stop_processing(self):
        """Stop real-time processing"""
        logger.info("Stopping real-time processing...")
        
        # Set the flag to stop processing loops
        self.processing_active = False
        
        # Cancel all active async tasks
        tasks_to_cancel = []
        
        if hasattr(self, 'monitor_task') and self.monitor_task and not self.monitor_task.done():
            tasks_to_cancel.append(self.monitor_task)
            
        if hasattr(self, 'process_task') and self.process_task and not self.process_task.done():
            tasks_to_cancel.append(self.process_task)
            
        if hasattr(self, 'generate_task') and self.generate_task and not self.generate_task.done():
            tasks_to_cancel.append(self.generate_task)
        
        # Cancel all active tasks
        if tasks_to_cancel:
            logger.info(f"Cancelling {len(tasks_to_cancel)} active tasks...")
            for task in tasks_to_cancel:
                try:
                    task.cancel()
                except Exception as e:
                    logger.error(f"Error cancelling task: {e}")
        
        logger.info("Real-time processing stopped")

# Global instance
realtime_manager = RealTimeBFSIDataManager()

# Convenience functions
async def start_real_time_bfsi():
    """Start real-time BFSI processing"""
    await realtime_manager.start_real_time_processing()

async def get_real_time_status():
    """Get real-time processing status"""
    return realtime_manager.get_real_time_metrics()

def stop_real_time_bfsi():
    """Stop real-time BFSI processing"""
    realtime_manager.stop_processing()

# Example usage
if __name__ == "__main__":
    async def main():
        print("🚀 Starting Real-Time BFSI Data Processing")
        print("=" * 60)
        
        try:
            # Start real-time processing
            await start_real_time_bfsi()
        except KeyboardInterrupt:
            print("\n🛑 Stopping real-time processing...")
            stop_real_time_bfsi()
    
    # Run the real-time system
    asyncio.run(main())



