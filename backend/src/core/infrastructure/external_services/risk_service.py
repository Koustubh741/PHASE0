"""
Risk Management Service
FastAPI microservice for GRC Risk Management
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
import os
from enum import Enum

# Validate required environment variables immediately
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is required but not set. "
        "Please set the DATABASE_URL environment variable with your database connection string."
    )

# Import shared utilities
import sys
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
    
    async def search(self, query, n_results=5):
        # Generate simple query embedding (zeros for now - in real implementation would use proper embedding model)
        query_embedding = [0.0] * 384  # 384 is a common embedding dimension
        
        return self.vector_store.query([query_embedding], n_results)
    
    async def add_risk_document(self, content, title, risk_id, organization_id, risk_type=None, metadata=None):
        """Add a risk document to the vector store"""
        try:
            import uuid
            
            # Create document ID
            doc_id = str(uuid.uuid4())
            
            # Generate simple embedding (zeros for now - in real implementation would use proper embedding model)
            embedding = [0.0] * 384  # 384 is a common embedding dimension
            
            # Prepare metadata
            doc_metadata = {
                "risk_id": risk_id,
                "title": title,
                "organization_id": organization_id,
                "risk_type": risk_type,
                "collection_type": "risks",
                "document": content
            }
            
            # Merge with additional metadata if provided
            if metadata:
                doc_metadata.update(metadata)
            
            # Add to vector store
            return self.vector_store.add([doc_id], [embedding], [doc_metadata], [content])
        except Exception as e:
            logger.error(f"Failed to add risk document: {e}")
            return {"status": "error", "message": str(e)}
    
    async def update_document(self, doc_id, content, metadata=None, collection_type=None):
        """Update a document in the vector store"""
        try:
            # Generate simple embedding (zeros for now - in real implementation would use proper embedding model)
            embedding = [0.0] * 384  # 384 is a common embedding dimension
            
            # Prepare metadata
            doc_metadata = {
                "doc_id": doc_id, 
                "collection_type": collection_type,
                "document": content
            }
            if metadata:
                doc_metadata.update(metadata)
            
            # For mock implementation, we'll add the updated document
            # In a real vector store, this would update the existing document
            return self.vector_store.add([doc_id], [embedding], [doc_metadata], [content])
        except Exception as e:
            logger.error(f"Failed to update document: {e}")
            return {"status": "error", "message": str(e)}
    
    async def delete_document(self, doc_id, collection_type=None):
        """Delete a document from the vector store"""
        try:
            # Delete from vector store
            self.vector_store.delete([doc_id])
            logger.info(f"Deleted document {doc_id} from collection {collection_type}")
            return {"status": "deleted", "doc_id": doc_id}
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            return {"status": "error", "message": str(e)}
    
    async def search_similar_documents(self, query, n_results=5, collection_type=None, filters=None, organization_id=None):
        """Search for similar documents"""
        try:
            # Use the existing search method
            results = await self.search(query, n_results)
            
            # Convert results to the expected format and apply filters
            filtered_results = []
            if results and 'ids' in results and results['ids']:
                for i, doc_id in enumerate(results['ids'][0]):
                    if i < len(results['metadatas'][0]):
                        metadata = results['metadatas'][0][i]
                        
                        # Apply collection type filter if specified
                        if collection_type and metadata.get("collection_type") != collection_type:
                            continue
                        
                        # Apply organization filter if specified
                        if organization_id and metadata.get("organization_id") != organization_id:
                            continue
                        
                        # Format result
                        result = {
                            "id": doc_id,
                            "document": results['documents'][0][i] if i < len(results['documents'][0]) else "",
                            "metadata": metadata,
                            "distance": results['distances'][0][i] if i < len(results['distances'][0]) else 0
                        }
                        filtered_results.append(result)
            
            return filtered_results
        except Exception as e:
            logger.error(f"Failed to search similar documents: {e}")
            return []
    
    async def get_collection_stats(self, collection_name):
        """Get statistics for a collection"""
        try:
            # Get actual count from vector store
            total_documents = self.vector_store.count()
            
            return {
                "collection_name": collection_name,
                "total_documents": total_documents,
                "status": "active",
                "mock_stats": False
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"status": "error", "message": str(e)}

vector_service = MockVectorService()

logger = logging.getLogger(__name__)

# Database setup

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Security
security = HTTPBearer()

# Enums
class RiskStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    ASSESSED = "ASSESSED"
    TREATED = "TREATED"
    MONITORED = "MONITORED"
    CLOSED = "CLOSED"

class RiskType(str, Enum):
    OPERATIONAL = "OPERATIONAL"
    FINANCIAL = "FINANCIAL"
    COMPLIANCE = "COMPLIANCE"
    TECHNOLOGY = "TECHNOLOGY"
    STRATEGIC = "STRATEGIC"
    REPUTATIONAL = "REPUTATIONAL"

class TreatmentType(str, Enum):
    ACCEPT = "ACCEPT"
    AVOID = "AVOID"
    MITIGATE = "MITIGATE"
    TRANSFER = "TRANSFER"

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
    risks: Mapped[List["Risk"]] = relationship("Risk", back_populates="organization")
    risk_categories: Mapped[List["RiskCategory"]] = relationship("RiskCategory", back_populates="organization")

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
    owned_risks: Mapped[List["Risk"]] = relationship("Risk", foreign_keys="Risk.owner_id", back_populates="owner")
    created_risks: Mapped[List["Risk"]] = relationship("Risk", foreign_keys="Risk.created_by", back_populates="creator")
    risk_assessments: Mapped[List["RiskAssessment"]] = relationship("RiskAssessment", back_populates="assessor")
    risk_treatments: Mapped[List["RiskTreatment"]] = relationship("RiskTreatment", back_populates="owner")

class RiskCategory(Base):
    __tablename__ = "risk_categories"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="risk_categories")
    risks: Mapped[List["Risk"]] = relationship("Risk", back_populates="category")

class Risk(Base):
    __tablename__ = "risks"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("risk_categories.id"))
    risk_type: Mapped[Optional[str]] = mapped_column(String(100))
    impact_score: Mapped[Optional[int]] = mapped_column(Integer)
    probability_score: Mapped[Optional[int]] = mapped_column(Integer)
    inherent_risk_score: Mapped[Optional[int]] = mapped_column(Integer)
    residual_risk_score: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50), default=RiskStatus.IDENTIFIED)
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    owner_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    created_by: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category: Mapped[Optional["RiskCategory"]] = relationship("RiskCategory", back_populates="risks")
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="risks")
    owner: Mapped[Optional["User"]] = relationship("User", foreign_keys=[owner_id], back_populates="owned_risks")
    creator: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by], back_populates="created_risks")
    assessments: Mapped[List["RiskAssessment"]] = relationship("RiskAssessment", back_populates="risk")
    treatments: Mapped[List["RiskTreatment"]] = relationship("RiskTreatment", back_populates="risk")

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    risk_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("risks.id"))
    assessment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    assessor_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    impact_score: Mapped[Optional[int]] = mapped_column(Integer)
    probability_score: Mapped[Optional[int]] = mapped_column(Integer)
    risk_score: Mapped[Optional[int]] = mapped_column(Integer)
    assessment_notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    risk: Mapped[Optional["Risk"]] = relationship("Risk", back_populates="assessments")
    assessor: Mapped[Optional["User"]] = relationship("User", back_populates="risk_assessments")

class RiskTreatment(Base):
    __tablename__ = "risk_treatments"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    risk_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("risks.id"))
    treatment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(50), default="PLANNED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    risk: Mapped[Optional["Risk"]] = relationship("Risk", back_populates="treatments")
    owner: Mapped[Optional["User"]] = relationship("User", back_populates="risk_treatments")

# Pydantic Models
class RiskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    category_id: Optional[str] = None
    risk_type: Optional[RiskType] = None
    impact_score: Optional[int] = Field(None, ge=1, le=5)
    probability_score: Optional[int] = Field(None, ge=1, le=5)
    owner_id: Optional[str] = None

class RiskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    category_id: Optional[str] = None
    risk_type: Optional[RiskType] = None
    impact_score: Optional[int] = Field(None, ge=1, le=5)
    probability_score: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[RiskStatus] = None
    owner_id: Optional[str] = None

class RiskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    category_id: Optional[str]
    risk_type: Optional[str]
    impact_score: Optional[int]
    probability_score: Optional[int]
    inherent_risk_score: Optional[int]
    residual_risk_score: Optional[int]
    status: RiskStatus
    organization_id: str
    owner_id: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RiskAssessmentCreate(BaseModel):
    risk_id: str
    impact_score: int = Field(..., ge=1, le=5)
    probability_score: int = Field(..., ge=1, le=5)
    assessment_notes: Optional[str] = None

class RiskTreatmentCreate(BaseModel):
    risk_id: str
    treatment_type: TreatmentType
    description: str = Field(..., min_length=1)
    owner_id: Optional[str] = None
    due_date: Optional[date] = None

class RiskSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    organization_id: Optional[str] = None
    risk_type: Optional[RiskType] = None
    status: Optional[RiskStatus] = None
    limit: int = Field(10, ge=1, le=100)

class RiskSearchResponse(BaseModel):
    risks: List[Dict[str, Any]]
    total_results: int
    query: str

# FastAPI App
app = FastAPI(
    title="GRC Risk Management Service",
    description="Microservice for managing GRC risks with AI-powered assessment",
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
    """Validate JWT token and extract user information"""
    try:
        import jwt
        from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
        
        # Get JWT secret from environment
        jwt_secret = os.getenv("JWT_SECRET_KEY")
        if not jwt_secret:
            raise HTTPException(status_code=500, detail="JWT secret not configured")
        
        # Decode and validate JWT token
        token = credentials.credentials
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=["HS256"],
            options={"verify_exp": True, "verify_aud": False}
        )
        
        # Extract user information from token claims
        user_id = payload.get("user_id")
        organization_id = payload.get("organization_id")
        role = payload.get("role")
        
        if not all([user_id, organization_id, role]):
            raise HTTPException(status_code=401, detail="Invalid token claims")
        
        return {
            "id": user_id,
            "organization_id": organization_id,
            "role": role
        }
        
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

def calculate_risk_score(impact: int, probability: int) -> int:
    """Calculate risk score based on impact and probability"""
    return impact * probability

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "risk-service"}

@app.post("/risks", response_model=RiskResponse)
async def create_risk(
    risk_data: RiskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new risk"""
    try:
        # Calculate risk scores
        inherent_risk_score = None
        if risk_data.impact_score and risk_data.probability_score:
            inherent_risk_score = calculate_risk_score(
                risk_data.impact_score, 
                risk_data.probability_score
            )
        
        # Create risk in database
        db_risk = Risk(
            title=risk_data.title,
            description=risk_data.description,
            category_id=risk_data.category_id,
            risk_type=risk_data.risk_type,
            impact_score=risk_data.impact_score,
            probability_score=risk_data.probability_score,
            inherent_risk_score=inherent_risk_score,
            organization_id=current_user["organization_id"],
            owner_id=risk_data.owner_id,
            created_by=current_user["id"]
        )
        
        db.add(db_risk)
        db.commit()
        db.refresh(db_risk)
        
        # Add to vector database for AI search
        try:
            risk_content = f"{risk_data.title}\n{risk_data.description or ''}"
            vector_service.add_risk_document(
                content=risk_content,
                title=risk_data.title,
                risk_id=db_risk.id,
                organization_id=current_user["organization_id"],
                risk_type=risk_data.risk_type,
                metadata={
                    "status": db_risk.status,
                    "impact_score": db_risk.impact_score,
                    "probability_score": db_risk.probability_score,
                    "inherent_risk_score": db_risk.inherent_risk_score,
                    "created_by": current_user["id"]
                }
            )
        except Exception as e:
            logger.warning(f"Failed to add risk to vector database: {e}")
        
        logger.info(f"Risk created: {db_risk.id}")
        return db_risk
        
    except Exception as e:
        logger.error(f"Error creating risk: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create risk")

@app.get("/risks", response_model=List[RiskResponse])
async def get_risks(
    organization_id: Optional[str] = None,
    status: Optional[RiskStatus] = None,
    risk_type: Optional[RiskType] = None,
    category_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risks with filtering"""
    try:
        stmt = select(Risk)
        
        # Filter by organization
        if organization_id:
            stmt = stmt.where(Risk.organization_id == organization_id)
        else:
            stmt = stmt.where(Risk.organization_id == current_user["organization_id"])
        
        # Filter by status
        if status:
            stmt = stmt.where(Risk.status == status)
        
        # Filter by risk type
        if risk_type:
            stmt = stmt.where(Risk.risk_type == risk_type)
        
        # Filter by category
        if category_id:
            stmt = stmt.where(Risk.category_id == category_id)
        
        # Apply pagination
        risks = db.scalars(stmt.offset(offset).limit(limit)).all()
        
        return risks
        
    except Exception as e:
        logger.error(f"Error getting risks: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to get risks")

@app.get("/risks/{risk_id}", response_model=RiskResponse)
async def get_risk(
    risk_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific risk by ID"""
    try:
        risk_stmt = select(Risk).where(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        )
        risk = db.scalar(risk_stmt)
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        return risk
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risk: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to get risk")

@app.put("/risks/{risk_id}", response_model=RiskResponse)
async def update_risk(
    risk_id: str,
    risk_data: RiskUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a risk"""
    try:
        risk_stmt = select(Risk).where(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        )
        risk = db.scalar(risk_stmt)
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        # Update fields
        update_data = risk_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(risk, field, value)
        
        # Recalculate risk score if impact or probability changed
        if risk_data.impact_score or risk_data.probability_score:
            if risk.impact_score and risk.probability_score:
                risk.inherent_risk_score = calculate_risk_score(
                    risk.impact_score, 
                    risk.probability_score
                )
        
        risk.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(risk)
        
        # Update in vector database asynchronously
        try:
            risk_content = f"{risk.title}\n{risk.description or ''}"
            await vector_service.update_document(
                doc_id=risk_id,
                content=risk_content,
                metadata={
                    "title": risk.title,
                    "status": risk.status,
                    "impact_score": risk.impact_score,
                    "probability_score": risk.probability_score,
                    "inherent_risk_score": risk.inherent_risk_score,
                    "updated_at": risk.updated_at.isoformat()
                },
                collection_type="risks"
            )
        except Exception as e:
            logger.warning(f"Failed to update risk in vector database: {e}")
        
        logger.info(f"Risk updated: {risk_id}")
        return risk
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating risk: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update risk")

@app.delete("/risks/{risk_id}")
async def delete_risk(
    risk_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a risk"""
    try:
        risk_stmt = select(Risk).where(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        )
        risk = db.scalar(risk_stmt)
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        # Delete from database
        db.delete(risk)
        db.commit()
        
        # Delete from vector database asynchronously
        try:
            await vector_service.delete_document(risk_id, collection_type="risks")
        except Exception as e:
            logger.warning(f"Failed to delete risk from vector database: {e}")
        
        logger.info(f"Risk deleted: {risk_id}")
        return {"message": "Risk deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting risk: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete risk")

@app.post("/risks/search", response_model=RiskSearchResponse)
async def search_risks(
    search_request: RiskSearchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search risks using AI-powered vector search"""
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
                
            # Apply risk_type filter if specified
            if search_request.risk_type and result.get("metadata", {}).get("risk_type") != search_request.risk_type:
                continue
                
            # Apply status filter if specified
            if search_request.status and result.get("metadata", {}).get("status") != search_request.status:
                continue
                
            filtered_results.append(result)
        
        # Format results
        risks = []
        for result in filtered_results:
            risks.append({
                "id": result.get("metadata", {}).get("risk_id"),
                "title": result.get("metadata", {}).get("title"),
                "content": result.get("document", "")[:500] + "..." if len(result.get("document", "")) > 500 else result.get("document", ""),
                "metadata": result.get("metadata", {}),
                "similarity_score": 1 - result.get("distance", 0) if result.get("distance") else 0
            })
        
        return RiskSearchResponse(
            risks=risks,
            total_results=len(risks),
            query=search_request.query
        )
        
    except Exception as e:
        logger.error(f"Error searching risks: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to search risks")

@app.post("/risks/{risk_id}/assessments")
async def create_risk_assessment(
    risk_id: str,
    assessment_data: RiskAssessmentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a risk assessment"""
    try:
        # Verify risk exists and belongs to organization
        risk_stmt = select(Risk).where(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        )
        risk = db.scalar(risk_stmt)
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        # Calculate risk score
        risk_score = calculate_risk_score(
            assessment_data.impact_score,
            assessment_data.probability_score
        )
        
        # Create assessment
        assessment = RiskAssessment(
            risk_id=risk_id,
            assessment_date=datetime.utcnow(),
            assessor_id=current_user["id"],
            impact_score=assessment_data.impact_score,
            probability_score=assessment_data.probability_score,
            risk_score=risk_score,
            assessment_notes=assessment_data.assessment_notes
        )
        
        db.add(assessment)
        
        # Update risk with new scores
        risk.impact_score = assessment_data.impact_score
        risk.probability_score = assessment_data.probability_score
        risk.inherent_risk_score = risk_score
        risk.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(assessment)
        
        logger.info(f"Risk assessment created: {assessment.id}")
        return {
            "id": assessment.id,
            "risk_id": risk_id,
            "risk_score": risk_score,
            "assessment_date": assessment.assessment_date,
            "message": "Risk assessment created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating risk assessment: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create risk assessment")

@app.post("/risks/{risk_id}/treatments")
async def create_risk_treatment(
    risk_id: str,
    treatment_data: RiskTreatmentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a risk treatment"""
    try:
        # Verify risk exists and belongs to organization
        risk_stmt = select(Risk).where(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        )
        risk = db.scalar(risk_stmt)
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        # Create treatment
        treatment = RiskTreatment(
            risk_id=risk_id,
            treatment_type=treatment_data.treatment_type,
            description=treatment_data.description,
            owner_id=treatment_data.owner_id or current_user["id"],
            due_date=treatment_data.due_date
        )
        
        db.add(treatment)
        db.commit()
        db.refresh(treatment)
        
        logger.info(f"Risk treatment created: {treatment.id}")
        return {
            "id": treatment.id,
            "risk_id": risk_id,
            "treatment_type": treatment.treatment_type,
            "message": "Risk treatment created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating risk treatment: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create risk treatment")

@app.get("/risks/categories")
async def get_risk_categories(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk categories"""
    try:
        categories_stmt = select(RiskCategory).where(
            RiskCategory.organization_id == current_user["organization_id"]
        )
        categories = db.scalars(categories_stmt).all()
        
        return [{"id": cat.id, "name": cat.name, "description": cat.description} for cat in categories]
        
    except Exception as e:
        logger.error(f"Error getting risk categories: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to get risk categories")

@app.get("/risks/stats")
async def get_risk_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk statistics"""
    try:
        total_risks_stmt = select(func.count(Risk.id)).where(
            Risk.organization_id == current_user["organization_id"]
        )
        total_risks = db.scalar(total_risks_stmt)
        
        # Return empty stats if no data exists
        if total_risks == 0:
            return {
                "total_risks": 0,
                "risks_by_status": {},
                "message": "No risk data available"
            }
        
        risks_by_status_stmt = select(
            Risk.status,
            func.count(Risk.id)
        ).where(
            Risk.organization_id == current_user["organization_id"]
        ).group_by(Risk.status)
        risks_by_status_result = db.execute(risks_by_status_stmt)
        risks_by_status = risks_by_status_result.all()
        
        risks_by_type_stmt = select(
            Risk.risk_type,
            func.count(Risk.id)
        ).where(
            Risk.organization_id == current_user["organization_id"]
        ).group_by(Risk.risk_type)
        risks_by_type_result = db.execute(risks_by_type_stmt)
        risks_by_type = risks_by_type_result.all()
        
        high_risks_stmt = select(func.count(Risk.id)).where(
            Risk.organization_id == current_user["organization_id"],
            Risk.inherent_risk_score >= 15  # High risk threshold
        )
        high_risks = db.scalar(high_risks_stmt)
        
        # Get vector database stats asynchronously
        try:
            vector_stats = await vector_service.get_collection_stats("risks")
        except Exception as e:
            logger.warning(f"Failed to get vector stats: {e}")
            vector_stats = {"error": "Vector stats unavailable"}
        
        return {
            "total_risks": total_risks,
            "risks_by_status": {status: count for status, count in risks_by_status},
            "risks_by_type": {risk_type: count for risk_type, count in risks_by_type},
            "high_risks": high_risks,
            "vector_db_stats": vector_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting risk stats: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to get risk stats")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)