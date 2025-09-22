#!/usr/bin/env python3
"""
Test script for BFSI Gap Analysis System
"""

import asyncio
import requests
import json
from bfsi_gap_analysis_service import BFSIGapAnalysisService
from bfsi_mitigation_workflow import BFSIMitigationWorkflowSystem

async def test_gap_analysis():
    """Test the gap analysis system"""
    
    print("🧪 Testing BFSI Gap Analysis System")
    print("=" * 50)
    
    # Test 1: Gap Analysis Service
    print("\n1️⃣ Testing Gap Analysis Service...")
    gap_service = BFSIGapAnalysisService()
    
    try:
        report = await gap_service.perform_comprehensive_gap_analysis(
            organization_name="Test Financial Institution"
        )
        
        print(f"✅ Gap Analysis Completed")
        print(f"   Organization: {report.organization_name}")
        print(f"   Compliance Score: {report.compliance_score:.1f}%")
        print(f"   Total Gaps: {len(report.gaps)}")
        print(f"   Critical Gaps: {report.critical_gaps}")
        print(f"   High Priority Gaps: {report.high_priority_gaps}")
        
    except Exception as e:
        print(f"❌ Gap Analysis Failed: {e}")
    
    # Test 2: Mitigation Workflow System
    print("\n2️⃣ Testing Mitigation Workflow System...")
    workflow_system = BFSIMitigationWorkflowSystem()
    
    try:
        workflow = workflow_system.create_mitigation_workflow(
            gap_id="test_gap_001",
            organization_name="Test Financial Institution",
            assigned_owner="Test Owner",
            target_completion_date="2024-03-15T00:00:00",
            gap_type="sox_compliance"
        )
        
        print(f"✅ Workflow Created")
        print(f"   Workflow ID: {workflow.workflow_id}")
        print(f"   Workflow Name: {workflow.workflow_name}")
        print(f"   Total Tasks: {len(workflow.tasks)}")
        print(f"   Assigned Owner: {workflow.assigned_owner}")
        
    except Exception as e:
        print(f"❌ Workflow Creation Failed: {e}")
    
    # Test 3: API Service (if running)
    print("\n3️⃣ Testing API Service...")
    try:
        response = requests.get("http://localhost:8011/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Service is running")
            print(f"   Health Status: {response.json()}")
        else:
            print(f"⚠️ API Service responded with status: {response.status_code}")
    except requests.exceptions.RequestException:
        print("⚠️ API Service is not running (start with: python bfsi_gap_analysis_api.py)")
    
    print("\n🎉 BFSI Gap Analysis System Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_gap_analysis())
