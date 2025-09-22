"""
SQLAlchemy repository implementations for the GRC platform.
These repositories implement the domain repository interfaces.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_, or_, desc, asc
from datetime import datetime
import uuid

from ...domain.entities.user import User
from ...domain.entities.policy import Policy, PolicyVersion
from ...domain.entities.risk import Risk, RiskAssessment, RiskTreatment, RiskMitigation
from ...domain.entities.control import Control, ControlOwner, ControlTest
from ...domain.entities.organization import Organization
from ...domain.repositories.user_repository import UserRepository
from ...domain.repositories.policy_repository import PolicyRepository
from ...domain.repositories.risk_repository import RiskRepository
from ...domain.repositories.organization_repository import OrganizationRepository
from ...domain.repositories.audit_log_repository import AuditLogRepository

from ..database.sqlalchemy_models import (
    UserModel, PolicyModel, PolicyVersionModel, RiskModel, RiskAssessmentModel,
    RiskTreatmentModel, RiskMitigationModel, ControlModel, ControlOwnerModel,
    ControlTestModel, IssueModel, IssueActionModel, IssueCommentModel,
    IssueEvidenceModel, AuditLogModel, OrganizationModel
)


class SQLAlchemyUserRepository:
    """SQLAlchemy implementation of UserRepository - simplified for demo"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, user: User) -> User:
        """Create a new user"""
        user_model = UserModel(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.value,
            status=user.status.value,
            organization_id=user.organization_id,
            department=user.department,
            job_title=user.job_title,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            failed_login_attempts=user.failed_login_attempts,
            locked_until=user.locked_until,
            password_hash=user.password_hash,
            password_reset_token=user.password_reset_token,
            password_reset_expires=user.password_reset_expires
        )
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        return self._to_domain(user_model)
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        user_model = self.session.get(UserModel, user_id)
        if user_model:
            return self._to_domain(user_model)
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_model = self.session.query(UserModel).filter(UserModel.email == email).first()
        if user_model:
            return self._to_domain(user_model)
        return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        user_model = self.session.query(UserModel).filter(UserModel.username == username).first()
        if user_model:
            return self._to_domain(user_model)
        return None
    
    def _to_domain(self, user_model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity"""
        return User(
            id=user_model.id,  # Already a UUID object
            email=user_model.email,
            username=user_model.username,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            role=user_model.role,
            status=user_model.status,
            organization_id=user_model.organization_id,
            department=user_model.department,
            job_title=user_model.job_title,
            phone=user_model.phone,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            last_login=user_model.last_login,
            failed_login_attempts=user_model.failed_login_attempts,
            locked_until=user_model.locked_until,
            password_hash=user_model.password_hash,
            password_reset_token=user_model.password_reset_token,
            password_reset_expires=user_model.password_reset_expires
        )


class SQLAlchemyPolicyRepository:
    """SQLAlchemy implementation of PolicyRepository - simplified for demo"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, policy: Policy) -> Policy:
        """Create a new policy"""
        policy_model = PolicyModel(
            id=str(policy.id),
            title=policy.title,
            description=policy.description,
            content=policy.content,
            policy_type=policy.policy_type.value,
            status=policy.status.value,
            organization_id=policy.organization_id,
            owner_id=policy.owner_id,
            created_at=policy.created_at,
            updated_at=policy.updated_at,
            effective_date=policy.effective_date,
            expiry_date=policy.expiry_date,
            tags=policy.tags or [],
            extra_metadata=policy.metadata or {}
        )
        self.session.add(policy_model)
        self.session.commit()
        self.session.refresh(policy_model)
        return self._to_domain(policy_model)
    
    def get_by_id(self, policy_id: str) -> Optional[Policy]:
        """Get policy by ID"""
        policy_model = self.session.get(PolicyModel, policy_id)
        if policy_model:
            return self._to_domain(policy_model)
        return None
    
    def get_by_title(self, title: str) -> Optional[Policy]:
        """Get policy by title"""
        policy_model = self.session.query(PolicyModel).filter(PolicyModel.title == title).first()
        if policy_model:
            return self._to_domain(policy_model)
        return None
    
    async def update(self, policy: Policy) -> Policy:
        """Update policy"""
        policy_model = await self.session.get(PolicyModel, str(policy.id))
        if policy_model:
            policy_model.title = policy.title
            policy_model.description = policy.description
            policy_model.policy_type = policy.policy_type
            policy_model.status = policy.status
            policy_model.owner_id = str(policy.owner_id) if policy.owner_id else None
            policy_model.department_id = str(policy.department_id) if policy.department_id else None
            policy_model.organization_id = str(policy.organization_id) if policy.organization_id else None
            policy_model.effective_date = policy.effective_date
            policy_model.review_date = policy.review_date
            policy_model.updated_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(policy_model)
            return self._to_domain(policy_model)
        raise ValueError(f"Policy with ID {policy.id} not found")
    
    async def delete(self, policy_id: str) -> bool:
        """Delete policy"""
        policy_model = await self.session.get(PolicyModel, policy_id)
        if policy_model:
            await self.session.delete(policy_model)
            await self.session.commit()
            return True
        return False
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Policy]:
        """List policies with pagination"""
        policy_models = self.session.query(PolicyModel).offset(skip).limit(limit).all()
        return [self._to_domain(policy_model) for policy_model in policy_models]
    
    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Policy]:
        """Search policies by query"""
        policy_models = self.session.query(PolicyModel).filter(
            or_(
                PolicyModel.title.ilike(f"%{query}%"),
                PolicyModel.description.ilike(f"%{query}%"),
                PolicyModel.policy_type.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
        return [self._to_domain(policy_model) for policy_model in policy_models]
    
    def _to_domain(self, policy_model: PolicyModel) -> Policy:
        """Convert SQLAlchemy model to domain entity"""
        from ...domain.entities.policy import PolicyType, PolicyStatus
        
        return Policy(
            id=policy_model.id,  # Already a UUID object
            title=policy_model.title,
            description=policy_model.description,
            content=policy_model.content,
            policy_type=PolicyType(policy_model.policy_type),
            status=PolicyStatus(policy_model.status),
            organization_id=policy_model.organization_id,
            owner_id=policy_model.owner_id,
            created_at=policy_model.created_at,
            updated_at=policy_model.updated_at,
            effective_date=policy_model.effective_date,
            expiry_date=policy_model.expiry_date,
            tags=policy_model.tags or [],
            metadata=policy_model.extra_metadata or {}
        )


class SQLAlchemyRiskRepository:
    """SQLAlchemy implementation of RiskRepository - simplified for demo"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, risk: Risk) -> Risk:
        """Create a new risk"""
        risk_model = RiskModel(
            id=str(risk.id),
            title=risk.title,
            description=risk.description,
            category=risk.category.value,
            status=risk.status.value,
            organization_id=risk.organization_id,
            owner_id=risk.owner_id,
            created_by=risk.created_by,
            created_at=risk.created_at,
            updated_at=risk.updated_at
        )
        self.session.add(risk_model)
        self.session.commit()
        self.session.refresh(risk_model)
        return self._to_domain(risk_model)
    
    async def get_by_id(self, risk_id: str) -> Optional[Risk]:
        """Get risk by ID"""
        risk_model = await self.session.get(RiskModel, risk_id)
        if risk_model:
            return self._to_domain(risk_model)
        return None
    
    async def get_by_title(self, title: str) -> Optional[Risk]:
        """Get risk by title"""
        risk_model = self.session.query(RiskModel).filter(RiskModel.title == title).first()
        if risk_model:
            return self._to_domain(risk_model)
        return None
    
    async def update(self, risk: Risk) -> Risk:
        """Update risk"""
        risk_model = await self.session.get(RiskModel, str(risk.id))
        if risk_model:
            risk_model.title = risk.title
            risk_model.description = risk.description
            risk_model.risk_type = risk.risk_type
            risk_model.category = risk.category
            risk_model.status = risk.status
            risk_model.owner_id = str(risk.owner_id) if risk.owner_id else None
            risk_model.department_id = str(risk.department_id) if risk.department_id else None
            risk_model.organization_id = str(risk.organization_id) if risk.organization_id else None
            risk_model.likelihood = risk.likelihood
            risk_model.impact = risk.impact
            risk_model.risk_score = risk.risk_score
            risk_model.updated_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(risk_model)
            return self._to_domain(risk_model)
        raise ValueError(f"Risk with ID {risk.id} not found")
    
    async def delete(self, risk_id: str) -> bool:
        """Delete risk"""
        risk_model = await self.session.get(RiskModel, risk_id)
        if risk_model:
            await self.session.delete(risk_model)
            await self.session.commit()
            return True
        return False
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Risk]:
        """List risks with pagination"""
        risk_models = self.session.query(RiskModel).offset(skip).limit(limit).all()
        return [self._to_domain(risk_model) for risk_model in risk_models]
    
    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Risk]:
        """Search risks by query"""
        risk_models = self.session.query(RiskModel).filter(
            or_(
                RiskModel.title.ilike(f"%{query}%"),
                RiskModel.description.ilike(f"%{query}%"),
                RiskModel.risk_type.ilike(f"%{query}%"),
                RiskModel.category.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
        return [self._to_domain(risk_model) for risk_model in risk_models]
    
    def _to_domain(self, risk_model: RiskModel) -> Risk:
        """Convert SQLAlchemy model to domain entity"""
        from ...domain.entities.risk import RiskCategory, RiskStatus
        
        return Risk(
            id=risk_model.id,  # Already a UUID object
            title=risk_model.title,
            description=risk_model.description,
            category=RiskCategory(risk_model.category),
            status=RiskStatus(risk_model.status),
            organization_id=risk_model.organization_id,
            owner_id=risk_model.owner_id,
            created_by=risk_model.created_by,
            created_at=risk_model.created_at,
            updated_at=risk_model.updated_at
        )


# Add other repository implementations here...
# For brevity, I'll add a few more key ones

class SQLAlchemyOrganizationRepository:
    """SQLAlchemy implementation of OrganizationRepository - simplified for demo"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, organization: Organization) -> Organization:
        """Create a new organization"""
        org_model = OrganizationModel(
            id=str(organization.id),
            name=organization.name,
            description=organization.description,
            organization_type=organization.organization_type,
            industry=organization.industry,
            size=organization.size,
            address=organization.address,
            contact_email=organization.contact_email,
            contact_phone=organization.contact_phone,
            website=organization.website,
            is_active=organization.is_active,
            created_at=organization.created_at,
            updated_at=organization.updated_at
        )
        self.session.add(org_model)
        self.session.commit()
        self.session.refresh(org_model)
        return self._to_domain(org_model)
    
    def get_by_id(self, org_id: str) -> Optional[Organization]:
        """Get organization by ID"""
        org_model = self.session.get(OrganizationModel, org_id)
        if org_model:
            return self._to_domain(org_model)
        return None
    
    def get_by_name(self, name: str) -> Optional[Organization]:
        """Get organization by name"""
        org_model = self.session.query(OrganizationModel).filter(OrganizationModel.name == name).first()
        if org_model:
            return self._to_domain(org_model)
        return None
    
    def update(self, organization: Organization) -> Organization:
        """Update organization"""
        org_model = self.session.get(OrganizationModel, str(organization.id))
        if org_model:
            org_model.name = organization.name
            org_model.description = organization.description
            org_model.organization_type = organization.organization_type
            org_model.industry = organization.industry
            org_model.size = organization.size
            org_model.address = organization.address
            org_model.contact_email = organization.contact_email
            org_model.contact_phone = organization.contact_phone
            org_model.website = organization.website
            org_model.is_active = organization.is_active
            org_model.updated_at = datetime.utcnow()
            self.session.commit()
            self.session.refresh(org_model)
            return self._to_domain(org_model)
        raise ValueError(f"Organization with ID {organization.id} not found")
    
    def delete(self, org_id: str) -> bool:
        """Delete organization"""
        org_model = self.session.get(OrganizationModel, org_id)
        if org_model:
            self.session.delete(org_model)
            self.session.commit()
            return True
        return False
    
    def list(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        """List organizations with pagination"""
        org_models = self.session.query(OrganizationModel).offset(skip).limit(limit).all()
        return [self._to_domain(org_model) for org_model in org_models]
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Organization]:
        """Search organizations by query"""
        org_models = self.session.query(OrganizationModel).filter(
            or_(
                OrganizationModel.name.ilike(f"%{query}%"),
                OrganizationModel.description.ilike(f"%{query}%"),
                OrganizationModel.industry.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
        return [self._to_domain(org_model) for org_model in org_models]
    
    def _to_domain(self, org_model: OrganizationModel) -> Organization:
        """Convert SQLAlchemy model to domain entity"""
        return Organization(
            id=org_model.id,  # Already a UUID object
            name=org_model.name,
            description=org_model.description,
            organization_type=org_model.organization_type,
            industry=org_model.industry,
            size=org_model.size,
            address=org_model.address,
            contact_email=org_model.contact_email,
            contact_phone=org_model.contact_phone,
            website=org_model.website,
            is_active=org_model.is_active,
            created_at=org_model.created_at,
            updated_at=org_model.updated_at
        )


class SQLAlchemyAuditLogRepository:
    """SQLAlchemy implementation of AuditLogRepository"""
    
    def __init__(self):
        self.session_factory = None
    
    def set_session_factory(self, session_factory):
        """Set the session factory"""
        self.session_factory = session_factory
    
    def create(self, audit_log):
        """Create a new audit log entry"""
        from ...domain.entities.audit_log import AuditLog
        
        session = self.session_factory()
        try:
            audit_log_model = AuditLogModel(
                id=audit_log.id,
                user_id=audit_log.user_id,
                action=audit_log.action.value,
                resource=audit_log.resource.value,
                resource_id=audit_log.resource_id,
                description=audit_log.details,
                ip_address=audit_log.ip_address,
                user_agent=audit_log.user_agent,
                severity=audit_log.severity.value if audit_log.severity else None,
                timestamp=audit_log.created_at
            )
            session.add(audit_log_model)
            session.commit()
            return audit_log
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_by_id(self, audit_log_id):
        """Get audit log by ID"""
        session = self.session_factory()
        try:
            audit_log_model = session.query(AuditLogModel).filter(AuditLogModel.id == audit_log_id).first()
            if audit_log_model:
                return self._to_domain(audit_log_model)
            return None
        finally:
            session.close()
    
    def get_by_user_id(self, user_id):
        """Get audit logs by user ID"""
        session = self.session_factory()
        try:
            audit_log_models = session.query(AuditLogModel).filter(
                AuditLogModel.user_id == user_id
            ).order_by(desc(AuditLogModel.timestamp)).all()
            return [self._to_domain(model) for model in audit_log_models]
        finally:
            session.close()
    
    def get_by_resource(self, resource, resource_id):
        """Get audit logs by resource"""
        session = self.session_factory()
        try:
            audit_log_models = session.query(AuditLogModel).filter(
                and_(
                    AuditLogModel.resource == resource.value,
                    AuditLogModel.resource_id == resource_id
                )
            ).order_by(desc(AuditLogModel.timestamp)).all()
            return [self._to_domain(model) for model in audit_log_models]
        finally:
            session.close()
    
    def get_by_date_range(self, start_date, end_date):
        """Get audit logs by date range"""
        session = self.session_factory()
        try:
            audit_log_models = session.query(AuditLogModel).filter(
                and_(
                    AuditLogModel.created_at >= start_date,
                    AuditLogModel.created_at <= end_date
                )
            ).order_by(desc(AuditLogModel.timestamp)).all()
            return [self._to_domain(model) for model in audit_log_models]
        finally:
            session.close()
    
    def _to_domain(self, audit_log_model):
        """Convert SQLAlchemy model to domain entity"""
        from ...domain.entities.audit_log import AuditLog, AuditAction, AuditResource, AuditSeverity
        
        return AuditLog(
            id=audit_log_model.id,
            user_id=audit_log_model.user_id,
            action=AuditAction(audit_log_model.action),
            resource=AuditResource(audit_log_model.resource),
            resource_id=audit_log_model.resource_id,
            details=audit_log_model.details,
            ip_address=audit_log_model.ip_address,
            user_agent=audit_log_model.user_agent,
            severity=AuditSeverity(audit_log_model.severity) if audit_log_model.severity else None,
            created_at=audit_log_model.timestamp
        )
