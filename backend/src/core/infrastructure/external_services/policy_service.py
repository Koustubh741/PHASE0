"""
Policy Management Service
FastAPI microservice for GRC Policy Management
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, ForeignKey, select, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, relationship, Mapped, mapped_column
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import uuid
import logging
from enum import Enum

# JWT Authentication imports
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
import os
import time
import hashlib
from typing import Set
from collections import defaultdict
from datetime import datetime, timezone

# JWT Configuration - Production Ready
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

# Security Configuration
RATE_LIMIT_REQUESTS_PER_MINUTE = int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "60"))
AUDIT_LOG_ENABLED = os.getenv("AUDIT_LOG_ENABLED", "true").lower() == "true"
DATA_ENCRYPTION_ENABLED = os.getenv("DATA_ENCRYPTION_ENABLED", "true").lower() == "true"

# Validate required environment variables
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is required for production deployment")

# Security headers and validation
ALLOWED_ISSUERS = ["bfsi-grc-platform", "bfsi-auth-service"]
ALLOWED_AUDIENCES = ["bfsi-api", "bfsi-policy-service"]
REQUIRED_SCOPES = ["policy:read", "policy:write"]

# Production Security Components
class SecurityManager:
    """Production-ready security manager for JWT validation and monitoring"""
    
    def __init__(self):
        self.blacklisted_tokens: Set[str] = set()
        self.rate_limit_tracker = defaultdict(list)
        self.failed_attempts = defaultdict(int)
        self.security_events = []
        
    def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return token_hash in self.blacklisted_tokens
    
    def blacklist_token(self, token: str):
        """Blacklist a token (for logout, security incidents)"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self.blacklisted_tokens.add(token_hash)
        
    def check_rate_limit(self, client_ip: str, user_id: str = None) -> bool:
        """Check if request is within rate limits"""
        current_time = time.time()
        identifier = user_id or client_ip
        
        # Clean old entries (older than 1 minute)
        self.rate_limit_tracker[identifier] = [
            timestamp for timestamp in self.rate_limit_tracker[identifier]
            if current_time - timestamp < 60
        ]
        
        # Check if under limit
        if len(self.rate_limit_tracker[identifier]) >= RATE_LIMIT_REQUESTS_PER_MINUTE:
            return False
            
        # Add current request
        self.rate_limit_tracker[identifier].append(current_time)
        return True
    
    def log_security_event(self, event_type: str, user_id: str = None, 
                          client_ip: str = None, details: str = None):
        """Log security events for monitoring and auditing"""
        if not AUDIT_LOG_ENABLED:
            return
            
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "client_ip": client_ip,
            "details": details,
            "service": "policy-service"
        }
        
        self.security_events.append(event)
        logging.warning(f"Security Event: {event_type} - {details}", extra=event)
        
        # Keep only last 1000 events in memory
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]

# Global security manager instance
security_manager = SecurityManager()

# Import shared utilities
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared', 'utils'))
from vector_store import SimpleVectorStore

# Mock vector service for compatibility
class MockVectorService:
    def __init__(self):
        self.vector_store = SimpleVectorStore()
    
    async def add_documents(self, documents, metadatas=None):
        return self.vector_store.add_documents(documents, metadatas)
    
    async def search(self, query, n_results=5):
        return self.vector_store.search(query, n_results)
    
    async def add_policy_document(self, content, title, policy_id, organization_id, category, metadata=None):
        """Add a policy document to the vector store"""
        document = {
            "content": content,
            "title": title,
            "policy_id": policy_id,
            "organization_id": organization_id,
            "category": category
        }
        if metadata:
            document.update(metadata)
        return await self.add_documents([document], [{"policy_id": policy_id, "title": title}])
    
    async def update_document(self, doc_id, content, metadata=None):
        """Update a document in the vector store"""
        # For mock implementation, we'll just add the updated document
        document = {"content": content, "doc_id": doc_id}
        if metadata:
            document.update(metadata)
        return await self.add_documents([document], [{"doc_id": doc_id}])
    
    async def delete_document(self, doc_id, collection_type=None):
        """Delete a document from the vector store"""
        # Mock implementation - in a real vector store, this would remove the document
        logger.info(f"Mock: Deleting document {doc_id} from collection {collection_type}")
        return {"status": "deleted", "doc_id": doc_id}
    
    async def search_similar_documents(self, query, n_results=5, filters=None):
        """Search for similar documents"""
        return await self.search(query, n_results)
    
    async def get_collection_stats(self, collection_name):
        """Get statistics for a collection"""
        # Mock implementation - return some basic stats
        return {
            "collection_name": collection_name,
            "total_documents": 0,
            "indexed_documents": 0,
            "last_updated": "2024-01-01T00:00:00Z"
        }

vector_service = MockVectorService()

logger = logging.getLogger(__name__)

# Database setup
def get_database_url():
    """Build database URL from environment variables with fallback to individual components"""
    # First try to get the complete DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        logger.info("Using DATABASE_URL from environment variables")
        return database_url
    
    # If not available, build from individual components
    db_user = os.getenv("DB_USER", "grc_user")
    db_password = os.getenv("DB_PASSWORD", "grc_password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "grc_platform")
    
    # Log that we're using individual components (without exposing credentials)
    logger.info(f"Building database URL from individual components: {db_user}@{db_host}:{db_port}/{db_name}")
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    DATABASE_URL = get_database_url()
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database connection configured successfully")
except Exception as e:
    logger.error(f"Failed to configure database connection: {e}")
    raise

class Base(DeclarativeBase):
    pass

# Security
security = HTTPBearer()

def verify_jwt_token(token: str, client_ip: str = None) -> Dict[str, Any]:
    """
    Production-ready JWT token verification with comprehensive security checks
    
    Args:
        token: JWT token string
        client_ip: Client IP address for rate limiting and logging
        
    Returns:
        Dict containing user claims (id, organization_id, role, etc.)
        
    Raises:
        HTTPException: If token is invalid, expired, blacklisted, or security check fails
    """
    # Security checks before token validation
    if security_manager.is_token_blacklisted(token):
        security_manager.log_security_event(
            "BLACKLISTED_TOKEN_ACCESS", 
            client_ip=client_ip, 
            details="Attempted access with blacklisted token"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Decode and verify the JWT token with comprehensive validation
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={
                "verify_exp": True,
                "verify_signature": True,
                "verify_aud": True,
                "verify_iss": True
            },
            audience=ALLOWED_AUDIENCES,
            issuer=ALLOWED_ISSUERS
        )
        
        # Extract and validate user information
        user_id = payload.get("sub") or payload.get("user_id")
        organization_id = payload.get("organization_id") or payload.get("org_id")
        role = payload.get("role") or payload.get("user_role")
        scopes = payload.get("scope", "").split() if payload.get("scope") else []
        
        # Comprehensive claim validation
        validation_errors = []
        
        if not user_id:
            validation_errors.append("missing user identifier")
        
        if not organization_id:
            validation_errors.append("missing organization identifier")
        
        # Validate required scopes for policy service
        if not any(scope in scopes for scope in REQUIRED_SCOPES):
            validation_errors.append(f"insufficient permissions - required: {REQUIRED_SCOPES}")
        
        # Validate token not before time (nbf claim)
        if payload.get("nbf") and payload.get("nbf") > time.time():
            validation_errors.append("token not yet valid")
        
        if validation_errors:
            security_manager.log_security_event(
                "INVALID_TOKEN_CLAIMS",
                user_id=user_id,
                client_ip=client_ip,
                details=f"Token validation failed: {', '.join(validation_errors)}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {', '.join(validation_errors)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check for suspicious activity patterns
        if security_manager.failed_attempts.get(client_ip, 0) > 5:
            security_manager.log_security_event(
                "SUSPICIOUS_ACTIVITY",
                user_id=user_id,
                client_ip=client_ip,
                details="Multiple failed authentication attempts from IP"
            )
            # Don't block immediately but log for monitoring
        
        # Reset failed attempts on successful authentication
        if client_ip in security_manager.failed_attempts:
            del security_manager.failed_attempts[client_ip]
        
        # Log successful authentication
        security_manager.log_security_event(
            "SUCCESSFUL_AUTHENTICATION",
            user_id=user_id,
            client_ip=client_ip,
            details="JWT token validation successful"
        )
        
        return {
            "id": user_id,
            "organization_id": organization_id,
            "role": role or "USER",
            "email": payload.get("email"),
            "username": payload.get("username") or payload.get("preferred_username"),
            "scopes": scopes,
            "exp": payload.get("exp"),
            "iat": payload.get("iat"),
            "jti": payload.get("jti"),  # JWT ID for token tracking
            "session_id": payload.get("session_id")
        }
        
    except ExpiredSignatureError:
        security_manager.log_security_event(
            "EXPIRED_TOKEN_ACCESS",
            client_ip=client_ip,
            details="Attempted access with expired token"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTClaimsError as e:
        security_manager.failed_attempts[client_ip] = security_manager.failed_attempts.get(client_ip, 0) + 1
        security_manager.log_security_event(
            "INVALID_TOKEN_CLAIMS",
            client_ip=client_ip,
            details=f"JWT claims error: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token claims: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        security_manager.failed_attempts[client_ip] = security_manager.failed_attempts.get(client_ip, 0) + 1
        security_manager.log_security_event(
            "INVALID_TOKEN",
            client_ip=client_ip,
            details=f"JWT validation error: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format or signature",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        security_manager.log_security_event(
            "AUTHENTICATION_ERROR",
            client_ip=client_ip,
            details=f"Unexpected error during token verification: {str(e)}"
        )
        logging.error(f"Unexpected error during token verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication",
        )

# Enums
class PolicyStatus(str, Enum):
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class PolicyCategoryEnum(str, Enum):
    INFORMATION_SECURITY = "INFORMATION_SECURITY"
    HUMAN_RESOURCES = "HUMAN_RESOURCES"
    FINANCIAL = "FINANCIAL"
    OPERATIONAL = "OPERATIONAL"
    COMPLIANCE = "COMPLIANCE"

# Database Models
class Organization(Base):
    __tablename__ = "organizations"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String(100))
    size: Mapped[Optional[str]] = mapped_column(String(50))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    users: Mapped[List["User"]] = relationship("User", back_populates="organization")
    policies: Mapped[List["Policy"]] = relationship("Policy", back_populates="organization")
    policy_categories: Mapped[List["PolicyCategory"]] = relationship("PolicyCategory", back_populates="organization")

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="USER")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="users")
    created_policies: Mapped[List["Policy"]] = relationship("Policy", foreign_keys="Policy.created_by", back_populates="creator")
    approved_policies: Mapped[List["Policy"]] = relationship("Policy", foreign_keys="Policy.approved_by", back_populates="approver")

class PolicyCategory(Base):
    __tablename__ = "policy_categories"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="policy_categories")
    policies: Mapped[List["Policy"]] = relationship("Policy", back_populates="category")

class Policy(Base):
    __tablename__ = "policies"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default=PolicyStatus.DRAFT)
    category_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("policy_categories.id"))
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    created_by: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    approved_by: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    effective_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    review_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category: Mapped[Optional["PolicyCategory"]] = relationship("PolicyCategory", back_populates="policies")
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="policies")
    creator: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by], back_populates="created_policies")
    approver: Mapped[Optional["User"]] = relationship("User", foreign_keys=[approved_by], back_populates="approved_policies")

# Pydantic Models
class PolicyCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = None
    category_id: Optional[str] = None
    effective_date: Optional[datetime] = None
    review_date: Optional[datetime] = None

class PolicyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None
    status: Optional[PolicyStatus] = None
    category_id: Optional[str] = None
    effective_date: Optional[datetime] = None
    review_date: Optional[datetime] = None

class PolicyResponse(BaseModel):
    id: str
    title: str
    content: str
    summary: Optional[str]
    version: str
    status: PolicyStatus
    category_id: Optional[str]
    organization_id: str
    created_by: str
    approved_by: Optional[str]
    effective_date: Optional[datetime]
    review_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PolicySearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    organization_id: Optional[str] = None
    category: Optional[str] = None
    status: Optional[PolicyStatus] = None
    limit: int = Field(10, ge=1, le=100)

class PolicySearchResponse(BaseModel):
    policies: List[Dict[str, Any]]
    total_results: int
    query: str

# FastAPI App
app = FastAPI(
    title="GRC Policy Management Service",
    description="Microservice for managing GRC policies with AI-powered search",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    request: Request = None
):
    """
    Production-ready user authentication with comprehensive security checks
    
    Args:
        credentials: HTTP Bearer token credentials
        request: FastAPI request object for IP extraction and rate limiting
        
    Returns:
        Dict containing authenticated user information
        
    Raises:
        HTTPException: If authentication fails or security checks fail
    """
    # Extract client IP for security monitoring
    client_ip = "unknown"
    if request:
        # Get real IP from headers (handles proxies, load balancers)
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
            request.headers.get("X-Real-IP") or
            request.client.host if request.client else "unknown"
        )
    
    # Rate limiting check
    if not security_manager.check_rate_limit(client_ip):
        security_manager.log_security_event(
            "RATE_LIMIT_EXCEEDED",
            client_ip=client_ip,
            details=f"Rate limit exceeded: {RATE_LIMIT_REQUESTS_PER_MINUTE} requests/minute"
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
            headers={"Retry-After": "60"}
        )
    
    # Validate credentials
    if not credentials or not credentials.credentials:
        security_manager.log_security_event(
            "MISSING_CREDENTIALS",
            client_ip=client_ip,
            details="Authentication credentials not provided"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify the JWT token with comprehensive security checks
    try:
        user_claims = verify_jwt_token(credentials.credentials, client_ip)
        
        # Additional security validations
        if not user_claims.get("organization_id"):
            security_manager.log_security_event(
                "INVALID_USER_ORGANIZATION",
                user_id=user_claims.get("id"),
                client_ip=client_ip,
                details="User missing organization context"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Invalid user organization",
            )
        
        # Check for required permissions
        if not any(scope in user_claims.get("scopes", []) for scope in REQUIRED_SCOPES):
            security_manager.log_security_event(
                "INSUFFICIENT_PERMISSIONS",
                user_id=user_claims.get("id"),
                client_ip=client_ip,
                details=f"User lacks required scopes: {REQUIRED_SCOPES}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Insufficient permissions",
            )
        
        return user_claims
        
    except HTTPException:
        # Re-raise HTTP exceptions (already handled by verify_jwt_token)
        raise
    except Exception as e:
        security_manager.log_security_event(
            "AUTHENTICATION_FAILURE",
            client_ip=client_ip,
            details=f"Unexpected authentication error: {str(e)}"
        )
        logging.error(f"Unexpected error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication",
        )

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "policy-service"}

@app.post("/security/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    request: Request = None
):
    """
    Logout endpoint - blacklist the current token
    """
    client_ip = "unknown"
    if request:
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
            request.headers.get("X-Real-IP") or
            request.client.host if request.client else "unknown"
        )
    
    if credentials and credentials.credentials:
        security_manager.blacklist_token(credentials.credentials)
        security_manager.log_security_event(
            "USER_LOGOUT",
            client_ip=client_ip,
            details="User successfully logged out"
        )
        return {"message": "Successfully logged out"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No valid token provided for logout"
    )

@app.get("/security/events")
async def get_security_events(
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get security events (admin only)
    """
    if current_user.get("role") != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin role required"
        )
    
    events = security_manager.security_events[-limit:] if limit > 0 else security_manager.security_events
    return {"events": events, "total": len(security_manager.security_events)}

@app.get("/security/status")
async def get_security_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get current security status and metrics
    """
    if current_user.get("role") not in ["ADMIN", "SECURITY_OFFICER"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin or Security Officer role required"
        )
    
    return {
        "blacklisted_tokens_count": len(security_manager.blacklisted_tokens),
        "failed_attempts_count": len(security_manager.failed_attempts),
        "active_rate_limits": len(security_manager.rate_limit_tracker),
        "security_events_count": len(security_manager.security_events),
        "rate_limit_threshold": RATE_LIMIT_REQUESTS_PER_MINUTE,
        "audit_logging_enabled": AUDIT_LOG_ENABLED
    }

@app.post("/policies", response_model=PolicyResponse)
async def create_policy(
    policy_data: PolicyCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new policy"""
    try:
        # Create policy in database
        db_policy = Policy(
            title=policy_data.title,
            content=policy_data.content,
            summary=policy_data.summary,
            category_id=policy_data.category_id,
            organization_id=current_user["organization_id"],
            created_by=current_user["id"],
            effective_date=policy_data.effective_date,
            review_date=policy_data.review_date
        )
        
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        
        # Add to vector database for AI search
        try:
            vector_service.add_policy_document(
                content=policy_data.content,
                title=policy_data.title,
                policy_id=db_policy.id,
                organization_id=current_user["organization_id"],
                category=policy_data.category_id,
                metadata={
                    "status": db_policy.status,
                    "version": db_policy.version,
                    "created_by": current_user["id"]
                }
            )
        except Exception as e:
            logger.warning(f"Failed to add policy to vector database: {e}")
        
        logger.info(f"Policy created: {db_policy.id}")
        return db_policy
        
    except Exception as e:
        logger.error(f"Error creating policy: {e}")
        raise HTTPException(status_code=500, detail="Failed to create policy")

@app.get("/policies", response_model=List[PolicyResponse])
async def get_policies(
    organization_id: Optional[str] = None,
    status: Optional[PolicyStatus] = None,
    category_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get policies with filtering"""
    try:
        stmt = select(Policy)
        
        # Filter by organization
        if organization_id:
            stmt = stmt.where(Policy.organization_id == organization_id)
        else:
            stmt = stmt.where(Policy.organization_id == current_user["organization_id"])
        
        # Filter by status
        if status:
            stmt = stmt.where(Policy.status == status)
        
        # Filter by category
        if category_id:
            stmt = stmt.where(Policy.category_id == category_id)
        
        # Apply pagination
        policies = db.scalars(stmt.offset(offset).limit(limit)).all()
        
        return policies
        
    except Exception as e:
        logger.error(f"Error getting policies: {e}")
        raise HTTPException(status_code=500, detail="Failed to get policies")

@app.get("/policies/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific policy by ID"""
    try:
        policy_stmt = select(Policy).where(
            Policy.id == policy_id,
            Policy.organization_id == current_user["organization_id"]
        )
        policy = db.scalar(policy_stmt)
        
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        return policy
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting policy: {e}")
        raise HTTPException(status_code=500, detail="Failed to get policy")

@app.put("/policies/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: str,
    policy_data: PolicyUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a policy"""
    try:
        policy_stmt = select(Policy).where(
            Policy.id == policy_id,
            Policy.organization_id == current_user["organization_id"]
        )
        policy = db.scalar(policy_stmt)
        
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        # Update fields
        update_data = policy_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(policy, field, value)
        
        policy.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(policy)
        
        # Update in vector database
        try:
            vector_service.update_document(
                doc_id=policy_id,
                content=policy.content,
                metadata={
                    "title": policy.title,
                    "status": policy.status,
                    "version": policy.version,
                    "updated_at": policy.updated_at.isoformat()
                },
                collection_type="policies"
            )
        except Exception as e:
            logger.warning(f"Failed to update policy in vector database: {e}")
        
        logger.info(f"Policy updated: {policy_id}")
        return policy
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating policy: {e}")
        raise HTTPException(status_code=500, detail="Failed to update policy")

@app.delete("/policies/{policy_id}")
async def delete_policy(
    policy_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a policy"""
    try:
        policy_stmt = select(Policy).where(
            Policy.id == policy_id,
            Policy.organization_id == current_user["organization_id"]
        )
        policy = db.scalar(policy_stmt)
        
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        # Delete from database
        db.delete(policy)
        db.commit()
        
        # Delete from vector database
        try:
            vector_service.delete_document(policy_id, collection_type="policies")
        except Exception as e:
            logger.warning(f"Failed to delete policy from vector database: {e}")
        
        logger.info(f"Policy deleted: {policy_id}")
        return {"message": "Policy deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting policy: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete policy")

@app.post("/policies/search", response_model=PolicySearchResponse)
async def search_policies(
    search_request: PolicySearchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search policies using AI-powered vector search"""
    try:
        # Use vector database for semantic search
        search_results = vector_service.search(
            query=search_request.query,
            n_results=search_request.limit
        )
        
        # Apply filtering logic outside of vector service
        filtered_results = []
        for result in search_results:
            # Check organization_id filter
            if result.get("metadata", {}).get("organization_id") != current_user["organization_id"]:
                continue
                
            # Apply category filter if specified
            if search_request.category and result.get("metadata", {}).get("category") != search_request.category:
                continue
                
            # Apply status filter if specified
            if search_request.status and result.get("metadata", {}).get("status") != search_request.status:
                continue
                
            filtered_results.append(result)
        
        # Format results
        policies = []
        for result in filtered_results:
            policies.append({
                "id": result.get("metadata", {}).get("policy_id"),
                "title": result.get("metadata", {}).get("title"),
                "content": result.get("document", "")[:500] + "..." if len(result.get("document", "")) > 500 else result.get("document", ""),
                "metadata": result.get("metadata", {}),
                "similarity_score": 1 - result.get("distance", 0) if result.get("distance") else 0
            })
        
        return PolicySearchResponse(
            policies=policies,
            total_results=len(policies),
            query=search_request.query
        )
        
    except Exception as e:
        logger.error(f"Error searching policies: {e}")
        raise HTTPException(status_code=500, detail="Failed to search policies")

@app.get("/policies/categories")
async def get_policy_categories(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get policy categories"""
    try:
        categories_stmt = select(PolicyCategory).where(
            PolicyCategory.organization_id == current_user["organization_id"]
        )
        categories = db.scalars(categories_stmt).all()
        
        return [{"id": cat.id, "name": cat.name, "description": cat.description} for cat in categories]
        
    except Exception as e:
        logger.error(f"Error getting policy categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get policy categories")

@app.get("/policies/stats")
async def get_policy_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get policy statistics"""
    try:
        total_policies_stmt = select(func.count(Policy.id)).where(
            Policy.organization_id == current_user["organization_id"]
        )
        total_policies = db.scalar(total_policies_stmt)
        
        # Return empty stats if no data exists
        if total_policies == 0:
            return {
                "total_policies": 0,
                "policies_by_status": {},
                "message": "No policy data available"
            }
        
        policies_by_status_stmt = select(
            Policy.status,
            func.count(Policy.id)
        ).where(
            Policy.organization_id == current_user["organization_id"]
        ).group_by(Policy.status)
        policies_by_status_result = db.execute(policies_by_status_stmt)
        policies_by_status = policies_by_status_result.all()
        
        return {
            "total_policies": total_policies,
            "policies_by_status": {status: count for status, count in policies_by_status},
            "vector_db_stats": vector_service.get_collection_stats("policies")
        }
        
    except Exception as e:
        logger.error(f"Error getting policy stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get policy stats")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
