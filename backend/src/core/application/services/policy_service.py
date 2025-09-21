"""
Policy Service
Handles policy business logic and operations
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...domain.entities.policy import Policy, PolicyStatus, PolicyType, PolicyVersion
from ...domain.repositories.policy_repository import PolicyRepository
from ...domain.repositories.audit_log_repository import AuditLogRepository


class PolicyService:
    """Policy service for business logic"""
    
    def __init__(
        self,
        policy_repository: PolicyRepository,
        audit_log_repository: AuditLogRepository
    ):
        self.policy_repository = policy_repository
        self.audit_log_repository = audit_log_repository
    
    async def create_policy(
        self,
        title: str,
        description: str,
        content: str,
        policy_type: PolicyType,
        organization_id: str,
        owner_id: str,
        created_by: str,
        effective_date: Optional[datetime] = None,
        expiry_date: Optional[datetime] = None,
        tags: List[str] = None
    ) -> Policy:
        """
        Create a new policy
        
        Args:
            title: Policy title
            description: Policy description
            content: Policy content
            policy_type: Policy type
            organization_id: Organization ID
            owner_id: Policy owner ID
            created_by: ID of user creating the policy
            effective_date: Effective date
            expiry_date: Expiry date
            tags: Policy tags
            
        Returns:
            Created policy
            
        Raises:
            ValueError: If validation fails
        """
        # Validate policy data
        self._validate_policy_data(title, description, content, effective_date, expiry_date)
        
        # Create policy
        policy = Policy.create_new(
            title=title,
            description=description,
            content=content,
            policy_type=policy_type,
            organization_id=organization_id,
            owner_id=owner_id,
            effective_date=effective_date,
            tags=tags or []
        )
        
        if expiry_date:
            policy.expiry_date = expiry_date
        
        # Save policy
        created_policy = await self.policy_repository.create(policy)
        
        return created_policy
    
    async def get_policy_by_id(self, policy_id: UUID) -> Optional[Policy]:
        """
        Get policy by ID
        
        Args:
            policy_id: Policy ID
            
        Returns:
            Policy or None if not found
        """
        return await self.policy_repository.get_by_id(policy_id)
    
    async def update_policy(
        self,
        policy_id: UUID,
        updates: Dict[str, Any],
        updated_by: str
    ) -> Policy:
        """
        Update policy information
        
        Args:
            policy_id: Policy ID
            updates: Updates to apply
            updated_by: ID of user making the update
            
        Returns:
            Updated policy
            
        Raises:
            ValueError: If validation fails
        """
        policy = await self.policy_repository.get_by_id(policy_id)
        if not policy:
            raise ValueError("Policy not found")
        
        # Validate updates
        await self._validate_policy_updates(policy, updates)
        
        # Apply updates
        for field, value in updates.items():
            if hasattr(policy, field) and field not in ['id', 'created_at', 'created_by']:
                setattr(policy, field, value)
        
        policy.updated_at = datetime.utcnow()
        
        # Save updated policy
        updated_policy = await self.policy_repository.update(policy)
        
        return updated_policy
    
    async def delete_policy(self, policy_id: UUID, deleted_by: str) -> bool:
        """
        Delete policy
        
        Args:
            policy_id: Policy ID
            deleted_by: ID of user performing the deletion
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If policy cannot be deleted
        """
        policy = await self.policy_repository.get_by_id(policy_id)
        if not policy:
            raise ValueError("Policy not found")
        
        # Check if policy can be deleted
        if policy.status == PolicyStatus.ACTIVE:
            raise ValueError("Cannot delete active policies")
        
        # Check if policy has dependencies (in real implementation)
        # await self._check_policy_dependencies(policy_id)
        
        # Delete policy
        success = await self.policy_repository.delete(policy_id)
        
        return success
    
    async def list_policies(
        self,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Policy]:
        """
        List policies with filtering
        
        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional filters
            
        Returns:
            List of policies
        """
        if not filters:
            return await self.policy_repository.get_by_organization(
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        # Apply filters
        if "status" in filters:
            return await self.policy_repository.get_by_status(
                status=filters["status"],
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        if "policy_type" in filters:
            return await self.policy_repository.get_by_type(
                policy_type=filters["policy_type"],
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        if "owner_id" in filters:
            return await self.policy_repository.get_by_owner(
                owner_id=filters["owner_id"],
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        
        # Default to organization filter
        return await self.policy_repository.get_by_organization(
            organization_id=organization_id,
            skip=skip,
            limit=limit
        )
    
    async def search_policies(
        self,
        query: str,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Policy]:
        """
        Search policies
        
        Args:
            query: Search query
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records
            filters: Optional additional filters
            
        Returns:
            List of matching policies
        """
        policies = await self.policy_repository.search(
            query=query,
            organization_id=organization_id,
            skip=skip,
            limit=limit
        )
        
        # Apply additional filters if provided
        if filters:
            policies = self._apply_filters(policies, filters)
        
        return policies
    
    async def count_policies(
        self,
        organization_id: str,
        filters: Optional[Dict[str, Any]] = None,
        search_query: Optional[str] = None
    ) -> int:
        """
        Count policies
        
        Args:
            organization_id: Organization ID
            filters: Optional filters
            search_query: Optional search query
            
        Returns:
            Number of policies
        """
        if search_query:
            # For search queries, we need to get the results and count them
            policies = await self.policy_repository.search(
                query=search_query,
                organization_id=organization_id,
                skip=0,
                limit=10000  # Large limit to get all results for counting
            )
            if filters:
                policies = self._apply_filters(policies, filters)
            return len(policies)
        
        # For regular queries, we can use more efficient counting
        if not filters:
            return await self.policy_repository.get_effective_policies_count(organization_id)
        
        # Apply filters and count
        if "status" in filters:
            policies = await self.policy_repository.get_by_status(
                status=filters["status"],
                organization_id=organization_id,
                skip=0,
                limit=10000
            )
            return len(policies)
        
        if "policy_type" in filters:
            policies = await self.policy_repository.get_by_type(
                policy_type=filters["policy_type"],
                organization_id=organization_id,
                skip=0,
                limit=10000
            )
            return len(policies)
        
        return 0
    
    async def approve_policy(
        self,
        policy_id: UUID,
        approved_by: str,
        approval_notes: str
    ) -> Policy:
        """
        Approve policy
        
        Args:
            policy_id: Policy ID
            approved_by: ID of user approving the policy
            approval_notes: Approval notes
            
        Returns:
            Updated policy
            
        Raises:
            ValueError: If policy cannot be approved
        """
        policy = await self.policy_repository.get_by_id(policy_id)
        if not policy:
            raise ValueError("Policy not found")
        
        # Validate approval
        if policy.status not in [PolicyStatus.DRAFT, PolicyStatus.UNDER_REVIEW]:
            raise ValueError("Only draft or under review policies can be approved")
        
        # Approve policy
        policy.activate()
        policy.metadata["approved_by"] = approved_by
        policy.metadata["approved_at"] = datetime.utcnow().isoformat()
        policy.metadata["approval_notes"] = approval_notes
        
        # Save updated policy
        updated_policy = await self.policy_repository.update(policy)
        
        return updated_policy
    
    async def reject_policy(
        self,
        policy_id: UUID,
        rejected_by: str,
        rejection_reason: str
    ) -> Policy:
        """
        Reject policy
        
        Args:
            policy_id: Policy ID
            rejected_by: ID of user rejecting the policy
            rejection_reason: Rejection reason
            
        Returns:
            Updated policy
            
        Raises:
            ValueError: If policy cannot be rejected
        """
        policy = await self.policy_repository.get_by_id(policy_id)
        if not policy:
            raise ValueError("Policy not found")
        
        # Validate rejection
        if policy.status not in [PolicyStatus.DRAFT, PolicyStatus.UNDER_REVIEW]:
            raise ValueError("Only draft or under review policies can be rejected")
        
        # Reject policy
        policy.status = PolicyStatus.DRAFT
        policy.metadata["rejected_by"] = rejected_by
        policy.metadata["rejected_at"] = datetime.utcnow().isoformat()
        policy.metadata["rejection_reason"] = rejection_reason
        
        # Save updated policy
        updated_policy = await self.policy_repository.update(policy)
        
        return updated_policy
    
    async def create_policy_version(
        self,
        policy_id: UUID,
        new_content: str,
        change_summary: str,
        created_by: str
    ) -> Policy:
        """
        Create new policy version
        
        Args:
            policy_id: Policy ID
            new_content: New policy content
            change_summary: Summary of changes
            created_by: ID of user creating the version
            
        Returns:
            Updated policy with new version
            
        Raises:
            ValueError: If version cannot be created
        """
        policy = await self.policy_repository.get_by_id(policy_id)
        if not policy:
            raise ValueError("Policy not found")
        
        # Validate version creation
        if policy.status == PolicyStatus.ARCHIVED:
            raise ValueError("Cannot create versions for archived policies")
        
        # Create new version
        policy.update_content(new_content, created_by, change_summary)
        
        # Save updated policy
        updated_policy = await self.policy_repository.update(policy)
        
        return updated_policy
    
    async def start_review(
        self,
        policy_id: UUID,
        started_by: str
    ) -> Policy:
        """
        Start policy review process
        
        Args:
            policy_id: Policy ID
            started_by: ID of user starting the review
            
        Returns:
            Updated policy
            
        Raises:
            ValueError: If review cannot be started
        """
        policy = await self.policy_repository.get_by_id(policy_id)
        if not policy:
            raise ValueError("Policy not found")
        
        # Start review
        policy.start_review()
        policy.metadata["review_started_by"] = started_by
        policy.metadata["review_started_at"] = datetime.utcnow().isoformat()
        
        # Save updated policy
        updated_policy = await self.policy_repository.update(policy)
        
        return updated_policy
    
    async def archive_policy(
        self,
        policy_id: UUID,
        archived_by: str,
        archive_reason: str
    ) -> Policy:
        """
        Archive policy
        
        Args:
            policy_id: Policy ID
            archived_by: ID of user archiving the policy
            archive_reason: Reason for archiving
            
        Returns:
            Updated policy
            
        Raises:
            ValueError: If policy cannot be archived
        """
        policy = await self.policy_repository.get_by_id(policy_id)
        if not policy:
            raise ValueError("Policy not found")
        
        # Archive policy
        policy.archive()
        policy.metadata["archived_by"] = archived_by
        policy.metadata["archived_at"] = datetime.utcnow().isoformat()
        policy.metadata["archive_reason"] = archive_reason
        
        # Save updated policy
        updated_policy = await self.policy_repository.update(policy)
        
        return updated_policy
    
    async def get_policy_statistics(self, organization_id: str) -> Dict[str, Any]:
        """
        Get policy statistics for organization
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Policy statistics
        """
        stats = await self.policy_repository.get_policy_statistics(organization_id)
        return stats
    
    async def get_expiring_policies(
        self,
        organization_id: str,
        days_ahead: int = 30,
        skip: int = 0,
        limit: int = 100
    ) -> List[Policy]:
        """
        Get policies expiring soon
        
        Args:
            organization_id: Organization ID
            days_ahead: Number of days to look ahead
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of expiring policies
        """
        return await self.policy_repository.get_policies_expiring_soon(
            days_ahead=days_ahead,
            organization_id=organization_id,
            skip=skip,
            limit=limit
        )
    
    async def bulk_update_policies(
        self,
        policy_ids: List[UUID],
        updates: Dict[str, Any],
        updated_by: str
    ) -> Dict[str, Any]:
        """
        Bulk update policies
        
        Args:
            policy_ids: List of policy IDs
            updates: Updates to apply
            updated_by: ID of user making the updates
            
        Returns:
            Update results
        """
        successful = 0
        failed = 0
        errors = []
        
        for policy_id in policy_ids:
            try:
                await self.update_policy(policy_id, updates, updated_by)
                successful += 1
            except Exception as e:
                failed += 1
                errors.append({
                    "policy_id": str(policy_id),
                    "error": str(e)
                })
        
        return {
            "successful": successful,
            "failed": failed,
            "errors": errors,
            "total": len(policy_ids)
        }
    
    def _apply_filters(self, policies: List[Policy], filters: Dict[str, Any]) -> List[Policy]:
        """
        Apply additional filters to policy list
        
        Args:
            policies: List of policies
            filters: Filters to apply
            
        Returns:
            Filtered list of policies
        """
        filtered_policies = policies
        
        if "status" in filters:
            filtered_policies = [
                policy for policy in filtered_policies
                if policy.status == filters["status"]
            ]
        
        if "policy_type" in filters:
            filtered_policies = [
                policy for policy in filtered_policies
                if policy.policy_type == filters["policy_type"]
            ]
        
        if "owner_id" in filters:
            filtered_policies = [
                policy for policy in filtered_policies
                if policy.owner_id == filters["owner_id"]
            ]
        
        if "tag" in filters:
            filtered_policies = [
                policy for policy in filtered_policies
                if filters["tag"] in policy.tags
            ]
        
        return filtered_policies
    
    def _validate_policy_data(
        self,
        title: str,
        description: str,
        content: str,
        effective_date: Optional[datetime],
        expiry_date: Optional[datetime]
    ) -> None:
        """
        Validate policy data
        
        Args:
            title: Policy title
            description: Policy description
            content: Policy content
            effective_date: Effective date
            expiry_date: Expiry date
            
        Raises:
            ValueError: If validation fails
        """
        if not title or len(title.strip()) == 0:
            raise ValueError("Policy title is required")
        
        if not description or len(description.strip()) == 0:
            raise ValueError("Policy description is required")
        
        if not content or len(content.strip()) == 0:
            raise ValueError("Policy content is required")
        
        if effective_date and expiry_date and effective_date >= expiry_date:
            raise ValueError("Effective date must be before expiry date")
        
        if effective_date and effective_date < datetime.utcnow().date():
            raise ValueError("Effective date cannot be in the past")
    
    async def _validate_policy_updates(self, policy: Policy, updates: Dict[str, Any]) -> None:
        """
        Validate policy updates
        
        Args:
            policy: Policy being updated
            updates: Updates to validate
            
        Raises:
            ValueError: If validation fails
        """
        # Validate effective date
        if "effective_date" in updates:
            effective_date = updates["effective_date"]
            if effective_date and policy.expiry_date and effective_date >= policy.expiry_date:
                raise ValueError("Effective date must be before expiry date")
        
        # Validate expiry date
        if "expiry_date" in updates:
            expiry_date = updates["expiry_date"]
            if expiry_date and policy.effective_date and policy.effective_date >= expiry_date:
                raise ValueError("Expiry date must be after effective date")
        
        # Validate content changes
        if "content" in updates:
            new_content = updates["content"]
            if not new_content or len(new_content.strip()) == 0:
                raise ValueError("Policy content cannot be empty")
