"""
Compliance Management Service
FastAPI microservice for GRC Compliance Management
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

class ComplianceFramework(Base):
    __tablename__ = "compliance_frameworks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    version = Column(String(50))
    industry = Column(String(100))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ComplianceRequirement(Base):
    __tablename__ = "compliance_requirements"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    framework_id = Column(String, ForeignKey("compliance_frameworks.id"))
    requirement_code = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100))
    priority = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    framework = relationship("ComplianceFramework", backref="requirements")

class ComplianceAssessment(Base):
    __tablename__ = "compliance_assessments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey("organizations.id"))
    framework_id = Column(String, ForeignKey("compliance_frameworks.id"))
    assessment_date = Column(DateTime, nullable=False)
    assessor_id = Column(String, ForeignKey("users.id"))
    status = Column(String(50), default=ComplianceStatus.IN_PROGRESS)
    overall_score = Column(DECIMAL(5, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    organization = relationship("Organization", backref="compliance_assessments")
    framework = relationship("ComplianceFramework", backref="assessments")
    assessor = relationship("User", backref="compliance_assessments")

class ComplianceEvidence(Base):
    __tablename__ = "compliance_evidence"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("compliance_assessments.id"))
    requirement_id = Column(String, ForeignKey("compliance_requirements.id"))
    evidence_type = Column(String(50))
    evidence_description = Column(Text)
    file_path = Column(String(500))
    is_compliant = Column(Boolean)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assessment = relationship("ComplianceAssessment", backref="evidence")
    requirement = relationship("ComplianceRequirement", backref="evidence")

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
    # Simplified authentication - in production, implement proper JWT validation
    return {
        "id": "user-123",
        "organization_id": "org-123",
        "role": "COMPLIANCE_OFFICER"
    }

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
        query = db.query(ComplianceFramework)
        
        if is_active:
            query = query.filter(ComplianceFramework.is_active == True)
        
        if industry:
            query = query.filter(ComplianceFramework.industry == industry)
        
        frameworks = query.all()
        
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
        query = db.query(ComplianceRequirement).filter(
            ComplianceRequirement.framework_id == framework_id
        )
        
        if category:
            query = query.filter(ComplianceRequirement.category == category)
        
        requirements = query.all()
        
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
        framework = db.query(ComplianceFramework).filter(
            ComplianceFramework.id == assessment_data.framework_id
        ).first()
        
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
        query = db.query(ComplianceAssessment)
        
        # Filter by organization
        if organization_id:
            query = query.filter(ComplianceAssessment.organization_id == organization_id)
        else:
            query = query.filter(ComplianceAssessment.organization_id == current_user["organization_id"])
        
        # Filter by framework
        if framework_id:
            query = query.filter(ComplianceAssessment.framework_id == framework_id)
        
        # Filter by status
        if status:
            query = query.filter(ComplianceAssessment.status == status)
        
        # Apply pagination
        assessments = query.offset(offset).limit(limit).all()
        
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
        assessment = db.query(ComplianceAssessment).filter(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).first()
        
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
        assessment = db.query(ComplianceAssessment).filter(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).first()
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Compliance assessment not found")
        
        # Update fields
        update_data = assessment_data.dict(exclude_unset=True)
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
        assessment = db.query(ComplianceAssessment).filter(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).first()
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Compliance assessment not found")
        
        # Verify requirement exists
        requirement = db.query(ComplianceRequirement).filter(
            ComplianceRequirement.id == evidence_data.requirement_id
        ).first()
        
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
        assessment = db.query(ComplianceAssessment).filter(
            ComplianceAssessment.id == assessment_id,
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).first()
        
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
        search_results = vector_service.search_similar_documents(
            query=search_request.query,
            collection_type="compliance",
            n_results=search_request.limit,
            organization_id=current_user["organization_id"],
            filters={
                "framework": search_request.framework_id,
                "status": search_request.status
            } if search_request.framework_id or search_request.status else None
        )
        
        # Format results
        results = []
        for result in search_results:
            results.append({
                "id": result["metadata"].get("compliance_id"),
                "title": result["metadata"].get("title"),
                "content": result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"],
                "metadata": result["metadata"],
                "similarity_score": 1 - result["distance"] if result["distance"] else 0
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
    """Get compliance statistics with mock data fallback"""
    try:
        total_assessments = db.query(ComplianceAssessment).filter(
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).count()
        
        # If no data exists, return mock data
        if total_assessments == 0:
            return {
                "total_assessments": 24,
                "assessments_by_status": {
                    "Completed": 15,
                    "In Progress": 6,
                    "Pending": 3
                },
                "assessments_by_framework": {
                    "ISO 27001": 4,
                    "SOX": 3,
                    "HIPAA": 3,
                    "GDPR": 3,
                    "NIST CSF": 3,
                    "Basel III": 2,
                    "FDA 21 CFR": 2,
                    "OSHA": 2,
                    "FCC": 2
                },
                "average_compliance_score": 82.5,
                "compliance_trend": "Improving",
                "overdue_assessments": 2,
                "mock_data": True
            }
        
        assessments_by_status = db.query(
            ComplianceAssessment.status,
            db.func.count(ComplianceAssessment.id)
        ).filter(
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).group_by(ComplianceAssessment.status).all()
        
        assessments_by_framework = db.query(
            ComplianceFramework.name,
            db.func.count(ComplianceAssessment.id)
        ).join(ComplianceAssessment).filter(
            ComplianceAssessment.organization_id == current_user["organization_id"]
        ).group_by(ComplianceFramework.name).all()
        
        avg_compliance_score = db.query(
            db.func.avg(ComplianceAssessment.overall_score)
        ).filter(
            ComplianceAssessment.organization_id == current_user["organization_id"],
            ComplianceAssessment.overall_score.isnot(None)
        ).scalar() or 0
        
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
