"""
BFSI Enhanced Agent Demo
Demonstrates the enhanced logical reasoning capabilities of the BFSI agent
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import enhanced agent
from bfsi_enhanced_agent import BFSIEnhancedAgent, ReasoningMode, ReasoningScope

async def demo_enhanced_reasoning():
    """Demonstrate enhanced reasoning capabilities"""
    logger.info("🚀 Starting BFSI Enhanced Agent Demo")
    
    # Initialize enhanced agent
    agent = BFSIEnhancedAgent(
        agent_id="bfsi-demo-agent",
        name="BFSI Demo Agent"
    )
    
    # Demo 1: Risk Management with Enhanced Reasoning
    await demo_risk_management(agent)
    
    # Demo 2: Compliance Analysis with Enhanced Reasoning
    await demo_compliance_analysis(agent)
    
    # Demo 3: Strategic Decision Making with Enhanced Reasoning
    await demo_strategic_decision_making(agent)
    
    # Demo 4: Portfolio Analysis with Enhanced Reasoning
    await demo_portfolio_analysis(agent)
    
    # Demo 5: Stress Testing with Enhanced Reasoning
    await demo_stress_testing(agent)
    
    # Get comprehensive analytics
    analytics = await agent.get_comprehensive_analytics()
    logger.info(f"📊 Comprehensive Analytics: {json.dumps(analytics, indent=2, default=str)}")
    
    logger.info("✅ BFSI Enhanced Agent Demo Completed Successfully")

async def demo_risk_management(agent: BFSIEnhancedAgent):
    """Demo risk management with enhanced reasoning"""
    logger.info("🎯 Demo 1: Risk Management with Enhanced Reasoning")
    
    context = {
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
            "industry_downturn",
            "geographic_concentration"
        ],
        "regulatory_requirements": [
            "basel_iii_capital_requirements",
            "stress_testing_requirements",
            "risk_reporting_requirements"
        ],
        "constraints": [
            "budget_limit: 500000",
            "timeline: 90_days",
            "regulatory_deadline: 2024-03-31"
        ],
        "stakeholders": [
            "risk_management_team",
            "compliance_officer",
            "senior_management"
        ]
    }
    
    operation = await agent.perform_enhanced_operation(
        operation_type="risk_management",
        context=context,
        reasoning_mode=ReasoningMode.ANALYTICAL,
        reasoning_scope=ReasoningScope.ORGANIZATIONAL
    )
    
    logger.info(f"📈 Risk Management Results:")
    logger.info(f"   Overall Confidence: {operation.overall_confidence:.2f}")
    logger.info(f"   Explainability Score: {operation.explainability_score:.2f}")
    logger.info(f"   Duration: {operation.duration:.2f} seconds")
    
    if operation.risk_assessment:
        logger.info(f"   Risk Score: {operation.risk_assessment.overall_risk_score:.2f}")
        logger.info(f"   Risk Level: {operation.risk_assessment.risk_level.value}")
        logger.info(f"   VaR 95%: ${operation.risk_assessment.var_95:,.2f}")
        logger.info(f"   VaR 99%: ${operation.risk_assessment.var_99:,.2f}")
    
    if operation.decision_result:
        logger.info(f"   Recommended Alternative: {operation.decision_result.recommended_alternative}")
        logger.info(f"   Decision Confidence: {operation.decision_result.confidence_score:.2f}")
    
    logger.info(f"   Recommendations: {len(operation.recommendations)}")
    for i, rec in enumerate(operation.recommendations[:3], 1):
        logger.info(f"     {i}. {rec}")

async def demo_compliance_analysis(agent: BFSIEnhancedAgent):
    """Demo compliance analysis with enhanced reasoning"""
    logger.info("🎯 Demo 2: Compliance Analysis with Enhanced Reasoning")
    
    context = {
        "framework": "basel_iii",
        "compliance_data": {
            "basel_capital_adequacy": {
                "tier_1_ratio": 8.5,
                "total_capital_ratio": 10.2,
                "leverage_ratio": 4.1,
                "lcr": 125.0,
                "nsfr": 110.0
            },
            "sox_internal_controls": {
                "effectiveness": 0.95,
                "testing_results": "passed",
                "audit_findings": 0
            },
            "pci_data_protection": {
                "encryption": True,
                "access_controls": True,
                "monitoring": True
            },
            "aml_transaction_monitoring": {
                "monitoring_active": True,
                "alerts_resolved": 95,
                "alerts_total": 100
            }
        },
        "regulatory_changes": [
            "basel_iv_implementation",
            "gdpr_enhancements"
        ],
        "audit_requirements": [
            "quarterly_compliance_review",
            "annual_audit",
            "regulatory_reporting"
        ]
    }
    
    operation = await agent.perform_enhanced_operation(
        operation_type="compliance_management",
        context=context,
        reasoning_mode=ReasoningMode.ANALYTICAL,
        reasoning_scope=ReasoningScope.ORGANIZATIONAL
    )
    
    logger.info(f"📋 Compliance Analysis Results:")
    logger.info(f"   Overall Confidence: {operation.overall_confidence:.2f}")
    logger.info(f"   Explainability Score: {operation.explainability_score:.2f}")
    logger.info(f"   Duration: {operation.duration:.2f} seconds")
    
    if operation.compliance_assessment:
        logger.info(f"   Compliance Score: {operation.compliance_assessment.compliance_score:.1f}%")
        logger.info(f"   Status: {operation.compliance_assessment.overall_status.value}")
        logger.info(f"   Requirements Met: {operation.compliance_assessment.requirements_met}/{operation.compliance_assessment.requirements_total}")
        logger.info(f"   Violations: {len(operation.compliance_assessment.violations)}")
        logger.info(f"   Gaps: {len(operation.compliance_assessment.gaps)}")
    
    logger.info(f"   Recommendations: {len(operation.recommendations)}")
    for i, rec in enumerate(operation.recommendations[:3], 1):
        logger.info(f"     {i}. {rec}")

async def demo_strategic_decision_making(agent: BFSIEnhancedAgent):
    """Demo strategic decision making with enhanced reasoning"""
    logger.info("🎯 Demo 3: Strategic Decision Making with Enhanced Reasoning")
    
    context = {
        "decision_type": "investment_strategy",
        "description": "Strategic investment decision for new market expansion",
        "alternatives": [
            {
                "alternative_id": "market_expansion",
                "name": "Market Expansion",
                "description": "Expand into new geographic markets",
                "performance_scores": {
                    "revenue_growth": 0.8,
                    "market_share": 0.7,
                    "risk_level": 0.6,
                    "implementation_feasibility": 0.8
                },
                "costs": {"investment": 5000000, "operational": 2000000},
                "benefits": {"revenue": 0.8, "market_presence": 0.9},
                "risks": ["market_volatility", "regulatory_changes", "competition"],
                "implementation_time": 365,
                "success_probability": 0.7
            },
            {
                "alternative_id": "product_development",
                "name": "Product Development",
                "description": "Develop new financial products",
                "performance_scores": {
                    "revenue_growth": 0.6,
                    "market_share": 0.8,
                    "risk_level": 0.4,
                    "implementation_feasibility": 0.9
                },
                "costs": {"development": 3000000, "marketing": 1000000},
                "benefits": {"innovation": 0.9, "customer_satisfaction": 0.8},
                "risks": ["development_delays", "market_acceptance", "regulatory_approval"],
                "implementation_time": 180,
                "success_probability": 0.8
            },
            {
                "alternative_id": "acquisition",
                "name": "Strategic Acquisition",
                "description": "Acquire complementary business",
                "performance_scores": {
                    "revenue_growth": 0.9,
                    "market_share": 0.9,
                    "risk_level": 0.8,
                    "implementation_feasibility": 0.6
                },
                "costs": {"acquisition": 10000000, "integration": 2000000},
                "benefits": {"synergies": 0.9, "market_position": 0.9},
                "risks": ["integration_challenges", "cultural_fit", "financial_impact"],
                "implementation_time": 540,
                "success_probability": 0.6
            }
        ],
        "constraints": [
            "budget_limit: 15000000",
            "timeline: 24_months",
            "regulatory_approval_required"
        ],
        "stakeholders": [
            "board_of_directors",
            "senior_management",
            "investment_committee",
            "regulatory_affairs"
        ]
    }
    
    operation = await agent.perform_enhanced_operation(
        operation_type="strategic_planning",
        context=context,
        reasoning_mode=ReasoningMode.ANALYTICAL,
        reasoning_scope=ReasoningScope.ORGANIZATIONAL
    )
    
    logger.info(f"🎯 Strategic Decision Making Results:")
    logger.info(f"   Overall Confidence: {operation.overall_confidence:.2f}")
    logger.info(f"   Explainability Score: {operation.explainability_score:.2f}")
    logger.info(f"   Duration: {operation.duration:.2f} seconds")
    
    if operation.decision_result:
        logger.info(f"   Recommended Alternative: {operation.decision_result.recommended_alternative}")
        logger.info(f"   Decision Confidence: {operation.decision_result.confidence_score:.2f}")
        logger.info(f"   Trade-offs: {len(operation.decision_result.trade_offs)}")
        logger.info(f"   Implementation Plan: {operation.decision_result.implementation_plan.get('status', 'N/A')}")
    
    logger.info(f"   Recommendations: {len(operation.recommendations)}")
    for i, rec in enumerate(operation.recommendations[:3], 1):
        logger.info(f"     {i}. {rec}")

async def demo_portfolio_analysis(agent: BFSIEnhancedAgent):
    """Demo portfolio analysis with enhanced reasoning"""
    logger.info("🎯 Demo 4: Portfolio Analysis with Enhanced Reasoning")
    
    context = {
        "portfolio_data": {
            "equity_portfolio": {
                "weight": 0.4,
                "risk_score": 0.7,
                "expected_return": 0.12,
                "volatility": 0.18
            },
            "bond_portfolio": {
                "weight": 0.3,
                "risk_score": 0.3,
                "expected_return": 0.06,
                "volatility": 0.08
            },
            "alternative_investments": {
                "weight": 0.2,
                "risk_score": 0.8,
                "expected_return": 0.15,
                "volatility": 0.25
            },
            "cash_equivalents": {
                "weight": 0.1,
                "risk_score": 0.1,
                "expected_return": 0.03,
                "volatility": 0.02
            }
        },
        "risk_tolerance": "moderate",
        "investment_horizon": "5_years",
        "regulatory_requirements": [
            "prudent_investor_rule",
            "diversification_requirements",
            "risk_management_standards"
        ]
    }
    
    operation = await agent.perform_enhanced_operation(
        operation_type="portfolio_analysis",
        context=context,
        reasoning_mode=ReasoningMode.ANALYTICAL,
        reasoning_scope=ReasoningScope.ORGANIZATIONAL
    )
    
    logger.info(f"📊 Portfolio Analysis Results:")
    logger.info(f"   Overall Confidence: {operation.overall_confidence:.2f}")
    logger.info(f"   Explainability Score: {operation.explainability_score:.2f}")
    logger.info(f"   Duration: {operation.duration:.2f} seconds")
    
    if operation.risk_assessment:
        logger.info(f"   Portfolio Risk Score: {operation.risk_assessment.overall_risk_score:.2f}")
        logger.info(f"   Risk Level: {operation.risk_assessment.risk_level.value}")
        logger.info(f"   Expected Loss: ${operation.risk_assessment.expected_loss:,.2f}")
    
    logger.info(f"   Recommendations: {len(operation.recommendations)}")
    for i, rec in enumerate(operation.recommendations[:3], 1):
        logger.info(f"     {i}. {rec}")

async def demo_stress_testing(agent: BFSIEnhancedAgent):
    """Demo stress testing with enhanced reasoning"""
    logger.info("🎯 Demo 5: Stress Testing with Enhanced Reasoning")
    
    context = {
        "stress_scenarios": [
            "economic_recession",
            "market_crash",
            "interest_rate_shock",
            "currency_crisis",
            "cyber_security_breach"
        ],
        "portfolio_data": {
            "total_assets": 5000000000,
            "total_liabilities": 4500000000,
            "capital": 500000000,
            "risk_weighted_assets": 4000000000
        },
        "regulatory_requirements": [
            "basel_iii_stress_testing",
            "ccar_requirements",
            "internal_stress_testing"
        ],
        "time_horizon": "2_years",
        "confidence_level": 0.99
    }
    
    operation = await agent.perform_enhanced_operation(
        operation_type="stress_testing",
        context=context,
        reasoning_mode=ReasoningMode.ANALYTICAL,
        reasoning_scope=ReasoningScope.ORGANIZATIONAL
    )
    
    logger.info(f"⚡ Stress Testing Results:")
    logger.info(f"   Overall Confidence: {operation.overall_confidence:.2f}")
    logger.info(f"   Explainability Score: {operation.explainability_score:.2f}")
    logger.info(f"   Duration: {operation.duration:.2f} seconds")
    
    if operation.risk_assessment:
        logger.info(f"   Stress Test Results: {len(operation.risk_assessment.stress_test_results)} scenarios")
        for scenario, result in operation.risk_assessment.stress_test_results.items():
            logger.info(f"     {scenario}: Impact {result.get('impact', 0):.2f}")
    
    logger.info(f"   Recommendations: {len(operation.recommendations)}")
    for i, rec in enumerate(operation.recommendations[:3], 1):
        logger.info(f"     {i}. {rec}")

async def main():
    """Main demo function"""
    try:
        await demo_enhanced_reasoning()
    except Exception as e:
        logger.error(f"❌ Demo failed with error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
