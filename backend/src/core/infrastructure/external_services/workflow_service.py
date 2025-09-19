"""
Workflow Management Service
FastAPI microservice for GRC Workflow Management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import uuid
import logging
from enum import Enum

logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = "postgresql://grc_user:grc_password@localhost:5432/grc_platform"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

class WorkflowTemplate(Base):
    __tablename__ = "workflow_templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    workflow_type = Column(String(100), nullable=False)
    steps = Column(JSON, nullable=False)  # JSON array of step definitions
    organization_id = Column(String, ForeignKey("organizations.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", backref="workflow_templates")

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id = Column(String, ForeignKey("workflow_templates.id"))
    name = Column(String(255), nullable=False)
    status = Column(String(50), default=WorkflowStatus.ACTIVE)
    current_step = Column(Integer, default=1)
    context = Column(JSON)  # JSON object for workflow context
    organization_id = Column(String, ForeignKey("organizations.id"))
    initiated_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    template = relationship("WorkflowTemplate", backref="workflows")
    organization = relationship("Organization", backref="workflows")
    initiator = relationship("User", backref="initiated_workflows")

class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id"))
    step_number = Column(Integer, nullable=False)
    step_name = Column(String(255), nullable=False)
    status = Column(String(50), default=StepStatus.PENDING)
    assigned_to = Column(String, ForeignKey("users.id"))
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", backref="instances")
    assignee = relationship("User", backref="workflow_assignments")

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
    return db.query(WorkflowInstance).filter(
        WorkflowInstance.workflow_id == workflow.id,
        WorkflowInstance.status == StepStatus.PENDING
    ).order_by(WorkflowInstance.step_number).first()

def complete_workflow_step(workflow_id: str, step_number: int, db: Session) -> bool:
    """Complete a workflow step and move to next"""
    # Mark current step as completed
    current_step = db.query(WorkflowInstance).filter(
        WorkflowInstance.workflow_id == workflow_id,
        WorkflowInstance.step_number == step_number
    ).first()
    
    if current_step:
        current_step.status = StepStatus.COMPLETED
        current_step.completed_at = datetime.utcnow()
    
    # Check if workflow is complete
    remaining_steps = db.query(WorkflowInstance).filter(
        WorkflowInstance.workflow_id == workflow_id,
        WorkflowInstance.status == StepStatus.PENDING
    ).count()
    
    if remaining_steps == 0:
        # Workflow is complete
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
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
        query = db.query(WorkflowTemplate).filter(
            WorkflowTemplate.organization_id == current_user["organization_id"]
        )
        
        if is_active:
            query = query.filter(WorkflowTemplate.is_active == True)
        
        if workflow_type:
            query = query.filter(WorkflowTemplate.workflow_type == workflow_type)
        
        templates = query.all()
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
        template = db.query(WorkflowTemplate).filter(
            WorkflowTemplate.id == template_id,
            WorkflowTemplate.organization_id == current_user["organization_id"]
        ).first()
        
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
        template = db.query(WorkflowTemplate).filter(
            WorkflowTemplate.id == workflow_data.template_id,
            WorkflowTemplate.organization_id == current_user["organization_id"]
        ).first()
        
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
        query = db.query(Workflow).filter(
            Workflow.organization_id == current_user["organization_id"]
        )
        
        if status:
            query = query.filter(Workflow.status == status)
        
        if workflow_type:
            query = query.join(WorkflowTemplate).filter(
                WorkflowTemplate.workflow_type == workflow_type
            )
        
        workflows = query.offset(offset).limit(limit).all()
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
        workflow = db.query(Workflow).filter(
            Workflow.id == workflow_id,
            Workflow.organization_id == current_user["organization_id"]
        ).first()
        
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
        workflow = db.query(Workflow).filter(
            Workflow.id == workflow_id,
            Workflow.organization_id == current_user["organization_id"]
        ).first()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        instances = db.query(WorkflowInstance).filter(
            WorkflowInstance.workflow_id == workflow_id
        ).order_by(WorkflowInstance.step_number).all()
        
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
        workflow = db.query(Workflow).filter(
            Workflow.id == workflow_id,
            Workflow.organization_id == current_user["organization_id"]
        ).first()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Get workflow instance
        instance = db.query(WorkflowInstance).filter(
            WorkflowInstance.id == instance_id,
            WorkflowInstance.workflow_id == workflow_id
        ).first()
        
        if not instance:
            raise HTTPException(status_code=404, detail="Workflow instance not found")
        
        # Perform action
        if action_data.action == "approve":
            instance.status = StepStatus.COMPLETED
            instance.completed_at = datetime.utcnow()
            instance.notes = action_data.notes
            
            # Update workflow context if provided
            if action_data.context_updates:
                workflow.context = {**(workflow.context or {}), **action_data.context_updates}
            
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
        query = db.query(WorkflowInstance).filter(
            WorkflowInstance.assigned_to == current_user["id"]
        )
        
        if status:
            query = query.filter(WorkflowInstance.status == status)
        
        instances = query.order_by(WorkflowInstance.due_date).all()
        return instances
        
    except Exception as e:
        logger.error(f"Error getting workflow assignments: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow assignments")

@app.get("/workflows/stats")
async def get_workflow_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow statistics with mock data fallback"""
    try:
        total_workflows = db.query(Workflow).filter(
            Workflow.organization_id == current_user["organization_id"]
        ).count()
        
        # If no data exists, return mock data
        if total_workflows == 0:
            return {
                "total_workflows": 32,
                "workflows_by_status": {
                    "Active": 25,
                    "Completed": 5,
                    "Pending": 2
                },
                "workflows_by_priority": {
                    "High": 12,
                    "Medium": 15,
                    "Low": 5
                },
                "my_pending_assignments": 8,
                "overdue_assignments": 3,
                "completed_this_month": 15,
                "workflow_efficiency": 78.5,
                "mock_data": True
            }
        
        workflows_by_status = db.query(
            Workflow.status,
            db.func.count(Workflow.id)
        ).filter(
            Workflow.organization_id == current_user["organization_id"]
        ).group_by(Workflow.status).all()
        
        my_pending_assignments = db.query(WorkflowInstance).filter(
            WorkflowInstance.assigned_to == current_user["id"],
            WorkflowInstance.status == StepStatus.PENDING
        ).count()
        
        overdue_assignments = db.query(WorkflowInstance).filter(
            WorkflowInstance.assigned_to == current_user["id"],
            WorkflowInstance.status == StepStatus.PENDING,
            WorkflowInstance.due_date < datetime.utcnow()
        ).count()
        
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
    from datetime import timedelta
    uvicorn.run(app, host="0.0.0.0", port=8004)
