"""
Compliance Management Service
FastAPI microservice for GRC Compliance Management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, ForeignKey, DECIMAL, select, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, relationship, Mapped, mapped_column
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import uuid
import logging
from enum import Enum
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError
import os

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
        # Generate IDs for documents
        import uuid
        ids = [str(uuid.uuid4()) for _ in documents]
        
        # Generate simple embeddings (zeros for now - in real implementation would use proper embedding model)
        embeddings = [[0.0] * 384 for _ in documents]  # 384 is a common embedding dimension
        
        return self.vector_store.add(ids, embeddings, metadatas, documents)
    
    async def add_compliance_document(self, content, title, compliance_id, organization_id, framework, metadata=None):
        """Add a compliance document to the vector store"""
        import uuid
        
        # Create document ID
        doc_id = str(uuid.uuid4())
        
        # Generate simple embedding (zeros for now - in real implementation would use proper embedding model)
        embedding = [0.0] * 384  # 384 is a common embedding dimension
        
        # Prepare metadata
        doc_metadata = {
            "title": title,
            "compliance_id": compliance_id,
            "organization_id": organization_id,
            "framework": framework,
            "document": content
        }
        
        # Merge with additional metadata if provided
        if metadata:
            doc_metadata.update(metadata)
        
        # Add to vector store
        return self.vector_store.add([doc_id], [embedding], [doc_metadata], [content])
    
    async def search(self, query, n_results=5):
        # Generate simple query embedding (zeros for now - in real implementation would use proper embedding model)
        query_embedding = [0.0] * 384  # 384 is a common embedding dimension
        
        return self.vector_store.query([query_embedding], n_results)
    
    def get_collection_stats(self, collection_name="compliance"):
        """Get collection statistics for the vector database"""
        try:
            # Get basic stats from the vector store
            total_documents = len(self.vector_store.ids) if hasattr(self.vector_store, 'ids') else 0
            
            # Return mock statistics
            return {
                "collection_name": collection_name,
                "total_documents": total_documents,
                "embedding_dimension": 384,
                "storage_size_mb": round(total_documents * 0.001, 2),  # Mock size calculation
                "last_updated": datetime.utcnow().isoformat(),
                "status": "active"
            }
        except Exception as e:
            # Return minimal stats if there's an error
            return {
                "collection_name": collection_name,
                "total_documents": 0,
                "embedding_dimension": 384,
                "storage_size_mb": 0.0,
                "last_updated": datetime.utcnow().isoformat(),
                "status": "error",
                "error": str(e)
            }

vector_service = MockVectorService()

logger = logging.getLogger(__name__)

# Database setup - using environment variables for security
DB_USER = os.getenv("DB_USER", "grc_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "grc_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "grc_platform")

# Construct DATABASE_URL from environment variables
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Validate that critical database credentials are provided
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
if not db_user or not db_password or db_user.strip() == "" or db_password.strip() == "":
    raise ValueError("DB_USER and DB_PASSWORD environment variables must be set for database connection")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Security
security = HTTPBearer()

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Expected JWT Token Format:
# {
#   "sub": "user_id",           # Required: Subject (user identifier)
#   "organization_id": "org_id", # Required: Organization identifier
#   "role": "COMPLIANCE_OFFICER", # Required: User role
#   "exp": 1234567890,          # Required: Expiration timestamp
#   "iat": 1234567890,          # Issued at timestamp
#   "iss": "issuer",            # Token issuer (optional)
#   "aud": "audience"           # Token audience (optional)
# }
#
# Example JWT Token Generation (for testing):
# import jwt
# import time
# 
# payload = {
#     "sub": "user-123",
#     "organization_id": "org-123", 
#     "role": "COMPLIANCE_OFFICER",
#     "exp": int(time.time()) + 3600,  # 1 hour from now
#     "iat": int(time.time()),
#     "iss": "grc-platform",
#     "aud": "compliance-service"
# }
# 
# token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# JWT Validation Utilities
def validate_jwt_token(token: str) -> Dict[str, Any]:
    """
    Validate JWT token and extract user information
    
    Args:
        token: JWT token string
        
    Returns:
        Dict containing user information from token claims
        
    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": True, "verify_signature": True}
        )
        
        # Extract required claims
        user_id = payload.get("sub") or payload.get("user_id")
        organization_id = payload.get("organization_id")
        role = payload.get("role")
        
        # Validate required claims
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing required 'sub' or 'user_id' claim"
            )
        
        if not organization_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing required 'organization_id' claim"
            )
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing required 'role' claim"
            )
        
        # Return user information
        return {
            "id": user_id,
            "organization_id": organization_id,
            "role": role,
            "exp": payload.get("exp"),
            "iat": payload.get("iat"),
            "iss": payload.get("iss"),
            "aud": payload.get("aud")
        }
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature"
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed"
        )

# Enums
class ComplianceStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class EvidenceType(str, Enum):
    DOCUMENT = "DOCUMENT"
    SCREENSHOT = "SCREENSHOT"
    POLICY = "POLICY"
    PROCEDURE = "PROCEDURE"
    TRAINING_RECORD = "TRAINING_RECORD"
    AUDIT_REPORT = "AUDIT_REPORT"

class FrameworkType(str, Enum):
    ISO_27001 = "ISO_27001"
    SOX = "SOX"
    HIPAA = "HIPAA"
    GDPR = "GDPR"
    NIST = "NIST"
    PCI_DSS = "PCI_DSS"
    SOC2 = "SOC2"

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
    compliance_assessments: Mapped[List["ComplianceAssessment"]] = relationship("ComplianceAssessment", back_populates="organization")

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
    compliance_assessments: Mapped[List["ComplianceAssessment"]] = relationship("ComplianceAssessment", back_populates="assessor")

class ComplianceFramework(Base):
    __tablename__ = "compliance_frameworks"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[Optional[str]] = mapped_column(String(50))
    industry: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    requirements: Mapped[List["ComplianceRequirement"]] = relationship("ComplianceRequirement", back_populates="framework")
    assessments: Mapped[List["ComplianceAssessment"]] = relationship("ComplianceAssessment", back_populates="framework")

class ComplianceRequirement(Base):
    __tablename__ = "compliance_requirements"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    framework_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("compliance_frameworks.id"))
    requirement_code: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    priority: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    framework: Mapped[Optional["ComplianceFramework"]] = relationship("ComplianceFramework", back_populates="requirements")
    evidence: Mapped[List["ComplianceEvidence"]] = relationship("ComplianceEvidence", back_populates="requirement")

class ComplianceAssessment(Base):
    __tablename__ = "compliance_assessments"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    framework_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("compliance_frameworks.id"))
    assessment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    assessor_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default=ComplianceStatus.IN_PROGRESS)
    overall_score: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="compliance_assessments")
    framework: Mapped[Optional["ComplianceFramework"]] = relationship("ComplianceFramework", back_populates="assessments")
    assessor: Mapped[Optional["User"]] = relationship("User", back_populates="compliance_assessments")
    evidence: Mapped[List["ComplianceEvidence"]] = relationship("ComplianceEvidence", back_populates="assessment")

class ComplianceEvidence(Base):
    __tablename__ = "compliance_evidence"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("compliance_assessments.id"))
    requirement_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("compliance_requirements.id"))
    evidence_type: Mapped[Optional[str]] = mapped_column(String(50))
    evidence_description: Mapped[Optional[str]] = mapped_column(Text)
    file_path: Mapped[Optional[str]] = mapped_column(String(500))
    is_compliant: Mapped[Optional[bool]] = mapped_column(Boolean)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    assessment: Mapped[Optional["ComplianceAssessment"]] = relationship("ComplianceAssessment", back_populates="evidence")
    requirement: Mapped[Optional["ComplianceRequirement"]] = relationship("ComplianceRequirement", back_populates="evidence")

# Pydantic Models
class ComplianceAssessmentCreate(BaseModel):
    framework_id: str
    assessment_date: Optional[date] = None
    assessor_notes: Optional[str] = None

class ComplianceAssessmentUpdate(BaseModel):
    status: Optional[ComplianceStatus] = None
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    assessor_notes: Optional[str] = None

class ComplianceEvidenceCreate(BaseModel):
    assessment_id: str
    requirement_id: str
    evidence_type: EvidenceType
    evidence_description: str = Field(..., min_length=1)
    file_path: Optional[str] = None
    is_compliant: bool
    notes: Optional[str] = None

class ComplianceSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    organization_id: Optional[str] = None
    framework_id: Optional[str] = None
    status: Optional[ComplianceStatus] = None
    limit: int = Field(10, ge=1, le=100)

class ComplianceSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_results: int
    query: str

class ComplianceResponse(BaseModel):
    id: str
    organization_id: str
    framework_id: str
    assessment_date: datetime
    assessor_id: str
    status: ComplianceStatus
    overall_score: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# FastAPI App
app = FastAPI(
    title="GRC Compliance Management Service",
    description="Microservice for managing GRC compliance assessments and evidence",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Authenticate user using JWT token validation
    
    Args:
        credentials: HTTP Authorization credentials containing the JWT token
        
    Returns:
        Dict containing authenticated user's details
        
    Raises:
        HTTPException: If token is invalid, expired, or missing required claims
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization credentials required"
        )
    
    if not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required"
        )
    
    # Validate JWT token and extract user information
    user_info = validate_jwt_token(credentials.credentials)
    
    # Log successful authentication for audit purposes
    logger.info(f"User authenticated: {user_info['id']} from organization {user_info['organization_id']} with role {user_info['role']}")
    
    return user_info

def calculate_compliance_score(evidence_list: List[ComplianceEvidence]) -> float:
    """Calculate overall compliance score based on evidence"""
    if not evidence_list:
        return 0.0
    
    compliant_count = sum(1 for evidence in evidence_list if evidence.is_compliant)
    total_count = len(evidence_list)
    
    return (compliant_count / total_count) * 100

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "compliance-service"}

@app.get("/frameworks")
async def get_compliance_frameworks(
    industry: Optional[str] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get available compliance frameworks"""
    try:
        stmt = select(ComplianceFramework)
        
        if is_active:
            stmt = stmt.where(ComplianceFramework.is_active == True)
        
        if industry:
            stmt = stmt.where(ComplianceFramework.industry == industry)
        
        frameworks = db.scalars(stmt).all()
        
        return [
            {
                "id": fw.id,
                "name": fw.name,
                "version": fw.version,
                "industry": fw.industry,
                "description": fw.description,
                "requirements_count": len(fw.requirements)
            }
            for fw in frameworks
        ]
        
    except Exception as e:
        logger.error(f"Error getting compliance frameworks: {e}")
        raise HTTPException(status_code=500, detail="Failed to get compliance frameworks")

@app.get("/frameworks/{framework_id}/requirements")
async def get_framework_requirements(
    framework_id: str,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get requirements for a specific framework"""
    try:
        stmt = select(ComplianceRequirement).where(
            ComplianceRequirement.framework_id == framework_id
        )
        
        if category:
            stmt = stmt.where(ComplianceRequirement.category == category)
        
        requirements = db.scalars(stmt).all()
        
        return [
            {
                "id": req.id,
                "requirement_code": req.requirement_code,
                "title": req.title,
                "description": req.description,
                "category": req.category,
                "priority": req.priority
            }
            for req in requirements
        ]
        
    except Exception as e:
        logger.error(f"Error getting framework requirements: {e}")
        raise HTTPException(status_code=500, detail="Failed to get framework requirements")

@app.post("/assessments", response_model=ComplianceResponse)
async def create_compliance_assessment(
    assessment_data: ComplianceAssessmentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new compliance assessment"""
    try:
        # Verify framework exists
        framework_stmt = select(ComplianceFramework).where(
            ComplianceFramework.id == assessment_data.framework_id
        )
        framework = db.scalar(framework_stmt)
        
        if not framework:
            raise HTTPException(status_code=404, detail="Compliance framework not found")
        
        # Create assessment
        assessment = ComplianceAssessment(
            organization_id=current_user["organization_id"],
            framework_id=assessment_data.framework_id,
            assessment_date=assessment_data.assessment_date or datetime.utcnow(),
            assessor_id=current_user["id"]
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        # Add framework information to vector database
        try:
            framework_content = f"{framework.name} {framework.description or ''}"
            vector_service.add_compliance_document(
                content=framework_content,
                title=framework.name,
                compliance_id=assessment.id,
                organization_id=current_user["organization_id"],
                framework=framework.name,
                metadata={
                    "assessment_id": assessment.id,
                    "framework_id": framework.id,
                    "status": assessment.status,
                    "assessor_id": current_user["id"]
                }
            )
        except Exception as e:
            logger.warning(f"Failed to add assessment to vector database: {e}")
        
        logger.info(f"Compliance assessment created: {assessment.id}")
        return assessment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating compliance assessment: {e}")
        raise HTTPException(status_code=500, detail="Failed to create compliance assessment")

@app.get("/assessments", response_model=List[ComplianceResponse])
async def get_compliance_assessments(
    organization_id: Optional[str] = None,
    framework_id: Optional[str] = None,
    status: Optional[ComplianceStatus] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get compliance assessments with filtering"""
    try:
        stmt = select(ComplianceAssessment)
        
        # Filter by organization
        if organization_id:
            stmt = stmt.where(ComplianceAssessment.organization_id == organization_id)
        else:
            stmt = stmt.where(ComplianceAssessment.organization_id == current_user["organization_id"])
        
        # Filter by framework
        if framework_id:
            stmt = stmt.where(ComplianceAssessment.framework_id == framework_id)
        
        # Filter by status
        if status:
            stmt = stmt.where(ComplianceAssessment.status == status)
        
        # Apply pagination
        assessments = db.scalars(stmt.offset(offset).limit(limit)).all()
        
        return assessments
        
    except Exception as e:
        logger.error(f"Error getting compliance assessments: {e}")
        raise HTTPException(status_code=500, detail="Failed to get compliance assessments")

@app.get("/assessments/{assessment_id}", response_model=ComplianceResponse)
async def get_compliance_assessment(
    assessment_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific compliance assessment by ID"""
    try:
        assessment_stmt = select(ComplianceAssessment).where(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        )
        assessment = db.scalar(assessment_stmt)
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Compliance assessment not found")
        
        return assessment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting compliance assessment: {e}")
        raise HTTPException(status_code=500, detail="Failed to get compliance assessment")

@app.put("/assessments/{assessment_id}", response_model=ComplianceResponse)
async def update_compliance_assessment(
    assessment_id: str,
    assessment_data: ComplianceAssessmentUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a compliance assessment"""
    try:
        assessment_stmt = select(ComplianceAssessment).where(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        )
        assessment = db.scalar(assessment_stmt)
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Compliance assessment not found")
        
        # Update fields
        update_data = assessment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assessment, field, value)
        
        # Recalculate overall score if evidence exists
        if assessment.evidence:
            assessment.overall_score = calculate_compliance_score(assessment.evidence)
        
        assessment.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(assessment)
        
        logger.info(f"Compliance assessment updated: {assessment_id}")
        return assessment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating compliance assessment: {e}")
        raise HTTPException(status_code=500, detail="Failed to update compliance assessment")

@app.post("/assessments/{assessment_id}/evidence")
async def add_compliance_evidence(
    assessment_id: str,
    evidence_data: ComplianceEvidenceCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add evidence to a compliance assessment"""
    try:
        # Verify assessment exists and belongs to organization
        assessment_stmt = select(ComplianceAssessment).where(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        )
        assessment = db.scalar(assessment_stmt)
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Compliance assessment not found")
        
        # Verify requirement exists
        requirement_stmt = select(ComplianceRequirement).where(
            ComplianceRequirement.id == evidence_data.requirement_id
        )
        requirement = db.scalar(requirement_stmt)
        
        if not requirement:
            raise HTTPException(status_code=404, detail="Compliance requirement not found")
        
        # Create evidence
        evidence = ComplianceEvidence(
            assessment_id=assessment_id,
            requirement_id=evidence_data.requirement_id,
            evidence_type=evidence_data.evidence_type,
            evidence_description=evidence_data.evidence_description,
            file_path=evidence_data.file_path,
            is_compliant=evidence_data.is_compliant,
            notes=evidence_data.notes
        )
        
        db.add(evidence)
        
        # Recalculate overall compliance score
        assessment.overall_score = calculate_compliance_score(assessment.evidence)
        assessment.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(evidence)
        
        logger.info(f"Compliance evidence added: {evidence.id}")
        return {
            "id": evidence.id,
            "assessment_id": assessment_id,
            "requirement_id": evidence_data.requirement_id,
            "is_compliant": evidence_data.is_compliant,
            "overall_score": assessment.overall_score,
            "message": "Compliance evidence added successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding compliance evidence: {e}")
        raise HTTPException(status_code=500, detail="Failed to add compliance evidence")

@app.get("/assessments/{assessment_id}/evidence")
async def get_compliance_evidence(
    assessment_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get evidence for a compliance assessment"""
    try:
        # Verify assessment exists and belongs to organization
        assessment_stmt = select(ComplianceAssessment).where(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        )
        assessment = db.scalar(assessment_stmt)
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Compliance assessment not found")
        
        evidence_list = []
        for evidence in assessment.evidence:
            evidence_list.append({
                "id": evidence.id,
                "requirement_id": evidence.requirement_id,
                "requirement_code": evidence.requirement.requirement_code,
                "requirement_title": evidence.requirement.title,
                "evidence_type": evidence.evidence_type,
                "evidence_description": evidence.evidence_description,
                "file_path": evidence.file_path,
                "is_compliant": evidence.is_compliant,
                "notes": evidence.notes,
                "created_at": evidence.created_at
            })
        
        return {
            "assessment_id": assessment_id,
            "evidence": evidence_list,
            "total_evidence": len(evidence_list),
            "compliance_score": assessment.overall_score
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting compliance evidence: {e}")
        raise HTTPException(status_code=500, detail="Failed to get compliance evidence")

@app.post("/compliance/search", response_model=ComplianceSearchResponse)
async def search_compliance(
    search_request: ComplianceSearchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search compliance information using AI-powered vector search"""
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
                
            # Apply framework filter if specified
            if search_request.framework_id and result.get("metadata", {}).get("framework") != search_request.framework_id:
                continue
                
            # Apply status filter if specified
            if search_request.status and result.get("metadata", {}).get("status") != search_request.status:
                continue
                
            filtered_results.append(result)
        
        # Format results
        results = []
        for result in filtered_results:
            results.append({
                "id": result.get("metadata", {}).get("compliance_id"),
                "title": result.get("metadata", {}).get("title"),
                "content": result.get("document", "")[:500] + "..." if len(result.get("document", "")) > 500 else result.get("document", ""),
                "metadata": result.get("metadata", {}),
                "similarity_score": 1 - result.get("distance", 0) if result.get("distance") else 0
            })
        
        return ComplianceSearchResponse(
            results=results,
            total_results=len(results),
            query=search_request.query
        )
        
    except Exception as e:
        logger.error(f"Error searching compliance: {e}")
        raise HTTPException(status_code=500, detail="Failed to search compliance")

@app.get("/compliance/stats")
async def get_compliance_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get compliance statistics"""
    try:
        total_assessments_stmt = select(func.count(ComplianceAssessment.id)).where(
            ComplianceAssessment.organization_id == current_user["organization_id"]
        )
        total_assessments = db.scalar(total_assessments_stmt)
        
        # Return empty stats if no data exists
        if total_assessments == 0:
            return {
                "total_assessments": 0,
                "assessments_by_status": {},
                "message": "No compliance data available"
            }
        
        assessments_by_status_stmt = select(
            ComplianceAssessment.status,
            func.count(ComplianceAssessment.id)
        ).where(
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).group_by(ComplianceAssessment.status)
        assessments_by_status_result = db.execute(assessments_by_status_stmt)
        assessments_by_status = assessments_by_status_result.all()
        
        assessments_by_framework_stmt = select(
            ComplianceFramework.name,
            func.count(ComplianceAssessment.id)
        ).join(ComplianceAssessment).where(
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).group_by(ComplianceFramework.name)
        assessments_by_framework_result = db.execute(assessments_by_framework_stmt)
        assessments_by_framework = assessments_by_framework_result.all()
        
        avg_compliance_score_stmt = select(
            func.avg(ComplianceAssessment.overall_score)
        ).where(
            ComplianceAssessment.organization_id == current_user["organization_id"],
            ComplianceAssessment.overall_score.isnot(None)
        )
        avg_compliance_score = db.scalar(avg_compliance_score_stmt) or 0
        
        return {
            "total_assessments": total_assessments,
            "assessments_by_status": {status: count for status, count in assessments_by_status},
            "assessments_by_framework": {framework: count for framework, count in assessments_by_framework},
            "average_compliance_score": round(float(avg_compliance_score), 2),
            "vector_db_stats": vector_service.get_collection_stats("compliance")
        }
        
    except Exception as e:
        logger.error(f"Error getting compliance stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get compliance stats")

@app.get("/auth/test", summary="Test JWT Authentication")
async def test_authentication(current_user: dict = Depends(get_current_user)):
    """
    Test endpoint to verify JWT authentication is working correctly
    """
    return {
        "message": "Authentication successful",
        "user": {
            "id": current_user["id"],
            "organization_id": current_user["organization_id"],
            "role": current_user["role"]
        },
        "authenticated_at": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
