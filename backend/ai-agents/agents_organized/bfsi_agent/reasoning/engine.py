"""
Enhanced BFSI Agent Logical Reasoning Engine
Advanced decision-making, risk analysis, and compliance reasoning capabilities
"""

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
import numpy as np
from collections import defaultdict
import math

# Configure logging
logger = logging.getLogger(__name__)

class ReasoningType(Enum):
    """Types of reasoning operations"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    CAUSAL = "causal"
    PROBABILISTIC = "probabilistic"
    TEMPORAL = "temporal"

class ConfidenceLevel(Enum):
    """Confidence levels for reasoning results"""
    VERY_LOW = 0.1
    LOW = 0.3
    MEDIUM = 0.5
    HIGH = 0.7
    VERY_HIGH = 0.9

@dataclass
class ReasoningContext:
    """Context for reasoning operations"""
    operation_id: str
    context_type: str
    data: Dict[str, Any]
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    temporal_window: Optional[timedelta] = None
    confidence_threshold: float = 0.7

@dataclass
class ReasoningResult:
    """Result of a reasoning operation"""
    result_id: str
    reasoning_type: ReasoningType
    conclusion: str
    confidence: float
    evidence: List[Dict[str, Any]]
    assumptions: List[str]
    limitations: List[str]
    recommendations: List[str]
    timestamp: datetime
    reasoning_chain: List[Dict[str, Any]]

@dataclass
class RiskFactor:
    """Risk factor with reasoning attributes"""
    factor_id: str
    name: str
    category: str
    weight: float
    probability: float
    impact: float
    correlation_factors: List[str]
    temporal_dependencies: List[str]
    reasoning_basis: str

@dataclass
class ComplianceRule:
    """Compliance rule with reasoning logic"""
    rule_id: str
    regulation: str
    requirement: str
    condition: str
    action: str
    reasoning_logic: str
    exceptions: List[str]
    dependencies: List[str]

class BFSIReasoningEngine:
    """
    Enhanced BFSI Reasoning Engine with advanced logical capabilities
    """
    
    def __init__(self):
        self.engine_id = "bfsi_reasoning_engine"
        self.reasoning_history: List[ReasoningResult] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.risk_factors: Dict[str, RiskFactor] = {}
        self.compliance_rules: Dict[str, ComplianceRule] = {}
        self.reasoning_patterns: Dict[str, List[Dict[str, Any]]] = {}
        
        # Initialize knowledge base
        self._initialize_knowledge_base()
        self._initialize_risk_factors()
        self._initialize_compliance_rules()
        
        logger.info("BFSI Reasoning Engine initialized with advanced logical capabilities")
    
    def _initialize_knowledge_base(self):
        """Initialize BFSI knowledge base with reasoning rules"""
        self.knowledge_base = {
            "regulatory_frameworks": {
                "basel_iii": {
                    "capital_requirements": {
                        "tier_1_minimum": 6.0,
                        "total_capital_minimum": 8.0,
                        "leverage_ratio_minimum": 3.0,
                        "reasoning": "Higher capital ratios indicate better financial stability"
                    },
                    "liquidity_requirements": {
                        "lcr_minimum": 100.0,
                        "nsfr_minimum": 100.0,
                        "reasoning": "Adequate liquidity ensures operational continuity"
                    }
                },
                "sox": {
                    "internal_controls": {
                        "effectiveness_threshold": 0.95,
                        "reasoning": "Strong internal controls prevent financial misstatements"
                    }
                }
            },
            "risk_categories": {
                "credit_risk": {
                    "factors": ["default_probability", "recovery_rate", "exposure_at_default"],
                    "reasoning": "Credit risk increases with higher default probability and lower recovery rates"
                },
                "market_risk": {
                    "factors": ["volatility", "correlation", "liquidity"],
                    "reasoning": "Market risk escalates during high volatility and low liquidity periods"
                },
                "operational_risk": {
                    "factors": ["process_failure", "system_outage", "human_error"],
                    "reasoning": "Operational risk is inversely related to process maturity and system reliability"
                }
            },
            "compliance_patterns": {
                "aml_patterns": {
                    "suspicious_transactions": {
                        "threshold": 10000,
                        "reasoning": "Transactions above threshold require enhanced due diligence"
                    }
                }
            }
        }
    
    def _initialize_risk_factors(self):
        """Initialize risk factors with reasoning attributes"""
        risk_factors_data = [
            {
                "factor_id": "credit_default_probability",
                "name": "Credit Default Probability",
                "category": "credit_risk",
                "weight": 0.4,
                "probability": 0.05,
                "impact": 0.8,
                "correlation_factors": ["economic_conditions", "industry_performance"],
                "temporal_dependencies": ["quarterly_reports", "market_conditions"],
                "reasoning_basis": "Historical default rates and current economic indicators"
            },
            {
                "factor_id": "market_volatility",
                "name": "Market Volatility",
                "category": "market_risk",
                "weight": 0.3,
                "probability": 0.3,
                "impact": 0.6,
                "correlation_factors": ["interest_rates", "currency_fluctuations"],
                "temporal_dependencies": ["daily_market_data", "economic_announcements"],
                "reasoning_basis": "Volatility clustering and mean reversion patterns"
            },
            {
                "factor_id": "operational_control_failure",
                "name": "Operational Control Failure",
                "category": "operational_risk",
                "weight": 0.3,
                "probability": 0.1,
                "impact": 0.7,
                "correlation_factors": ["system_reliability", "staff_training"],
                "temporal_dependencies": ["system_updates", "staff_changes"],
                "reasoning_basis": "Control effectiveness and process maturity assessment"
            }
        ]
        
        for factor_data in risk_factors_data:
            self.risk_factors[factor_data["factor_id"]] = RiskFactor(**factor_data)
    
    def _initialize_compliance_rules(self):
        """Initialize compliance rules with reasoning logic"""
        compliance_rules_data = [
            {
                "rule_id": "basel_capital_adequacy",
                "regulation": "Basel III",
                "requirement": "Maintain minimum capital ratios",
                "condition": "tier_1_ratio >= 6.0 AND total_capital_ratio >= 8.0",
                "action": "Monitor capital levels and implement capital planning",
                "reasoning_logic": "Capital ratios below minimum indicate insufficient capital buffer",
                "exceptions": ["temporary_waivers", "regulatory_approval"],
                "dependencies": ["capital_calculation", "risk_weighted_assets"]
            },
            {
                "rule_id": "aml_transaction_monitoring",
                "regulation": "AML/CTF",
                "requirement": "Monitor suspicious transactions",
                "condition": "transaction_amount > 10000 OR unusual_pattern_detected",
                "action": "File SAR and conduct enhanced due diligence",
                "reasoning_logic": "Large transactions and unusual patterns may indicate money laundering",
                "exceptions": ["legitimate_business_transactions"],
                "dependencies": ["customer_risk_assessment", "transaction_history"]
            }
        ]
        
        for rule_data in compliance_rules_data:
            self.compliance_rules[rule_data["rule_id"]] = ComplianceRule(**rule_data)
    
    async def perform_deductive_reasoning(self, context: ReasoningContext) -> ReasoningResult:
        """Perform deductive reasoning from general principles to specific conclusions"""
        logger.info(f"Performing deductive reasoning for operation: {context.operation_id}")
        
        try:
            reasoning_chain = []
            evidence = []
            assumptions = []
            limitations = []
            
            # Extract premises from context
            premises = context.data.get("premises", [])
            conclusion = context.data.get("conclusion", "")
            
            # Build reasoning chain
            for premise in premises:
                reasoning_chain.append({
                    "step": "premise",
                    "content": premise,
                    "confidence": 0.9,
                    "reasoning": "Given premise"
                })
            
            # Apply logical rules
            if context.context_type == "risk_assessment":
                conclusion, confidence = await self._deduce_risk_conclusion(premises, context)
            elif context.context_type == "compliance_check":
                conclusion, confidence = await self._deduce_compliance_conclusion(premises, context)
            else:
                conclusion = "No specific conclusion reached"
                confidence = 0.5
            
            # Generate evidence
            evidence = await self._generate_evidence(conclusion, context)
            
            # Identify assumptions
            assumptions = await self._identify_assumptions(premises, context)
            
            # Identify limitations
            limitations = await self._identify_limitations(context)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(conclusion, confidence, context)
            
            result = ReasoningResult(
                result_id=str(uuid.uuid4()),
                reasoning_type=ReasoningType.DEDUCTIVE,
                conclusion=conclusion,
                confidence=confidence,
                evidence=evidence,
                assumptions=assumptions,
                limitations=limitations,
                recommendations=recommendations,
                timestamp=datetime.now(),
                reasoning_chain=reasoning_chain
            )
            
            self.reasoning_history.append(result)
            return result
            
        except Exception as e:
            logger.error(f"Deductive reasoning failed for operation {context.operation_id}: {str(e)}")
            
            # Return failure result with comprehensive error information
            error_result = ReasoningResult(
                result_id=str(uuid.uuid4()),
                reasoning_type=ReasoningType.DEDUCTIVE,
                conclusion=f"Deductive reasoning failed: {str(e)}",
                confidence=0.0,
                evidence=[],
                assumptions=[f"Error occurred during reasoning: {type(e).__name__}"],
                limitations=[f"System error prevented successful reasoning execution"],
                recommendations=[
                    "Review input data for validity",
                    "Check system logs for detailed error information",
                    "Retry operation after addressing underlying issues"
                ],
                timestamp=datetime.now(),
                reasoning_chain=[]
            )
            
            self.reasoning_history.append(error_result)
            return error_result
    
    async def perform_inductive_reasoning(self, context: ReasoningContext) -> ReasoningResult:
        """Perform inductive reasoning from specific observations to general patterns"""
        logger.info(f"Performing inductive reasoning for operation: {context.operation_id}")
        
        observations = context.data.get("observations", [])
        patterns = await self._identify_patterns(observations, context)
        
        # Build reasoning chain
        reasoning_chain = []
        for i, observation in enumerate(observations):
            reasoning_chain.append({
                "step": f"observation_{i+1}",
                "content": observation,
                "confidence": 0.8,
                "reasoning": "Observed data point"
            })
        
        # Generalize from patterns
        conclusion = await self._generalize_from_patterns(patterns, context)
        confidence = await self._calculate_inductive_confidence(patterns, observations)
        
        # Generate evidence
        evidence = await self._generate_evidence(conclusion, context)
        
        # Identify assumptions
        assumptions = await self._identify_assumptions(observations, context)
        
        # Identify limitations
        limitations = await self._identify_limitations(context)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(conclusion, confidence, context)
        
        result = ReasoningResult(
            result_id=str(uuid.uuid4()),
            reasoning_type=ReasoningType.INDUCTIVE,
            conclusion=conclusion,
            confidence=confidence,
            evidence=evidence,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            timestamp=datetime.now(),
            reasoning_chain=reasoning_chain
        )
        
        self.reasoning_history.append(result)
        return result
    
    async def perform_abductive_reasoning(self, context: ReasoningContext) -> ReasoningResult:
        """Perform abductive reasoning to find the best explanation for observations"""
        logger.info(f"Performing abductive reasoning for operation: {context.operation_id}")
        
        observations = context.data.get("observations", [])
        possible_explanations = await self._generate_explanations(observations, context)
        
        # Evaluate explanations
        best_explanation = await self._evaluate_explanations(possible_explanations, context)
        
        # Build reasoning chain
        reasoning_chain = []
        for i, observation in enumerate(observations):
            reasoning_chain.append({
                "step": f"observation_{i+1}",
                "content": observation,
                "confidence": 0.8,
                "reasoning": "Observed phenomenon"
            })
        
        reasoning_chain.append({
            "step": "explanation",
            "content": best_explanation["explanation"],
            "confidence": best_explanation["confidence"],
            "reasoning": "Best explanation for observations"
        })
        
        conclusion = best_explanation["explanation"]
        confidence = best_explanation["confidence"]
        
        # Generate evidence
        evidence = await self._generate_evidence(conclusion, context)
        
        # Identify assumptions
        assumptions = await self._identify_assumptions(observations, context)
        
        # Identify limitations
        limitations = await self._identify_limitations(context)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(conclusion, confidence, context)
        
        result = ReasoningResult(
            result_id=str(uuid.uuid4()),
            reasoning_type=ReasoningType.ABDUCTIVE,
            conclusion=conclusion,
            confidence=confidence,
            evidence=evidence,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            timestamp=datetime.now(),
            reasoning_chain=reasoning_chain
        )
        
        self.reasoning_history.append(result)
        return result
    
    async def perform_probabilistic_reasoning(self, context: ReasoningContext) -> ReasoningResult:
        """Perform probabilistic reasoning with uncertainty quantification"""
        logger.info(f"Performing probabilistic reasoning for operation: {context.operation_id}")
        
        # Extract probability distributions
        distributions = context.data.get("distributions", {})
        events = context.data.get("events", [])
        
        # Calculate joint probabilities
        joint_probability = await self._calculate_joint_probability(distributions, events)
        
        # Perform Bayesian inference
        posterior_probability = await self._bayesian_inference(distributions, context)
        
        # Build reasoning chain
        reasoning_chain = []
        for event, prob in distributions.items():
            reasoning_chain.append({
                "step": f"probability_{event}",
                "content": f"P({event}) = {prob}",
                "confidence": 0.9,
                "reasoning": "Given probability distribution"
            })
        
        reasoning_chain.append({
            "step": "joint_probability",
            "content": f"Joint probability = {joint_probability}",
            "confidence": 0.8,
            "reasoning": "Calculated joint probability"
        })
        
        conclusion = f"Based on probabilistic analysis, the likelihood is {posterior_probability:.2f}"
        confidence = posterior_probability
        
        # Generate evidence
        evidence = await self._generate_evidence(conclusion, context)
        
        # Identify assumptions
        assumptions = await self._identify_assumptions(list(distributions.keys()), context)
        
        # Identify limitations
        limitations = await self._identify_limitations(context)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(conclusion, confidence, context)
        
        result = ReasoningResult(
            result_id=str(uuid.uuid4()),
            reasoning_type=ReasoningType.PROBABILISTIC,
            conclusion=conclusion,
            confidence=confidence,
            evidence=evidence,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            timestamp=datetime.now(),
            reasoning_chain=reasoning_chain
        )
        
        self.reasoning_history.append(result)
        return result
    
    async def perform_causal_reasoning(self, context: ReasoningContext) -> ReasoningResult:
        """Perform causal reasoning to identify cause-effect relationships"""
        logger.info(f"Performing causal reasoning for operation: {context.operation_id}")
        
        # Extract causal relationships
        causes = context.data.get("causes", [])
        effects = context.data.get("effects", [])
        
        # Identify causal chains
        causal_chains = await self._identify_causal_chains(causes, effects, context)
        
        # Calculate causal strength
        causal_strength = await self._calculate_causal_strength(causal_chains, context)
        
        # Build reasoning chain
        reasoning_chain = []
        for i, cause in enumerate(causes):
            reasoning_chain.append({
                "step": f"cause_{i+1}",
                "content": cause,
                "confidence": 0.8,
                "reasoning": "Identified causal factor"
            })
        
        for i, effect in enumerate(effects):
            reasoning_chain.append({
                "step": f"effect_{i+1}",
                "content": effect,
                "confidence": 0.8,
                "reasoning": "Observed effect"
            })
        
        reasoning_chain.append({
            "step": "causal_relationship",
            "content": f"Causal strength: {causal_strength:.2f}",
            "confidence": 0.7,
            "reasoning": "Calculated causal relationship strength"
        })
        
        conclusion = f"Causal analysis shows {causal_strength:.2f} strength relationship between identified factors"
        confidence = causal_strength
        
        # Generate evidence
        evidence = await self._generate_evidence(conclusion, context)
        
        # Identify assumptions
        assumptions = await self._identify_assumptions(causes + effects, context)
        
        # Identify limitations
        limitations = await self._identify_limitations(context)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(conclusion, confidence, context)
        
        result = ReasoningResult(
            result_id=str(uuid.uuid4()),
            reasoning_type=ReasoningType.CAUSAL,
            conclusion=conclusion,
            confidence=confidence,
            evidence=evidence,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            timestamp=datetime.now(),
            reasoning_chain=reasoning_chain
        )
        
        self.reasoning_history.append(result)
        return result
    
    async def perform_temporal_reasoning(self, context: ReasoningContext) -> ReasoningResult:
        """Perform temporal reasoning to analyze time-based patterns and predictions"""
        logger.info(f"Performing temporal reasoning for operation: {context.operation_id}")
        
        # Extract temporal data
        time_series = context.data.get("time_series", [])
        temporal_patterns = await self._identify_temporal_patterns(time_series, context)
        
        # Predict future trends
        predictions = await self._predict_future_trends(temporal_patterns, context)
        
        # Build reasoning chain
        reasoning_chain = []
        for i, data_point in enumerate(time_series):
            reasoning_chain.append({
                "step": f"temporal_data_{i+1}",
                "content": f"Time: {data_point.get('timestamp', 'unknown')}, Value: {data_point.get('value', 'unknown')}",
                "confidence": 0.8,
                "reasoning": "Temporal data point"
            })
        
        reasoning_chain.append({
            "step": "temporal_pattern",
            "content": f"Identified pattern: {temporal_patterns}",
            "confidence": 0.7,
            "reasoning": "Pattern analysis"
        })
        
        reasoning_chain.append({
            "step": "prediction",
            "content": f"Future prediction: {predictions}",
            "confidence": 0.6,
            "reasoning": "Temporal projection"
        })
        
        conclusion = f"Temporal analysis reveals {temporal_patterns} with predicted future trend: {predictions}"
        confidence = 0.7
        
        # Generate evidence
        evidence = await self._generate_evidence(conclusion, context)
        
        # Identify assumptions
        assumptions = await self._identify_assumptions(time_series, context)
        
        # Identify limitations
        limitations = await self._identify_limitations(context)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(conclusion, confidence, context)
        
        result = ReasoningResult(
            result_id=str(uuid.uuid4()),
            reasoning_type=ReasoningType.TEMPORAL,
            conclusion=conclusion,
            confidence=confidence,
            evidence=evidence,
            assumptions=assumptions,
            limitations=limitations,
            recommendations=recommendations,
            timestamp=datetime.now(),
            reasoning_chain=reasoning_chain
        )
        
        self.reasoning_history.append(result)
        return result
    
    async def _deduce_risk_conclusion(self, premises: List[str], context: ReasoningContext) -> Tuple[str, float]:
        """Deduce risk-related conclusions from premises"""
        # Analyze premises for risk indicators
        risk_indicators = []
        for premise in premises:
            # Skip non-string premises to prevent AttributeError
            if not isinstance(premise, str):
                continue
            
            premise_lower = premise.lower()
            if "high" in premise_lower and ("risk" in premise_lower or "volatility" in premise_lower):
                risk_indicators.append("high_risk")
            elif "low" in premise_lower and ("risk" in premise_lower or "volatility" in premise_lower):
                risk_indicators.append("low_risk")
        
        if "high_risk" in risk_indicators:
            return "High risk conditions detected requiring immediate attention", 0.8
        elif "low_risk" in risk_indicators:
            return "Low risk conditions with acceptable risk levels", 0.7
        else:
            return "Moderate risk conditions requiring monitoring", 0.6
    
    async def _deduce_compliance_conclusion(self, premises: List[str], context: ReasoningContext) -> Tuple[str, float]:
        """Deduce compliance-related conclusions from premises"""
        # Analyze premises for compliance indicators
        compliance_indicators = []
        for premise in premises:
            # Skip non-string premises to prevent AttributeError
            if not isinstance(premise, str):
                continue
            
            premise_lower = premise.lower()
            if "compliant" in premise_lower or "meets" in premise_lower:
                compliance_indicators.append("compliant")
            elif "violation" in premise_lower or "non-compliant" in premise_lower:
                compliance_indicators.append("non_compliant")
        
        if "non_compliant" in compliance_indicators:
            return "Compliance violations detected requiring immediate remediation", 0.9
        elif "compliant" in compliance_indicators:
            return "Compliance requirements met with current controls", 0.8
        else:
            return "Compliance status requires further assessment", 0.6
    
    async def _identify_patterns(self, observations: List[Any], context: ReasoningContext) -> List[str]:
        """Identify patterns in observations"""
        patterns = []
        
        # Simple pattern identification
        if len(observations) > 1:
            # Validate that all observations are numeric before trend analysis
            try:
                # Validate that all observations are instances of int or float
                numeric_observations = []
                for obs in observations:
                    if isinstance(obs, (int, float)):
                        numeric_observations.append(obs)
                    else:
                        logger.warning(f"Non-numeric observation found in trend analysis: {obs} (type: {type(obs).__name__})")
                        return patterns  # Return early if non-numeric values found
                
                # Check for increasing trend
                if all(numeric_observations[i] < numeric_observations[i+1] for i in range(len(numeric_observations)-1)):
                    patterns.append("increasing_trend")
                
                # Check for decreasing trend
                if all(numeric_observations[i] > numeric_observations[i+1] for i in range(len(numeric_observations)-1)):
                    patterns.append("decreasing_trend")
                    
            except (TypeError, ValueError) as e:
                logger.warning(f"Error during trend analysis due to non-numeric values: {str(e)}")
                return patterns
            
            # Check for cyclical pattern
            if len(numeric_observations) >= 4:
                mid_point = len(numeric_observations) // 2
                first_half = numeric_observations[:mid_point]
                second_half = numeric_observations[mid_point:]
                if abs(sum(first_half) - sum(second_half)) < 0.1 * sum(numeric_observations):
                    patterns.append("cyclical_pattern")
        
        return patterns
    
    async def _generalize_from_patterns(self, patterns: List[str], context: ReasoningContext) -> str:
        """Generalize conclusions from identified patterns"""
        if "increasing_trend" in patterns:
            return "Data shows increasing trend indicating potential escalation"
        elif "decreasing_trend" in patterns:
            return "Data shows decreasing trend indicating improvement"
        elif "cyclical_pattern" in patterns:
            return "Data shows cyclical pattern indicating recurring behavior"
        else:
            return "No clear patterns identified in the data"
    
    async def _calculate_inductive_confidence(self, patterns: List[str], observations: List[Any]) -> float:
        """Calculate confidence for inductive reasoning"""
        base_confidence = 0.5
        
        # Increase confidence based on pattern strength
        if len(patterns) > 0:
            base_confidence += 0.2
        
        # Increase confidence based on number of observations
        if len(observations) > 5:
            base_confidence += 0.1
        
        return min(base_confidence, 0.9)
    
    async def _generate_explanations(self, observations: List[Any], context: ReasoningContext) -> List[Dict[str, Any]]:
        """Generate possible explanations for observations"""
        explanations = []
        
        # Generate explanations based on context type
        if context.context_type == "risk_assessment":
            explanations.extend([
                {
                    "explanation": "Market volatility causing increased risk exposure",
                    "confidence": 0.7,
                    "evidence": ["volatility_indicators", "market_data"]
                },
                {
                    "explanation": "Operational inefficiencies leading to risk accumulation",
                    "confidence": 0.6,
                    "evidence": ["process_metrics", "control_effectiveness"]
                }
            ])
        elif context.context_type == "compliance_check":
            explanations.extend([
                {
                    "explanation": "Regulatory changes requiring policy updates",
                    "confidence": 0.8,
                    "evidence": ["regulatory_updates", "policy_gaps"]
                },
                {
                    "explanation": "Control failures leading to compliance gaps",
                    "confidence": 0.7,
                    "evidence": ["control_testing", "audit_findings"]
                }
            ])
        
        return explanations
    
    async def _evaluate_explanations(self, explanations: List[Dict[str, Any]], context: ReasoningContext) -> Dict[str, Any]:
        """Evaluate and select the best explanation"""
        if not explanations:
            return {
                "explanation": "No explanation available",
                "confidence": 0.0
            }
        
        # Select explanation with highest confidence
        best_explanation = max(explanations, key=lambda x: x["confidence"])
        return best_explanation
    
    async def _calculate_joint_probability(self, distributions: Dict[str, float], events: List[str]) -> float:
        """Calculate joint probability of events"""
        if not distributions or not events:
            return 0.0
        
        # Simple joint probability calculation
        joint_prob = 1.0
        for event in events:
            if event in distributions:
                joint_prob *= distributions[event]
        
        return joint_prob
    
    async def _bayesian_inference(self, distributions: Dict[str, float], context: ReasoningContext) -> float:
        """Perform Bayesian inference"""
        # Extract prior and likelihood from distributions with fallback defaults
        prior = distributions.get('prior', 0.5)  # Default prior if not provided
        likelihood = distributions.get('likelihood', 0.7)  # Default likelihood if not provided
        
        # Calculate posterior probability using Bayes' theorem
        posterior = (likelihood * prior) / ((likelihood * prior) + ((1 - likelihood) * (1 - prior)))
        
        return posterior
    
    async def _identify_causal_chains(self, causes: List[str], effects: List[str], context: ReasoningContext) -> List[Dict[str, Any]]:
        """Identify causal chains between causes and effects"""
        causal_chains = []
        
        for cause in causes:
            for effect in effects:
                # Simple causal relationship identification
                causal_strength = 0.5  # Default strength
                
                # Adjust strength based on context
                if context.context_type == "risk_assessment":
                    if "risk" in cause.lower() and "risk" in effect.lower():
                        causal_strength = 0.8
                
                causal_chains.append({
                    "cause": cause,
                    "effect": effect,
                    "strength": causal_strength
                })
        
        return causal_chains
    
    async def _calculate_causal_strength(self, causal_chains: List[Dict[str, Any]], context: ReasoningContext) -> float:
        """Calculate overall causal strength"""
        if not causal_chains:
            return 0.0
        
        # Calculate average causal strength
        total_strength = sum(chain["strength"] for chain in causal_chains)
        average_strength = total_strength / len(causal_chains)
        
        return average_strength
    
    async def _identify_temporal_patterns(self, time_series: List[Dict[str, Any]], context: ReasoningContext) -> List[str]:
        """Identify temporal patterns in time series data"""
        patterns = []
        
        if len(time_series) < 2:
            return patterns
        
        # Extract values
        values = [point.get("value", 0) for point in time_series if "value" in point]
        
        if len(values) < 2:
            return patterns
        
        # Validate that all values are numeric before trend analysis
        try:
            # Validate that all values are instances of int or float
            numeric_values = []
            for value in values:
                if isinstance(value, (int, float)):
                    numeric_values.append(value)
                else:
                    logger.warning(f"Non-numeric value found in temporal trend analysis: {value} (type: {type(value).__name__})")
                    return patterns  # Return early if non-numeric values found
            
            # Check for trends
            if all(numeric_values[i] <= numeric_values[i+1] for i in range(len(numeric_values)-1)):
                patterns.append("increasing_trend")
            elif all(numeric_values[i] >= numeric_values[i+1] for i in range(len(numeric_values)-1)):
                patterns.append("decreasing_trend")
                
        except (TypeError, ValueError) as e:
            logger.warning(f"Error during temporal trend analysis due to non-numeric values: {str(e)}")
            return patterns
        
        # Check for seasonality
        if len(numeric_values) >= 4:
            # Simple seasonality check
            mid_point = len(numeric_values) // 2
            first_half_avg = sum(numeric_values[:mid_point]) / mid_point
            second_half_avg = sum(numeric_values[mid_point:]) / (len(numeric_values) - mid_point)
            
            if abs(first_half_avg - second_half_avg) < 0.1 * max(numeric_values):
                patterns.append("seasonal_pattern")
        
        return patterns
    
    async def _predict_future_trends(self, patterns: List[str], context: ReasoningContext) -> str:
        """Predict future trends based on identified patterns"""
        if "increasing_trend" in patterns:
            return "Continued increase expected"
        elif "decreasing_trend" in patterns:
            return "Continued decrease expected"
        elif "seasonal_pattern" in patterns:
            return "Seasonal pattern likely to continue"
        else:
            return "Stable trend expected"
    
    async def _generate_evidence(self, conclusion: str, context: ReasoningContext) -> List[Dict[str, Any]]:
        """Generate evidence supporting the conclusion"""
        evidence = []
        
        # Generate evidence based on context type
        if context.context_type == "risk_assessment":
            evidence.append({
                "type": "risk_metrics",
                "description": "Risk assessment metrics",
                "confidence": 0.8,
                "source": "internal_risk_models"
            })
        elif context.context_type == "compliance_check":
            evidence.append({
                "type": "compliance_data",
                "description": "Compliance monitoring data",
                "confidence": 0.9,
                "source": "compliance_systems"
            })
        
        return evidence
    
    async def _identify_assumptions(self, data: List[Any], context: ReasoningContext) -> List[str]:
        """Identify assumptions made during reasoning"""
        assumptions = []
        
        # Common assumptions
        assumptions.append("Data quality is sufficient for analysis")
        assumptions.append("Historical patterns will continue")
        assumptions.append("External factors remain stable")
        
        # Context-specific assumptions
        if context.context_type == "risk_assessment":
            assumptions.append("Risk models are accurate and up-to-date")
        elif context.context_type == "compliance_check":
            assumptions.append("Regulatory requirements are correctly interpreted")
        
        return assumptions
    
    async def _identify_limitations(self, context: ReasoningContext) -> List[str]:
        """Identify limitations of the reasoning process"""
        limitations = []
        
        # Common limitations
        limitations.append("Limited by available data quality and quantity")
        limitations.append("Reasoning based on current knowledge and assumptions")
        limitations.append("External factors may change unexpectedly")
        
        # Context-specific limitations
        if context.context_type == "risk_assessment":
            limitations.append("Risk models may not capture all risk factors")
        elif context.context_type == "compliance_check":
            limitations.append("Regulatory interpretations may change")
        
        return limitations
    
    async def _generate_recommendations(self, conclusion: str, confidence: float, context: ReasoningContext) -> List[str]:
        """Generate recommendations based on reasoning results"""
        recommendations = []
        
        # Confidence-based recommendations
        if confidence < 0.5:
            recommendations.append("Gather additional data to improve confidence")
            recommendations.append("Consider alternative analysis methods")
        elif confidence > 0.8:
            recommendations.append("Proceed with high confidence in the conclusion")
            recommendations.append("Monitor for any changes in conditions")
        
        # Context-specific recommendations
        if context.context_type == "risk_assessment":
            recommendations.append("Implement risk mitigation measures")
            recommendations.append("Monitor risk indicators closely")
        elif context.context_type == "compliance_check":
            recommendations.append("Address any compliance gaps identified")
            recommendations.append("Update compliance monitoring procedures")
        
        return recommendations
    
    async def get_reasoning_history(self) -> List[Dict[str, Any]]:
        """Get history of reasoning operations"""
        return [asdict(result) for result in self.reasoning_history]
    
    async def get_reasoning_statistics(self) -> Dict[str, Any]:
        """Get statistics about reasoning operations"""
        if not self.reasoning_history:
            return {"total_operations": 0}
        
        reasoning_types = defaultdict(int)
        confidence_scores = []
        
        for result in self.reasoning_history:
            reasoning_types[result.reasoning_type.value] += 1
            confidence_scores.append(result.confidence)
        
        return {
            "total_operations": len(self.reasoning_history),
            "reasoning_type_distribution": dict(reasoning_types),
            "average_confidence": sum(confidence_scores) / len(confidence_scores),
            "highest_confidence": max(confidence_scores),
            "lowest_confidence": min(confidence_scores)
        }
