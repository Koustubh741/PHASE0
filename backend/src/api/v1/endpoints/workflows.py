"""
Workflow Management API Endpoints
Handles workflow creation, approval, and status tracking
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request, Query
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ....core.application.services.workflow_service import WorkflowService, WorkflowType
from ....core.application.services.audit_service import AuditService
from ....core.infrastructure.dependency_injection import get_workflow_service, get_audit_service
from ....core.domain.entities.user import User
from ....core.domain.entities.audit_log import AuditAction, AuditResource
from ....core.application.dto.workflow_dto import (
    WorkflowCreateRequest, WorkflowResponse, WorkflowListResponse,
    WorkflowApprovalRequest, WorkflowRejectionRequest, WorkflowEscalationRequest,
    WorkflowStatusResponse, WorkflowStatisticsResponse
)
from ...middleware.auth_middleware import require_auth, require_permission


router = APIRouter(prefix="/workflows", tags=["Workflow Management"])


class WorkflowController:
    """Workflow management controller"""
    
    def __init__(
        self,
        workflow_service: WorkflowService,
        audit_service: AuditService
    ):
        self.workflow_service = workflow_service
        self.audit_service = audit_service
    
    async def create_workflow(
        self,
        workflow_request: WorkflowCreateRequest,
        current_user: User = Depends(require_auth)
    ) -> WorkflowResponse:
        """Create a new workflow"""
        try:
            if workflow_request.workflow_type == "policy_approval":
                workflow = await self.workflow_service.create_policy_approval_workflow(
                    policy_id=workflow_request.entity_id,
                    policy_title=workflow_request.entity_title,
                    initiated_by=str(current_user.id),
                    organization_id=current_user.organization_id,
                    policy_type=workflow_request.metadata.get("policy_type", "operational"),
                    priority=workflow_request.priority
                )
            elif workflow_request.workflow_type == "risk_escalation":
                workflow = await self.workflow_service.create_risk_escalation_workflow(
                    risk_id=workflow_request.entity_id,
                    risk_title=workflow_request.entity_title,
                    risk_level=workflow_request.metadata.get("risk_level", "medium"),
                    initiated_by=str(current_user.id),
                    organization_id=current_user.organization_id,
                    escalation_reason=workflow_request.metadata.get("escalation_reason", "")
                )
            elif workflow_request.workflow_type == "control_review":
                workflow = await self.workflow_service.create_control_review_workflow(
                    control_id=workflow_request.entity_id,
                    control_title=workflow_request.entity_title,
                    review_type=workflow_request.metadata.get("review_type", "standard"),
                    initiated_by=str(current_user.id),
                    organization_id=current_user.organization_id,
                    review_frequency=workflow_request.metadata.get("review_frequency", "quarterly")
                )
            else:
                raise ValueError(f"Unsupported workflow type: {workflow_request.workflow_type}")
            
            await self.audit_service.log_workflow_action(
                action=AuditAction.CREATE,
                workflow_id=str(workflow.id),
                description=f"Created {workflow_request.workflow_type} workflow for {workflow_request.entity_title}",
                user=current_user,
                metadata={
                    "entity_id": workflow_request.entity_id,
                    "entity_type": workflow_request.entity_type,
                    "workflow_type": workflow_request.workflow_type
                }
            )
            
            return WorkflowResponse.from_workflow(workflow)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_workflow(
        self,
        workflow_id: UUID,
        current_user: User = Depends(require_auth)
    ) -> WorkflowStatusResponse:
        """Get workflow status"""
        workflow_status = await self.workflow_service.get_workflow_status(workflow_id)
        if not workflow_status:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Check organization access
        if workflow_status["organization_id"] != current_user.organization_id:
            raise HTTPException(status_code=403, detail="Workflow not found in your organization")
        
        return WorkflowStatusResponse(**workflow_status)
    
    async def approve_workflow_step(
        self,
        workflow_id: UUID,
        step_id: str,
        approval_request: WorkflowApprovalRequest,
        current_user: User = Depends(require_auth)
    ) -> Dict[str, str]:
        """Approve a workflow step"""
        try:
            success, message = await self.workflow_service.approve_workflow_step(
                workflow_id=workflow_id,
                step_id=step_id,
                approved_by=str(current_user.id),
                comments=approval_request.comments
            )
            
            if not success:
                raise HTTPException(status_code=400, detail=message)
            
            await self.audit_service.log_workflow_action(
                action=AuditAction.APPROVE,
                workflow_id=str(workflow_id),
                description=f"Approved workflow step: {step_id}",
                user=current_user,
                metadata={
                    "step_id": step_id,
                    "comments": approval_request.comments
                }
            )
            
            return {"message": message}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def reject_workflow_step(
        self,
        workflow_id: UUID,
        step_id: str,
        rejection_request: WorkflowRejectionRequest,
        current_user: User = Depends(require_auth)
    ) -> Dict[str, str]:
        """Reject a workflow step"""
        try:
            success, message = await self.workflow_service.reject_workflow_step(
                workflow_id=workflow_id,
                step_id=step_id,
                rejected_by=str(current_user.id),
                rejection_reason=rejection_request.reason
            )
            
            if not success:
                raise HTTPException(status_code=400, detail=message)
            
            await self.audit_service.log_workflow_action(
                action=AuditAction.REJECT,
                workflow_id=str(workflow_id),
                description=f"Rejected workflow step: {step_id}",
                user=current_user,
                metadata={
                    "step_id": step_id,
                    "rejection_reason": rejection_request.reason
                }
            )
            
            return {"message": message}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def escalate_workflow(
        self,
        workflow_id: UUID,
        escalation_request: WorkflowEscalationRequest,
        current_user: User = Depends(require_auth)
    ) -> Dict[str, str]:
        """Escalate a workflow"""
        try:
            success, message = await self.workflow_service.escalate_workflow(
                workflow_id=workflow_id,
                escalated_by=str(current_user.id),
                escalation_reason=escalation_request.reason
            )
            
            if not success:
                raise HTTPException(status_code=400, detail=message)
            
            await self.audit_service.log_workflow_action(
                action=AuditAction.UPDATE,
                workflow_id=str(workflow_id),
                description=f"Escalated workflow: {escalation_request.reason}",
                user=current_user,
                metadata={
                    "escalation_reason": escalation_request.reason,
                    "escalated_by": str(current_user.id)
                }
            )
            
            return {"message": message}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def list_user_pending_workflows(
        self,
        current_user: User = Depends(require_auth)
    ) -> WorkflowListResponse:
        """List workflows pending user approval"""
        try:
            pending_workflows = await self.workflow_service.get_user_pending_workflows(
                user_id=str(current_user.id),
                organization_id=current_user.organization_id,
                user_role=current_user.role.value
            )
            
            return WorkflowListResponse(
                workflows=[WorkflowStatusResponse(**wf) for wf in pending_workflows],
                total=len(pending_workflows),
                skip=0,
                limit=len(pending_workflows)
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to get pending workflows")
    
    async def list_workflows(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        workflow_type: Optional[str] = Query(None),
        status: Optional[str] = Query(None),
        entity_type: Optional[str] = Query(None),
        current_user: User = Depends(require_auth)
    ) -> WorkflowListResponse:
        """List workflows with filtering"""
        try:
            # This would need to be implemented in the workflow service
            # For now, return empty list
            workflows = []
            total = 0
            
            return WorkflowListResponse(
                workflows=workflows,
                total=total,
                skip=skip,
                limit=limit
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to list workflows")
    
    async def get_workflow_statistics(
        self,
        current_user: User = Depends(require_auth)
    ) -> WorkflowStatisticsResponse:
        """Get workflow statistics"""
        try:
            # This would need to be implemented in the workflow service
            stats = {
                "total_workflows": 0,
                "pending_workflows": 0,
                "completed_workflows": 0,
                "escalated_workflows": 0,
                "expired_workflows": 0,
                "workflows_by_type": {},
                "workflows_by_status": {},
                "average_completion_time": 0,
                "workflow_success_rate": 0.0
            }
            
            return WorkflowStatisticsResponse(**stats)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to get workflow statistics")


# Dependency injection for workflow controller
def get_workflow_controller(
    workflow_service: WorkflowService = Depends(get_workflow_service),
    audit_service: AuditService = Depends(get_audit_service)
) -> WorkflowController:
    """Get workflow controller instance with dependency injection"""
    return WorkflowController(workflow_service, audit_service)


# API Routes
@router.post("", response_model=WorkflowResponse)
async def create_workflow(
    workflow_request: WorkflowCreateRequest,
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """Create a new workflow"""
    return await controller.create_workflow(workflow_request, current_user)


@router.get("/{workflow_id}", response_model=WorkflowStatusResponse)
async def get_workflow(
    workflow_id: UUID,
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """Get workflow status"""
    return await controller.get_workflow(workflow_id, current_user)


@router.post("/{workflow_id}/steps/{step_id}/approve")
async def approve_workflow_step(
    workflow_id: UUID,
    step_id: str,
    approval_request: WorkflowApprovalRequest,
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """Approve a workflow step"""
    return await controller.approve_workflow_step(workflow_id, step_id, approval_request, current_user)


@router.post("/{workflow_id}/steps/{step_id}/reject")
async def reject_workflow_step(
    workflow_id: UUID,
    step_id: str,
    rejection_request: WorkflowRejectionRequest,
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """Reject a workflow step"""
    return await controller.reject_workflow_step(workflow_id, step_id, rejection_request, current_user)


@router.post("/{workflow_id}/escalate")
async def escalate_workflow(
    workflow_id: UUID,
    escalation_request: WorkflowEscalationRequest,
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """Escalate a workflow"""
    return await controller.escalate_workflow(workflow_id, escalation_request, current_user)


@router.get("/pending", response_model=WorkflowListResponse)
async def list_user_pending_workflows(
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """List workflows pending user approval"""
    return await controller.list_user_pending_workflows(current_user)


@router.get("", response_model=WorkflowListResponse)
async def list_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    workflow_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """List workflows with filtering"""
    return await controller.list_workflows(skip, limit, workflow_type, status, entity_type, current_user)


@router.get("/statistics", response_model=WorkflowStatisticsResponse)
async def get_workflow_statistics(
    controller: WorkflowController = Depends(get_workflow_controller),
    current_user: User = Depends(require_auth)
):
    """Get workflow statistics"""
    return await controller.get_workflow_statistics(current_user)
