"""
Enhanced BFSI Decision-Making Engine
Advanced multi-criteria decision analysis with explainable AI capabilities
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

# Configure logging
logger = logging.getLogger(__name__)

class DecisionType(Enum):
    """Types of decisions"""
    RISK_MANAGEMENT = "risk_management"
    COMPLIANCE = "compliance"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    TACTICAL = "tactical"

class DecisionPriority(Enum):
    """Decision priorities"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class DecisionStatus(Enum):
    """Decision status"""
    PENDING = "pending"
    IN_ANALYSIS = "in_analysis"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    MONITORING = "monitoring"

@dataclass
class DecisionCriteria:
    """Decision criteria with weights and constraints"""
    criteria_id: str
    name: str
    weight: float
    constraint_type: str  # "minimize", "maximize", "target"
    target_value: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    importance: float = 1.0

@dataclass
class DecisionAlternative:
    """Decision alternative with performance metrics"""
    alternative_id: str
    name: str
    description: str
    performance_scores: Dict[str, float]
    costs: Dict[str, float]
    benefits: Dict[str, float]
    risks: List[str]
    implementation_time: int  # days
    success_probability: float

@dataclass
class DecisionContext:
    """Context for decision making"""
    decision_id: str
    decision_type: DecisionType
    priority: DecisionPriority
    description: str
    constraints: List[str]
    stakeholders: List[str]
    deadline: Optional[datetime] = None
    budget_limit: Optional[float] = None
    regulatory_requirements: List[str] = None

@dataclass
class DecisionResult:
    """Result of decision analysis"""
    result_id: str
    decision_id: str
    recommended_alternative: str
    confidence_score: float
    reasoning: str
    trade_offs: List[Dict[str, Any]]
    implementation_plan: Dict[str, Any]
    monitoring_requirements: List[str]
    risk_assessment: Dict[str, Any]
    compliance_impact: Dict[str, Any]
    timestamp: datetime

class BFSIDecisionEngine:
    """
    Enhanced BFSI Decision-Making Engine with advanced multi-criteria analysis
    """
    
    def __init__(self):
        self.engine_id = "bfsi_decision_engine"
        self.decision_history: List[DecisionResult] = []
        self.decision_criteria: Dict[str, DecisionCriteria] = {}
        self.decision_alternatives: Dict[str, DecisionAlternative] = {}
        self.decision_contexts: Dict[str, DecisionContext] = {}
        
        # Initialize decision frameworks
        self._initialize_decision_frameworks()
        self._initialize_criteria()
        
        logger.info("BFSI Decision Engine initialized with advanced multi-criteria analysis")
    
    def _initialize_decision_frameworks(self):
        """Initialize BFSI-specific decision frameworks"""
        self.decision_frameworks = {
            "risk_management": {
                "criteria": ["risk_reduction", "cost_effectiveness", "implementation_feasibility", "regulatory_compliance"],
                "weights": [0.4, 0.3, 0.2, 0.1],
                "constraints": ["budget_limit", "timeline", "regulatory_requirements"]
            },
            "compliance": {
                "criteria": ["regulatory_compliance", "cost_effectiveness", "operational_impact", "implementation_time"],
                "weights": [0.5, 0.2, 0.2, 0.1],
                "constraints": ["regulatory_deadlines", "budget", "resource_availability"]
            },
            "operational": {
                "criteria": ["efficiency", "cost_reduction", "quality_improvement", "customer_impact"],
                "weights": [0.3, 0.3, 0.2, 0.2],
                "constraints": ["budget", "timeline", "resource_constraints"]
            }
        }
    
    def _initialize_criteria(self):
        """Initialize decision criteria for BFSI operations"""
        criteria_data = [
            {
                "criteria_id": "risk_reduction",
                "name": "Risk Reduction",
                "weight": 0.4,
                "constraint_type": "maximize",
                "importance": 0.9
            },
            {
                "criteria_id": "cost_effectiveness",
                "name": "Cost Effectiveness",
                "weight": 0.3,
                "constraint_type": "maximize",
                "importance": 0.8
            },
            {
                "criteria_id": "regulatory_compliance",
                "name": "Regulatory Compliance",
                "weight": 0.5,
                "constraint_type": "target",
                "target_value": 1.0,
                "importance": 1.0
            },
            {
                "criteria_id": "implementation_feasibility",
                "name": "Implementation Feasibility",
                "weight": 0.2,
                "constraint_type": "maximize",
                "importance": 0.7
            },
            {
                "criteria_id": "operational_impact",
                "name": "Operational Impact",
                "weight": 0.2,
                "constraint_type": "minimize",
                "importance": 0.6
            }
        ]
        
        for criteria_data_item in criteria_data:
            self.decision_criteria[criteria_data_item["criteria_id"]] = DecisionCriteria(**criteria_data_item)
    
    async def analyze_decision(self, context: DecisionContext, alternatives: List[DecisionAlternative]) -> DecisionResult:
        """Analyze decision using multi-criteria analysis"""
        logger.info(f"Analyzing decision: {context.decision_id}")
        
        # Store context and alternatives
        self.decision_contexts[context.decision_id] = context
        for alternative in alternatives:
            self.decision_alternatives[alternative.alternative_id] = alternative
        
        # Perform multi-criteria analysis
        analysis_results = await self._perform_multi_criteria_analysis(context, alternatives)
        
        # Select best alternative
        recommended_alternative = await self._select_best_alternative(analysis_results, context)
        
        # Generate reasoning
        reasoning = await self._generate_decision_reasoning(recommended_alternative, analysis_results, context)
        
        # Calculate confidence score
        confidence_score = await self._calculate_confidence_score(analysis_results, context)
        
        # Identify trade-offs
        trade_offs = await self._identify_trade_offs(recommended_alternative, alternatives, context)
        
        # Create implementation plan
        implementation_plan = await self._create_implementation_plan(recommended_alternative, context)
        
        # Define monitoring requirements
        monitoring_requirements = await self._define_monitoring_requirements(recommended_alternative, context)
        
        # Assess risks
        risk_assessment = await self._assess_decision_risks(recommended_alternative, context)
        
        # Assess compliance impact
        compliance_impact = await self._assess_compliance_impact(recommended_alternative, context)
        
        # Create decision result
        result = DecisionResult(
            result_id=str(uuid.uuid4()),
            decision_id=context.decision_id,
            recommended_alternative=recommended_alternative,
            confidence_score=confidence_score,
            reasoning=reasoning,
            trade_offs=trade_offs,
            implementation_plan=implementation_plan,
            monitoring_requirements=monitoring_requirements,
            risk_assessment=risk_assessment,
            compliance_impact=compliance_impact,
            timestamp=datetime.now()
        )
        
        self.decision_history.append(result)
        return result
    
    async def _perform_multi_criteria_analysis(self, context: DecisionContext, alternatives: List[DecisionAlternative]) -> Dict[str, Any]:
        """Perform multi-criteria decision analysis"""
        analysis_results = {}
        
        # Get relevant criteria for decision type
        framework = self.decision_frameworks.get(context.decision_type.value, {})
        criteria_list = framework.get("criteria", [])
        weights = framework.get("weights", [])
        
        # Normalize weights
        if weights:
            total_weight = sum(weights)
            normalized_weights = [w / total_weight for w in weights]
        else:
            normalized_weights = [1.0 / len(criteria_list)] * len(criteria_list)
        
        # Calculate scores for each alternative
        for alternative in alternatives:
            scores = {}
            weighted_score = 0.0
            
            for i, criteria in enumerate(criteria_list):
                if criteria in alternative.performance_scores:
                    score = alternative.performance_scores[criteria]
                    scores[criteria] = score
                    weighted_score += score * normalized_weights[i]
            
            analysis_results[alternative.alternative_id] = {
                "scores": scores,
                "weighted_score": weighted_score,
                "alternative": alternative
            }
        
        return analysis_results
    
    async def _select_best_alternative(self, analysis_results: Dict[str, Any], context: DecisionContext) -> str:
        """Select the best alternative based on analysis results"""
        if not analysis_results:
            return "no_alternative"
        
        # Find alternative with highest weighted score
        best_alternative = max(analysis_results.items(), key=lambda x: x[1]["weighted_score"])
        
        return best_alternative[0]
    
    async def _generate_decision_reasoning(self, recommended_alternative: str, analysis_results: Dict[str, Any], context: DecisionContext) -> str:
        """Generate reasoning for the decision"""
        if recommended_alternative == "no_alternative":
            return "No suitable alternatives found for the given criteria"
        
        reasoning_parts = []
        
        # Add context reasoning
        reasoning_parts.append(f"Decision type: {context.decision_type.value}")
        reasoning_parts.append(f"Priority: {context.priority.value}")
        
        # Add criteria reasoning
        framework = self.decision_frameworks.get(context.decision_type.value, {})
        criteria_list = framework.get("criteria", [])
        reasoning_parts.append(f"Analysis based on criteria: {', '.join(criteria_list)}")
        
        # Add alternative reasoning
        if recommended_alternative in analysis_results:
            result = analysis_results[recommended_alternative]
            reasoning_parts.append(f"Selected alternative scored {result['weighted_score']:.2f} on weighted criteria")
            
            # Add specific criteria scores
            for criteria, score in result["scores"].items():
                reasoning_parts.append(f"{criteria}: {score:.2f}")
        
        return " | ".join(reasoning_parts)
    
    async def _calculate_confidence_score(self, analysis_results: Dict[str, Any], context: DecisionContext) -> float:
        """Calculate confidence score for the decision"""
        if not analysis_results:
            return 0.0
        
        # Base confidence on score differences
        scores = [result["weighted_score"] for result in analysis_results.values()]
        
        if len(scores) < 2:
            return 0.5
        
        # Calculate confidence based on score separation
        max_score = max(scores)
        second_max_score = sorted(scores, reverse=True)[1] if len(scores) > 1 else max_score
        
        score_difference = max_score - second_max_score
        confidence = min(0.5 + (score_difference * 2), 0.95)
        
        # Adjust confidence based on decision priority
        if context.priority == DecisionPriority.CRITICAL:
            confidence *= 0.9  # Lower confidence for critical decisions
        elif context.priority == DecisionPriority.LOW:
            confidence *= 1.1  # Higher confidence for low priority decisions
        
        return min(confidence, 0.95)
    
    async def _identify_trade_offs(self, recommended_alternative: str, alternatives: List[DecisionAlternative], context: DecisionContext) -> List[Dict[str, Any]]:
        """Identify trade-offs in the decision"""
        trade_offs = []
        
        if recommended_alternative == "no_alternative":
            return trade_offs
        
        # Find recommended alternative
        recommended = next((alt for alt in alternatives if alt.alternative_id == recommended_alternative), None)
        if not recommended:
            return trade_offs
        
        # Compare with other alternatives
        for alternative in alternatives:
            if alternative.alternative_id == recommended_alternative:
                continue
            
            trade_off = {
                "alternative": alternative.name,
                "advantages": [],
                "disadvantages": []
            }
            
            # Compare performance scores
            for criteria in recommended.performance_scores:
                if criteria in alternative.performance_scores:
                    recommended_score = recommended.performance_scores[criteria]
                    alternative_score = alternative.performance_scores[criteria]
                    
                    if recommended_score > alternative_score:
                        trade_off["advantages"].append(f"Better {criteria}: {recommended_score:.2f} vs {alternative_score:.2f}")
                    elif alternative_score > recommended_score:
                        trade_off["disadvantages"].append(f"Worse {criteria}: {recommended_score:.2f} vs {alternative_score:.2f}")
            
            if trade_off["advantages"] or trade_off["disadvantages"]:
                trade_offs.append(trade_off)
        
        return trade_offs
    
    async def _create_implementation_plan(self, recommended_alternative: str, context: DecisionContext) -> Dict[str, Any]:
        """Create implementation plan for the recommended alternative"""
        if recommended_alternative == "no_alternative":
            return {"status": "no_plan", "message": "No alternative selected"}
        
        # Find recommended alternative
        alternative = self.decision_alternatives.get(recommended_alternative)
        if not alternative:
            return {"status": "error", "message": "Alternative not found"}
        
        implementation_plan = {
            "status": "planned",
            "alternative_name": alternative.name,
            "implementation_time": alternative.implementation_time,
            "success_probability": alternative.success_probability,
            "phases": await self._create_implementation_phases(alternative, context),
            "resource_requirements": await self._estimate_resource_requirements(alternative, context),
            "risk_mitigation": await self._identify_risk_mitigation_measures(alternative, context)
        }
        
        return implementation_plan
    
    async def _create_implementation_phases(self, alternative: DecisionAlternative, context: DecisionContext) -> List[Dict[str, Any]]:
        """Create implementation phases for the alternative"""
        phases = []
        
        # Phase 1: Planning and Preparation
        phases.append({
            "phase": 1,
            "name": "Planning and Preparation",
            "duration": max(1, alternative.implementation_time // 4),
            "activities": [
                "Detailed planning",
                "Resource allocation",
                "Stakeholder communication",
                "Risk assessment"
            ],
            "deliverables": ["Implementation plan", "Resource allocation", "Risk register"]
        })
        
        # Phase 2: Implementation
        phases.append({
            "phase": 2,
            "name": "Implementation",
            "duration": alternative.implementation_time // 2,
            "activities": [
                "Execute implementation",
                "Monitor progress",
                "Address issues",
                "Quality assurance"
            ],
            "deliverables": ["Implemented solution", "Progress reports", "Quality metrics"]
        })
        
        # Phase 3: Testing and Validation
        phases.append({
            "phase": 3,
            "name": "Testing and Validation",
            "duration": max(1, alternative.implementation_time // 4),
            "activities": [
                "System testing",
                "User acceptance testing",
                "Performance validation",
                "Compliance verification"
            ],
            "deliverables": ["Test results", "Validation report", "Compliance certificate"]
        })
        
        # Phase 4: Deployment and Monitoring
        phases.append({
            "phase": 4,
            "name": "Deployment and Monitoring",
            "duration": max(1, alternative.implementation_time // 4),
            "activities": [
                "Production deployment",
                "User training",
                "Performance monitoring",
                "Issue resolution"
            ],
            "deliverables": ["Deployed solution", "Training materials", "Monitoring dashboard"]
        })
        
        return phases
    
    async def _estimate_resource_requirements(self, alternative: DecisionAlternative, context: DecisionContext) -> Dict[str, Any]:
        """Estimate resource requirements for implementation"""
        # Base resource estimation
        base_resources = {
            "personnel": {
                "project_manager": 1,
                "technical_lead": 1,
                "developers": 2,
                "testers": 1,
                "business_analyst": 1
            },
            "budget": {
                "personnel_costs": alternative.costs.get("personnel", 100000),
                "technology_costs": alternative.costs.get("technology", 50000),
                "training_costs": alternative.costs.get("training", 10000),
                "contingency": alternative.costs.get("contingency", 20000)
            },
            "technology": {
                "hardware": "Standard development environment",
                "software": "Required development tools and licenses",
                "infrastructure": "Cloud or on-premises infrastructure"
            }
        }
        
        # Adjust based on decision type
        if context.decision_type == DecisionType.COMPLIANCE:
            base_resources["personnel"]["compliance_specialist"] = 1
            base_resources["budget"]["compliance_costs"] = 15000
        
        return base_resources
    
    async def _identify_risk_mitigation_measures(self, alternative: DecisionAlternative, context: DecisionContext) -> List[Dict[str, Any]]:
        """Identify risk mitigation measures for the alternative"""
        mitigation_measures = []
        
        # General risk mitigation
        mitigation_measures.append({
            "risk": "Implementation delays",
            "mitigation": "Regular progress monitoring and milestone tracking",
            "owner": "Project Manager",
            "timeline": "Throughout implementation"
        })
        
        mitigation_measures.append({
            "risk": "Budget overrun",
            "mitigation": "Cost monitoring and budget controls",
            "owner": "Financial Controller",
            "timeline": "Throughout implementation"
        })
        
        mitigation_measures.append({
            "risk": "Technical issues",
            "mitigation": "Thorough testing and quality assurance",
            "owner": "Technical Lead",
            "timeline": "During implementation and testing"
        })
        
        # Context-specific mitigation
        if context.decision_type == DecisionType.COMPLIANCE:
            mitigation_measures.append({
                "risk": "Regulatory non-compliance",
                "mitigation": "Regular compliance reviews and expert consultation",
                "owner": "Compliance Officer",
                "timeline": "Throughout implementation"
            })
        
        return mitigation_measures
    
    async def _define_monitoring_requirements(self, recommended_alternative: str, context: DecisionContext) -> List[str]:
        """Define monitoring requirements for the decision"""
        monitoring_requirements = []
        
        # General monitoring requirements
        monitoring_requirements.extend([
            "Track implementation progress against timeline",
            "Monitor budget utilization and cost controls",
            "Assess quality metrics and deliverables",
            "Evaluate stakeholder satisfaction",
            "Review risk indicators and mitigation effectiveness"
        ])
        
        # Context-specific monitoring
        if context.decision_type == DecisionType.RISK_MANAGEMENT:
            monitoring_requirements.extend([
                "Monitor risk reduction metrics",
                "Track risk mitigation effectiveness",
                "Assess residual risk levels"
            ])
        elif context.decision_type == DecisionType.COMPLIANCE:
            monitoring_requirements.extend([
                "Monitor compliance status and metrics",
                "Track regulatory requirement fulfillment",
                "Assess compliance risk levels"
            ])
        
        return monitoring_requirements
    
    async def _assess_decision_risks(self, recommended_alternative: str, context: DecisionContext) -> Dict[str, Any]:
        """Assess risks associated with the decision"""
        if recommended_alternative == "no_alternative":
            return {"status": "no_risk_assessment", "message": "No alternative selected"}
        
        alternative = self.decision_alternatives.get(recommended_alternative)
        if not alternative:
            return {"status": "error", "message": "Alternative not found"}
        
        risk_assessment = {
            "overall_risk_level": "medium",
            "risk_factors": [],
            "mitigation_strategies": [],
            "monitoring_requirements": []
        }
        
        # Assess implementation risks
        if alternative.implementation_time > 90:
            risk_assessment["risk_factors"].append({
                "risk": "Long implementation timeline",
                "impact": "high",
                "probability": "medium",
                "description": "Extended timeline increases risk of scope creep and resource constraints"
            })
        
        # Assess success probability risks
        if alternative.success_probability < 0.7:
            risk_assessment["risk_factors"].append({
                "risk": "Low success probability",
                "impact": "high",
                "probability": "high",
                "description": "Low success probability indicates high risk of failure"
            })
        
        # Assess cost risks
        total_cost = sum(alternative.costs.values())
        if total_cost > 500000:
            risk_assessment["risk_factors"].append({
                "risk": "High implementation cost",
                "impact": "medium",
                "probability": "high",
                "description": "High cost increases financial risk and budget pressure"
            })
        
        # Assess regulatory risks
        if context.decision_type == DecisionType.COMPLIANCE:
            risk_assessment["risk_factors"].append({
                "risk": "Regulatory compliance risk",
                "impact": "high",
                "probability": "medium",
                "description": "Non-compliance could result in regulatory penalties"
            })
        
        return risk_assessment
    
    async def _assess_compliance_impact(self, recommended_alternative: str, context: DecisionContext) -> Dict[str, Any]:
        """Assess compliance impact of the decision"""
        compliance_impact = {
            "regulatory_impact": "neutral",
            "compliance_requirements": [],
            "regulatory_risks": [],
            "compliance_benefits": []
        }
        
        if context.decision_type == DecisionType.COMPLIANCE:
            compliance_impact["regulatory_impact"] = "positive"
            compliance_impact["compliance_benefits"].extend([
                "Improved regulatory compliance",
                "Reduced compliance risk",
                "Enhanced regulatory relationship"
            ])
        elif context.decision_type == DecisionType.RISK_MANAGEMENT:
            compliance_impact["compliance_requirements"].extend([
                "Risk management framework compliance",
                "Regulatory reporting requirements",
                "Internal control effectiveness"
            ])
        
        return compliance_impact
    
    async def get_decision_history(self) -> List[Dict[str, Any]]:
        """Get history of decisions"""
        return [asdict(result) for result in self.decision_history]
    
    async def get_decision_statistics(self) -> Dict[str, Any]:
        """Get statistics about decisions"""
        if not self.decision_history:
            return {"total_decisions": 0}
        
        decision_types = defaultdict(int)
        confidence_scores = []
        
        for result in self.decision_history:
            # Get decision type from context
            context = self.decision_contexts.get(result.decision_id)
            if context:
                decision_types[context.decision_type.value] += 1
            confidence_scores.append(result.confidence_score)
        
        return {
            "total_decisions": len(self.decision_history),
            "decision_type_distribution": dict(decision_types),
            "average_confidence": sum(confidence_scores) / len(confidence_scores),
            "highest_confidence": max(confidence_scores),
            "lowest_confidence": min(confidence_scores)
        }
    
    async def evaluate_decision_outcome(self, decision_id: str, actual_outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the outcome of a decision against predictions"""
        # Find the decision result
        decision_result = next((result for result in self.decision_history if result.decision_id == decision_id), None)
        if not decision_result:
            return {"status": "error", "message": "Decision not found"}
        
        # Compare predicted vs actual outcomes
        evaluation = {
            "decision_id": decision_id,
            "predicted_confidence": decision_result.confidence_score,
            "actual_outcome": actual_outcome,
            "accuracy_assessment": "pending",
            "lessons_learned": [],
            "recommendations": []
        }
        
        # Assess accuracy
        if actual_outcome.get("success", False):
            evaluation["accuracy_assessment"] = "successful"
            evaluation["lessons_learned"].append("Decision criteria were appropriate")
        else:
            evaluation["accuracy_assessment"] = "unsuccessful"
            evaluation["lessons_learned"].append("Decision criteria may need adjustment")
        
        return evaluation
