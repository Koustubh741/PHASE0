"""
Policy Management API Endpoints
Handles policy CRUD operations, versioning, and approval workflows
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request, Query
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ....core.application.services.policy_service import PolicyService
from ....core.application.services.audit_service import AuditService
from ....core.infrastructure.dependency_injection import get_policy_service, get_audit_service
from ....core.domain.entities.policy import Policy, PolicyStatus, PolicyType
from ....core.domain.entities.user import User
from ....core.domain.entities.audit_log import AuditAction, AuditResource
from ....core.application.dto.policy_dto import (
    PolicyCreateRequest, PolicyUpdateRequest, PolicyResponse, PolicyListResponse,
    PolicyVersionRequest, PolicyApprovalRequest, PolicySearchRequest,
    PolicyStatisticsResponse
)
from ...middleware.auth_middleware import require_auth, require_admin, require_permission


router = APIRouter(prefix="/policies", tags=["Policy Management"])


class PolicyController:
    """Policy management controller"""
    
    def __init__(
        self,
        policy_service: PolicyService,
        audit_service: AuditService
    ):
        self.policy_service = policy_service
        self.audit_service = audit_service
    
    async def create_policy(
        self,
        policy_request: PolicyCreateRequest,
        current_user: User = Depends(require_permission("can_create_policies"))
    ) -> PolicyResponse:
        """Create a new policy"""
        try:
            policy = await self.policy_service.create_policy(
                title=policy_request.title,
                description=policy_request.description,
                content=policy_request.content,
                policy_type=PolicyType(policy_request.policy_type),
                organization_id=current_user.organization_id,
                owner_id=str(current_user.id),
                effective_date=policy_request.effective_date,
                tags=policy_request.tags
            )
            
            await self.audit_service.log_policy_action(
                action=AuditAction.CREATE,
                policy_id=str(policy.id),
                description=f"Created policy: {policy.title}",
                user=current_user
            )
            
            return PolicyResponse.from_policy(policy)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_policy(
        self,
        policy_id: UUID,
        current_user: User = Depends(require_auth)
    ) -> PolicyResponse:
        """Get policy by ID"""
        policy = await self.policy_service.get_policy_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        # Check organization access
        if policy.organization_id != current_user.organization_id:
            raise HTTPException(status_code=403, detail="Policy not found in your organization")
        
        return PolicyResponse.from_policy(policy)
    
    async def update_policy(
        self,
        policy_id: UUID,
        policy_request: PolicyUpdateRequest,
        current_user: User = Depends(require_auth)
    ) -> PolicyResponse:
        """Update policy"""
        policy = await self.policy_service.get_policy_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        # Check permissions
        can_edit = (current_user.has_permission("can_edit_policies") or 
                   policy.owner_id == str(current_user.id))
        
        if not can_edit:
            raise HTTPException(status_code=403, detail="Cannot edit this policy")
        
        old_values = policy.to_dict()
        
        try:
            updated_policy = await self.policy_service.update_policy(
                policy_id=policy_id,
                updates=policy_request.dict(exclude_unset=True),
                updated_by=str(current_user.id)
            )
            
            await self.audit_service.log_policy_action(
                action=AuditAction.UPDATE,
                policy_id=str(policy_id),
                description=f"Updated policy: {policy.title}",
                user=current_user,
                old_values=old_values,
                new_values=updated_policy.to_dict()
            )
            
            return PolicyResponse.from_policy(updated_policy)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def delete_policy(
        self,
        policy_id: UUID,
        current_user: User = Depends(require_permission("can_delete_policies"))
    ) -> Dict[str, str]:
        """Delete policy"""
        policy = await self.policy_service.get_policy_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        if policy.organization_id != current_user.organization_id:
            raise HTTPException(status_code=403, detail="Policy not found in your organization")
        
        try:
            await self.policy_service.delete_policy(policy_id, str(current_user.id))
            
            await self.audit_service.log_policy_action(
                action=AuditAction.DELETE,
                policy_id=str(policy_id),
                description=f"Deleted policy: {policy.title}",
                user=current_user
            )
            
            return {"message": "Policy deleted successfully"}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to delete policy")
    
    async def list_policies(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        status: Optional[str] = Query(None),
        policy_type: Optional[str] = Query(None),
        owner_id: Optional[str] = Query(None),
        current_user: User = Depends(require_auth)
    ) -> PolicyListResponse:
        """List policies with filtering and pagination"""
        try:
            filters = {}
            if status:
                filters["status"] = PolicyStatus(status)
            if policy_type:
                filters["policy_type"] = PolicyType(policy_type)
            if owner_id:
                filters["owner_id"] = owner_id
            
            policies = await self.policy_service.list_policies(
                organization_id=current_user.organization_id,
                skip=skip,
                limit=limit,
                filters=filters
            )
            
            total = await self.policy_service.count_policies(
                organization_id=current_user.organization_id,
                filters=filters
            )
            
            return PolicyListResponse(
                policies=[PolicyResponse.from_policy(policy) for policy in policies],
                total=total,
                skip=skip,
                limit=limit
            )
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def approve_policy(
        self,
        policy_id: UUID,
        approval_request: PolicyApprovalRequest,
        current_user: User = Depends(require_permission("can_approve_policies"))
    ) -> PolicyResponse:
        """Approve policy"""
        policy = await self.policy_service.get_policy_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        if policy.organization_id != current_user.organization_id:
            raise HTTPException(status_code=403, detail="Policy not found in your organization")
        
        old_values = policy.to_dict()
        
        try:
            if approval_request.approved:
                updated_policy = await self.policy_service.approve_policy(
                    policy_id=policy_id,
                    approved_by=str(current_user.id),
                    approval_notes=approval_request.notes
                )
            else:
                updated_policy = await self.policy_service.reject_policy(
                    policy_id=policy_id,
                    rejected_by=str(current_user.id),
                    rejection_reason=approval_request.notes
                )
            
            await self.audit_service.log_policy_action(
                action=AuditAction.APPROVE if approval_request.approved else AuditAction.REJECT,
                policy_id=str(policy_id),
                description=f"{'Approved' if approval_request.approved else 'Rejected'} policy: {policy.title}",
                user=current_user,
                old_values=old_values,
                new_values=updated_policy.to_dict(),
                metadata={"approval_notes": approval_request.notes}
            )
            
            return PolicyResponse.from_policy(updated_policy)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def create_policy_version(
        self,
        policy_id: UUID,
        version_request: PolicyVersionRequest,
        current_user: User = Depends(require_auth)
    ) -> PolicyResponse:
        """Create new policy version"""
        policy = await self.policy_service.get_policy_by_id(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        # Check permissions
        can_edit = (current_user.has_permission("can_edit_policies") or 
                   policy.owner_id == str(current_user.id))
        
        if not can_edit:
            raise HTTPException(status_code=403, detail="Cannot edit this policy")
        
        old_values = policy.to_dict()
        
        try:
            updated_policy = await self.policy_service.create_policy_version(
                policy_id=policy_id,
                new_content=version_request.content,
                change_summary=version_request.change_summary,
                created_by=str(current_user.id)
            )
            
            await self.audit_service.log_policy_action(
                action=AuditAction.UPDATE,
                policy_id=str(policy_id),
                description=f"Created new version of policy: {policy.title}",
                user=current_user,
                old_values=old_values,
                new_values=updated_policy.to_dict(),
                metadata={"change_summary": version_request.change_summary}
            )
            
            return PolicyResponse.from_policy(updated_policy)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_policy_statistics(
        self,
        current_user: User = Depends(require_auth)
    ) -> PolicyStatisticsResponse:
        """Get policy statistics"""
        try:
            stats = await self.policy_service.get_policy_statistics(
                organization_id=current_user.organization_id
            )
            
            return PolicyStatisticsResponse(**stats)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to get policy statistics")


# Dependency injection for policy controller
def get_policy_controller(
    policy_service: PolicyService = Depends(get_policy_service),
    audit_service: AuditService = Depends(get_audit_service)
) -> PolicyController:
    """Get policy controller instance with dependency injection"""
    return PolicyController(policy_service, audit_service)


# API Routes
@router.post("", response_model=PolicyResponse)
async def create_policy(
    policy_request: PolicyCreateRequest,
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_permission("can_create_policies"))
):
    """Create a new policy"""
    return await controller.create_policy(policy_request, current_user)


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: UUID,
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_auth)
):
    """Get policy by ID"""
    return await controller.get_policy(policy_id, current_user)


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: UUID,
    policy_request: PolicyUpdateRequest,
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_auth)
):
    """Update policy"""
    return await controller.update_policy(policy_id, policy_request, current_user)


@router.delete("/{policy_id}")
async def delete_policy(
    policy_id: UUID,
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_permission("can_delete_policies"))
):
    """Delete policy"""
    return await controller.delete_policy(policy_id, current_user)


@router.get("", response_model=PolicyListResponse)
async def list_policies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    policy_type: Optional[str] = Query(None),
    owner_id: Optional[str] = Query(None),
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_auth)
):
    """List policies with filtering and pagination"""
    return await controller.list_policies(skip, limit, status, policy_type, owner_id, current_user)


@router.post("/{policy_id}/approve", response_model=PolicyResponse)
async def approve_policy(
    policy_id: UUID,
    approval_request: PolicyApprovalRequest,
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_permission("can_approve_policies"))
):
    """Approve or reject policy"""
    return await controller.approve_policy(policy_id, approval_request, current_user)


@router.post("/{policy_id}/versions", response_model=PolicyResponse)
async def create_policy_version(
    policy_id: UUID,
    version_request: PolicyVersionRequest,
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_auth)
):
    """Create new policy version"""
    return await controller.create_policy_version(policy_id, version_request, current_user)


@router.get("/statistics", response_model=PolicyStatisticsResponse)
async def get_policy_statistics(
    controller: PolicyController = Depends(get_policy_controller),
    current_user: User = Depends(require_auth)
):
    """Get policy statistics"""
    return await controller.get_policy_statistics(current_user)
