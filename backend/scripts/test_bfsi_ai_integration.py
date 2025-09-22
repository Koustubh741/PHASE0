#!/usr/bin/env python3
"""
BFSI AI Integration Test Script
Tests the integration between BFSI AI agents and backend services
"""

import asyncio
import sys
import os
from datetime import datetime
from uuid import uuid4

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.infrastructure.database import SessionLocal
from core.infrastructure.persistence.repositories import (
    SQLAlchemyUserRepository, SQLAlchemyPolicyRepository, 
    SQLAlchemyRiskRepository, SQLAlchemyAuditLogRepository
)
from core.application.services.bfsi_ai_service import BFSIAIService, BFSIAnalysisRequest
from core.domain.entities.user import User, UserRole, UserStatus
from core.domain.entities.policy import Policy, PolicyType, PolicyStatus
from core.domain.entities.risk import Risk, RiskCategory, RiskStatus, RiskLikelihood, RiskImpact

async def test_bfsi_ai_integration():
    """
    Test BFSI AI integration with backend services
    """
    print("🤖 Testing BFSI AI Integration with GRC Platform...")
    
    try:
        # Initialize database session
        print("📡 Initializing database session...")
        session = SessionLocal()
        
        # Initialize repositories
        print("🔧 Initializing repositories...")
        user_repo = SQLAlchemyUserRepository(session)
        policy_repo = SQLAlchemyPolicyRepository(session)
        risk_repo = SQLAlchemyRiskRepository(session)
        audit_log_repo = SQLAlchemyAuditLogRepository()
        audit_log_repo.set_session_factory(lambda: session)
        
        # Initialize BFSI AI service
        print("🤖 Initializing BFSI AI service...")
        bfsi_ai_service = BFSIAIService(policy_repo, risk_repo, audit_log_repo)
        
        # Test 1: Create test user
        print("\n👤 Test 1: Creating test user...")
        test_user_id = str(uuid4())
        test_org_id = str(uuid4())
        test_user = User(
            id=test_user_id,
            username=f"bfsi_test_{uuid4().hex[:8]}@example.com",
            email=f"bfsi_test_{uuid4().hex[:8]}@example.com",
            first_name="BFSI",
            last_name="Test",
            password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/4Qz8K2K",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            organization_id=test_org_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        user_repo.create(test_user)
        print(f"✅ Test user created: {test_user.username}")
        
        # Test 2: Create test policy
        print("\n📋 Test 2: Creating test policy...")
        test_policy_id = str(uuid4())
        test_policy = Policy(
            id=test_policy_id,
            title="BFSI Test Policy",
            description="Test policy for BFSI AI integration",
            content="This is a test policy for BFSI AI integration testing.",
            policy_type=PolicyType.OPERATIONAL,
            status=PolicyStatus.ACTIVE,
            organization_id=test_org_id,
            owner_id=test_user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        policy_repo.create(test_policy)
        print(f"✅ Test policy created: {test_policy.title}")
        
        # Test 3: Test BFSI AI agent status
        print("\n🤖 Test 3: Testing BFSI AI agent status...")
        status_info = await bfsi_ai_service.get_agent_status()
        print(f"✅ Agent status: {status_info['status']}")
        print(f"✅ Agent capabilities: {', '.join(status_info['capabilities'])}")
        
        # Test 4: Test risk assessment
        print("\n🔍 Test 4: Testing BFSI risk assessment...")
        risk_request = BFSIAnalysisRequest(
            analysis_type="risk_assessment",
            business_unit="retail",
            industry_type="bfsi",
            context={"risk_factors": ["market_volatility", "regulatory_changes"]},
            user_id=test_user_id,
            organization_id=test_org_id
        )
        
        risk_result = await bfsi_ai_service.perform_risk_assessment(risk_request, test_user)
        print(f"✅ Risk assessment completed: {risk_result.analysis_id}")
        print(f"✅ Risk score: {risk_result.risk_score}")
        print(f"✅ Compliance score: {risk_result.compliance_score}")
        print(f"✅ Confidence score: {risk_result.confidence_score}")
        
        # Test 5: Test compliance check
        print("\n📊 Test 5: Testing BFSI compliance check...")
        compliance_request = BFSIAnalysisRequest(
            analysis_type="compliance_check",
            business_unit="commercial",
            industry_type="bfsi",
            context={"frameworks": ["SOX", "Basel III", "PCI DSS"]},
            user_id=test_user_id,
            organization_id=test_org_id
        )
        
        compliance_result = await bfsi_ai_service.perform_compliance_check(compliance_request, test_user)
        print(f"✅ Compliance check completed: {compliance_result.analysis_id}")
        print(f"✅ Risk score: {compliance_result.risk_score}")
        print(f"✅ Compliance score: {compliance_result.compliance_score}")
        print(f"✅ AI insights: {compliance_result.ai_insights[:100]}...")
        
        # Test 6: Test policy review
        print("\n📝 Test 6: Testing BFSI policy review...")
        policy_review_request = BFSIAnalysisRequest(
            analysis_type="policy_review",
            business_unit="risk_management",
            industry_type="bfsi",
            context={"review_scope": "comprehensive"},
            user_id=test_user_id,
            organization_id=test_org_id
        )
        
        policy_review_result = await bfsi_ai_service.perform_policy_review(
            test_policy_id, policy_review_request, test_user
        )
        print(f"✅ Policy review completed: {policy_review_result.analysis_id}")
        print(f"✅ Risk score: {policy_review_result.risk_score}")
        print(f"✅ Compliance score: {policy_review_result.compliance_score}")
        print(f"✅ Recommendations: {len(policy_review_result.recommendations)} items")
        
        # Test 7: Test gap analysis
        print("\n🔍 Test 7: Testing BFSI gap analysis...")
        gap_analysis_request = BFSIAnalysisRequest(
            analysis_type="gap_analysis",
            business_unit="compliance",
            industry_type="bfsi",
            context={"frameworks": ["SOX", "Basel III", "PCI DSS", "GDPR"]},
            user_id=test_user_id,
            organization_id=test_org_id
        )
        
        gap_results = await bfsi_ai_service.perform_gap_analysis(gap_analysis_request, test_user)
        print(f"✅ Gap analysis completed: {len(gap_results)} gaps identified")
        for i, gap in enumerate(gap_results[:3], 1):  # Show first 3 gaps
            print(f"  Gap {i}: {gap.policy_name} ({gap.severity} severity)")
        
        # Test 8: Test audit logging
        print("\n📝 Test 8: Testing audit logging...")
        audit_logs = audit_log_repo.get_by_user_id(test_user_id)
        print(f"✅ Audit logs created: {len(audit_logs)} entries")
        for log in audit_logs[:3]:  # Show first 3 logs
            print(f"  - {log.action.value}: {log.resource.value} at {log.created_at}")
        
        session.close()
        
        print("\n🎉 BFSI AI integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n💥 BFSI AI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """
    Main function to run BFSI AI integration tests
    """
    success = await test_bfsi_ai_integration()
    if success:
        print("\n✅ All BFSI AI integration tests passed!")
        print("🤖 BFSI AI agents are successfully integrated with the GRC platform.")
    else:
        print("\n❌ BFSI AI integration tests failed!")
        print("🔧 Please check the BFSI AI integration implementation.")

if __name__ == "__main__":
    asyncio.run(main())
