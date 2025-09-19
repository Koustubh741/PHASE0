#!/usr/bin/env python3
"""
AI Agents Status Test Script
Tests the current state of all AI agents and multi-agent systems
"""

import asyncio
import sys
import os
import requests
import json
from datetime import datetime

# Add ai-agents directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'ai-agents', 'agents_organized'))

def test_multi_agent_import():
    """Test if multi-agent system can be imported"""
    try:
        from multi_agent_main import (
            BFSIMultiAgentOrchestrator, 
            TelecomMultiAgentOrchestrator,
            ManufacturingMultiAgentOrchestrator,
            HealthcareMultiAgentOrchestrator,
            bfsi_orchestrator
        )
        print("✅ Multi-agent system imports successfully")
        return True
    except Exception as e:
        print(f"❌ Multi-agent import failed: {e}")
        return False

def test_bfsi_agents():
    """Test BFSI agents configuration"""
    try:
        from multi_agent_main import bfsi_orchestrator
        agents = bfsi_orchestrator.agents
        print(f"✅ BFSI Agents: {list(agents.keys())}")
        print(f"   - Compliance Agent: {agents.get('compliance_agent', 'Not found')}")
        print(f"   - Risk Agent: {agents.get('risk_agent', 'Not found')}")
        print(f"   - Reporting Agent: {agents.get('reporting_agent', 'Not found')}")
        
        # Check that fraud and AML agents are removed
        if 'fraud_agent' not in agents and 'aml_agent' not in agents:
            print("✅ Fraud and AML agents successfully removed")
        else:
            print("❌ Fraud and AML agents still present")
            
        return True
    except Exception as e:
        print(f"❌ BFSI agents test failed: {e}")
        return False

async def test_bfsi_analysis():
    """Test BFSI multi-agent analysis"""
    try:
        from multi_agent_main import bfsi_orchestrator
        
        # Test different types of analysis
        test_cases = [
            "Basel III capital adequacy assessment",
            "Credit risk portfolio analysis", 
            "Regulatory reporting compliance check"
        ]
        
        for test_case in test_cases:
            result = await bfsi_orchestrator.orchestrate_analysis(test_case, {})
            print(f"✅ Analysis: {test_case}")
            print(f"   Result: {result.result[:100]}...")
            print(f"   Confidence: {result.confidence}")
            print(f"   Agents Used: {result.agents_used}")
            print()
            
        return True
    except Exception as e:
        print(f"❌ BFSI analysis test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    endpoints = [
        ("http://localhost:8005/health", "Multi-Agent Service Health"),
        ("http://localhost:8005/agents/status", "Multi-Agent Status"),
        ("http://localhost:8000/health", "API Gateway Health"),
        ("http://localhost:8000/grc/dashboard", "GRC Dashboard")
    ]
    
    results = []
    for url, description in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: {url} - Status {response.status_code}")
                results.append(True)
            else:
                print(f"⚠️  {description}: {url} - Status {response.status_code}")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: {url} - Connection failed")
            results.append(False)
    
    return all(results)

def test_sample_data():
    """Test sample data availability"""
    try:
        # Check if clean sample data file exists
        sample_file = os.path.join('database', 'bfsi_sample_data_clean.sql')
        if os.path.exists(sample_file):
            print("✅ Clean BFSI sample data file exists")
            
            # Read and check content
            with open(sample_file, 'r') as f:
                content = f.read()
                
            # Check for removed agents
            if 'fraud_agent' not in content and 'aml_agent' not in content:
                print("✅ Sample data cleaned of fraud and AML agents")
            else:
                print("❌ Sample data still contains fraud/AML references")
                
            # Count records
            policies_count = content.count("INSERT INTO policies")
            risks_count = content.count("INSERT INTO risks")
            agents_count = content.count("INSERT INTO ai_agent_records")
            
            print(f"   - Policies: {policies_count}")
            print(f"   - Risks: {risks_count}")
            print(f"   - AI Agents: {agents_count}")
            
            return True
        else:
            print("❌ Clean sample data file not found")
            return False
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("AI AGENTS STATUS TEST")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Multi-Agent Import", test_multi_agent_import),
        ("BFSI Agents Configuration", test_bfsi_agents),
        ("BFSI Analysis", lambda: asyncio.run(test_bfsi_analysis())),
        ("API Endpoints", test_api_endpoints),
        ("Sample Data", test_sample_data)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AI agents are ready.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
