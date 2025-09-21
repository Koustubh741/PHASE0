"""
BFSI Agent Test Script
=====================

Simple script to test the BFSI LLM Integrated Agent functionality.
This script demonstrates how to call the BFSI agent with full functionality.
"""

import asyncio
import json
import logging
from datetime import datetime
from bfsi_llm_integrated_agent import BFSILLMIntegratedAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_bfsi_agent_full_functionality():
    """Test BFSI agent with full functionality"""
    
    print("🚀 Testing BFSI Agent Full Functionality")
    print("=" * 50)
    
    async with BFSILLMIntegratedAgent() as agent:
        
        # Test 1: Agent Status
        print("\n📊 1. Agent Status Check")
        status = await agent.get_agent_status()
        print(f"   Agent: {status['name']}")
        print(f"   Ollama Status: {status['llm_services']['ollama']['status']}")
        print(f"   Hugging Face Status: {status['llm_services']['huggingface']['status']}")
        print(f"   Capabilities: {len(status['capabilities'])}")
        
        # Test 2: Risk Analysis
        print("\n🎯 2. Risk Analysis Test")
        risk_context = {
            "risk_type": "credit_risk",
            "portfolio_data": {
                "total_exposure": 1000000000,
                "number_of_borrowers": 1000,
                "average_credit_score": 720,
                "default_rate": 0.02,
                "recovery_rate": 0.4
            },
            "stress_scenarios": [
                "economic_recession",
                "industry_downturn"
            ]
        }
        
        risk_result = await agent.analyze_risk(risk_context)
        print(f"   Analysis ID: {risk_result.analysis_id}")
        print(f"   Risk Score: {risk_result.risk_score:.2f}")
        print(f"   Confidence: {risk_result.confidence_score:.2f}")
        print(f"   Status: {risk_result.compliance_status}")
        print(f"   Recommendations: {len(risk_result.recommendations)}")
        print(f"   Duration: {risk_result.duration:.2f}s")
        
        # Print LLM insights
        if risk_result.llm_insights.get('ollama_analysis') != "Not available":
            print(f"   Ollama Insight: {risk_result.llm_insights['ollama_analysis'][:100]}...")
        
        # Test 3: Compliance Analysis
        print("\n📋 3. Compliance Analysis Test")
        compliance_context = {
            "framework": "basel_iii",
            "compliance_data": {
                "basel_capital_adequacy": {
                    "tier_1_ratio": 8.5,
                    "total_capital_ratio": 10.2,
                    "leverage_ratio": 4.1
                },
                "sox_internal_controls": {
                    "effectiveness": 0.95,
                    "testing_results": "passed"
                }
            },
            "regulatory_changes": [
                "basel_iv_implementation"
            ]
        }
        
        compliance_result = await agent.analyze_compliance(compliance_context)
        print(f"   Analysis ID: {compliance_result.analysis_id}")
        print(f"   Compliance Score: {1.0 - compliance_result.risk_score:.2f}")
        print(f"   Status: {compliance_result.compliance_status}")
        print(f"   Recommendations: {len(compliance_result.recommendations)}")
        print(f"   Duration: {compliance_result.duration:.2f}s")
        
        # Test 4: Portfolio Analysis
        print("\n📊 4. Portfolio Analysis Test")
        portfolio_context = {
            "portfolio_data": {
                "equity_portfolio": {
                    "weight": 0.4,
                    "risk_score": 0.7,
                    "expected_return": 0.12
                },
                "bond_portfolio": {
                    "weight": 0.3,
                    "risk_score": 0.3,
                    "expected_return": 0.06
                },
                "cash_equivalents": {
                    "weight": 0.3,
                    "risk_score": 0.1,
                    "expected_return": 0.03
                }
            },
            "risk_tolerance": "moderate",
            "investment_horizon": "5_years"
        }
        
        portfolio_result = await agent.analyze_portfolio(portfolio_context)
        print(f"   Analysis ID: {portfolio_result.analysis_id}")
        print(f"   Portfolio Risk: {portfolio_result.risk_score:.2f}")
        print(f"   Status: {portfolio_result.compliance_status}")
        print(f"   Recommendations: {len(portfolio_result.recommendations)}")
        print(f"   Duration: {portfolio_result.duration:.2f}s")
        
        # Test 5: Strategic Decision Analysis
        print("\n🎯 5. Strategic Decision Analysis Test")
        decision_context = {
            "decision_type": "investment_strategy",
            "description": "Strategic investment decision for market expansion",
            "alternatives": [
                {
                    "name": "Market Expansion",
                    "description": "Expand into new geographic markets",
                    "success_probability": 0.7,
                    "performance_scores": {
                        "implementation_feasibility": 0.8
                    }
                },
                {
                    "name": "Product Development", 
                    "description": "Develop new financial products",
                    "success_probability": 0.8,
                    "performance_scores": {
                        "implementation_feasibility": 0.9
                    }
                }
            ],
            "constraints": ["budget_limit: 10000000"],
            "stakeholders": ["board_of_directors", "senior_management"]
        }
        
        decision_result = await agent.strategic_decision_analysis(decision_context)
        print(f"   Analysis ID: {decision_result.analysis_id}")
        print(f"   Decision Confidence: {1.0 - decision_result.risk_score:.2f}")
        print(f"   Recommended Alternative: {decision_result.llm_insights.get('recommended_alternative', 'N/A')}")
        print(f"   Status: {decision_result.compliance_status}")
        print(f"   Recommendations: {len(decision_result.recommendations)}")
        print(f"   Duration: {decision_result.duration:.2f}s")
        
        # Test 6: Analysis History
        print("\n📈 6. Analysis History")
        history = agent.get_analysis_history()
        print(f"   Total Analyses: {len(history)}")
        for analysis in history:
            print(f"   - {analysis['analysis_type']}: {analysis['analysis_id']} (Score: {analysis['risk_score']:.2f})")
        
        # Summary
        print("\n✅ BFSI Agent Full Functionality Test Completed")
        print("=" * 50)
        print(f"Total Tests: 6")
        print(f"LLM Services: Ollama + Hugging Face")
        print(f"Analysis Types: Risk, Compliance, Portfolio, Strategic Decision")
        print(f"Total Analyses Performed: {len(history)}")
        
        return True

async def simple_risk_assessment_example():
    """Simple example of how to call BFSI agent for risk assessment"""
    
    print("\n🎯 Simple Risk Assessment Example")
    print("-" * 30)
    
    # Simple risk data
    risk_data = {
        "risk_type": "credit_risk",
        "portfolio_data": {
            "total_exposure": 500000000,
            "average_credit_score": 680,
            "default_rate": 0.03
        }
    }
    
    async with BFSILLMIntegratedAgent() as agent:
        result = await agent.analyze_risk(risk_data)
        
        print(f"Risk Assessment Results:")
        print(f"  Risk Score: {result.risk_score:.2f} ({'High' if result.risk_score > 0.7 else 'Medium' if result.risk_score > 0.4 else 'Low'})")
        print(f"  Confidence: {result.confidence_score:.2f}")
        print(f"  Status: {result.compliance_status}")
        print(f"  Top Recommendations:")
        for i, rec in enumerate(result.recommendations[:3], 1):
            print(f"    {i}. {rec}")
        
        return result

async def simple_compliance_check_example():
    """Simple example of how to call BFSI agent for compliance check"""
    
    print("\n📋 Simple Compliance Check Example")
    print("-" * 30)
    
    # Simple compliance data
    compliance_data = {
        "framework": "basel_iii",
        "compliance_data": {
            "basel_capital_adequacy": {
                "tier_1_ratio": 9.0,
                "total_capital_ratio": 11.5
            }
        }
    }
    
    async with BFSILLMIntegratedAgent() as agent:
        result = await agent.analyze_compliance(compliance_data)
        
        compliance_score = 1.0 - result.risk_score
        print(f"Compliance Assessment Results:")
        print(f"  Compliance Score: {compliance_score:.2f} ({'Good' if compliance_score > 0.8 else 'Needs Improvement'})")
        print(f"  Status: {result.compliance_status}")
        print(f"  Top Recommendations:")
        for i, rec in enumerate(result.recommendations[:3], 1):
            print(f"    {i}. {rec}")
        
        return result

async def main():
    """Main execution"""
    try:
        # Run full functionality test
        await test_bfsi_agent_full_functionality()
        
        # Run simple examples
        await simple_risk_assessment_example()
        await simple_compliance_check_example()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
