#!/usr/bin/env python3
"""
Secure Data Access Layer for BFSI API
Repository pattern with connection pooling and encryption
"""

import psycopg2
from psycopg2 import pool
import threading
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
import json
from queue import Queue, Empty
import hashlib
from cryptography.fernet import InvalidToken
import os

from security_config import security_config, encryption_manager

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration for PostgreSQL connection pooling"""
    # PostgreSQL connection parameters
    host: str = "localhost"
    port: int = 5432
    database: str = "bfsi_security"
    username: str = "bfsi_user"
    password: str = ""
    
    # Connection pool settings
    max_connections: int = 10
    min_connections: int = 2
    connection_timeout: int = 30
    
    # Security settings
    encryption_enabled: bool = True
    audit_enabled: bool = True
    ssl_mode: str = "prefer"  # prefer, require, verify-ca, verify-full
    
    # Legacy compatibility (deprecated)
    db_path: str = ""
    
    @classmethod
    def from_environment(cls) -> 'DatabaseConfig':
        """Create DatabaseConfig from environment variables"""
        return cls(
            host=os.getenv('BFSI_DB_HOST', 'localhost'),
            port=int(os.getenv('BFSI_DB_PORT', '5432')),
            database=os.getenv('BFSI_DB_NAME', 'bfsi_security'),
            username=os.getenv('BFSI_DB_USER', 'bfsi_user'),
            password=os.getenv('BFSI_DB_PASSWORD', ''),
            max_connections=int(os.getenv('BFSI_DB_MAX_CONNECTIONS', '10')),
            min_connections=int(os.getenv('BFSI_DB_MIN_CONNECTIONS', '2')),
            connection_timeout=int(os.getenv('BFSI_DB_TIMEOUT', '30')),
            ssl_mode=os.getenv('BFSI_DB_SSL_MODE', 'prefer'),
            encryption_enabled=os.getenv('BFSI_DB_ENCRYPTION_ENABLED', 'true').lower() == 'true',
            audit_enabled=os.getenv('BFSI_DB_AUDIT_ENABLED', 'true').lower() == 'true'
        )

class ConnectionPool:
    """Thread-safe PostgreSQL database connection pool"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.pool = Queue(maxsize=config.max_connections)
        self.active_connections = 0
        self.lock = threading.Lock()
        
        # Initialize pool with connections
        for _ in range(config.min_connections):
            conn = self._create_connection()
            if conn:
                self.pool.put(conn)
    
    def _create_connection(self) -> Optional[psycopg2.extensions.connection]:
        """Create a new PostgreSQL database connection"""
        try:
            # Build connection parameters
            conn_params = {
                'host': self.config.host,
                'port': self.config.port,
                'database': self.config.database,
                'user': self.config.username,
                'password': self.config.password,
                'connect_timeout': self.config.connection_timeout,
                'sslmode': self.config.ssl_mode,
                'application_name': 'bfsi_security_service'
            }
            
            # Remove empty password if not set
            if not conn_params['password']:
                conn_params.pop('password')
            
            conn = psycopg2.connect(**conn_params)
            
            # Configure connection for optimal performance
            with conn.cursor() as cursor:
                # Set connection-level settings for BFSI compliance
                cursor.execute("SET statement_timeout = 30000")  # 30 seconds
                cursor.execute("SET idle_in_transaction_session_timeout = 60000")  # 60 seconds
                cursor.execute("SET lock_timeout = 10000")  # 10 seconds
                
                # Enable row-level security if available
                try:
                    cursor.execute("SET row_security = on")
                except psycopg2.Error:
                    pass  # RLS not available in older PostgreSQL versions
                
                # Set timezone for consistent timestamps
                cursor.execute("SET timezone = 'UTC'")
            
            return conn
            
        except Exception as e:
            logger.error(f"Failed to create PostgreSQL database connection: {e}")
            return None
    
    @contextmanager
    def get_connection(self):
        """Get a PostgreSQL connection from the pool with proper error handling"""
        conn = None
        try:
            # Try to get connection from pool
            try:
                conn = self.pool.get(timeout=self.config.connection_timeout)
                # Check if connection is still alive
                if conn.closed:
                    conn = None
                    raise Empty("Connection is closed")
            except Empty:
                # Create new connection if pool is empty
                with self.lock:
                    if self.active_connections < self.config.max_connections:
                        conn = self._create_connection()
                        if conn:
                            self.active_connections += 1
            
            if not conn:
                raise Exception("Unable to get PostgreSQL database connection")
            
            # Ensure connection is in autocommit mode for better performance
            if not conn.autocommit:
                conn.autocommit = True
            
            yield conn
            
        except psycopg2.OperationalError as e:
            logger.error(f"PostgreSQL operational error: {e}")
            if conn and not conn.closed:
                conn.close()
            raise Exception(f"Database connection error: {e}")
        except psycopg2.Error as e:
            logger.error(f"PostgreSQL error: {e}")
            if conn and not conn.closed:
                conn.close()
            raise Exception(f"Database error: {e}")
        finally:
            if conn and not conn.closed:
                try:
                    # Return connection to pool if it's still healthy
                    self.pool.put(conn)
                except:
                    # If pool is full or connection is bad, close it
                    try:
                        conn.close()
                    except:
                        pass
                    with self.lock:
                        self.active_connections -= 1
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        while not self.pool.empty():
            try:
                conn = self.pool.get_nowait()
                if conn and not conn.closed:
                    conn.close()
            except Empty:
                break
        
        with self.lock:
            self.active_connections = 0
    
    def test_connection(self) -> bool:
        """Test PostgreSQL connection"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return result[0] == 1
        except Exception as e:
            logger.error(f"PostgreSQL connection test failed: {e}")
            return False

class SecureDataRepository:
    """Secure data access repository with encryption and audit logging"""
    
    def __init__(self, db_config: DatabaseConfig):
        self.config = db_config
        self.pool = ConnectionPool(db_config)
        self.audit_logger = logging.getLogger("data_audit")
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        self._setup_audit_logging()
    
    def _setup_audit_logging(self):
        """Setup audit logging for data access with log rotation"""
        if not self.config.audit_enabled:
            return
        
        # Check if a RotatingFileHandler already exists to prevent duplicates
        for existing_handler in self.audit_logger.handlers:
            if isinstance(existing_handler, RotatingFileHandler):
                return  # Handler already exists, don't add another
        
        # Create rotating file handler with size and backup limits
        handler = RotatingFileHandler(
            "data_audit.log",
            maxBytes=10*1024*1024,  # 10MB max file size
            backupCount=5  # Keep 5 backup files
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.audit_logger.addHandler(handler)
        self.audit_logger.setLevel(logging.INFO)
        self._create_audit_table()
    
    def _create_audit_table(self):
        """Create audit_logs table if it doesn't exist"""
        try:
            with self.pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS audit_logs (
                            id SERIAL PRIMARY KEY,
                            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            operation VARCHAR(50) NOT NULL,
                            table_name VARCHAR(100) NOT NULL,
                            user_id VARCHAR(100),
                            data_id VARCHAR(100),
                            ip_address VARCHAR(45),
                            details JSONB,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to create audit_logs table: {e}")
    
    def _log_data_access(self, operation: str, table: str, user_id: str = None, 
                        data_id: str = None, details: Dict[str, Any] = None):
        """Log data access for audit purposes"""
        if not self.config.audit_enabled:
            return
        
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "table": table,
            "user_id": user_id,
            "data_id": data_id,
            "details": details or {},
            "ip_address": "system"  # Would be passed from request context
        }
        
        # Log to file
        self.audit_logger.info(json.dumps(audit_entry))
        
        # Store in database
        try:
            with self.pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO audit_logs 
                        (timestamp, operation, table_name, user_id, data_id, ip_address, details)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        audit_entry["timestamp"],
                        audit_entry["operation"],
                        audit_entry["table"],
                        audit_entry["user_id"],
                        audit_entry["data_id"],
                        audit_entry["ip_address"],
                        json.dumps(audit_entry["details"])
                    ))
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to store audit entry in database: {e}")
    
    def _retry_on_connection_error(self, func, *args, **kwargs):
        """Retry function on PostgreSQL connection errors"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Max retries exceeded for database operation: {e}")
                    raise
                
                logger.warning(f"Database connection error (attempt {attempt + 1}/{self.max_retries}): {e}")
                time.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                
                # Recreate connection pool if needed
                if "connection" in str(e).lower():
                    logger.info("Recreating connection pool due to connection error")
                    self.pool = ConnectionPool(self.config)
    
    def _encrypt_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive fields in data"""
        if not self.config.encryption_enabled:
            return data
        
        encrypted_data = data.copy()
        sensitive_fields = [
            "customer_id", "account_number", "card_number", "ssn", 
            "email", "phone", "address", "transaction_id"
        ]
        
        for field in sensitive_fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[field] = encryption_manager.encrypt(str(encrypted_data[field]))
        
        return encrypted_data
    
    def _decrypt_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt sensitive fields in data"""
        if not self.config.encryption_enabled:
            return data
        
        decrypted_data = data.copy()
        sensitive_fields = [
            "customer_id", "account_number", "card_number", "ssn",
            "email", "phone", "address", "transaction_id"
        ]
        
        for field in sensitive_fields:
            if field in decrypted_data and decrypted_data[field]:
                try:
                    decrypted_data[field] = encryption_manager.decrypt(str(decrypted_data[field]))
                except:
                    # If decryption fails, return original value
                    pass
        
        return decrypted_data
    
    def _hash_sensitive_data(self, data: str) -> str:
        """Create irreversible hash for sensitive data"""
        return encryption_manager.hash_sensitive_data(data)
    
    # Transaction operations
    def get_transactions(self, limit: int = 50, offset: int = 0, 
                        user_id: str = None, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get transactions with security controls"""
        def _execute_query():
            with self.pool.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build query with security filters
                query = """
                    SELECT id, transaction_id, amount, customer_id, transaction_type,
                           location, timestamp, risk_score, processed
                    FROM transactions
                    WHERE 1=1
                """
                params = []
                
                if filters:
                    if "start_date" in filters:
                        query += " AND timestamp >= %s"
                        params.append(filters["start_date"])
                    if "end_date" in filters:
                        query += " AND timestamp <= %s"
                        params.append(filters["end_date"])
                    if "risk_threshold" in filters:
                        query += " AND risk_score >= %s"
                        params.append(filters["risk_threshold"])
                
                query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Process results
                transactions = []
                for row in rows:
                    transaction = {
                        "id": row[0],
                        "transaction_id": row[1],
                        "amount": row[2],
                        "customer_id": row[3],
                        "transaction_type": row[4],
                        "location": row[5],
                        "timestamp": row[6],
                        "risk_score": row[7],
                        "processed": bool(row[8])
                    }
                    
                    # Decrypt sensitive data
                    transaction = self._decrypt_sensitive_data(transaction)
                    transactions.append(transaction)
                
                return transactions
        
        # Execute with retry logic
        transactions = self._retry_on_connection_error(_execute_query)
        
        # Log data access
        self._log_data_access(
            "SELECT", "transactions", user_id,
            details={"limit": limit, "offset": offset, "filters": filters}
        )
        
        return transactions
    
    def test_database_connection(self) -> bool:
        """Test the database connection"""
        return self.pool.test_connection()
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database connection information"""
        try:
            with self.pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Get PostgreSQL version
                    cursor.execute("SELECT version()")
                    version = cursor.fetchone()[0]
                    
                    # Get current database name
                    cursor.execute("SELECT current_database()")
                    db_name = cursor.fetchone()[0]
                    
                    # Get connection count
                    cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE datname = %s", (db_name,))
                    connection_count = cursor.fetchone()[0]
                    
                    return {
                        "version": version,
                        "database": db_name,
                        "active_connections": connection_count,
                        "pool_size": self.pool.active_connections,
                        "ssl_mode": self.config.ssl_mode
                    }
        except Exception as e:
            logger.error(f"Failed to get database info: {e}")
            return {"error": str(e)}
    
    def close(self):
        """Close all database connections and cleanup resources"""
        try:
            self.pool.close_all_connections()
            logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        self.close()
    
    def get_transaction_by_id(self, transaction_id: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """Get specific transaction by ID"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, transaction_id, amount, customer_id, transaction_type,
                       location, timestamp, risk_score, processed
                FROM transactions
                WHERE transaction_id = %s
            """, (transaction_id,))
            
            row = cursor.fetchone()
            
            # Log data access
            self._log_data_access(
                "SELECT", "transactions", user_id, transaction_id
            )
            
            if row:
                transaction = {
                    "id": row[0],
                    "transaction_id": row[1],
                    "amount": row[2],
                    "customer_id": row[3],
                    "transaction_type": row[4],
                    "location": row[5],
                    "timestamp": row[6],
                    "risk_score": row[7],
                    "processed": bool(row[8])
                }
                
                # Decrypt sensitive data
                return self._decrypt_sensitive_data(transaction)
            
            return None
    
    def create_transaction(self, transaction_data: Dict[str, Any], user_id: str = None) -> str:
        """Create new transaction with security controls"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Encrypt sensitive data
            encrypted_data = self._encrypt_sensitive_data(transaction_data)
            
            # Generate transaction ID if not provided
            if "transaction_id" not in encrypted_data:
                encrypted_data["transaction_id"] = f"TXN_{uuid.uuid4()}"
            
            # Insert transaction
            cursor.execute("""
                INSERT INTO transactions 
                (transaction_id, amount, customer_id, transaction_type, location, 
                 timestamp, risk_score, processed)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                encrypted_data["transaction_id"],
                encrypted_data["amount"],
                encrypted_data["customer_id"],
                encrypted_data["transaction_type"],
                encrypted_data["location"],
                encrypted_data.get("timestamp", datetime.utcnow().isoformat()),
                encrypted_data.get("risk_score", 0.0),
                encrypted_data.get("processed", False)
            ))
            
            conn.commit()
            
            # Log data access
            self._log_data_access(
                "INSERT", "transactions", user_id, encrypted_data["transaction_id"],
                details={"amount": encrypted_data["amount"], "type": encrypted_data["transaction_type"]}
            )
            
            return encrypted_data["transaction_id"]
    
    def update_transaction(self, transaction_id: str, update_data: Dict[str, Any], 
                          user_id: str = None) -> bool:
        """Update transaction with audit logging"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Encrypt sensitive data
            encrypted_data = self._encrypt_sensitive_data(update_data)
            
            # Build update query
            set_clauses = []
            params = []
            
            for field, value in encrypted_data.items():
                if field != "transaction_id":  # Don't update ID
                    set_clauses.append(f"{field} = %s")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            params.append(transaction_id)
            
            query = f"UPDATE transactions SET {', '.join(set_clauses)} WHERE transaction_id = %s"
            cursor.execute(query, params)
            
            conn.commit()
            
            # Log data access
            self._log_data_access(
                "UPDATE", "transactions", user_id, transaction_id,
                details={"updated_fields": list(encrypted_data.keys())}
            )
            
            return cursor.rowcount > 0
    
    def delete_transaction(self, transaction_id: str, user_id: str = None) -> bool:
        """Soft delete transaction (mark as deleted)"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Instead of hard delete, mark as deleted
            cursor.execute("""
                UPDATE transactions 
                SET processed = false, deleted_at = %s
                WHERE transaction_id = %s
            """, (datetime.utcnow().isoformat(), transaction_id))
            
            conn.commit()
            
            # Log data access
            self._log_data_access(
                "DELETE", "transactions", user_id, transaction_id
            )
            
            return cursor.rowcount > 0
    
    # Compliance operations
    def get_compliance_checks(self, limit: int = 50, offset: int = 0,
                             user_id: str = None) -> List[Dict[str, Any]]:
        """Get compliance checks with security controls"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, regulation, process, controls, documents, 
                       timestamp, compliance_score, processed
                FROM compliance_checks
                ORDER BY timestamp DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            
            rows = cursor.fetchall()
            
            # Log data access
            self._log_data_access(
                "SELECT", "compliance_checks", user_id,
                details={"limit": limit, "offset": offset}
            )
            
            compliance_checks = []
            for row in rows:
                # Safely parse JSON fields with error handling
                try:
                    controls = json.loads(row[3]) if row[3] else []
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Failed to parse controls JSON for compliance check {row[0]}: {e}")
                    controls = []
                
                try:
                    documents = json.loads(row[4]) if row[4] else []
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Failed to parse documents JSON for compliance check {row[0]}: {e}")
                    documents = []
                
                compliance_check = {
                    "id": row[0],
                    "regulation": row[1],
                    "process": row[2],
                    "controls": controls,
                    "documents": documents,
                    "timestamp": row[5],
                    "compliance_score": row[6],
                    "processed": bool(row[7])
                }
                compliance_checks.append(compliance_check)
            
            return compliance_checks
    
    # Risk assessment operations
    def get_risk_assessments(self, limit: int = 50, offset: int = 0,
                            user_id: str = None) -> List[Dict[str, Any]]:
        """Get risk assessments with security controls"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, risk_type, portfolio, exposure, probability, 
                       impact, timestamp, risk_score, processed
                FROM risk_assessments
                ORDER BY timestamp DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            
            rows = cursor.fetchall()
            
            # Log data access
            self._log_data_access(
                "SELECT", "risk_assessments", user_id,
                details={"limit": limit, "offset": offset}
            )
            
            risk_assessments = []
            for row in rows:
                risk_assessment = {
                    "id": row[0],
                    "risk_type": row[1],
                    "portfolio": row[2],
                    "exposure": row[3],
                    "probability": row[4],
                    "impact": row[5],
                    "timestamp": row[6],
                    "risk_score": row[7],
                    "processed": bool(row[8])
                }
                risk_assessments.append(risk_assessment)
            
            return risk_assessments
    
    # Document operations
    def get_documents(self, limit: int = 50, offset: int = 0,
                      user_id: str = None) -> List[Dict[str, Any]]:
        """Get documents with security controls"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, document_type, classification, compliance_framework,
                       timestamp, processed
                FROM documents
                ORDER BY timestamp DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            
            rows = cursor.fetchall()
            
            # Log data access
            self._log_data_access(
                "SELECT", "documents", user_id,
                details={"limit": limit, "offset": offset}
            )
            
            documents = []
            for row in rows:
                document = {
                    "id": row[0],
                    "document_type": row[1],
                    "classification": row[2],
                    "compliance_framework": row[3],
                    "timestamp": row[4],
                    "processed": bool(row[5])
                }
                documents.append(document)
            
            return documents
    
    def get_audit_logs(self, start_date: str = None, end_date: str = None,
                      user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit logs for compliance"""
        try:
            with self.pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Build the base query
                    query = """
                        SELECT timestamp, operation, table_name, user_id, 
                               ip_address, details, created_at
                        FROM audit_logs
                        WHERE 1=1
                    """
                    params = []
                    
                    # Add date filters
                    if start_date:
                        query += " AND timestamp >= %s"
                        params.append(start_date)
                    
                    if end_date:
                        query += " AND timestamp <= %s"
                        params.append(end_date)
                    
                    # Add user filter
                    if user_id:
                        query += " AND user_id = %s"
                        params.append(user_id)
                    
                    # Add ordering and limit
                    query += " ORDER BY timestamp DESC LIMIT %s"
                    params.append(limit)
                    
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    
                    # Convert to list of dictionaries
                    audit_logs = []
                    for row in results:
                        audit_log = {
                            "timestamp": row[0].isoformat() if row[0] else None,
                            "operation": row[1],
                            "table": row[2],
                            "user_id": row[3],
                            "ip_address": row[4],
                            "details": row[5] if row[5] else {},
                            "created_at": row[6].isoformat() if row[6] else None
                        }
                        audit_logs.append(audit_log)
                    
                    return audit_logs
                    
        except Exception as e:
            logger.error(f"Failed to retrieve audit logs: {e}")
            return []
