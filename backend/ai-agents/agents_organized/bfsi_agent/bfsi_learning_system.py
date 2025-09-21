"""
BFSI Learning System for Continuous Reasoning Improvement
Machine learning capabilities for adaptive reasoning and knowledge enhancement
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
import pickle
import hashlib

# Configure logging
logger = logging.getLogger(__name__)

class LearningType(Enum):
    """Types of learning"""
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    TRANSFER = "transfer"
    META = "meta"

class LearningMode(Enum):
    """Learning modes"""
    ONLINE = "online"
    BATCH = "batch"
    INCREMENTAL = "incremental"
    ADAPTIVE = "adaptive"

class PerformanceMetric(Enum):
    """Performance metrics"""
    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"
    CONFIDENCE = "confidence"
    EXPLAINABILITY = "explainability"
    EFFICIENCY = "efficiency"

@dataclass
class LearningExample:
    """Learning example with features and outcomes"""
    example_id: str
    features: Dict[str, Any]
    outcome: Any
    context: Dict[str, Any]
    timestamp: datetime
    quality_score: float
    learning_type: LearningType

@dataclass
class LearningModel:
    """Learning model with performance metrics"""
    model_id: str
    model_type: str
    parameters: Dict[str, Any]
    performance_metrics: Dict[str, float]
    training_data_size: int
    last_updated: datetime
    version: str
    confidence_threshold: float

@dataclass
class LearningInsight:
    """Learning insight from pattern analysis"""
    insight_id: str
    pattern_type: str
    description: str
    confidence: float
    evidence: List[Dict[str, Any]]
    implications: List[str]
    recommendations: List[str]
    learning_value: float

@dataclass
class LearningSession:
    """Learning session with results"""
    session_id: str
    learning_type: LearningType
    mode: LearningMode
    training_data: List[LearningExample]
    model_updates: List[Dict[str, Any]]
    performance_improvements: Dict[str, float]
    insights_generated: List[LearningInsight]
    timestamp: datetime
    duration: float

class BFSILearningSystem:
    """
    BFSI Learning System for continuous reasoning improvement
    """
    
    def __init__(self):
        self.system_id = "bfsi_learning_system"
        self.learning_models: Dict[str, LearningModel] = {}
        self.learning_examples: List[LearningExample] = []
        self.learning_insights: List[LearningInsight] = []
        self.learning_sessions: List[LearningSession] = []
        self.performance_history: List[Dict[str, Any]] = []
        
        # Initialize learning system
        self._initialize_learning_system()
        
        logger.info("BFSI Learning System initialized with continuous improvement capabilities")
    
    def _initialize_learning_system(self):
        """Initialize the learning system"""
        self.learning_capabilities = {
            "pattern_recognition": True,
            "anomaly_detection": True,
            "performance_optimization": True,
            "knowledge_extraction": True,
            "adaptive_reasoning": True,
            "explainable_learning": True
        }
        
        self.learning_algorithms = {
            "classification": ["decision_tree", "random_forest", "neural_network"],
            "regression": ["linear_regression", "polynomial_regression", "svr"],
            "clustering": ["kmeans", "hierarchical", "dbscan"],
            "reinforcement": ["q_learning", "policy_gradient", "actor_critic"]
        }
        
        self.learning_workflows = {
            "reasoning_improvement": {
                "data_sources": ["reasoning_sessions", "decision_outcomes", "user_feedback"],
                "algorithms": ["neural_network", "random_forest"],
                "objectives": ["accuracy", "confidence", "explainability"]
            },
            "risk_prediction": {
                "data_sources": ["risk_assessments", "market_data", "historical_events"],
                "algorithms": ["lstm", "transformer", "ensemble"],
                "objectives": ["precision", "recall", "early_detection"]
            },
            "compliance_optimization": {
                "data_sources": ["compliance_data", "regulatory_changes", "audit_results"],
                "algorithms": ["rule_learning", "decision_tree", "bayesian"],
                "objectives": ["compliance_score", "efficiency", "cost_reduction"]
            }
        }
    
    async def learn_from_reasoning_session(self, session_data: Dict[str, Any]) -> LearningSession:
        """Learn from a reasoning session"""
        logger.info("Learning from reasoning session")
        
        session_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # Extract learning examples from session
        examples = await self._extract_learning_examples(session_data)
        
        # Update learning models
        model_updates = await self._update_learning_models(examples)
        
        # Generate performance improvements
        performance_improvements = await self._calculate_performance_improvements(model_updates)
        
        # Generate insights
        insights = await self._generate_learning_insights(examples, session_data)
        
        # Create learning session
        learning_session = LearningSession(
            session_id=session_id,
            learning_type=LearningType.SUPERVISED,
            mode=LearningMode.ONLINE,
            training_data=examples,
            model_updates=model_updates,
            performance_improvements=performance_improvements,
            insights_generated=insights,
            timestamp=start_time,
            duration=(datetime.now() - start_time).total_seconds()
        )
        
        # Store session
        self.learning_sessions.append(learning_session)
        
        # Update performance history
        await self._update_performance_history(learning_session)
        
        return learning_session
    
    async def _extract_learning_examples(self, session_data: Dict[str, Any]) -> List[LearningExample]:
        """Extract learning examples from session data"""
        examples = []
        
        # Extract reasoning examples
        reasoning_chain = session_data.get("reasoning_chain", [])
        for i, step in enumerate(reasoning_chain):
            if i > 0:
                example = LearningExample(
                    example_id=str(uuid.uuid4()),
                    features={
                        "previous_step": reasoning_chain[i-1],
                        "current_step": step,
                        "context": session_data.get("context", {}),
                        "mode": session_data.get("mode", "analytical")
                    },
                    outcome=step.get("outputs", {}),
                    context=session_data.get("context", {}),
                    timestamp=datetime.now(),
                    quality_score=step.get("confidence", 0.5),
                    learning_type=LearningType.SUPERVISED
                )
                examples.append(example)
        
        # Extract decision examples
        if "decision_result" in session_data:
            decision_example = LearningExample(
                example_id=str(uuid.uuid4()),
                features={
                    "decision_context": session_data.get("decision_context", {}),
                    "alternatives": session_data.get("alternatives", []),
                    "constraints": session_data.get("constraints", [])
                },
                outcome=session_data["decision_result"],
                context=session_data.get("context", {}),
                timestamp=datetime.now(),
                quality_score=session_data.get("confidence", 0.5),
                learning_type=LearningType.SUPERVISED
            )
            examples.append(decision_example)
        
        return examples
    
    async def _update_learning_models(self, examples: List[LearningExample]) -> List[Dict[str, Any]]:
        """Update learning models with new examples"""
        model_updates = []
        
        # Group examples by type
        example_groups = defaultdict(list)
        for example in examples:
            example_groups[example.learning_type.value].append(example)
        
        # Update models for each type
        for learning_type, type_examples in example_groups.items():
            if learning_type == "supervised":
                update = await self._update_supervised_models(type_examples)
                model_updates.append(update)
            elif learning_type == "unsupervised":
                update = await self._update_unsupervised_models(type_examples)
                model_updates.append(update)
            elif learning_type == "reinforcement":
                update = await self._update_reinforcement_models(type_examples)
                model_updates.append(update)
        
        return model_updates
    
    async def _update_supervised_models(self, examples: List[LearningExample]) -> Dict[str, Any]:
        """Update supervised learning models"""
        if not examples:
            return {"status": "no_examples", "improvements": {}}
        
        # Extract features and labels
        features = []
        labels = []
        
        for example in examples:
            features.append(self._extract_features(example.features))
            labels.append(example.outcome)
        
        # Update models
        improvements = {}
        
        # Update reasoning model
        reasoning_improvement = await self._update_reasoning_model(features, labels)
        improvements["reasoning_model"] = reasoning_improvement
        
        # Update decision model
        decision_improvement = await self._update_decision_model(features, labels)
        improvements["decision_model"] = decision_improvement
        
        # Update risk model
        risk_improvement = await self._update_risk_model(features, labels)
        improvements["risk_model"] = risk_improvement
        
        return {
            "status": "updated",
            "improvements": improvements,
            "examples_processed": len(examples)
        }
    
    async def _update_unsupervised_models(self, examples: List[LearningExample]) -> Dict[str, Any]:
        """Update unsupervised learning models"""
        if not examples:
            return {"status": "no_examples", "improvements": {}}
        
        # Extract features
        features = [self._extract_features(example.features) for example in examples]
        
        # Update clustering models
        clustering_improvement = await self._update_clustering_models(features)
        
        # Update anomaly detection
        anomaly_improvement = await self._update_anomaly_detection(features)
        
        return {
            "status": "updated",
            "improvements": {
                "clustering": clustering_improvement,
                "anomaly_detection": anomaly_improvement
            },
            "examples_processed": len(examples)
        }
    
    async def _update_reinforcement_models(self, examples: List[LearningExample]) -> Dict[str, Any]:
        """Update reinforcement learning models"""
        if not examples:
            return {"status": "no_examples", "improvements": {}}
        
        # Extract state-action-reward tuples
        state_action_rewards = []
        for example in examples:
            if "state" in example.features and "action" in example.features:
                state_action_rewards.append({
                    "state": example.features["state"],
                    "action": example.features["action"],
                    "reward": example.outcome.get("reward", 0.0)
                })
        
        # Update Q-learning model
        q_learning_improvement = await self._update_q_learning_model(state_action_rewards)
        
        return {
            "status": "updated",
            "improvements": {
                "q_learning": q_learning_improvement
            },
            "examples_processed": len(examples)
        }
    
    def _extract_features(self, features_dict: Dict[str, Any]) -> List[float]:
        """Extract numerical features from feature dictionary"""
        features = []
        
        for key, value in features_dict.items():
            if isinstance(value, (int, float)):
                features.append(float(value))
            elif isinstance(value, bool):
                features.append(1.0 if value else 0.0)
            elif isinstance(value, str):
                # Deterministic string encoding using SHA-256 hash
                hash_obj = hashlib.sha256(value.encode('utf-8'))
                hash_int = int(hash_obj.hexdigest(), 16)
                features.append(hash_int / (2**256))
            elif isinstance(value, list):
                # Convert list to fixed-length features using statistical summaries
                numeric_values = [float(x) if isinstance(x, (int, float)) else 0.0 for x in value]
                if numeric_values:
                    features.extend([
                        float(np.mean(numeric_values)),  # Mean
                        float(np.max(numeric_values)),  # Max
                        float(np.min(numeric_values)),  # Min
                        float(np.std(numeric_values)) if len(numeric_values) > 1 else 0.0,  # Standard deviation
                        float(len(numeric_values))  # Length
                    ])
                else:
                    # Empty list - add zeros for consistency
                    features.extend([0.0, 0.0, 0.0, 0.0, 0.0])
        
        return features
    
    async def _update_reasoning_model(self, features: List[List[float]], labels: List[Any]) -> Dict[str, Any]:
        """Update reasoning model"""
        # Simulate model update
        model_id = "reasoning_model"
        
        if model_id not in self.learning_models:
            self.learning_models[model_id] = LearningModel(
                model_id=model_id,
                model_type="neural_network",
                parameters={"layers": 3, "neurons": 128},
                performance_metrics={"accuracy": 0.8, "confidence": 0.7},
                training_data_size=0,
                last_updated=datetime.now(),
                version="1.0",
                confidence_threshold=0.7
            )
        
        # Update model
        model = self.learning_models[model_id]
        model.training_data_size += len(features)
        model.last_updated = datetime.now()
        
        # Simulate performance improvement
        accuracy_improvement = min(0.1, len(features) * 0.001)
        model.performance_metrics["accuracy"] = min(0.95, model.performance_metrics["accuracy"] + accuracy_improvement)
        
        return {
            "model_id": model_id,
            "accuracy_improvement": accuracy_improvement,
            "new_accuracy": model.performance_metrics["accuracy"],
            "training_samples": len(features)
        }
    
    async def _update_decision_model(self, features: List[List[float]], labels: List[Any]) -> Dict[str, Any]:
        """Update decision model"""
        model_id = "decision_model"
        
        if model_id not in self.learning_models:
            self.learning_models[model_id] = LearningModel(
                model_id=model_id,
                model_type="random_forest",
                parameters={"trees": 100, "depth": 10},
                performance_metrics={"accuracy": 0.75, "precision": 0.8},
                training_data_size=0,
                last_updated=datetime.now(),
                version="1.0",
                confidence_threshold=0.7
            )
        
        # Update model
        model = self.learning_models[model_id]
        model.training_data_size += len(features)
        model.last_updated = datetime.now()
        
        # Simulate performance improvement
        accuracy_improvement = min(0.05, len(features) * 0.0005)
        model.performance_metrics["accuracy"] = min(0.9, model.performance_metrics["accuracy"] + accuracy_improvement)
        
        return {
            "model_id": model_id,
            "accuracy_improvement": accuracy_improvement,
            "new_accuracy": model.performance_metrics["accuracy"],
            "training_samples": len(features)
        }
    
    async def _update_risk_model(self, features: List[List[float]], labels: List[Any]) -> Dict[str, Any]:
        """Update risk model"""
        model_id = "risk_model"
        
        if model_id not in self.learning_models:
            self.learning_models[model_id] = LearningModel(
                model_id=model_id,
                model_type="lstm",
                parameters={"layers": 2, "units": 64},
                performance_metrics={"accuracy": 0.85, "precision": 0.8},
                training_data_size=0,
                last_updated=datetime.now(),
                version="1.0",
                confidence_threshold=0.8
            )
        
        # Update model
        model = self.learning_models[model_id]
        model.training_data_size += len(features)
        model.last_updated = datetime.now()
        
        # Simulate performance improvement
        accuracy_improvement = min(0.03, len(features) * 0.0003)
        model.performance_metrics["accuracy"] = min(0.95, model.performance_metrics["accuracy"] + accuracy_improvement)
        
        return {
            "model_id": model_id,
            "accuracy_improvement": accuracy_improvement,
            "new_accuracy": model.performance_metrics["accuracy"],
            "training_samples": len(features)
        }
    
    async def _update_clustering_models(self, features: List[List[float]]) -> Dict[str, Any]:
        """Update clustering models"""
        # Simulate clustering improvement
        return {
            "clusters_identified": min(10, len(features) // 10),
            "silhouette_score": 0.7,
            "improvement": 0.02
        }
    
    async def _update_anomaly_detection(self, features: List[List[float]]) -> Dict[str, Any]:
        """Update anomaly detection"""
        # Simulate anomaly detection improvement
        return {
            "anomalies_detected": len(features) // 20,
            "detection_rate": 0.9,
            "false_positive_rate": 0.1,
            "improvement": 0.01
        }
    
    async def _update_q_learning_model(self, state_action_rewards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update Q-learning model"""
        # Simulate Q-learning improvement
        return {
            "q_values_updated": len(state_action_rewards),
            "convergence_rate": 0.8,
            "improvement": 0.05
        }
    
    async def _calculate_performance_improvements(self, model_updates: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate overall performance improvements"""
        improvements = {}
        
        for update in model_updates:
            if "improvements" in update:
                for model_id, improvement in update["improvements"].items():
                    if "accuracy_improvement" in improvement:
                        improvements[f"{model_id}_accuracy"] = improvement["accuracy_improvement"]
                    elif "improvement" in improvement:
                        improvements[f"{model_id}_general"] = improvement["improvement"]
        
        return improvements
    
    async def _generate_learning_insights(self, examples: List[LearningExample], session_data: Dict[str, Any]) -> List[LearningInsight]:
        """Generate learning insights from examples"""
        insights = []
        
        # Pattern recognition insights
        if len(examples) > 5:
            pattern_insight = LearningInsight(
                insight_id=str(uuid.uuid4()),
                pattern_type="reasoning_pattern",
                description="Identified recurring reasoning pattern in decision making",
                confidence=0.8,
                evidence=[{"type": "pattern", "frequency": len(examples)}],
                implications=["Improved reasoning efficiency", "Enhanced decision quality"],
                recommendations=["Apply pattern to similar contexts", "Document reasoning approach"],
                learning_value=0.7
            )
            insights.append(pattern_insight)
        
        # Performance insights
        if session_data.get("confidence_score", 0) > 0.8:
            performance_insight = LearningInsight(
                insight_id=str(uuid.uuid4()),
                pattern_type="performance_pattern",
                description="High confidence reasoning session identified",
                confidence=0.9,
                evidence=[{"type": "performance", "score": session_data.get("confidence_score", 0)}],
                implications=["Successful reasoning approach", "Replicable methodology"],
                recommendations=["Document successful approach", "Apply to similar scenarios"],
                learning_value=0.8
            )
            insights.append(performance_insight)
        
        # Store insights
        self.learning_insights.extend(insights)
        
        return insights
    
    async def _update_performance_history(self, learning_session: LearningSession):
        """Update performance history"""
        performance_record = {
            "session_id": learning_session.session_id,
            "timestamp": learning_session.timestamp,
            "learning_type": learning_session.learning_type.value,
            "examples_processed": len(learning_session.training_data),
            "performance_improvements": learning_session.performance_improvements,
            "insights_generated": len(learning_session.insights_generated),
            "duration": learning_session.duration
        }
        
        self.performance_history.append(performance_record)
        
        # Keep only last 1000 records
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
    
    async def predict_reasoning_outcome(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict reasoning outcome using learned models"""
        # Extract features from context
        features = self._extract_features(context)
        
        # Use reasoning model for prediction
        reasoning_model = self.learning_models.get("reasoning_model")
        if reasoning_model:
            # Simulate prediction
            prediction = {
                "outcome": "successful_reasoning",
                "confidence": 0.8,
                "reasoning": "Based on learned patterns",
                "recommendations": ["Apply standard reasoning approach", "Monitor for anomalies"]
            }
        else:
            prediction = {
                "outcome": "unknown",
                "confidence": 0.5,
                "reasoning": "Insufficient training data",
                "recommendations": ["Gather more training data", "Improve model training"]
            }
        
        return prediction
    
    async def optimize_reasoning_process(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize reasoning process using learned insights"""
        optimizations = []
        
        # Analyze performance patterns
        if self.performance_history:
            recent_performance = self.performance_history[-10:]
            avg_improvement = sum(p.get("performance_improvements", {}).get("reasoning_model_accuracy", 0) 
                                for p in recent_performance) / len(recent_performance)
            
            if avg_improvement > 0.05:
                optimizations.append("Increase reasoning model confidence threshold")
                optimizations.append("Apply ensemble reasoning approaches")
        
        # Analyze learning insights
        recent_insights = [insight for insight in self.learning_insights 
                          if insight.learning_value > 0.7]
        
        if recent_insights:
            optimizations.append("Apply high-value learning insights")
            optimizations.append("Implement pattern-based reasoning")
        
        return {
            "optimizations": optimizations,
            "confidence": 0.8,
            "expected_improvement": 0.1
        }
    
    async def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        stats = {
            "total_learning_sessions": len(self.learning_sessions),
            "total_learning_examples": len(self.learning_examples),
            "total_insights": len(self.learning_insights),
            "active_models": len(self.learning_models),
            "average_performance_improvement": 0.0,
            "learning_effectiveness": 0.0
        }
        
        if self.learning_sessions:
            # Calculate average performance improvement
            total_improvements = []
            for session in self.learning_sessions:
                for improvement in session.performance_improvements.values():
                    total_improvements.append(improvement)
            
            if total_improvements:
                stats["average_performance_improvement"] = sum(total_improvements) / len(total_improvements)
        
        # Calculate learning effectiveness
        if self.learning_insights:
            high_value_insights = [insight for insight in self.learning_insights if insight.learning_value > 0.7]
            stats["learning_effectiveness"] = len(high_value_insights) / len(self.learning_insights)
        
        return stats
    
    def _serialize_dataclass(self, obj) -> Dict[str, Any]:
        """Custom serialization function that converts datetime objects to ISO format strings"""
        if hasattr(obj, '__dataclass_fields__'):
            # It's a dataclass, serialize its fields
            result = {}
            for field_name, field_value in obj.__dict__.items():
                if isinstance(field_value, datetime):
                    result[field_name] = field_value.isoformat()
                elif isinstance(field_value, list):
                    # Handle lists that might contain dataclasses or datetime objects
                    result[field_name] = [self._serialize_dataclass(item) if hasattr(item, '__dataclass_fields__') 
                                        else item.isoformat() if isinstance(item, datetime) 
                                        else item for item in field_value]
                elif isinstance(field_value, dict):
                    # Handle dictionaries that might contain datetime objects
                    result[field_name] = {k: (v.isoformat() if isinstance(v, datetime) else v) 
                                        for k, v in field_value.items()}
                else:
                    result[field_name] = field_value
            return result
        else:
            # Not a dataclass, return as is
            return obj

    async def export_learning_report(self) -> Dict[str, Any]:
        """Export comprehensive learning report"""
        report = {
            "learning_system_id": self.system_id,
            "capabilities": self.learning_capabilities,
            "statistics": await self.get_learning_statistics(),
            "models": {model_id: self._serialize_dataclass(model) for model_id, model in self.learning_models.items()},
            "recent_insights": [self._serialize_dataclass(insight) for insight in self.learning_insights[-10:]],
            "performance_trends": self.performance_history[-20:],
            "recommendations": await self._generate_learning_recommendations(),
            "timestamp": datetime.now().isoformat()
        }
        
        return report
    
    async def _generate_learning_recommendations(self) -> List[str]:
        """Generate learning recommendations"""
        recommendations = []
        
        # Model performance recommendations
        for model_id, model in self.learning_models.items():
            if model.performance_metrics.get("accuracy", 0) < 0.8:
                recommendations.append(f"Improve {model_id} model performance")
                recommendations.append(f"Increase training data for {model_id}")
        
        # Learning effectiveness recommendations
        if len(self.learning_insights) < 10:
            recommendations.append("Generate more learning insights")
            recommendations.append("Increase learning session frequency")
        
        # Performance improvement recommendations
        if self.performance_history:
            recent_improvements = [p.get("performance_improvements", {}) for p in self.performance_history[-5:]]
            if not any(improvements for improvements in recent_improvements):
                recommendations.append("Focus on performance improvement")
                recommendations.append("Analyze learning bottlenecks")
        
        return recommendations
