"""
Enhanced BFSI Risk Reasoning System
Advanced probabilistic risk analysis with scenario modeling and stress testing
"""

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
import numpy as np
from collections import defaultdict
import math
import statistics

# Configure logging
logger = logging.getLogger(__name__)

class RiskType(Enum):
    """Types of financial risks"""
    CREDIT_RISK = "credit_risk"
    MARKET_RISK = "market_risk"
    OPERATIONAL_RISK = "operational_risk"
    LIQUIDITY_RISK = "liquidity_risk"
    REPUTATIONAL_RISK = "reputational_risk"
    REGULATORY_RISK = "regulatory_risk"
    CYBER_RISK = "cyber_risk"
    CONCENTRATION_RISK = "concentration_risk"

class RiskSeverity(Enum):
    """Risk severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class RiskProbability(Enum):
    """Risk probability levels"""
    VERY_LOW = 0.1
    LOW = 0.3
    MEDIUM = 0.5
    HIGH = 0.7
    VERY_HIGH = 0.9

@dataclass
class RiskFactor:
    """Risk factor with probabilistic attributes"""
    factor_id: str
    name: str
    risk_type: RiskType
    probability: float
    impact: float
    correlation_matrix: Dict[str, float]
    temporal_dependencies: List[str]
    stress_scenarios: List[str]
    mitigation_effectiveness: float
    monitoring_indicators: List[str]

@dataclass
class RiskScenario:
    """Risk scenario for stress testing"""
    scenario_id: str
    name: str
    description: str
    probability: float
    impact: float
    duration: int  # days
    triggers: List[str]
    consequences: List[str]
    mitigation_actions: List[str]
    recovery_time: int  # days

@dataclass
class RiskAssessment:
    """Comprehensive risk assessment"""
    assessment_id: str
    risk_type: RiskType
    overall_risk_score: float
    risk_level: RiskSeverity
    probability: float
    impact: float
    var_95: float  # Value at Risk 95%
    var_99: float  # Value at Risk 99%
    expected_loss: float
    stress_test_results: Dict[str, Any]
    correlation_analysis: Dict[str, Any]
    scenario_analysis: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime

@dataclass
class RiskModel:
    """Risk model with parameters"""
    model_id: str
    model_type: str
    parameters: Dict[str, float]
    validation_metrics: Dict[str, float]
    backtesting_results: Dict[str, Any]
    confidence_interval: Tuple[float, float]
    model_limitations: List[str]

class BFSIRiskReasoning:
    """
    Enhanced BFSI Risk Reasoning System with advanced probabilistic analysis
    """
    
    def __init__(self):
        self.system_id = "bfsi_risk_reasoning"
        self.risk_factors: Dict[str, RiskFactor] = {}
        self.risk_scenarios: Dict[str, RiskScenario] = {}
        self.risk_models: Dict[str, RiskModel] = {}
        self.assessment_history: List[RiskAssessment] = []
        
        # Initialize risk frameworks
        self._initialize_risk_frameworks()
        self._initialize_risk_factors()
        self._initialize_risk_scenarios()
        self._initialize_risk_models()
        
        logger.info("BFSI Risk Reasoning System initialized with advanced probabilistic analysis")
    
    def _initialize_risk_frameworks(self):
        """Initialize BFSI risk frameworks"""
        self.risk_frameworks = {
            "credit_risk": {
                "models": ["PD", "LGD", "EAD"],
                "stress_scenarios": ["economic_recession", "industry_downturn", "geographic_concentration"],
                "monitoring_indicators": ["default_rates", "recovery_rates", "exposure_at_default"]
            },
            "market_risk": {
                "models": ["VaR", "ES", "Stressed_VaR"],
                "stress_scenarios": ["market_crash", "interest_rate_shock", "currency_crisis"],
                "monitoring_indicators": ["price_volatility", "correlation_changes", "liquidity_conditions"]
            },
            "operational_risk": {
                "models": ["LDA", "Scenario_Analysis", "Scorecard"],
                "stress_scenarios": ["system_failure", "cyber_attack", "regulatory_breach"],
                "monitoring_indicators": ["loss_events", "near_misses", "control_effectiveness"]
            }
        }
    
    def _initialize_risk_factors(self):
        """Initialize BFSI risk factors"""
        risk_factors_data = [
            {
                "factor_id": "credit_default_probability",
                "name": "Credit Default Probability",
                "risk_type": RiskType.CREDIT_RISK,
                "probability": 0.05,
                "impact": 0.8,
                "correlation_matrix": {
                    "economic_conditions": 0.7,
                    "industry_performance": 0.6,
                    "geographic_factors": 0.4
                },
                "temporal_dependencies": ["quarterly_reports", "economic_indicators"],
                "stress_scenarios": ["recession", "industry_crisis"],
                "mitigation_effectiveness": 0.7,
                "monitoring_indicators": ["default_rates", "credit_spreads", "recovery_rates"]
            },
            {
                "factor_id": "market_volatility",
                "name": "Market Volatility",
                "risk_type": RiskType.MARKET_RISK,
                "probability": 0.3,
                "impact": 0.6,
                "correlation_matrix": {
                    "interest_rates": 0.8,
                    "currency_fluctuations": 0.6,
                    "commodity_prices": 0.4
                },
                "temporal_dependencies": ["daily_market_data", "economic_announcements"],
                "stress_scenarios": ["market_crash", "volatility_spike"],
                "mitigation_effectiveness": 0.6,
                "monitoring_indicators": ["vix", "price_movements", "trading_volumes"]
            },
            {
                "factor_id": "operational_control_failure",
                "name": "Operational Control Failure",
                "risk_type": RiskType.OPERATIONAL_RISK,
                "probability": 0.1,
                "impact": 0.7,
                "correlation_matrix": {
                    "system_reliability": 0.8,
                    "staff_training": 0.6,
                    "process_maturity": 0.7
                },
                "temporal_dependencies": ["system_updates", "staff_changes"],
                "stress_scenarios": ["system_failure", "cyber_attack"],
                "mitigation_effectiveness": 0.8,
                "monitoring_indicators": ["system_uptime", "error_rates", "audit_findings"]
            }
        ]
        
        for factor_data in risk_factors_data:
            self.risk_factors[factor_data["factor_id"]] = RiskFactor(**factor_data)
    
    def _initialize_risk_scenarios(self):
        """Initialize risk scenarios for stress testing"""
        scenarios_data = [
            {
                "scenario_id": "economic_recession",
                "name": "Economic Recession",
                "description": "Severe economic downturn affecting multiple sectors",
                "probability": 0.15,
                "impact": 0.8,
                "duration": 365,
                "triggers": ["GDP_decline", "unemployment_increase", "market_volatility"],
                "consequences": ["increased_defaults", "reduced_liquidity", "regulatory_pressure"],
                "mitigation_actions": ["diversification", "stress_testing", "capital_buffers"],
                "recovery_time": 730
            },
            {
                "scenario_id": "cyber_security_breach",
                "name": "Cyber Security Breach",
                "description": "Major cyber attack compromising systems and data",
                "probability": 0.1,
                "impact": 0.9,
                "duration": 30,
                "triggers": ["system_vulnerability", "social_engineering", "insider_threat"],
                "consequences": ["data_breach", "system_outage", "reputational_damage"],
                "mitigation_actions": ["incident_response", "system_recovery", "customer_communication"],
                "recovery_time": 90
            },
            {
                "scenario_id": "regulatory_changes",
                "name": "Regulatory Changes",
                "description": "Significant changes in regulatory requirements",
                "probability": 0.2,
                "impact": 0.6,
                "duration": 180,
                "triggers": ["new_regulations", "compliance_requirements", "reporting_standards"],
                "consequences": ["compliance_costs", "system_changes", "operational_impact"],
                "mitigation_actions": ["regulatory_monitoring", "system_updates", "training"],
                "recovery_time": 365
            }
        ]
        
        for scenario_data in scenarios_data:
            self.risk_scenarios[scenario_data["scenario_id"]] = RiskScenario(**scenario_data)
    
    def _initialize_risk_models(self):
        """Initialize risk models"""
        models_data = [
            {
                "model_id": "credit_risk_model",
                "model_type": "PD_LGD_EAD",
                "parameters": {
                    "default_probability": 0.05,
                    "loss_given_default": 0.4,
                    "exposure_at_default": 1000000
                },
                "validation_metrics": {
                    "accuracy": 0.85,
                    "precision": 0.80,
                    "recall": 0.75
                },
                "backtesting_results": {
                    "hit_rate": 0.95,
                    "mean_squared_error": 0.02
                },
                "confidence_interval": (0.8, 0.95),
                "model_limitations": ["Limited historical data", "Model assumptions"]
            },
            {
                "model_id": "market_risk_model",
                "model_type": "VaR_ES",
                "parameters": {
                    "confidence_level": 0.95,
                    "holding_period": 10,
                    "volatility": 0.2
                },
                "validation_metrics": {
                    "accuracy": 0.90,
                    "precision": 0.85,
                    "recall": 0.80
                },
                "backtesting_results": {
                    "hit_rate": 0.95,
                    "mean_squared_error": 0.01
                },
                "confidence_interval": (0.85, 0.95),
                "model_limitations": ["Market assumptions", "Correlation stability"]
            }
        ]
        
        for model_data in models_data:
            self.risk_models[model_data["model_id"]] = RiskModel(**model_data)
    
    async def assess_risk(self, risk_type: RiskType, context: Dict[str, Any]) -> RiskAssessment:
        """Perform comprehensive risk assessment"""
        logger.info(f"Assessing {risk_type.value} risk")
        
        # Get relevant risk factors
        relevant_factors = [factor for factor in self.risk_factors.values() if factor.risk_type == risk_type]
        
        # Calculate risk metrics
        risk_score = await self._calculate_risk_score(relevant_factors, context)
        probability = await self._calculate_risk_probability(relevant_factors, context)
        impact = await self._calculate_risk_impact(relevant_factors, context)
        
        # Calculate VaR metrics
        var_95, var_99 = await self._calculate_var_metrics(relevant_factors, context)
        expected_loss = await self._calculate_expected_loss(relevant_factors, context)
        
        # Perform stress testing
        stress_test_results = await self._perform_stress_testing(risk_type, context)
        
        # Analyze correlations
        correlation_analysis = await self._analyze_correlations(relevant_factors, context)
        
        # Scenario analysis
        scenario_analysis = await self._analyze_scenarios(risk_type, context)
        
        # Generate recommendations
        recommendations = await self._generate_risk_recommendations(risk_score, relevant_factors, context)
        
        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)
        
        assessment = RiskAssessment(
            assessment_id=str(uuid.uuid4()),
            risk_type=risk_type,
            overall_risk_score=risk_score,
            risk_level=risk_level,
            probability=probability,
            impact=impact,
            var_95=var_95,
            var_99=var_99,
            expected_loss=expected_loss,
            stress_test_results=stress_test_results,
            correlation_analysis=correlation_analysis,
            scenario_analysis=scenario_analysis,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
        
        self.assessment_history.append(assessment)
        return assessment
    
    async def _calculate_risk_score(self, factors: List[RiskFactor], context: Dict[str, Any]) -> float:
        """Calculate overall risk score"""
        if not factors:
            return 0.0
        
        # Weighted average of risk factors
        total_weight = 0.0
        weighted_score = 0.0
        
        for factor in factors:
            weight = factor.probability * factor.impact
            total_weight += weight
            weighted_score += weight * (factor.probability + factor.impact) / 2
        
        if total_weight == 0:
            return 0.0
        
        return weighted_score / total_weight
    
    async def _calculate_risk_probability(self, factors: List[RiskFactor], context: Dict[str, Any]) -> float:
        """Calculate risk probability"""
        if not factors:
            return 0.0
        
        # Use maximum probability among factors
        max_probability = max(factor.probability for factor in factors)
        
        # Adjust based on correlations
        correlation_adjustment = await self._calculate_correlation_adjustment(factors)
        
        return min(max_probability * correlation_adjustment, 1.0)
    
    async def _calculate_risk_impact(self, factors: List[RiskFactor], context: Dict[str, Any]) -> float:
        """Calculate risk impact"""
        if not factors:
            return 0.0
        
        # Weighted average of impact
        total_weight = 0.0
        weighted_impact = 0.0
        
        for factor in factors:
            weight = factor.probability
            total_weight += weight
            weighted_impact += weight * factor.impact
        
        if total_weight == 0:
            return 0.0
        
        return weighted_impact / total_weight
    
    async def _calculate_var_metrics(self, factors: List[RiskFactor], context: Dict[str, Any]) -> Tuple[float, float]:
        """Calculate Value at Risk metrics"""
        if not factors:
            return 0.0, 0.0
        
        # Simulate risk scenarios
        scenarios = await self._simulate_risk_scenarios(factors, context, 10000)
        
        # Calculate VaR at 95% and 99% confidence levels
        var_95 = np.percentile(scenarios, 5)  # 5th percentile
        var_99 = np.percentile(scenarios, 1)   # 1st percentile
        
        return var_95, var_99
    
    async def _calculate_expected_loss(self, factors: List[RiskFactor], context: Dict[str, Any]) -> float:
        """Calculate expected loss"""
        if not factors:
            return 0.0
        
        expected_loss = 0.0
        for factor in factors:
            expected_loss += factor.probability * factor.impact * 1000000  # Assume 1M exposure
        
        return expected_loss
    
    async def _simulate_risk_scenarios(self, factors: List[RiskFactor], context: Dict[str, Any], num_scenarios: int) -> List[float]:
        """Simulate risk scenarios using Monte Carlo"""
        scenarios = []
        
        for _ in range(num_scenarios):
            scenario_loss = 0.0
            
            for factor in factors:
                # Generate random probability
                random_prob = np.random.random()
                
                if random_prob < factor.probability:
                    # Risk materializes
                    impact = factor.impact * np.random.normal(1.0, 0.1)  # Add some randomness
                    scenario_loss += impact * 1000000  # Assume 1M exposure
            
            scenarios.append(scenario_loss)
        
        return scenarios
    
    async def _calculate_correlation_adjustment(self, factors: List[RiskFactor]) -> float:
        """Calculate correlation adjustment for risk probability"""
        if len(factors) < 2:
            return 1.0
        
        # Calculate average correlation
        total_correlation = 0.0
        correlation_count = 0
        
        for i, factor1 in enumerate(factors):
            for j, factor2 in enumerate(factors[i+1:], i+1):
                if factor2.factor_id in factor1.correlation_matrix:
                    correlation = factor1.correlation_matrix[factor2.factor_id]
                    total_correlation += correlation
                    correlation_count += 1
        
        if correlation_count == 0:
            return 1.0
        
        average_correlation = total_correlation / correlation_count
        
        # Higher correlation increases risk probability
        return 1.0 + (average_correlation * 0.2)
    
    async def _perform_stress_testing(self, risk_type: RiskType, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform stress testing for the risk type"""
        stress_results = {}
        
        # Get relevant scenarios
        relevant_scenarios = [scenario for scenario in self.risk_scenarios.values() 
                             if risk_type.value in scenario.triggers or risk_type.value in scenario.consequences]
        
        for scenario in relevant_scenarios:
            # Calculate stress impact
            stress_impact = await self._calculate_stress_impact(scenario, risk_type, context)
            stress_results[scenario.scenario_id] = {
                "scenario_name": scenario.name,
                "probability": scenario.probability,
                "impact": stress_impact,
                "duration": scenario.duration,
                "recovery_time": scenario.recovery_time
            }
        
        return stress_results
    
    async def _calculate_stress_impact(self, scenario: RiskScenario, risk_type: RiskType, context: Dict[str, Any]) -> float:
        """Calculate impact of stress scenario"""
        # Base impact from scenario
        base_impact = scenario.impact
        
        # Adjust based on risk type
        if risk_type == RiskType.CREDIT_RISK:
            impact_multiplier = 1.2  # Credit risk amplifies in stress
        elif risk_type == RiskType.MARKET_RISK:
            impact_multiplier = 1.5  # Market risk highly sensitive to stress
        elif risk_type == RiskType.OPERATIONAL_RISK:
            impact_multiplier = 1.1  # Operational risk moderately sensitive
        else:
            impact_multiplier = 1.0
        
        return base_impact * impact_multiplier
    
    async def _analyze_correlations(self, factors: List[RiskFactor], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze correlations between risk factors"""
        correlation_analysis = {
            "factor_correlations": {},
            "high_correlations": [],
            "diversification_opportunities": []
        }
        
        # Calculate pairwise correlations
        for i, factor1 in enumerate(factors):
            for j, factor2 in enumerate(factors[i+1:], i+1):
                correlation = factor1.correlation_matrix.get(factor2.factor_id, 0.0)
                correlation_analysis["factor_correlations"][f"{factor1.factor_id}_{factor2.factor_id}"] = correlation
                
                if correlation > 0.7:
                    correlation_analysis["high_correlations"].append({
                        "factor1": factor1.factor_id,
                        "factor2": factor2.factor_id,
                        "correlation": correlation
                    })
                elif correlation < 0.3:
                    correlation_analysis["diversification_opportunities"].append({
                        "factor1": factor1.factor_id,
                        "factor2": factor2.factor_id,
                        "correlation": correlation
                    })
        
        return correlation_analysis
    
    async def _analyze_scenarios(self, risk_type: RiskType, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk scenarios"""
        scenario_analysis = {
            "relevant_scenarios": [],
            "scenario_probabilities": {},
            "scenario_impacts": {},
            "mitigation_effectiveness": {}
        }
        
        # Get relevant scenarios
        relevant_scenarios = [scenario for scenario in self.risk_scenarios.values() 
                             if risk_type.value in scenario.triggers or risk_type.value in scenario.consequences]
        
        for scenario in relevant_scenarios:
            scenario_analysis["relevant_scenarios"].append(scenario.scenario_id)
            scenario_analysis["scenario_probabilities"][scenario.scenario_id] = scenario.probability
            scenario_analysis["scenario_impacts"][scenario.scenario_id] = scenario.impact
            
            # Calculate mitigation effectiveness
            mitigation_effectiveness = await self._calculate_mitigation_effectiveness(scenario, risk_type)
            scenario_analysis["mitigation_effectiveness"][scenario.scenario_id] = mitigation_effectiveness
        
        return scenario_analysis
    
    async def _calculate_mitigation_effectiveness(self, scenario: RiskScenario, risk_type: RiskType) -> float:
        """Calculate effectiveness of mitigation actions"""
        # Base effectiveness from scenario mitigation actions
        base_effectiveness = 0.5
        
        # Adjust based on risk type
        if risk_type == RiskType.CREDIT_RISK:
            effectiveness_multiplier = 0.8  # Credit risk mitigation is challenging
        elif risk_type == RiskType.MARKET_RISK:
            effectiveness_multiplier = 0.6  # Market risk mitigation is difficult
        elif risk_type == RiskType.OPERATIONAL_RISK:
            effectiveness_multiplier = 0.9  # Operational risk mitigation is more effective
        else:
            effectiveness_multiplier = 0.7
        
        return base_effectiveness * effectiveness_multiplier
    
    async def _generate_risk_recommendations(self, risk_score: float, factors: List[RiskFactor], context: Dict[str, Any]) -> List[str]:
        """Generate risk recommendations"""
        recommendations = []
        
        # Risk level based recommendations
        if risk_score > 0.8:
            recommendations.append("CRITICAL: Implement immediate risk mitigation measures")
            recommendations.append("Consider reducing exposure to high-risk areas")
            recommendations.append("Increase monitoring frequency and intensity")
        elif risk_score > 0.6:
            recommendations.append("HIGH: Implement enhanced risk controls")
            recommendations.append("Review and update risk management policies")
            recommendations.append("Conduct additional stress testing")
        elif risk_score > 0.4:
            recommendations.append("MEDIUM: Monitor risk indicators closely")
            recommendations.append("Consider preventive measures")
            recommendations.append("Review risk appetite and limits")
        else:
            recommendations.append("LOW: Maintain current risk management practices")
            recommendations.append("Continue regular monitoring")
        
        # Factor-specific recommendations
        for factor in factors:
            if factor.probability > 0.7:
                recommendations.append(f"High probability risk factor: {factor.name} - implement specific controls")
            if factor.impact > 0.7:
                recommendations.append(f"High impact risk factor: {factor.name} - develop mitigation strategies")
        
        return recommendations
    
    def _determine_risk_level(self, risk_score: float) -> RiskSeverity:
        """Determine risk level based on score"""
        if risk_score >= 0.8:
            return RiskSeverity.CRITICAL
        elif risk_score >= 0.6:
            return RiskSeverity.HIGH
        elif risk_score >= 0.4:
            return RiskSeverity.MEDIUM
        else:
            return RiskSeverity.LOW
    
    async def perform_stress_test(self, risk_type: RiskType, scenario_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform specific stress test"""
        scenario = self.risk_scenarios.get(scenario_id)
        if not scenario:
            return {"error": "Scenario not found"}
        
        # Calculate stress test results
        stress_impact = await self._calculate_stress_impact(scenario, risk_type, context)
        
        # Calculate capital impact
        capital_impact = stress_impact * 0.1  # Assume 10% capital impact
        
        # Calculate liquidity impact
        liquidity_impact = stress_impact * 0.05  # Assume 5% liquidity impact
        
        return {
            "scenario_id": scenario_id,
            "scenario_name": scenario.name,
            "stress_impact": stress_impact,
            "capital_impact": capital_impact,
            "liquidity_impact": liquidity_impact,
            "duration": scenario.duration,
            "recovery_time": scenario.recovery_time,
            "mitigation_actions": scenario.mitigation_actions
        }
    
    async def calculate_portfolio_risk(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate portfolio-level risk"""
        portfolio_risk = {
            "total_risk_score": 0.0,
            "risk_contributions": {},
            "diversification_benefit": 0.0,
            "concentration_risk": 0.0,
            "correlation_risk": 0.0
        }
        
        # Calculate individual risk contributions
        total_weight = 0.0
        weighted_risk = 0.0
        
        for asset, data in portfolio_data.items():
            weight = data.get("weight", 0.0)
            risk_score = data.get("risk_score", 0.0)
            
            total_weight += weight
            weighted_risk += weight * risk_score
            portfolio_risk["risk_contributions"][asset] = weight * risk_score
        
        if total_weight > 0:
            portfolio_risk["total_risk_score"] = weighted_risk / total_weight
        
        # Calculate diversification benefit
        individual_risks = [data.get("risk_score", 0.0) for data in portfolio_data.values()]
        if individual_risks:
            max_individual_risk = max(individual_risks)
            portfolio_risk["diversification_benefit"] = max(0, max_individual_risk - portfolio_risk["total_risk_score"])
        
        return portfolio_risk
    
    async def get_risk_statistics(self) -> Dict[str, Any]:
        """Get risk statistics"""
        if not self.assessment_history:
            return {"total_assessments": 0}
        
        risk_types = defaultdict(int)
        risk_scores = []
        
        for assessment in self.assessment_history:
            risk_types[assessment.risk_type.value] += 1
            risk_scores.append(assessment.overall_risk_score)
        
        return {
            "total_assessments": len(self.assessment_history),
            "risk_type_distribution": dict(risk_types),
            "average_risk_score": sum(risk_scores) / len(risk_scores),
            "highest_risk_score": max(risk_scores),
            "lowest_risk_score": min(risk_scores)
        }
