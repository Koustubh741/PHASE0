"""
Workflow Automation Data Transfer Objects
DTOs for workflow automation operations
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class TriggerType(str, Enum):
    """Trigger type enumeration"""
    SCHEDULED = "scheduled"
    EVENT_BASED = "event_based"
    THRESHOLD = "threshold"
    CONDITIONAL = "conditional"
    EXTERNAL = "external"
    AI_POWERED = "ai_powered"


class ActionType(str, Enum):
    """Action type enumeration"""
    NOTIFICATION = "notification"
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    TEAMS = "teams"
    WEBHOOK = "webhook"
    DATABASE_UPDATE = "database_update"
    API_CALL = "api_call"
    WORKFLOW_START = "workflow_start"
    WORKFLOW_STOP = "workflow_stop"
    ESCALATION = "escalation"
    REPORT_GENERATION = "report_generation"
    AI_ANALYSIS = "ai_analysis"


class WorkflowStatus(str, Enum):
    """Workflow status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionStatus(str, Enum):
    """Execution status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class WorkflowCreateRequest(BaseModel):
    """Request to create a new workflow"""
    template_id: str = Field(..., description="Template ID to use")
    name: str = Field(..., description="Workflow name")
    description: str = Field("", description="Workflow description")
    customizations: Dict[str, Any] = Field(default_factory=dict, description="Customizations to apply")
    
    class Config:
        json_schema_extra = {
            "example": {
                "template_id": "risk-alert-workflow",
                "name": "Credit Risk Alert Workflow",
                "description": "Automated credit risk alert and escalation",
                "customizations": {
                    "risk_threshold": 0.85,
                    "escalation_levels": 2,
                    "notification_channels": ["email", "slack"]
                }
            }
        }


class WorkflowResponse(BaseModel):
    """Workflow response"""
    workflow_id: str = Field(..., description="Workflow ID")
    template_id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Workflow name")
    description: str = Field(..., description="Workflow description")
    status: WorkflowStatus = Field(..., description="Workflow status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    customizations: Dict[str, Any] = Field(default_factory=dict, description="Customizations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "123e4567-e89b-12d3-a456-426614174000",
                "template_id": "risk-alert-workflow",
                "name": "Credit Risk Alert Workflow",
                "description": "Automated credit risk alert and escalation",
                "status": "active",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "customizations": {
                    "risk_threshold": 0.85,
                    "escalation_levels": 2
                }
            }
        }


class TriggerCreateRequest(BaseModel):
    """Request to create a custom trigger"""
    name: str = Field(..., description="Trigger name")
    description: str = Field("", description="Trigger description")
    trigger_type: TriggerType = Field(..., description="Trigger type")
    conditions: Dict[str, Any] = Field(..., description="Trigger conditions")
    actions: List[str] = Field(..., description="Actions to execute")
    priority: int = Field(1, description="Trigger priority")
    enabled: bool = Field(True, description="Whether trigger is enabled")
    ai_powered: bool = Field(False, description="Whether trigger uses AI")
    ml_model: Optional[str] = Field(None, description="Machine learning model")
    confidence_threshold: float = Field(0.8, description="Confidence threshold for AI triggers")
    context_variables: Dict[str, Any] = Field(default_factory=dict, description="Context variables")
    escalation_rules: Dict[str, Any] = Field(default_factory=dict, description="Escalation rules")
    retry_policy: Dict[str, Any] = Field(default_factory=dict, description="Retry policy")
    timeout_seconds: int = Field(300, description="Timeout in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TriggerResponse(BaseModel):
    """Trigger response"""
    trigger_id: str = Field(..., description="Trigger ID")
    name: str = Field(..., description="Trigger name")
    description: str = Field(..., description="Trigger description")
    trigger_type: TriggerType = Field(..., description="Trigger type")
    conditions: Dict[str, Any] = Field(..., description="Trigger conditions")
    actions: List[str] = Field(..., description="Actions to execute")
    priority: int = Field(..., description="Trigger priority")
    enabled: bool = Field(..., description="Whether trigger is enabled")
    ai_powered: bool = Field(..., description="Whether trigger uses AI")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ExecutionRequest(BaseModel):
    """Request to execute a workflow"""
    workflow_id: str = Field(..., description="Workflow ID to execute")
    trigger_id: str = Field(..., description="Trigger ID that initiated execution")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input data for execution")


class ExecutionResponse(BaseModel):
    """Execution response"""
    execution_id: str = Field(..., description="Execution ID")
    workflow_id: str = Field(..., description="Workflow ID")
    trigger_id: str = Field(..., description="Trigger ID")
    status: ExecutionStatus = Field(..., description="Execution status")
    started_at: datetime = Field(..., description="Start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    duration_seconds: Optional[float] = Field(None, description="Execution duration")
    input_data: Dict[str, Any] = Field(..., description="Input data")
    output_data: Dict[str, Any] = Field(default_factory=dict, description="Output data")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    retry_count: int = Field(0, description="Number of retries")


class WorkflowTemplateResponse(BaseModel):
    """Workflow template response"""
    template_id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    category: str = Field(..., description="Template category")
    version: str = Field(..., description="Template version")
    created_by: str = Field(..., description="Template creator")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    usage_count: int = Field(..., description="Usage count")
    rating: float = Field(..., description="Template rating")
    tags: List[str] = Field(..., description="Template tags")


class PerformanceMetricsResponse(BaseModel):
    """Performance metrics response"""
    total_workflows: int = Field(..., description="Total number of workflows")
    active_workflows: int = Field(..., description="Number of active workflows")
    total_executions: int = Field(..., description="Total number of executions")
    successful_executions: int = Field(..., description="Number of successful executions")
    failed_executions: int = Field(..., description="Number of failed executions")
    average_execution_time: float = Field(..., description="Average execution time")
    ai_powered_triggers: int = Field(..., description="Number of AI-powered triggers")
    automation_savings: float = Field(..., description="Automation savings in hours")
    active_triggers: int = Field(..., description="Number of active triggers")
    pending_executions: int = Field(..., description="Number of pending executions")
    execution_threads: int = Field(..., description="Number of execution threads")
    last_updated: str = Field(..., description="Last update timestamp")