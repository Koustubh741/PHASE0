"""
SQLAlchemy Database Models
Database schema definitions for GRC Platform
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, JSON, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class UserModel(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    organization_id = Column(String(100), nullable=False, index=True)
    department = Column(String(100), nullable=True)
    job_title = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    password_hash = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    email_verification_token = Column(String(255), nullable=True)
    email_verified = Column(Boolean, default=False, nullable=False)
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    two_factor_secret = Column(String(255), nullable=True)
    extra_metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationships
    audit_logs = relationship("AuditLogModel", back_populates="user")
    
    # Indexes
    __table_args__ = (
        Index('idx_users_org_status', 'organization_id', 'status'),
        Index('idx_users_org_role', 'organization_id', 'role'),
        Index('idx_users_created_at', 'created_at'),
        Index('idx_users_last_login', 'last_login'),
        UniqueConstraint('username', name='uq_users_username'),
        UniqueConstraint('email', name='uq_users_email'),
    )


class PolicyModel(Base):
    """Policy database model"""
    __tablename__ = "policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    policy_type = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    organization_id = Column(String(100), nullable=False, index=True)
    owner_id = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    effective_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    tags = Column(JSON, default=list, nullable=False)
    extra_metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationships
    versions = relationship("PolicyVersionModel", back_populates="policy", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLogModel", back_populates="policy")
    
    # Indexes
    __table_args__ = (
        Index('idx_policies_org_status', 'organization_id', 'status'),
        Index('idx_policies_org_type', 'organization_id', 'policy_type'),
        Index('idx_policies_owner', 'owner_id'),
        Index('idx_policies_effective_date', 'effective_date'),
        Index('idx_policies_expiry_date', 'expiry_date'),
        Index('idx_policies_created_at', 'created_at'),
    )


class PolicyVersionModel(Base):
    """Policy version database model"""
    __tablename__ = "policy_versions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"), nullable=False)
    version_number = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(100), nullable=False)
    change_summary = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    policy = relationship("PolicyModel", back_populates="versions")
    
    # Indexes
    __table_args__ = (
        Index('idx_policy_versions_policy_id', 'policy_id'),
        Index('idx_policy_versions_created_at', 'created_at'),
        Index('idx_policy_versions_active', 'is_active'),
    )


class RiskModel(Base):
    """Risk database model"""
    __tablename__ = "risks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    organization_id = Column(String(100), nullable=False, index=True)
    owner_id = Column(String(100), nullable=False, index=True)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    source = Column(String(255), nullable=True)
    business_impact = Column(Text, nullable=True)
    affected_assets = Column(JSON, default=list, nullable=False)
    affected_processes = Column(JSON, default=list, nullable=False)
    affected_systems = Column(JSON, default=list, nullable=False)
    treatment_strategy = Column(String(50), nullable=True)
    treatment_plan = Column(Text, nullable=True)
    next_review_date = Column(DateTime(timezone=True), nullable=True)
    review_frequency_days = Column(Integer, default=90, nullable=False)
    escalation_threshold = Column(Integer, nullable=True)
    tags = Column(JSON, default=list, nullable=False)
    extra_metadata = Column(JSON, default=dict, nullable=False)
    external_references = Column(JSON, default=list, nullable=False)
    
    # Current assessment fields
    current_likelihood = Column(String(20), nullable=True)
    current_impact = Column(String(20), nullable=True)
    current_risk_score = Column(Integer, nullable=True)
    current_risk_level = Column(String(20), nullable=True)
    assessed_by = Column(String(100), nullable=True)
    assessed_at = Column(DateTime(timezone=True), nullable=True)
    assessment_notes = Column(Text, nullable=True)
    confidence_level = Column(Integer, default=5, nullable=False)
    
    # Relationships
    assessments = relationship("RiskAssessmentModel", back_populates="risk", cascade="all, delete-orphan")
    treatments = relationship("RiskTreatmentModel", back_populates="risk", cascade="all, delete-orphan")
    mitigations = relationship("RiskMitigationModel", back_populates="risk", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLogModel", back_populates="risk")
    
    # Indexes
    __table_args__ = (
        Index('idx_risks_org_status', 'organization_id', 'status'),
        Index('idx_risks_org_category', 'organization_id', 'category'),
        Index('idx_risks_owner', 'owner_id'),
        Index('idx_risks_review_date', 'next_review_date'),
        Index('idx_risks_risk_level', 'current_risk_level'),
        Index('idx_risks_created_at', 'created_at'),
    )


class RiskAssessmentModel(Base):
    """Risk assessment database model"""
    __tablename__ = "risk_assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_id = Column(UUID(as_uuid=True), ForeignKey("risks.id"), nullable=False)
    likelihood = Column(String(20), nullable=False)
    impact = Column(String(20), nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String(20), nullable=False)
    assessed_by = Column(String(100), nullable=False)
    assessed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)
    confidence_level = Column(Integer, default=5, nullable=False)
    
    # Relationships
    risk = relationship("RiskModel", back_populates="assessments")
    
    # Indexes
    __table_args__ = (
        Index('idx_risk_assessments_risk_id', 'risk_id'),
        Index('idx_risk_assessments_assessed_at', 'assessed_at'),
        Index('idx_risk_assessments_risk_level', 'risk_level'),
    )


class RiskTreatmentModel(Base):
    """Risk treatment database model"""
    __tablename__ = "risk_treatments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_id = Column(UUID(as_uuid=True), ForeignKey("risks.id"), nullable=False)
    strategy = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(String(100), nullable=False)
    target_date = Column(DateTime(timezone=True), nullable=True)
    cost_estimate = Column(Integer, nullable=True)  # Store as cents
    status = Column(String(50), default="planned", nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    risk = relationship("RiskModel", back_populates="treatments")
    
    # Indexes
    __table_args__ = (
        Index('idx_risk_treatments_risk_id', 'risk_id'),
        Index('idx_risk_treatments_owner', 'owner'),
        Index('idx_risk_treatments_status', 'status'),
        Index('idx_risk_treatments_target_date', 'target_date'),
    )


class RiskMitigationModel(Base):
    """Risk mitigation database model"""
    __tablename__ = "risk_mitigations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_id = Column(UUID(as_uuid=True), ForeignKey("risks.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(String(100), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    completion_percentage = Column(Integer, default=0, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    risk = relationship("RiskModel", back_populates="mitigations")
    
    # Indexes
    __table_args__ = (
        Index('idx_risk_mitigations_risk_id', 'risk_id'),
        Index('idx_risk_mitigations_owner', 'owner'),
        Index('idx_risk_mitigations_status', 'status'),
        Index('idx_risk_mitigations_due_date', 'due_date'),
    )


class ControlModel(Base):
    """Control database model"""
    __tablename__ = "controls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    control_type = Column(String(50), nullable=False, index=True)
    control_nature = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, index=True)
    organization_id = Column(String(100), nullable=False, index=True)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    objective = Column(Text, nullable=True)
    risk_mitigated = Column(JSON, default=list, nullable=False)
    applicable_regulations = Column(JSON, default=list, nullable=False)
    applicable_frameworks = Column(JSON, default=list, nullable=False)
    implementation_date = Column(DateTime(timezone=True), nullable=True)
    implementation_notes = Column(Text, nullable=True)
    cost_estimate = Column(Integer, nullable=True)  # Store as cents
    last_test_date = Column(DateTime(timezone=True), nullable=True)
    next_test_date = Column(DateTime(timezone=True), nullable=True)
    test_frequency_days = Column(Integer, default=90, nullable=False)
    primary_owner = Column(String(100), nullable=True)
    effectiveness_rating = Column(Integer, nullable=True)
    effectiveness_notes = Column(Text, nullable=True)
    last_effectiveness_review = Column(DateTime(timezone=True), nullable=True)
    dependent_controls = Column(JSON, default=list, nullable=False)
    supporting_processes = Column(JSON, default=list, nullable=False)
    supporting_systems = Column(JSON, default=list, nullable=False)
    tags = Column(JSON, default=list, nullable=False)
    extra_metadata = Column(JSON, default=dict, nullable=False)
    external_references = Column(JSON, default=list, nullable=False)
    
    # Relationships
    owners = relationship("ControlOwnerModel", back_populates="control", cascade="all, delete-orphan")
    tests = relationship("ControlTestModel", back_populates="control", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLogModel", back_populates="control")
    
    # Indexes
    __table_args__ = (
        Index('idx_controls_org_status', 'organization_id', 'status'),
        Index('idx_controls_org_type', 'organization_id', 'control_type'),
        Index('idx_controls_primary_owner', 'primary_owner'),
        Index('idx_controls_next_test_date', 'next_test_date'),
        Index('idx_controls_effectiveness', 'effectiveness_rating'),
        Index('idx_controls_created_at', 'created_at'),
    )


class ControlOwnerModel(Base):
    """Control owner database model"""
    __tablename__ = "control_owners"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(UUID(as_uuid=True), ForeignKey("controls.id"), nullable=False)
    user_id = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    assigned_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_primary = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    control = relationship("ControlModel", back_populates="owners")
    
    # Indexes
    __table_args__ = (
        Index('idx_control_owners_control_id', 'control_id'),
        Index('idx_control_owners_user_id', 'user_id'),
        Index('idx_control_owners_primary', 'is_primary'),
    )


class ControlTestModel(Base):
    """Control test database model"""
    __tablename__ = "control_tests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(UUID(as_uuid=True), ForeignKey("controls.id"), nullable=False)
    test_name = Column(String(255), nullable=False)
    test_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    tester = Column(String(100), nullable=False)
    test_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    result = Column(String(50), nullable=False)
    findings = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    evidence = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    control = relationship("ControlModel", back_populates="tests")
    
    # Indexes
    __table_args__ = (
        Index('idx_control_tests_control_id', 'control_id'),
        Index('idx_control_tests_test_date', 'test_date'),
        Index('idx_control_tests_result', 'result'),
        Index('idx_control_tests_tester', 'tester'),
    )


class IssueModel(Base):
    """Issue database model"""
    __tablename__ = "issues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    issue_type = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    priority = Column(String(20), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    organization_id = Column(String(100), nullable=False, index=True)
    reported_by = Column(String(100), nullable=False)
    assigned_to = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    root_cause = Column(Text, nullable=True)
    impact_assessment = Column(Text, nullable=True)
    business_impact = Column(Text, nullable=True)
    affected_areas = Column(JSON, default=list, nullable=False)
    affected_processes = Column(JSON, default=list, nullable=False)
    affected_systems = Column(JSON, default=list, nullable=False)
    detected_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    resolved_date = Column(DateTime(timezone=True), nullable=True)
    closed_date = Column(DateTime(timezone=True), nullable=True)
    related_risks = Column(JSON, default=list, nullable=False)
    related_controls = Column(JSON, default=list, nullable=False)
    related_policies = Column(JSON, default=list, nullable=False)
    related_audits = Column(JSON, default=list, nullable=False)
    financial_impact = Column(Integer, nullable=True)  # Store as cents
    remediation_cost = Column(Integer, nullable=True)  # Store as cents
    regulatory_implications = Column(JSON, default=list, nullable=False)
    compliance_framework = Column(String(100), nullable=True)
    regulatory_notification_required = Column(Boolean, default=False, nullable=False)
    regulatory_notification_date = Column(DateTime(timezone=True), nullable=True)
    escalated_to = Column(String(100), nullable=True)
    escalation_reason = Column(Text, nullable=True)
    escalation_date = Column(DateTime(timezone=True), nullable=True)
    tags = Column(JSON, default=list, nullable=False)
    extra_metadata = Column(JSON, default=dict, nullable=False)
    external_references = Column(JSON, default=list, nullable=False)
    
    # Relationships
    actions = relationship("IssueActionModel", back_populates="issue", cascade="all, delete-orphan")
    comments = relationship("IssueCommentModel", back_populates="issue", cascade="all, delete-orphan")
    evidence = relationship("IssueEvidenceModel", back_populates="issue", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLogModel", back_populates="issue")
    
    # Indexes
    __table_args__ = (
        Index('idx_issues_org_status', 'organization_id', 'status'),
        Index('idx_issues_org_type', 'organization_id', 'issue_type'),
        Index('idx_issues_priority', 'priority'),
        Index('idx_issues_assigned_to', 'assigned_to'),
        Index('idx_issues_due_date', 'due_date'),
        Index('idx_issues_created_at', 'created_at'),
        Index('idx_issues_resolved_date', 'resolved_date'),
    )


class IssueActionModel(Base):
    """Issue action database model"""
    __tablename__ = "issue_actions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id"), nullable=False)
    action_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    assigned_to = Column(String(100), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completed_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    issue = relationship("IssueModel", back_populates="actions")
    
    # Indexes
    __table_args__ = (
        Index('idx_issue_actions_issue_id', 'issue_id'),
        Index('idx_issue_actions_assigned_to', 'assigned_to'),
        Index('idx_issue_actions_status', 'status'),
        Index('idx_issue_actions_due_date', 'due_date'),
    )


class IssueCommentModel(Base):
    """Issue comment database model"""
    __tablename__ = "issue_comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id"), nullable=False)
    comment = Column(Text, nullable=False)
    author_id = Column(String(100), nullable=False)
    author_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_internal = Column(Boolean, default=False, nullable=False)
    attachments = Column(JSON, default=list, nullable=False)
    
    # Relationships
    issue = relationship("IssueModel", back_populates="comments")
    
    # Indexes
    __table_args__ = (
        Index('idx_issue_comments_issue_id', 'issue_id'),
        Index('idx_issue_comments_author_id', 'author_id'),
        Index('idx_issue_comments_created_at', 'created_at'),
    )


class IssueEvidenceModel(Base):
    """Issue evidence database model"""
    __tablename__ = "issue_evidence"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id"), nullable=False)
    evidence_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=True)
    url = Column(String(500), nullable=True)
    collected_by = Column(String(100), nullable=False)
    collected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    verified_by = Column(String(100), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    issue = relationship("IssueModel", back_populates="evidence")
    
    # Indexes
    __table_args__ = (
        Index('idx_issue_evidence_issue_id', 'issue_id'),
        Index('idx_issue_evidence_collected_by', 'collected_by'),
        Index('idx_issue_evidence_collected_at', 'collected_at'),
        Index('idx_issue_evidence_verified', 'verified'),
    )


class AuditLogModel(Base):
    """Audit log database model"""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String(50), nullable=False, index=True)
    resource = Column(String(50), nullable=False, index=True)
    resource_id = Column(String(100), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user_name = Column(String(255), nullable=True)
    organization_id = Column(String(100), nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True, index=True)
    user_agent = Column(Text, nullable=True)
    session_id = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=False)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    severity = Column(String(20), nullable=False, index=True)
    source_system = Column(String(100), nullable=True)
    source_module = Column(String(100), nullable=True)
    correlation_id = Column(String(255), nullable=True, index=True)
    success = Column(Boolean, default=True, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    extra_metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="audit_logs")
    policy = relationship("PolicyModel", back_populates="audit_logs")
    risk = relationship("RiskModel", back_populates="audit_logs")
    control = relationship("ControlModel", back_populates="audit_logs")
    issue = relationship("IssueModel", back_populates="audit_logs")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_logs_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_audit_logs_org_timestamp', 'organization_id', 'timestamp'),
        Index('idx_audit_logs_resource_timestamp', 'resource', 'resource_id', 'timestamp'),
        Index('idx_audit_logs_action_timestamp', 'action', 'timestamp'),
        Index('idx_audit_logs_severity_timestamp', 'severity', 'timestamp'),
        Index('idx_audit_logs_ip_timestamp', 'ip_address', 'timestamp'),
        Index('idx_audit_logs_success_timestamp', 'success', 'timestamp'),
    )
