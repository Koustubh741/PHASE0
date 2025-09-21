"""
Workflow Data Transfer Objects
DTOs for workflow management operations
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...application.services.workflow_service import Workflow, WorkflowStep, WorkflowStatus, WorkflowType, ApprovalLevel


class WorkflowCreateRequest(BaseModel):
    """Workflow creation request DTO"""
    workflow_type: str = Field(..., description="Type of workflow")
    entity_id: str = Field(..., description="ID of entity being processed")
    entity_type: str = Field(..., description="Type of entity")
    entity_title: str = Field(..., description="Title of entity")
    priority: str = Field(default="medium", description="Workflow priority")
    due_date: Optional[datetime] = Field(None, description="Workflow due date")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('workflow_type')
    def validate_workflow_type(cls, v):
        valid_types = [wt.value for wt in WorkflowType]
        if v not in valid_types:
            raise ValueError(f'Workflow type must be one of: {", ".join(valid_types)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ["low", "medium", "high", "critical"]
        if v not in valid_priorities:
            raise ValueError(f'Priority must be one of: {", ".join(valid_priorities)}')
        return v


class WorkflowStepResponse(BaseModel):
    """Workflow step response DTO"""
    step_id: str = Field(..., description="Step ID")
    step_name: str = Field(..., description="Step name")
    approver_role: str = Field(..., description="Approver role")
    approval_level: str = Field(..., description="Approval level")
    is_required: bool = Field(..., description="Whether step is required")
    auto_approve: bool = Field(..., description="Whether step auto-approves")
    escalation_hours: Optional[int] = Field(None, description="Escalation hours")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    approved_by: Optional[str] = Field(None, description="Approver user ID")
    comments: Optional[str] = Field(None, description="Approval comments")
    status: str = Field(..., description="Step status")


class WorkflowResponse(BaseModel):
    """Workflow response DTO"""
    id: UUID = Field(..., description="Workflow ID")
    workflow_type: str = Field(..., description="Workflow type")
    entity_id: str = Field(..., description="Entity ID")
    entity_type: str = Field(..., description="Entity type")
    initiated_by: str = Field(..., description="Initiator user ID")
    organization_id: str = Field(..., description="Organization ID")
    steps: List[WorkflowStepResponse] = Field(..., description="Workflow steps")
    priority: str = Field(..., description="Workflow priority")
    due_date: Optional[datetime] = Field(None, description="Due date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    status: str = Field(..., description="Workflow status")
    current_step_index: int = Field(..., description="Current step index")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    metadata: Dict[str, Any] = Field(..., description="Workflow metadata")
    
    @classmethod
    def from_workflow(cls, workflow: Workflow) -> "WorkflowResponse":
        """Create WorkflowResponse from Workflow entity"""
        return cls(
            id=workflow.id,
            workflow_type=workflow.workflow_type.value,
            entity_id=workflow.entity_id,
            entity_type=workflow.entity_type,
            initiated_by=workflow.initiated_by,
            organization_id=workflow.organization_id,
            steps=[
                WorkflowStepResponse(
                    step_id=step.step_id,
                    step_name=step.step_name,
                    approver_role=step.approver_role,
                    approval_level=step.approval_level.value,
                    is_required=step.is_required,
                    auto_approve=step.auto_approve,
                    escalation_hours=step.escalation_hours,
                    completed_at=step.completed_at,
                    approved_by=step.approved_by,
                    comments=step.comments,
                    status=step.status.value
                )
                for step in workflow.steps
            ],
            priority=workflow.priority,
            due_date=workflow.due_date,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at,
            status=workflow.status.value,
            current_step_index=workflow.current_step_index,
            completed_at=workflow.completed_at,
            metadata=workflow.metadata
        )


class WorkflowStatusResponse(BaseModel):
    """Workflow status response DTO"""
    workflow_id: str = Field(..., description="Workflow ID")
    workflow_type: str = Field(..., description="Workflow type")
    status: str = Field(..., description="Workflow status")
    entity_id: str = Field(..., description="Entity ID")
    entity_type: str = Field(..., description="Entity type")
    initiated_by: str = Field(..., description="Initiator user ID")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    due_date: Optional[str] = Field(None, description="Due date")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    current_step: Optional[Dict[str, Any]] = Field(None, description="Current step information")
    escalated_steps: List[str] = Field(..., description="List of escalated step IDs")
    is_expired: bool = Field(..., description="Whether workflow is expired")
    priority: str = Field(..., description="Workflow priority")
    metadata: Dict[str, Any] = Field(..., description="Workflow metadata")


class WorkflowListResponse(BaseModel):
    """Workflow list response DTO"""
    workflows: List[WorkflowStatusResponse] = Field(..., description="List of workflows")
    total: int = Field(..., description="Total number of workflows")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum number of records")


class WorkflowApprovalRequest(BaseModel):
    """Workflow approval request DTO"""
    comments: str = Field(default="", description="Approval comments")


class WorkflowRejectionRequest(BaseModel):
    """Workflow rejection request DTO"""
    reason: str = Field(..., min_length=1, description="Rejection reason")


class WorkflowEscalationRequest(BaseModel):
    """Workflow escalation request DTO"""
    reason: str = Field(..., min_length=1, description="Escalation reason")


class WorkflowStatisticsResponse(BaseModel):
    """Workflow statistics response DTO"""
    total_workflows: int = Field(..., description="Total number of workflows")
    pending_workflows: int = Field(..., description="Number of pending workflows")
    completed_workflows: int = Field(..., description="Number of completed workflows")
    escalated_workflows: int = Field(..., description="Number of escalated workflows")
    expired_workflows: int = Field(..., description="Number of expired workflows")
    workflows_by_type: Dict[str, int] = Field(..., description="Workflow count by type")
    workflows_by_status: Dict[str, int] = Field(..., description="Workflow count by status")
    average_completion_time: int = Field(..., description="Average completion time in hours")
    workflow_success_rate: float = Field(..., description="Workflow success rate (0.0-1.0)")


class WorkflowTemplateRequest(BaseModel):
    """Workflow template request DTO"""
    template_name: str = Field(..., description="Template name")
    workflow_type: str = Field(..., description="Workflow type")
    steps: List[Dict[str, Any]] = Field(..., description="Workflow steps definition")
    default_priority: str = Field(default="medium", description="Default priority")
    default_due_days: int = Field(default=7, description="Default due days")


class WorkflowTemplateResponse(BaseModel):
    """Workflow template response DTO"""
    id: str = Field(..., description="Template ID")
    template_name: str = Field(..., description="Template name")
    workflow_type: str = Field(..., description="Workflow type")
    steps: List[WorkflowStepResponse] = Field(..., description="Template steps")
    default_priority: str = Field(..., description="Default priority")
    default_due_days: int = Field(..., description="Default due days")
    is_active: bool = Field(..., description="Whether template is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class WorkflowBulkActionRequest(BaseModel):
    """Workflow bulk action request DTO"""
    workflow_ids: List[UUID] = Field(..., min_items=1, description="List of workflow IDs")
    action: str = Field(..., description="Action to perform")
    reason: str = Field(..., min_length=1, description="Reason for action")
    
    @validator('action')
    def validate_action(cls, v):
        valid_actions = ["approve", "reject", "escalate", "cancel"]
        if v not in valid_actions:
            raise ValueError(f'Action must be one of: {", ".join(valid_actions)}')
        return v


class WorkflowNotificationRequest(BaseModel):
    """Workflow notification request DTO"""
    workflow_id: UUID = Field(..., description="Workflow ID")
    notification_type: str = Field(..., description="Notification type")
    recipients: List[str] = Field(..., description="List of recipient user IDs")
    message: str = Field(..., description="Notification message")
    
    @validator('notification_type')
    def validate_notification_type(cls, v):
        valid_types = ["approval_required", "workflow_completed", "escalation", "reminder"]
        if v not in valid_types:
            raise ValueError(f'Notification type must be one of: {", ".join(valid_types)}')
        return v


class WorkflowAuditRequest(BaseModel):
    """Workflow audit request DTO"""
    workflow_id: UUID = Field(..., description="Workflow ID")
    audit_type: str = Field(..., description="Audit type")
    include_steps: bool = Field(default=True, description="Include step details")
    include_metadata: bool = Field(default=True, description="Include metadata")
    
    @validator('audit_type')
    def validate_audit_type(cls, v):
        valid_types = ["full", "summary", "steps_only"]
        if v not in valid_types:
            raise ValueError(f'Audit type must be one of: {", ".join(valid_types)}')
        return v
