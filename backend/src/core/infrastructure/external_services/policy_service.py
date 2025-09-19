"""
Policy Management Service
FastAPI microservice for GRC Policy Management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field
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
class PolicyStatus(str, Enum):
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class PolicyCategory(str, Enum):
    INFORMATION_SECURITY = "INFORMATION_SECURITY"
    HUMAN_RESOURCES = "HUMAN_RESOURCES"
    FINANCIAL = "FINANCIAL"
    OPERATIONAL = "OPERATIONAL"
    COMPLIANCE = "COMPLIANCE"

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

class PolicyCategory(Base):
    __tablename__ = "policy_categories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    organization_id = Column(String, ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", backref="policy_categories")

class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    version = Column(String(20), nullable=False, default="1.0")
    status = Column(String(50), nullable=False, default=PolicyStatus.DRAFT)
    category_id = Column(String, ForeignKey("policy_categories.id"))
    organization_id = Column(String, ForeignKey("organizations.id"))
    created_by = Column(String, ForeignKey("users.id"))
    approved_by = Column(String, ForeignKey("users.id"))
    effective_date = Column(DateTime)
    review_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = relationship("PolicyCategory", backref="policies")
    organization = relationship("Organization", backref="policies")
    creator = relationship("User", foreign_keys=[created_by], backref="created_policies")
    approver = relationship("User", foreign_keys=[approved_by], backref="approved_policies")

# Pydantic Models
class PolicyCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = None
    category_id: Optional[str] = None
    effective_date: Optional[date] = None
    review_date: Optional[date] = None

class PolicyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None
    status: Optional[PolicyStatus] = None
    category_id: Optional[str] = None
    effective_date: Optional[date] = None
    review_date: Optional[date] = None

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

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Simplified authentication - in production, implement proper JWT validation
    return {
        "id": "user-123",
        "organization_id": "org-123",
        "role": "ADMIN"
    }

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "policy-service"}

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
        query = db.query(Policy)
        
        # Filter by organization
        if organization_id:
            query = query.filter(Policy.organization_id == organization_id)
        else:
            query = query.filter(Policy.organization_id == current_user["organization_id"])
        
        # Filter by status
        if status:
            query = query.filter(Policy.status == status)
        
        # Filter by category
        if category_id:
            query = query.filter(Policy.category_id == category_id)
        
        # Apply pagination
        policies = query.offset(offset).limit(limit).all()
        
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
        policy = db.query(Policy).filter(
            Policy.id == policy_id,
            Policy.organization_id == current_user["organization_id"]
        ).first()
        
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
        policy = db.query(Policy).filter(
            Policy.id == policy_id,
            Policy.organization_id == current_user["organization_id"]
        ).first()
        
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
        policy = db.query(Policy).filter(
            Policy.id == policy_id,
            Policy.organization_id == current_user["organization_id"]
        ).first()
        
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
        search_results = vector_service.search_similar_documents(
            query=search_request.query,
            collection_type="policies",
            n_results=search_request.limit,
            organization_id=current_user["organization_id"],
            filters={
                "category": search_request.category,
                "status": search_request.status
            } if search_request.category or search_request.status else None
        )
        
        # Format results
        policies = []
        for result in search_results:
            policies.append({
                "id": result["metadata"].get("policy_id"),
                "title": result["metadata"].get("title"),
                "content": result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"],
                "metadata": result["metadata"],
                "similarity_score": 1 - result["distance"] if result["distance"] else 0
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
        categories = db.query(PolicyCategory).filter(
            PolicyCategory.organization_id == current_user["organization_id"]
        ).all()
        
        return [{"id": cat.id, "name": cat.name, "description": cat.description} for cat in categories]
        
    except Exception as e:
        logger.error(f"Error getting policy categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get policy categories")

@app.get("/policies/stats")
async def get_policy_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get policy statistics with mock data fallback"""
    try:
        total_policies = db.query(Policy).filter(
            Policy.organization_id == current_user["organization_id"]
        ).count()
        
        policies_by_status = db.query(
            Policy.status,
            db.func.count(Policy.id)
        ).filter(
            Policy.organization_id == current_user["organization_id"]
        ).group_by(Policy.status).all()
        
        # If no data exists, return mock data
        if total_policies == 0:
            return {
                "total_policies": 25,
                "policies_by_status": {
                    "Active": 18,
                    "Under Review": 4,
                    "Draft": 2,
                    "Archived": 1
                },
                "policies_by_category": {
                    "Information Security": 6,
                    "Compliance": 5,
                    "Risk Management": 4,
                    "Operational": 4,
                    "Financial": 3,
                    "Human Resources": 3
                },
                "recent_policies": 3,
                "policies_due_for_review": 2,
                "mock_data": True
            }
        
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
