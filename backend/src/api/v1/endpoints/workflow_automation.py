"""
Workflow Automation API Endpoints
RESTful API endpoints for workflow automation service
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from ...core.application.services.workflow_automation_service import (
    WorkflowAutomationService,
    WorkflowTemplate,
    WorkflowTrigger,
    WorkflowAction,
    WorkflowExecution,
    TriggerType,
    ActionType,
    WorkflowStatus,
    ExecutionStatus
)
from ...core.application.dto.workflow_dto import (
    WorkflowCreateRequest,
    WorkflowResponse,
    TriggerCreateRequest,
    TriggerResponse,
    ExecutionRequest,
    ExecutionResponse,
    WorkflowTemplateResponse,
    PerformanceMetricsResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/workflow-automation", tags=["Workflow Automation"])

# Global service instance
workflow_service = WorkflowAutomationService()

@router.on_event("startup")
async def startup_event():
    """Initialize workflow automation service on startup"""
    await workflow_service.start_execution_engine()
    logger.info("Workflow automation service started")

@router.get("/templates", response_model=List[WorkflowTemplateResponse])
async def get_workflow_templates():
    """Get all available workflow templates"""
    try:
        templates = workflow_service.get_workflow_templates()
        return templates
    except Exception as e:
        logger.error(f"Error getting workflow templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/{template_id}", response_model=WorkflowTemplateResponse)
async def get_workflow_template(template_id: str):
    """Get specific workflow template"""
    try:
        templates = workflow_service.get_workflow_templates()
        template = next((t for t in templates if t["template_id"] == template_id), None)
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow template: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflows", response_model=WorkflowResponse)
async def create_workflow(request: WorkflowCreateRequest):
    """Create a new workflow from template"""
    try:
        workflow_id = await workflow_service.create_workflow(
            template_id=request.template_id,
            customizations=request.customizations
        )
        
        return WorkflowResponse(
            workflow_id=workflow_id,
            template_id=request.template_id,
            name=request.name,
            description=request.description,
            status=WorkflowStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            customizations=request.customizations
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    """Get workflow details"""
    try:
        templates = workflow_service.get_workflow_templates()
        workflow = next((t for t in templates if t["template_id"] == workflow_id), None)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return WorkflowResponse(
            workflow_id=workflow_id,
            template_id=workflow["template_id"],
            name=workflow["name"],
            description=workflow["description"],
            status=WorkflowStatus.ACTIVE,
            created_at=workflow["created_at"],
            updated_at=workflow["updated_at"],
            customizations=workflow.get("customizations", {})
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/triggers", response_model=TriggerResponse)
async def create_trigger(request: TriggerCreateRequest):
    """Create a custom trigger"""
    try:
        trigger_id = workflow_service.create_custom_trigger(
            name=request.name,
            trigger_type=TriggerType(request.trigger_type),
            conditions=request.conditions,
            actions=request.actions,
            ai_powered=request.ai_powered,
            description=request.description,
            priority=request.priority,
            enabled=request.enabled,
            ml_model=request.ml_model,
            confidence_threshold=request.confidence_threshold,
            context_variables=request.context_variables,
            escalation_rules=request.escalation_rules,
            retry_policy=request.retry_policy,
            timeout_seconds=request.timeout_seconds,
            metadata=request.metadata
        )
        
        return TriggerResponse(
            trigger_id=trigger_id,
            name=request.name,
            description=request.description,
            trigger_type=request.trigger_type,
            conditions=request.conditions,
            actions=request.actions,
            priority=request.priority,
            enabled=request.enabled,
            ai_powered=request.ai_powered,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error creating trigger: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/triggers", response_model=List[TriggerResponse])
async def get_active_triggers():
    """Get all active triggers"""
    try:
        triggers = workflow_service.get_active_triggers()
        return triggers
    except Exception as e:
        logger.error(f"Error getting active triggers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/triggers/{trigger_id}", response_model=TriggerResponse)
async def get_trigger(trigger_id: str):
    """Get specific trigger"""
    try:
        triggers = workflow_service.get_active_triggers()
        trigger = next((t for t in triggers if t["trigger_id"] == trigger_id), None)
        
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        
        return trigger
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trigger: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/triggers/{trigger_id}/test")
async def test_trigger(trigger_id: str, test_data: Dict[str, Any]):
    """Test a trigger with sample data"""
    try:
        result = await workflow_service.test_trigger(trigger_id, test_data)
        return result
    except Exception as e:
        logger.error(f"Error testing trigger: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/executions", response_model=ExecutionResponse)
async def execute_workflow(request: ExecutionRequest):
    """Execute a workflow"""
    try:
        execution_id = await workflow_service.execute_workflow(
            workflow_id=request.workflow_id,
            trigger_id=request.trigger_id,
            input_data=request.input_data
        )
        
        return ExecutionResponse(
            execution_id=execution_id,
            workflow_id=request.workflow_id,
            trigger_id=request.trigger_id,
            status=ExecutionStatus.PENDING,
            started_at=datetime.utcnow(),
            input_data=request.input_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/executions", response_model=List[ExecutionResponse])
async def get_execution_history(workflow_id: Optional[str] = None):
    """Get execution history"""
    try:
        executions = workflow_service.get_execution_history(workflow_id)
        return executions
    except Exception as e:
        logger.error(f"Error getting execution history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(execution_id: str):
    """Get specific execution details"""
    try:
        executions = workflow_service.get_execution_history()
        execution = next((e for e in executions if e["execution_id"] == execution_id), None)
        
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")
        
        return execution
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics", response_model=PerformanceMetricsResponse)
async def get_performance_metrics():
    """Get performance metrics"""
    try:
        metrics = workflow_service.get_performance_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/triggers/{trigger_id}/enable")
async def enable_trigger(trigger_id: str):
    """Enable a trigger"""
    try:
        triggers = workflow_service.get_active_triggers()
        trigger = next((t for t in triggers if t["trigger_id"] == trigger_id), None)
        
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        
        # Update trigger status
        trigger["enabled"] = True
        trigger["updated_at"] = datetime.utcnow()
        
        return {"message": "Trigger enabled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enabling trigger: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/triggers/{trigger_id}/disable")
async def disable_trigger(trigger_id: str):
    """Disable a trigger"""
    try:
        triggers = workflow_service.get_active_triggers()
        trigger = next((t for t in triggers if t["trigger_id"] == trigger_id), None)
        
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        
        # Update trigger status
        trigger["enabled"] = False
        trigger["updated_at"] = datetime.utcnow()
        
        return {"message": "Trigger disabled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disabling trigger: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/triggers/{trigger_id}")
async def delete_trigger(trigger_id: str):
    """Delete a trigger"""
    try:
        triggers = workflow_service.get_active_triggers()
        trigger = next((t for t in triggers if t["trigger_id"] == trigger_id), None)
        
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        
        # Remove trigger from active triggers
        del workflow_service.active_triggers[trigger_id]
        
        return {"message": "Trigger deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting trigger: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        metrics = workflow_service.get_performance_metrics()
        return {
            "status": "healthy",
            "service": "workflow-automation",
            "version": "2.0.0",
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "workflow-automation",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
