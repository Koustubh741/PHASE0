"""
Dependency injection container for the GRC platform.
Wires together repositories, services, and other dependencies.
"""

from typing import Dict, Type, Any
from functools import lru_cache
from sqlalchemy.orm import Session

from ..application.services.user_service import UserService
from ..application.services.policy_service import PolicyService
from ..application.services.risk_service import RiskService
from ..application.services.organization_service import OrganizationService
from ..application.services.auth_service import AuthService
from ..application.services.audit_service import AuditService
from ..application.services.bfsi_ai_service import BFSIAIService

from .persistence.repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyPolicyRepository,
    SQLAlchemyRiskRepository,
    SQLAlchemyOrganizationRepository,
    SQLAlchemyAuditLogRepository,
)

from .database import get_db, get_async_session


class DependencyContainer:
    """Dependency injection container"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._repositories: Dict[str, Any] = {}
    
    def register_repository(self, name: str, repository_class: Type, session: Session):
        """Register a repository with the container"""
        self._repositories[name] = repository_class(session)
    
    def register_service(self, name: str, service_instance: Any):
        """Register a service with the container"""
        self._services[name] = service_instance
    
    def get_repository(self, name: str):
        """Get a repository from the container"""
        return self._repositories.get(name)
    
    def get_service(self, name: str):
        """Get a service from the container"""
        return self._services.get(name)


# Global dependency container instance
_container = DependencyContainer()


def get_container() -> DependencyContainer:
    """Get the global dependency container"""
    return _container


def setup_dependencies(session: Session):
    """Setup all dependencies in the container"""
    # Register repositories
    _container.register_repository("user", SQLAlchemyUserRepository, session)
    _container.register_repository("policy", SQLAlchemyPolicyRepository, session)
    _container.register_repository("risk", SQLAlchemyRiskRepository, session)
    _container.register_repository("organization", SQLAlchemyOrganizationRepository, session)
    _container.register_repository("audit_log", SQLAlchemyAuditLogRepository, session)
    
    # Register services
    user_repo = _container.get_repository("user")
    policy_repo = _container.get_repository("policy")
    risk_repo = _container.get_repository("risk")
    organization_repo = _container.get_repository("organization")
    audit_log_repo = _container.get_repository("audit_log")
    
    _container.register_service("user", UserService(user_repo))
    _container.register_service("policy", PolicyService(policy_repo))
    _container.register_service("risk", RiskService(risk_repo))
    _container.register_service("organization", OrganizationService(organization_repo))
    _container.register_service("audit", AuditService(audit_log_repo))
    _container.register_service("bfsi_ai", BFSIAIService(policy_repo, risk_repo, audit_log_repo))
    _container.register_service("auth", AuthService(user_repo, audit_log_repo))


# FastAPI dependency functions
def get_user_service() -> UserService:
    """Get user service dependency"""
    return _container.get_service("user")


def get_policy_service() -> PolicyService:
    """Get policy service dependency"""
    return _container.get_service("policy")


def get_risk_service() -> RiskService:
    """Get risk service dependency"""
    return _container.get_service("risk")


def get_organization_service() -> OrganizationService:
    """Get organization service dependency"""
    return _container.get_service("organization")


def get_auth_service() -> AuthService:
    """Get auth service dependency"""
    return _container.get_service("auth")


def get_audit_service() -> AuditService:
    """Get audit service dependency"""
    return _container.get_service("audit")


def get_bfsi_ai_service() -> BFSIAIService:
    """Get BFSI AI service dependency"""
    return _container.get_service("bfsi_ai")


# Initialize dependencies when module is imported
@lru_cache()
def initialize_dependencies():
    """Initialize dependencies with database session"""
    from .database import SessionLocal
    session = SessionLocal()
    setup_dependencies(session)
    return session
