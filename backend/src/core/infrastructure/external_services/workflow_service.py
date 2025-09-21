"""
Workflow Management Service
FastAPI microservice for GRC Workflow Management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, ForeignKey, JSON, select, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, relationship, Mapped, mapped_column
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import uuid
import logging
import os
from enum import Enum
from ..config.database_config import get_database_url, is_secure_config

logger = logging.getLogger(__name__)

# Database setup with centralized configuration
try:
    DATABASE_URL = get_database_url()
    logger.info("Database configuration loaded successfully")
    
    # Log security status
    if is_secure_config():
        logger.info("Using secure database configuration from environment variables")
    else:
        logger.warning("Using development database configuration. Consider setting DATABASE_URL for production.")
        
except Exception as e:
    logger.error(f"Database configuration error: {e}")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Security
security = HTTPBearer()

# Enums
class WorkflowStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    PAUSED = "PAUSED"

class StepStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"

class WorkflowType(str, Enum):
    POLICY_APPROVAL = "POLICY_APPROVAL"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    COMPLIANCE_AUDIT = "COMPLIANCE_AUDIT"
    INCIDENT_RESPONSE = "INCIDENT_RESPONSE"
    CHANGE_MANAGEMENT = "CHANGE_MANAGEMENT"
    VENDOR_ASSESSMENT = "VENDOR_ASSESSMENT"

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
    workflow_templates: Mapped[List["WorkflowTemplate"]] = relationship("WorkflowTemplate", back_populates="organization")
    workflows: Mapped[List["Workflow"]] = relationship("Workflow", back_populates="organization")

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
    initiated_workflows: Mapped[List["Workflow"]] = relationship("Workflow", foreign_keys="Workflow.initiated_by", back_populates="initiator")
    workflow_assignments: Mapped[List["WorkflowInstance"]] = relationship("WorkflowInstance", back_populates="assignee")

class WorkflowTemplate(Base):
    __tablename__ = "workflow_templates"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    workflow_type: Mapped[str] = mapped_column(String(100), nullable=False)
    steps: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)  # JSON array of step definitions
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="workflow_templates")
    workflows: Mapped[List["Workflow"]] = relationship("Workflow", back_populates="template")

class Workflow(Base):
    __tablename__ = "workflows"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("workflow_templates.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=WorkflowStatus.ACTIVE)
    current_step: Mapped[int] = mapped_column(Integer, default=1)
    context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)  # JSON object for workflow context
    organization_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("organizations.id"))
    initiated_by: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    template: Mapped[Optional["WorkflowTemplate"]] = relationship("WorkflowTemplate", back_populates="workflows")
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="workflows")
    initiator: Mapped[Optional["User"]] = relationship("User", foreign_keys=[initiated_by], back_populates="initiated_workflows")
    instances: Mapped[List["WorkflowInstance"]] = relationship("WorkflowInstance", back_populates="workflow")

class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("workflows.id"))
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    step_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=StepStatus.PENDING)
    assigned_to: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    workflow: Mapped[Optional["Workflow"]] = relationship("Workflow", back_populates="instances")
    assignee: Mapped[Optional["User"]] = relationship("User", back_populates="workflow_assignments")

# Pydantic Models
class WorkflowStep(BaseModel):
    step_number: int
    step_name: str
    description: str
    assigned_role: str
    due_days: int
    is_required: bool = True
    auto_approve: bool = False

class WorkflowTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    workflow_type: WorkflowType
    steps: List[WorkflowStep]

class WorkflowTemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    workflow_type: WorkflowType
    steps: List[Dict[str, Any]]
    organization_id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class WorkflowCreate(BaseModel):
    template_id: str
    name: str = Field(..., min_length=1, max_length=255)
    context: Optional[Dict[str, Any]] = None

class WorkflowResponse(BaseModel):
    id: str
    template_id: str
    name: str
    status: WorkflowStatus
    current_step: int
    context: Optional[Dict[str, Any]]
    organization_id: str
    initiated_by: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class WorkflowInstanceResponse(BaseModel):
    id: str
    workflow_id: str
    step_number: int
    step_name: str
    status: StepStatus
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class WorkflowAction(BaseModel):
    action: str = Field(..., pattern="^(approve|reject|complete|skip|escalate)$")
    notes: Optional[str] = None
    context_updates: Optional[Dict[str, Any]] = None

# FastAPI App
app = FastAPI(
    title="GRC Workflow Management Service",
    description="Microservice for managing GRC workflows and approvals",
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
        "role": "WORKFLOW_MANAGER"
    }

# Workflow Engine Functions
def create_workflow_instances(workflow: Workflow, template: WorkflowTemplate, db: Session):
    """Create workflow instances for each step"""
    instances = []
    for step_data in template.steps:
        instance = WorkflowInstance(
            workflow_id=workflow.id,
            step_number=step_data["step_number"],
            step_name=step_data["step_name"],
            assigned_to=None,  # Will be assigned based on role
            due_date=datetime.utcnow() + timedelta(days=step_data.get("due_days", 7))
        )
        instances.append(instance)
        db.add(instance)
    
    return instances

def get_next_workflow_step(workflow: Workflow, db: Session) -> Optional[WorkflowInstance]:
    """Get the next pending workflow step"""
    stmt = select(WorkflowInstance).where(
        WorkflowInstance.workflow_id == workflow.id,
        WorkflowInstance.status == StepStatus.PENDING
    ).order_by(WorkflowInstance.step_number)
    return db.scalar(stmt)

def complete_workflow_step(workflow_id: str, step_number: int, db: Session) -> bool:
    """Complete a workflow step and move to next"""
    # Mark current step as completed
    stmt = select(WorkflowInstance).where(
        WorkflowInstance.workflow_id == workflow_id,
        WorkflowInstance.step_number == step_number
    )
    current_step = db.scalar(stmt)
    
    if current_step:
        current_step.status = StepStatus.COMPLETED
        current_step.completed_at = datetime.utcnow()
    
    # Check if workflow is complete
    remaining_steps_stmt = select(func.count(WorkflowInstance.id)).where(
        WorkflowInstance.workflow_id == workflow_id,
        WorkflowInstance.status == StepStatus.PENDING
    )
    remaining_steps = db.scalar(remaining_steps_stmt)
    
    if remaining_steps == 0:
        # Workflow is complete
        workflow_stmt = select(Workflow).where(Workflow.id == workflow_id)
        workflow = db.scalar(workflow_stmt)
        if workflow:
            workflow.status = WorkflowStatus.COMPLETED
            workflow.updated_at = datetime.utcnow()
        return True
    
    return False

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "workflow-service"}

@app.post("/templates", response_model=WorkflowTemplateResponse)
async def create_workflow_template(
    template_data: WorkflowTemplateCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new workflow template"""
    try:
        # Convert steps to JSON format
        steps_json = [step.dict() for step in template_data.steps]
        
        # Create template
        template = WorkflowTemplate(
            name=template_data.name,
            description=template_data.description,
            workflow_type=template_data.workflow_type,
            steps=steps_json,
            organization_id=current_user["organization_id"]
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        
        logger.info(f"Workflow template created: {template.id}")
        return template
        
    except Exception as e:
        logger.error(f"Error creating workflow template: {e}")
        raise HTTPException(status_code=500, detail="Failed to create workflow template")

@app.get("/templates", response_model=List[WorkflowTemplateResponse])
async def get_workflow_templates(
    workflow_type: Optional[WorkflowType] = None,
    is_active: bool = True,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow templates"""
    try:
        stmt = select(WorkflowTemplate).where(
            WorkflowTemplate.organization_id == current_user["organization_id"]
        )
        
        if is_active:
            stmt = stmt.where(WorkflowTemplate.is_active == True)
        
        if workflow_type:
            stmt = stmt.where(WorkflowTemplate.workflow_type == workflow_type)
        
        templates = db.scalars(stmt).all()
        return templates
        
    except Exception as e:
        logger.error(f"Error getting workflow templates: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow templates")

@app.get("/templates/{template_id}", response_model=WorkflowTemplateResponse)
async def get_workflow_template(
    template_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific workflow template"""
    try:
        template_stmt = select(WorkflowTemplate).where(
            WorkflowTemplate.id == template_id,
            WorkflowTemplate.organization_id == current_user["organization_id"]
        )
        template = db.scalar(template_stmt)
        
        if not template:
            raise HTTPException(status_code=404, detail="Workflow template not found")
        
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow template: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow template")

@app.post("/workflows", response_model=WorkflowResponse)
async def create_workflow(
    workflow_data: WorkflowCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new workflow instance"""
    try:
        # Verify template exists
        template_stmt = select(WorkflowTemplate).where(
            WorkflowTemplate.id == workflow_data.template_id,
            WorkflowTemplate.organization_id == current_user["organization_id"]
        )
        template = db.scalar(template_stmt)
        
        if not template:
            raise HTTPException(status_code=404, detail="Workflow template not found")
        
        # Create workflow
        workflow = Workflow(
            template_id=workflow_data.template_id,
            name=workflow_data.name,
            context=workflow_data.context or {},
            organization_id=current_user["organization_id"],
            initiated_by=current_user["id"]
        )
        
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        
        # Create workflow instances for each step
        create_workflow_instances(workflow, template, db)
        db.commit()
        
        logger.info(f"Workflow created: {workflow.id}")
        return workflow
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail="Failed to create workflow")

@app.get("/workflows", response_model=List[WorkflowResponse])
async def get_workflows(
    status: Optional[WorkflowStatus] = None,
    workflow_type: Optional[WorkflowType] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflows with filtering"""
    try:
        stmt = select(Workflow).where(
            Workflow.organization_id == current_user["organization_id"]
        )
        
        if status:
            stmt = stmt.where(Workflow.status == status)
        
        if workflow_type:
            stmt = stmt.join(WorkflowTemplate).where(
                WorkflowTemplate.workflow_type == workflow_type
            )
        
        workflows = db.scalars(stmt.offset(offset).limit(limit)).all()
        return workflows
        
    except Exception as e:
        logger.error(f"Error getting workflows: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflows")

@app.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific workflow by ID"""
    try:
        workflow_stmt = select(Workflow).where(
            Workflow.id == workflow_id,
            Workflow.organization_id == current_user["organization_id"]
        )
        workflow = db.scalar(workflow_stmt)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return workflow
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow")

@app.get("/workflows/{workflow_id}/instances", response_model=List[WorkflowInstanceResponse])
async def get_workflow_instances(
    workflow_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow instances for a specific workflow"""
    try:
        # Verify workflow exists and belongs to organization
        workflow_stmt = select(Workflow).where(
            Workflow.id == workflow_id,
            Workflow.organization_id == current_user["organization_id"]
        )
        workflow = db.scalar(workflow_stmt)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        instances_stmt = select(WorkflowInstance).where(
            WorkflowInstance.workflow_id == workflow_id
        ).order_by(WorkflowInstance.step_number)
        instances = db.scalars(instances_stmt).all()
        
        return instances
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow instances: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow instances")

@app.post("/workflows/{workflow_id}/instances/{instance_id}/action")
async def perform_workflow_action(
    workflow_id: str,
    instance_id: str,
    action_data: WorkflowAction,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform an action on a workflow instance"""
    try:
        # Verify workflow exists and belongs to organization
        workflow_stmt = select(Workflow).where(
            Workflow.id == workflow_id,
            Workflow.organization_id == current_user["organization_id"]
        )
        workflow = db.scalar(workflow_stmt)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Get workflow instance
        instance_stmt = select(WorkflowInstance).where(
            WorkflowInstance.id == instance_id,
            WorkflowInstance.workflow_id == workflow_id
        )
        instance = db.scalar(instance_stmt)
        
        if not instance:
            raise HTTPException(status_code=404, detail="Workflow instance not found")
        
        # Perform action
        if action_data.action == "approve":
            instance.status = StepStatus.COMPLETED
            instance.completed_at = datetime.utcnow()
            instance.notes = action_data.notes
            
            # Update workflow context if provided
            if action_data.context_updates:
                workflow.context = (workflow.context or {}) | action_data.context_updates
            
            # Check if workflow is complete
            is_complete = complete_workflow_step(workflow_id, instance.step_number, db)
            
        elif action_data.action == "reject":
            instance.status = StepStatus.FAILED
            instance.notes = action_data.notes
            workflow.status = WorkflowStatus.CANCELLED
            
        elif action_data.action == "skip":
            instance.status = StepStatus.SKIPPED
            instance.notes = action_data.notes
            complete_workflow_step(workflow_id, instance.step_number, db)
            
        elif action_data.action == "escalate":
            instance.notes = f"ESCALATED: {action_data.notes}"
            # In a real system, this would trigger escalation logic
        
        workflow.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Workflow action performed: {action_data.action} on {instance_id}")
        return {
            "message": f"Action '{action_data.action}' performed successfully",
            "workflow_status": workflow.status,
            "instance_status": instance.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing workflow action: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform workflow action")

@app.get("/workflows/my-assignments", response_model=List[WorkflowInstanceResponse])
async def get_my_workflow_assignments(
    status: Optional[StepStatus] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow instances assigned to current user"""
    try:
        stmt = select(WorkflowInstance).where(
            WorkflowInstance.assigned_to == current_user["id"]
        )
        
        if status:
            stmt = stmt.where(WorkflowInstance.status == status)
        
        instances = db.scalars(stmt.order_by(WorkflowInstance.due_date)).all()
        return instances
        
    except Exception as e:
        logger.error(f"Error getting workflow assignments: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow assignments")

@app.get("/workflows/stats")
async def get_workflow_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow statistics"""
    try:
        total_workflows_stmt = select(func.count(Workflow.id)).where(
            Workflow.organization_id == current_user["organization_id"]
        )
        total_workflows = db.scalar(total_workflows_stmt)
        
        # Return empty stats if no data exists
        if total_workflows == 0:
            return {
                "total_workflows": 0,
                "workflows_by_status": {},
                "my_pending_assignments": 0,
                "overdue_assignments": 0,
                "message": "No workflow data available"
            }
        
        workflows_by_status_stmt = select(
            Workflow.status,
            func.count(Workflow.id)
        ).where(
            Workflow.organization_id == current_user["organization_id"]
        ).group_by(Workflow.status)
        workflows_by_status_result = db.execute(workflows_by_status_stmt)
        workflows_by_status = workflows_by_status_result.all()
        
        my_pending_assignments_stmt = select(func.count(WorkflowInstance.id)).where(
            WorkflowInstance.assigned_to == current_user["id"],
            WorkflowInstance.status == StepStatus.PENDING
        )
        my_pending_assignments = db.scalar(my_pending_assignments_stmt)
        
        overdue_assignments_stmt = select(func.count(WorkflowInstance.id)).where(
            WorkflowInstance.assigned_to == current_user["id"],
            WorkflowInstance.status == StepStatus.PENDING,
            WorkflowInstance.due_date < datetime.utcnow()
        )
        overdue_assignments = db.scalar(overdue_assignments_stmt)
        
        return {
            "total_workflows": total_workflows,
            "workflows_by_status": {status: count for status, count in workflows_by_status},
            "my_pending_assignments": my_pending_assignments,
            "overdue_assignments": overdue_assignments
        }
        
    except Exception as e:
        logger.error(f"Error getting workflow stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow stats")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
