"""
Demo data seeding script for GRC platform.
Creates sample organizations, users, policies, risks, and other demo data.
"""

import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4
import asyncio

# Add the src directory to the Python path
src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, str(src_dir))

from core.infrastructure.database import SessionLocal, get_db
from core.infrastructure.database.sqlalchemy_models import *
from core.domain.entities.user import User, UserRole, UserStatus
from core.domain.entities.organization import Organization
from core.domain.entities.policy import Policy, PolicyType, PolicyStatus
from core.domain.entities.risk import Risk, RiskStatus, RiskCategory, RiskLikelihood, RiskImpact
# Services not needed for seeding - using repositories directly
from core.infrastructure.persistence.repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyOrganizationRepository,
    SQLAlchemyPolicyRepository,
    SQLAlchemyRiskRepository
)


async def create_demo_organizations(session):
    """Create demo organizations"""
    print("Creating demo organizations...")
    
    org_repo = SQLAlchemyOrganizationRepository(session)
    
    # Create main demo organization
    demo_org = Organization(
        id=uuid4(),
        name="GRC Demo Corporation",
        description="A comprehensive GRC platform demonstration organization",
        organization_type="Corporation",
        industry="Financial Services",
        size="Large (1000+ employees)",
        address="123 GRC Street, Compliance City, CC 12345",
        contact_email="admin@grc-demo.com",
        contact_phone="+1-555-GRC-DEMO",
        website="https://grc-demo.com",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    org_repo.create(demo_org)
    print(f"✓ Created organization: {demo_org.name}")
    
    # Create subsidiary organization
    subsidiary_org = Organization(
        id=uuid4(),
        name="GRC Demo Subsidiary",
        description="A subsidiary company for GRC platform demonstration",
        organization_type="Subsidiary",
        industry="Technology",
        size="Medium (100-999 employees)",
        address="456 Subsidiary Ave, Tech City, TC 67890",
        contact_email="admin@subsidiary-demo.com",
        contact_phone="+1-555-SUB-DEMO",
        website="https://subsidiary-demo.com",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    org_repo.create(subsidiary_org)
    print(f"✓ Created organization: {subsidiary_org.name}")
    
    return demo_org, subsidiary_org


async def create_demo_users(session, organizations):
    """Create demo users"""
    print("Creating demo users...")
    
    user_repo = SQLAlchemyUserRepository(session)
    main_org, subsidiary_org = organizations
    
    # Create admin user
    admin_user = User(
        id=uuid4(),
        email="admin@grc-demo.com",
        username="admin",
        first_name="GRC",
        last_name="Admin",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        organization_id=str(main_org.id),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j4H4M8W2y"  # "admin123"
    )
    
    user_repo.create(admin_user)
    print(f"✓ Created admin user: {admin_user.email}")
    
    # Create compliance officer
    compliance_user = User(
        id=uuid4(),
        email="compliance@grc-demo.com",
        username="compliance_officer",
        first_name="Sarah",
        last_name="Compliance",
        role=UserRole.COMPLIANCE_MANAGER,
        status=UserStatus.ACTIVE,
        organization_id=str(main_org.id),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j4H4M8W2y"  # "admin123"
    )
    
    user_repo.create(compliance_user)
    print(f"✓ Created compliance officer: {compliance_user.email}")
    
    # Create risk manager
    risk_user = User(
        id=uuid4(),
        email="risk@grc-demo.com",
        username="risk_manager",
        first_name="John",
        last_name="Risk",
        role=UserRole.RISK_OWNER,
        status=UserStatus.ACTIVE,
        organization_id=str(main_org.id),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j4H4M8W2y"  # "admin123"
    )
    
    user_repo.create(risk_user)
    print(f"✓ Created risk manager: {risk_user.email}")
    
    # Create regular user
    regular_user = User(
        id=uuid4(),
        email="user@grc-demo.com",
        username="demo_user",
        first_name="Demo",
        last_name="User",
        role=UserRole.VIEWER,
        status=UserStatus.ACTIVE,
        organization_id=str(subsidiary_org.id),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j4H4M8W2y"  # "admin123"
    )
    
    user_repo.create(regular_user)
    print(f"✓ Created regular user: {regular_user.email}")
    
    return [admin_user, compliance_user, risk_user, regular_user]


async def create_demo_policies(session, organizations, users):
    """Create demo policies"""
    print("Creating demo policies...")
    
    policy_repo = SQLAlchemyPolicyRepository(session)
    main_org = organizations[0]
    compliance_user = users[1]
    
    policies_data = [
        {
            "title": "Information Security Policy",
            "description": "Comprehensive policy governing the protection of organizational information assets, including data classification, access controls, and incident response procedures.",
            "content": "This policy establishes the framework for protecting organizational information assets through proper classification, access controls, and incident response procedures.",
            "policy_type": PolicyType.SECURITY,
            "status": PolicyStatus.ACTIVE,
            "effective_date": datetime.utcnow() - timedelta(days=30),
            "expiry_date": datetime.utcnow() + timedelta(days=335)
        },
        {
            "title": "Data Privacy and Protection Policy",
            "description": "Policy outlining procedures for handling personal data in compliance with GDPR, CCPA, and other privacy regulations.",
            "content": "This policy defines how personal data is collected, processed, stored, and protected in compliance with applicable privacy regulations.",
            "policy_type": PolicyType.COMPLIANCE,
            "status": PolicyStatus.ACTIVE,
            "effective_date": datetime.utcnow() - timedelta(days=15),
            "expiry_date": datetime.utcnow() + timedelta(days=350)
        },
        {
            "title": "Risk Management Framework",
            "description": "Establishes the organization's approach to identifying, assessing, and managing operational, financial, and strategic risks.",
            "content": "This framework provides the methodology and processes for comprehensive risk management across the organization.",
            "policy_type": PolicyType.GOVERNANCE,
            "status": PolicyStatus.ACTIVE,
            "effective_date": datetime.utcnow() - timedelta(days=45),
            "expiry_date": datetime.utcnow() + timedelta(days=320)
        },
        {
            "title": "Business Continuity and Disaster Recovery Policy",
            "description": "Defines procedures for maintaining business operations during disruptions and recovering from disasters.",
            "content": "This policy establishes procedures for maintaining business operations and recovering from various types of disruptions.",
            "policy_type": PolicyType.OPERATIONAL,
            "status": PolicyStatus.DRAFT,
            "effective_date": datetime.utcnow() + timedelta(days=30),
            "expiry_date": datetime.utcnow() + timedelta(days=395)
        },
        {
            "title": "Employee Code of Conduct",
            "description": "Standards of behavior and ethical guidelines for all employees, including conflict of interest and reporting procedures.",
            "content": "This code establishes ethical standards and behavioral expectations for all employees.",
            "policy_type": PolicyType.GOVERNANCE,
            "status": PolicyStatus.ACTIVE,
            "effective_date": datetime.utcnow() - timedelta(days=60),
            "expiry_date": datetime.utcnow() + timedelta(days=305)
        },
        {
            "title": "Third-Party Vendor Management Policy",
            "description": "Guidelines for selecting, managing, and monitoring third-party vendors and service providers.",
            "content": "This policy establishes guidelines for managing third-party relationships and ensuring vendor compliance.",
            "policy_type": PolicyType.OPERATIONAL,
            "status": PolicyStatus.UNDER_REVIEW,
            "effective_date": datetime.utcnow() - timedelta(days=20),
            "expiry_date": datetime.utcnow() + timedelta(days=345)
        },
        {
            "title": "Financial Controls and Audit Policy",
            "description": "Internal controls and audit procedures for financial reporting and compliance with accounting standards.",
            "content": "This policy establishes internal controls and audit procedures for financial reporting and compliance.",
            "policy_type": PolicyType.FINANCIAL,
            "status": PolicyStatus.ACTIVE,
            "effective_date": datetime.utcnow() - timedelta(days=90),
            "expiry_date": datetime.utcnow() + timedelta(days=275)
        },
        {
            "title": "Cybersecurity Incident Response Plan",
            "description": "Detailed procedures for detecting, responding to, and recovering from cybersecurity incidents.",
            "content": "This plan provides detailed procedures for cybersecurity incident detection, response, and recovery.",
            "policy_type": PolicyType.SECURITY,
            "status": PolicyStatus.ACTIVE,
            "effective_date": datetime.utcnow() - timedelta(days=10),
            "expiry_date": datetime.utcnow() + timedelta(days=355)
        }
    ]
    
    created_policies = []
    for policy_data in policies_data:
        policy = Policy(
            id=uuid4(),
            title=policy_data["title"],
            description=policy_data["description"],
            content=policy_data["content"],
            policy_type=policy_data["policy_type"],
            status=policy_data["status"],
            organization_id=str(main_org.id),
            owner_id=str(compliance_user.id),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            effective_date=policy_data["effective_date"],
            expiry_date=policy_data["expiry_date"]
        )
        
        policy_repo.create(policy)
        created_policies.append(policy)
        print(f"✓ Created policy: {policy.title}")
    
    return created_policies


async def create_demo_risks(session, organizations, users):
    """Create demo risks"""
    print("Creating demo risks...")
    
    risk_repo = SQLAlchemyRiskRepository(session)
    main_org = organizations[0]
    risk_user = users[2]
    
    risks_data = [
        {
            "title": "Data Breach Risk",
            "description": "Risk of unauthorized access to sensitive customer and employee data through cyber attacks or insider threats.",
            "category": RiskCategory.CYBERSECURITY,
            "status": RiskStatus.IDENTIFIED,
            "likelihood": RiskLikelihood.MEDIUM,
            "impact": RiskImpact.HIGH
        },
        {
            "title": "Regulatory Compliance Risk",
            "description": "Risk of non-compliance with evolving financial services regulations, resulting in penalties and reputational damage.",
            "category": RiskCategory.REGULATORY,
            "status": RiskStatus.IDENTIFIED,
            "likelihood": RiskLikelihood.MEDIUM,
            "impact": RiskImpact.HIGH
        },
        {
            "title": "Operational Disruption Risk",
            "description": "Risk of business operations disruption due to system failures, natural disasters, or supply chain issues.",
            "category": RiskCategory.OPERATIONAL,
            "status": RiskStatus.IDENTIFIED,
            "likelihood": RiskLikelihood.LOW,
            "impact": RiskImpact.HIGH
        },
        {
            "title": "Third-Party Vendor Risk",
            "description": "Risk associated with reliance on third-party vendors for critical business functions and data processing.",
            "category": RiskCategory.THIRD_PARTY,
            "status": RiskStatus.IDENTIFIED,
            "likelihood": RiskLikelihood.MEDIUM,
            "impact": RiskImpact.MEDIUM
        },
        {
            "title": "Financial Market Risk",
            "description": "Risk of losses due to adverse movements in interest rates, foreign exchange rates, or commodity prices.",
            "category": RiskCategory.FINANCIAL,
            "status": RiskStatus.IDENTIFIED,
            "likelihood": RiskLikelihood.MEDIUM,
            "impact": RiskImpact.MEDIUM
        },
        {
            "title": "Reputation Risk",
            "description": "Risk of damage to the organization's reputation due to negative publicity, customer complaints, or regulatory actions.",
            "category": RiskCategory.REPUTATIONAL,
            "status": RiskStatus.IDENTIFIED,
            "likelihood": RiskLikelihood.LOW,
            "impact": RiskImpact.HIGH
        }
    ]
    
    created_risks = []
    for risk_data in risks_data:
        risk = Risk(
            id=uuid4(),
            title=risk_data["title"],
            description=risk_data["description"],
            category=risk_data["category"],
            status=risk_data["status"],
            organization_id=str(main_org.id),
            owner_id=str(risk_user.id),
            created_by=str(risk_user.id),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        risk_repo.create(risk)
        created_risks.append(risk)
        print(f"✓ Created risk: {risk.title}")
    
    return created_risks


async def main():
    """Main function to seed demo data"""
    print("Starting GRC platform demo data seeding...")
    
    # Create database session
    session = SessionLocal()
    
    try:
        # Create demo data
        organizations = await create_demo_organizations(session)
        users = await create_demo_users(session, organizations)
        policies = await create_demo_policies(session, organizations, users)
        risks = await create_demo_risks(session, organizations, users)
        
        print("\n" + "="*50)
        print("Demo data seeding completed successfully!")
        print("="*50)
        print(f"✓ Created {len(organizations)} organizations")
        print(f"✓ Created {len(users)} users")
        print(f"✓ Created {len(policies)} policies")
        print(f"✓ Created {len(risks)} risks")
        print("\nDemo login credentials:")
        print("Email: admin@grc-demo.com")
        print("Password: admin123")
        print("="*50)
        
    except Exception as e:
        print(f"Error seeding demo data: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(main())
