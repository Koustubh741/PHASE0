"""
Workflow Service
Handles approval, escalation, and review cycle workflows for GRC entities
"""

from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from datetime import datetime, timedelta
from enum import Enum

from ...domain.entities.user import User
from ...domain.entities.audit_log import AuditAction, AuditResource, AuditSeverity
from ...domain.repositories.audit_log_repository import AuditLogRepository


class WorkflowStatus(Enum):
    """Workflow status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class WorkflowType(Enum):
    """Workflow type enumeration"""
    POLICY_APPROVAL = "policy_approval"
    RISK_ESCALATION = "risk_escalation"
    CONTROL_REVIEW = "control_review"
    ISSUE_RESOLUTION = "issue_resolution"
    USER_ROLE_CHANGE = "user_role_change"
    DATA_EXPORT = "data_export"


class ApprovalLevel(Enum):
    """Approval level enumeration"""
    IMMEDIATE = "immediate"
    SUPERVISOR = "supervisor"
    MANAGER = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"
    BOARD = "board"


class WorkflowStep:
    """Workflow step definition"""
    
    def __init__(
        self,
        step_id: str,
        step_name: str,
        approver_role: str,
        approval_level: ApprovalLevel,
        is_required: bool = True,
        auto_approve: bool = False,
        escalation_hours: Optional[int] = None
    ):
        self.step_id = step_id
        self.step_name = step_name
        self.approver_role = approver_role
        self.approval_level = approval_level
        self.is_required = is_required
        self.auto_approve = auto_approve
        self.escalation_hours = escalation_hours
        self.completed_at: Optional[datetime] = None
        self.approved_by: Optional[str] = None
        self.comments: Optional[str] = None
        self.status: WorkflowStatus = WorkflowStatus.PENDING


class Workflow:
    """Workflow definition"""
    
    def __init__(
        self,
        workflow_id: UUID,
        workflow_type: WorkflowType,
        entity_id: str,
        entity_type: str,
        initiated_by: str,
        organization_id: str,
        steps: List[WorkflowStep],
        priority: str = "medium",
        due_date: Optional[datetime] = None
    ):
        self.id = workflow_id
        self.workflow_type = workflow_type
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.initiated_by = initiated_by
        self.organization_id = organization_id
        self.steps = steps
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.status = WorkflowStatus.PENDING
        self.current_step_index = 0
        self.completed_at: Optional[datetime] = None
        self.metadata: Dict[str, Any] = {}
    
    def get_current_step(self) -> Optional[WorkflowStep]:
        """Get current workflow step"""
        if self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def advance_to_next_step(self) -> bool:
        """Advance to next workflow step"""
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def complete_workflow(self, status: WorkflowStatus) -> None:
        """Complete the workflow"""
        self.status = status
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def is_expired(self) -> bool:
        """Check if workflow is expired"""
        if self.due_date:
            return datetime.utcnow() > self.due_date
        return False
    
    def get_escalated_steps(self) -> List[WorkflowStep]:
        """Get steps that have escalated"""
        escalated_steps = []
        for step in self.steps:
            if (step.escalation_hours and 
                step.completed_at is None and 
                step.status == WorkflowStatus.PENDING):
                hours_pending = (datetime.utcnow() - self.created_at).total_seconds() / 3600
                if hours_pending > step.escalation_hours:
                    escalated_steps.append(step)
        return escalated_steps


class WorkflowService:
    """Workflow service for managing approval and escalation workflows"""
    
    def __init__(self, audit_log_repository: AuditLogRepository):
        self.audit_log_repository = audit_log_repository
        self.active_workflows: Dict[UUID, Workflow] = {}
    
    async def create_policy_approval_workflow(
        self,
        policy_id: str,
        policy_title: str,
        initiated_by: str,
        organization_id: str,
        policy_type: str,
        priority: str = "medium"
    ) -> Workflow:
        """
        Create policy approval workflow
        
        Args:
            policy_id: Policy ID
            policy_title: Policy title
            initiated_by: User ID who initiated
            organization_id: Organization ID
            policy_type: Type of policy
            priority: Workflow priority
            
        Returns:
            Created workflow
        """
        from uuid import uuid4
        
        # Define workflow steps based on policy type and priority
        steps = self._get_policy_approval_steps(policy_type, priority)
        
        workflow_id = uuid4()
        due_date = datetime.utcnow() + timedelta(days=self._get_workflow_due_days(policy_type, priority))
        
        workflow = Workflow(
            workflow_id=workflow_id,
            workflow_type=WorkflowType.POLICY_APPROVAL,
            entity_id=policy_id,
            entity_type="policy",
            initiated_by=initiated_by,
            organization_id=organization_id,
            steps=steps,
            priority=priority,
            due_date=due_date
        )
        
        workflow.metadata = {
            "policy_title": policy_title,
            "policy_type": policy_type,
            "workflow_type": "policy_approval"
        }
        
        self.active_workflows[workflow_id] = workflow
        
        # Log workflow creation
        await self._log_workflow_event(
            action="workflow_created",
            workflow_id=str(workflow_id),
            entity_id=policy_id,
            entity_type="policy",
            user_id=initiated_by,
            organization_id=organization_id,
            description=f"Policy approval workflow created for: {policy_title}"
        )
        
        return workflow
    
    async def create_risk_escalation_workflow(
        self,
        risk_id: str,
        risk_title: str,
        risk_level: str,
        initiated_by: str,
        organization_id: str,
        escalation_reason: str
    ) -> Workflow:
        """
        Create risk escalation workflow
        
        Args:
            risk_id: Risk ID
            risk_title: Risk title
            risk_level: Risk level (high, critical)
            initiated_by: User ID who initiated
            organization_id: Organization ID
            escalation_reason: Reason for escalation
            
        Returns:
            Created workflow
        """
        from uuid import uuid4
        
        # Define escalation steps based on risk level
        steps = self._get_risk_escalation_steps(risk_level)
        
        workflow_id = uuid4()
        due_date = datetime.utcnow() + timedelta(hours=self._get_escalation_due_hours(risk_level))
        
        workflow = Workflow(
            workflow_id=workflow_id,
            workflow_type=WorkflowType.RISK_ESCALATION,
            entity_id=risk_id,
            entity_type="risk",
            initiated_by=initiated_by,
            organization_id=organization_id,
            steps=steps,
            priority="high" if risk_level == "critical" else "medium",
            due_date=due_date
        )
        
        workflow.metadata = {
            "risk_title": risk_title,
            "risk_level": risk_level,
            "escalation_reason": escalation_reason,
            "workflow_type": "risk_escalation"
        }
        
        self.active_workflows[workflow_id] = workflow
        
        # Log workflow creation
        await self._log_workflow_event(
            action="workflow_created",
            workflow_id=str(workflow_id),
            entity_id=risk_id,
            entity_type="risk",
            user_id=initiated_by,
            organization_id=organization_id,
            description=f"Risk escalation workflow created for: {risk_title} (Level: {risk_level})"
        )
        
        return workflow
    
    async def create_control_review_workflow(
        self,
        control_id: str,
        control_title: str,
        review_type: str,
        initiated_by: str,
        organization_id: str,
        review_frequency: str = "quarterly"
    ) -> Workflow:
        """
        Create control review workflow
        
        Args:
            control_id: Control ID
            control_title: Control title
            review_type: Type of review
            initiated_by: User ID who initiated
            organization_id: Organization ID
            review_frequency: Review frequency
            
        Returns:
            Created workflow
        """
        from uuid import uuid4
        
        # Define review steps
        steps = self._get_control_review_steps(review_type)
        
        workflow_id = uuid4()
        due_date = datetime.utcnow() + timedelta(days=self._get_review_due_days(review_frequency))
        
        workflow = Workflow(
            workflow_id=workflow_id,
            workflow_type=WorkflowType.CONTROL_REVIEW,
            entity_id=control_id,
            entity_type="control",
            initiated_by=initiated_by,
            organization_id=organization_id,
            steps=steps,
            priority="medium",
            due_date=due_date
        )
        
        workflow.metadata = {
            "control_title": control_title,
            "review_type": review_type,
            "review_frequency": review_frequency,
            "workflow_type": "control_review"
        }
        
        self.active_workflows[workflow_id] = workflow
        
        # Log workflow creation
        await self._log_workflow_event(
            action="workflow_created",
            workflow_id=str(workflow_id),
            entity_id=control_id,
            entity_type="control",
            user_id=initiated_by,
            organization_id=organization_id,
            description=f"Control review workflow created for: {control_title}"
        )
        
        return workflow
    
    async def approve_workflow_step(
        self,
        workflow_id: UUID,
        step_id: str,
        approved_by: str,
        comments: str = "",
        auto_approve: bool = False
    ) -> Tuple[bool, str]:
        """
        Approve a workflow step
        
        Args:
            workflow_id: Workflow ID
            step_id: Step ID to approve
            approved_by: User ID approving
            comments: Approval comments
            auto_approve: Whether this is an auto-approval
            
        Returns:
            Tuple of (success, message)
        """
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            return False, "Workflow not found"
        
        if workflow.status != WorkflowStatus.PENDING:
            return False, "Workflow is not pending"
        
        # Find the step
        current_step = workflow.get_current_step()
        if not current_step or current_step.step_id != step_id:
            return False, "Invalid step for approval"
        
        # Approve the step
        current_step.status = WorkflowStatus.APPROVED
        current_step.completed_at = datetime.utcnow()
        current_step.approved_by = approved_by
        current_step.comments = comments
        
        # Check if workflow is complete
        if workflow.advance_to_next_step():
            # Move to next step
            workflow.status = WorkflowStatus.IN_PROGRESS
            next_step = workflow.get_current_step()
            if next_step and next_step.auto_approve:
                # Auto-approve if configured
                return await self.approve_workflow_step(
                    workflow_id, next_step.step_id, "system", "Auto-approved", True
                )
        else:
            # Workflow completed
            workflow.complete_workflow(WorkflowStatus.APPROVED)
        
        # Log approval
        await self._log_workflow_event(
            action="step_approved",
            workflow_id=str(workflow_id),
            entity_id=workflow.entity_id,
            entity_type=workflow.entity_type,
            user_id=approved_by,
            organization_id=workflow.organization_id,
            description=f"Workflow step approved: {current_step.step_name}",
            metadata={
                "step_id": step_id,
                "auto_approve": auto_approve,
                "comments": comments
            }
        )
        
        return True, "Step approved successfully"
    
    async def reject_workflow_step(
        self,
        workflow_id: UUID,
        step_id: str,
        rejected_by: str,
        rejection_reason: str
    ) -> Tuple[bool, str]:
        """
        Reject a workflow step
        
        Args:
            workflow_id: Workflow ID
            step_id: Step ID to reject
            rejected_by: User ID rejecting
            rejection_reason: Rejection reason
            
        Returns:
            Tuple of (success, message)
        """
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            return False, "Workflow not found"
        
        if workflow.status != WorkflowStatus.PENDING:
            return False, "Workflow is not pending"
        
        # Find the step
        current_step = workflow.get_current_step()
        if not current_step or current_step.step_id != step_id:
            return False, "Invalid step for rejection"
        
        # Reject the step and workflow
        current_step.status = WorkflowStatus.REJECTED
        current_step.completed_at = datetime.utcnow()
        current_step.approved_by = rejected_by
        current_step.comments = rejection_reason
        
        workflow.complete_workflow(WorkflowStatus.REJECTED)
        
        # Log rejection
        await self._log_workflow_event(
            action="step_rejected",
            workflow_id=str(workflow_id),
            entity_id=workflow.entity_id,
            entity_type=workflow.entity_type,
            user_id=rejected_by,
            organization_id=workflow.organization_id,
            description=f"Workflow step rejected: {current_step.step_name}",
            metadata={
                "step_id": step_id,
                "rejection_reason": rejection_reason
            }
        )
        
        return True, "Step rejected successfully"
    
    async def escalate_workflow(
        self,
        workflow_id: UUID,
        escalated_by: str,
        escalation_reason: str
    ) -> Tuple[bool, str]:
        """
        Escalate a workflow
        
        Args:
            workflow_id: Workflow ID
            escalated_by: User ID escalating
            escalation_reason: Escalation reason
            
        Returns:
            Tuple of (success, message)
        """
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            return False, "Workflow not found"
        
        # Check for escalated steps
        escalated_steps = workflow.get_escalated_steps()
        if not escalated_steps:
            return False, "No steps to escalate"
        
        # Mark workflow as escalated
        workflow.status = WorkflowStatus.ESCALATED
        workflow.updated_at = datetime.utcnow()
        
        # Log escalation
        await self._log_workflow_event(
            action="workflow_escalated",
            workflow_id=str(workflow_id),
            entity_id=workflow.entity_id,
            entity_type=workflow.entity_type,
            user_id=escalated_by,
            organization_id=workflow.organization_id,
            description=f"Workflow escalated: {escalation_reason}",
            metadata={
                "escalation_reason": escalation_reason,
                "escalated_steps": [step.step_id for step in escalated_steps]
            }
        )
        
        return True, "Workflow escalated successfully"
    
    async def get_workflow_status(self, workflow_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get workflow status
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow status information
        """
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            return None
        
        current_step = workflow.get_current_step()
        escalated_steps = workflow.get_escalated_steps()
        
        return {
            "workflow_id": str(workflow.id),
            "workflow_type": workflow.workflow_type.value,
            "status": workflow.status.value,
            "entity_id": workflow.entity_id,
            "entity_type": workflow.entity_type,
            "initiated_by": workflow.initiated_by,
            "created_at": workflow.created_at.isoformat(),
            "updated_at": workflow.updated_at.isoformat(),
            "due_date": workflow.due_date.isoformat() if workflow.due_date else None,
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "current_step": {
                "step_id": current_step.step_id,
                "step_name": current_step.step_name,
                "approver_role": current_step.approver_role,
                "approval_level": current_step.approval_level.value,
                "status": current_step.status.value
            } if current_step else None,
            "escalated_steps": [step.step_id for step in escalated_steps],
            "is_expired": workflow.is_expired(),
            "priority": workflow.priority,
            "metadata": workflow.metadata
        }
    
    async def get_user_pending_workflows(
        self,
        user_id: str,
        organization_id: str,
        user_role: str
    ) -> List[Dict[str, Any]]:
        """
        Get workflows pending user approval
        
        Args:
            user_id: User ID
            organization_id: Organization ID
            user_role: User role
            
        Returns:
            List of pending workflows
        """
        pending_workflows = []
        
        for workflow in self.active_workflows.values():
            if (workflow.organization_id != organization_id or 
                workflow.status != WorkflowStatus.PENDING):
                continue
            
            current_step = workflow.get_current_step()
            if (current_step and 
                current_step.status == WorkflowStatus.PENDING and
                current_step.approver_role == user_role):
                
                workflow_info = await self.get_workflow_status(workflow.id)
                if workflow_info:
                    pending_workflows.append(workflow_info)
        
        return pending_workflows
    
    def _get_policy_approval_steps(self, policy_type: str, priority: str) -> List[WorkflowStep]:
        """Get approval steps for policy workflow"""
        steps = []
        
        # Define steps based on policy type and priority
        if policy_type in ["compliance", "security"] and priority == "high":
            steps = [
                WorkflowStep("review", "Technical Review", "compliance_manager", ApprovalLevel.MANAGER),
                WorkflowStep("legal", "Legal Review", "legal_counsel", ApprovalLevel.MANAGER),
                WorkflowStep("approval", "Final Approval", "director", ApprovalLevel.DIRECTOR)
            ]
        elif policy_type in ["operational", "financial"]:
            steps = [
                WorkflowStep("review", "Department Review", "department_manager", ApprovalLevel.MANAGER),
                WorkflowStep("approval", "Final Approval", "director", ApprovalLevel.DIRECTOR)
            ]
        else:
            steps = [
                WorkflowStep("approval", "Direct Approval", "policy_owner", ApprovalLevel.SUPERVISOR)
            ]
        
        return steps
    
    def _get_risk_escalation_steps(self, risk_level: str) -> List[WorkflowStep]:
        """Get escalation steps for risk workflow"""
        steps = []
        
        if risk_level == "critical":
            steps = [
                WorkflowStep("immediate", "Immediate Response", "risk_manager", ApprovalLevel.MANAGER, escalation_hours=1),
                WorkflowStep("executive", "Executive Notification", "executive", ApprovalLevel.EXECUTIVE, escalation_hours=4),
                WorkflowStep("board", "Board Notification", "board_member", ApprovalLevel.BOARD, escalation_hours=24)
            ]
        elif risk_level == "high":
            steps = [
                WorkflowStep("review", "Risk Review", "risk_manager", ApprovalLevel.MANAGER, escalation_hours=8),
                WorkflowStep("approval", "Management Approval", "director", ApprovalLevel.DIRECTOR, escalation_hours=48)
            ]
        else:
            steps = [
                WorkflowStep("review", "Standard Review", "risk_owner", ApprovalLevel.SUPERVISOR, escalation_hours=72)
            ]
        
        return steps
    
    def _get_control_review_steps(self, review_type: str) -> List[WorkflowStep]:
        """Get review steps for control workflow"""
        steps = []
        
        if review_type == "effectiveness":
            steps = [
                WorkflowStep("test", "Control Testing", "control_owner", ApprovalLevel.SUPERVISOR),
                WorkflowStep("review", "Effectiveness Review", "compliance_manager", ApprovalLevel.MANAGER),
                WorkflowStep("approval", "Final Approval", "director", ApprovalLevel.DIRECTOR)
            ]
        elif review_type == "design":
            steps = [
                WorkflowStep("design", "Design Review", "control_owner", ApprovalLevel.SUPERVISOR),
                WorkflowStep("approval", "Design Approval", "compliance_manager", ApprovalLevel.MANAGER)
            ]
        else:
            steps = [
                WorkflowStep("review", "Standard Review", "control_owner", ApprovalLevel.SUPERVISOR)
            ]
        
        return steps
    
    def _get_workflow_due_days(self, policy_type: str, priority: str) -> int:
        """Get workflow due days based on type and priority"""
        if priority == "high":
            return 3
        elif priority == "medium":
            return 7
        else:
            return 14
    
    def _get_escalation_due_hours(self, risk_level: str) -> int:
        """Get escalation due hours based on risk level"""
        if risk_level == "critical":
            return 24
        elif risk_level == "high":
            return 72
        else:
            return 168  # 1 week
    
    def _get_review_due_days(self, review_frequency: str) -> int:
        """Get review due days based on frequency"""
        if review_frequency == "monthly":
            return 30
        elif review_frequency == "quarterly":
            return 90
        else:
            return 365
    
    async def _log_workflow_event(
        self,
        action: str,
        workflow_id: str,
        entity_id: str,
        entity_type: str,
        user_id: str,
        organization_id: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log workflow event"""
        await self.audit_log_repository.create(
            {
                "action": action,
                "resource": entity_type,
                "resource_id": entity_id,
                "user_id": user_id,
                "organization_id": organization_id,
                "description": description,
                "metadata": {
                    "workflow_id": workflow_id,
                    "workflow_event": True,
                    **(metadata or {})
                },
                "severity": AuditSeverity.MEDIUM,
                "success": True,
                "timestamp": datetime.utcnow()
            }
        )
