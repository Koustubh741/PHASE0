"""
Risk Management Service
FastAPI microservice for GRC Risk Management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import uuid
import logging
from enum import Enum

# Import vector service
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vector-db'))
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ai-agents'))
from simple_vector_store import SimpleVectorStore

# Mock vector service for compatibility
class MockVectorService:
    def __init__(self):
        self.vector_store = SimpleVectorStore()
    
    async def add_documents(self, documents, metadatas=None):
        return self.vector_store.add_documents(documents, metadatas)
    
    async def search(self, query, n_results=5):
        return self.vector_store.search(query, n_results)

vector_service = MockVectorService()

logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = "postgresql://grc_user:grc_password@localhost:5432/grc_platform"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    industry = Column(String(100))
    size = Column(String(50))
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"))
    role = Column(String(50), nullable=False, default="USER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", backref="users")

class RiskCategory(Base):
    __tablename__ = "risk_categories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    organization_id = Column(String, ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", backref="risk_categories")

class Risk(Base):
    __tablename__ = "risks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    description = Column(Text)
    category_id = Column(String, ForeignKey("risk_categories.id"))
    risk_type = Column(String(100))
    impact_score = Column(Integer)
    probability_score = Column(Integer)
    inherent_risk_score = Column(Integer)
    residual_risk_score = Column(Integer)
    status = Column(String(50), default=RiskStatus.IDENTIFIED)
    organization_id = Column(String, ForeignKey("organizations.id"))
    owner_id = Column(String, ForeignKey("users.id"))
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = relationship("RiskCategory", backref="risks")
    organization = relationship("Organization", backref="risks")
    owner = relationship("User", foreign_keys=[owner_id], backref="owned_risks")
    creator = relationship("User", foreign_keys=[created_by], backref="created_risks")

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    risk_id = Column(String, ForeignKey("risks.id"))
    assessment_date = Column(DateTime, nullable=False)
    assessor_id = Column(String, ForeignKey("users.id"))
    impact_score = Column(Integer)
    probability_score = Column(Integer)
    risk_score = Column(Integer)
    assessment_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    risk = relationship("Risk", backref="assessments")
    assessor = relationship("User", backref="risk_assessments")

class RiskTreatment(Base):
    __tablename__ = "risk_treatments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    risk_id = Column(String, ForeignKey("risks.id"))
    treatment_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"))
    due_date = Column(DateTime)
    status = Column(String(50), default="PLANNED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    risk = relationship("Risk", backref="treatments")
    owner = relationship("User", backref="risk_treatments")

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
    # Simplified authentication - in production, implement proper JWT validation
    return {
        "id": "user-123",
        "organization_id": "org-123",
        "role": "RISK_MANAGER"
    }

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
        query = db.query(Risk)
        
        # Filter by organization
        if organization_id:
            query = query.filter(Risk.organization_id == organization_id)
        else:
            query = query.filter(Risk.organization_id == current_user["organization_id"])
        
        # Filter by status
        if status:
            query = query.filter(Risk.status == status)
        
        # Filter by risk type
        if risk_type:
            query = query.filter(Risk.risk_type == risk_type)
        
        # Filter by category
        if category_id:
            query = query.filter(Risk.category_id == category_id)
        
        # Apply pagination
        risks = query.offset(offset).limit(limit).all()
        
        return risks
        
    except Exception as e:
        logger.error(f"Error getting risks: {e}")
        raise HTTPException(status_code=500, detail="Failed to get risks")

@app.get("/risks/{risk_id}", response_model=RiskResponse)
async def get_risk(
    risk_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific risk by ID"""
    try:
        risk = db.query(Risk).filter(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        ).first()
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        return risk
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risk: {e}")
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
        risk = db.query(Risk).filter(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        ).first()
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        # Update fields
        update_data = risk_data.dict(exclude_unset=True)
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
        
        # Update in vector database
        try:
            risk_content = f"{risk.title}\n{risk.description or ''}"
            vector_service.update_document(
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
        raise HTTPException(status_code=500, detail="Failed to update risk")

@app.delete("/risks/{risk_id}")
async def delete_risk(
    risk_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a risk"""
    try:
        risk = db.query(Risk).filter(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        ).first()
        
        if not risk:
            raise HTTPException(status_code=404, detail="Risk not found")
        
        # Delete from database
        db.delete(risk)
        db.commit()
        
        # Delete from vector database
        try:
            vector_service.delete_document(risk_id, collection_type="risks")
        except Exception as e:
            logger.warning(f"Failed to delete risk from vector database: {e}")
        
        logger.info(f"Risk deleted: {risk_id}")
        return {"message": "Risk deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting risk: {e}")
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
        search_results = vector_service.search_similar_documents(
            query=search_request.query,
            collection_type="risks",
            n_results=search_request.limit,
            organization_id=current_user["organization_id"],
            filters={
                "risk_type": search_request.risk_type,
                "status": search_request.status
            } if search_request.risk_type or search_request.status else None
        )
        
        # Format results
        risks = []
        for result in search_results:
            risks.append({
                "id": result["metadata"].get("risk_id"),
                "title": result["metadata"].get("title"),
                "content": result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"],
                "metadata": result["metadata"],
                "similarity_score": 1 - result["distance"] if result["distance"] else 0
            })
        
        return RiskSearchResponse(
            risks=risks,
            total_results=len(risks),
            query=search_request.query
        )
        
    except Exception as e:
        logger.error(f"Error searching risks: {e}")
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
        risk = db.query(Risk).filter(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        ).first()
        
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
        risk = db.query(Risk).filter(
            Risk.id == risk_id,
            Risk.organization_id == current_user["organization_id"]
        ).first()
        
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
        raise HTTPException(status_code=500, detail="Failed to create risk treatment")

@app.get("/risks/categories")
async def get_risk_categories(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk categories"""
    try:
        categories = db.query(RiskCategory).filter(
            RiskCategory.organization_id == current_user["organization_id"]
        ).all()
        
        return [{"id": cat.id, "name": cat.name, "description": cat.description} for cat in categories]
        
    except Exception as e:
        logger.error(f"Error getting risk categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get risk categories")

@app.get("/risks/stats")
async def get_risk_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk statistics with mock data fallback"""
    try:
        total_risks = db.query(Risk).filter(
            Risk.organization_id == current_user["organization_id"]
        ).count()
        
        risks_by_status = db.query(
            Risk.status,
            db.func.count(Risk.id)
        ).filter(
            Risk.organization_id == current_user["organization_id"]
        ).group_by(Risk.status).all()
        
        # If no data exists, return mock data
        if total_risks == 0:
            return {
                "total_risks": 35,
                "risks_by_status": {
                    "Active": 28,
                    "Mitigated": 5,
                    "Closed": 2
                },
                "risks_by_level": {
                    "High": 7,
                    "Medium": 18,
                    "Low": 10
                },
                "risks_by_type": {
                    "Operational Risk": 12,
                    "Compliance Risk": 8,
                    "Technology Risk": 6,
                    "Financial Risk": 5,
                    "Strategic Risk": 4
                },
                "high_risks": 7,
                "overdue_risks": 3,
                "mock_data": True
            }
        
        risks_by_type = db.query(
            Risk.risk_type,
            db.func.count(Risk.id)
        ).filter(
            Risk.organization_id == current_user["organization_id"]
        ).group_by(Risk.risk_type).all()
        
        high_risks = db.query(Risk).filter(
            Risk.organization_id == current_user["organization_id"],
            Risk.inherent_risk_score >= 15  # High risk threshold
        ).count()
        
        return {
            "total_risks": total_risks,
            "risks_by_status": {status: count for status, count in risks_by_status},
            "risks_by_type": {risk_type: count for risk_type, count in risks_by_type},
            "high_risks": high_risks,
            "vector_db_stats": vector_service.get_collection_stats("risks")
        }
        
    except Exception as e:
        logger.error(f"Error getting risk stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get risk stats")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
