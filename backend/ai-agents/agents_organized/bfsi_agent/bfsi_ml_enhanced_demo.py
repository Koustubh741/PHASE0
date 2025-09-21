"""
BFSI ML Enhanced Demo
Demonstrates the advanced ML and AI capabilities for continuous reasoning improvement
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import enhanced BFSI agent with ML capabilities
from bfsi_enhanced_agent import BFSIEnhancedAgent, EnhancedCapability
from bfsi_advanced_ml_system import BFSIAdvancedMLSystem, MLAlgorithm, ModelArchitecture
from bfsi_ml_integration import BFSIMLIntegration, MLIntegrationMode

class BFSIMLEnhancedDemo:
    """
    Demo class showcasing ML-enhanced BFSI agent capabilities
    """
    
    def __init__(self):
        self.agent = BFSIEnhancedAgent()
        self.demo_scenarios = self._create_demo_scenarios()
        
        logger.info("BFSI ML Enhanced Demo initialized")
    
    def _create_demo_scenarios(self) -> List[Dict[str, Any]]:
        """Create demo scenarios for ML capabilities"""
        return [
            {
                "name": "Credit Risk Assessment with ML",
                "operation_type": "risk_assessment",
                "context": {
                    "customer_profile": {
                        "credit_score": 750,
                        "annual_income": 120000,
                        "debt_to_income": 0.35,
                        "employment_history": 5,
                        "loan_amount": 50000
                    },
                    "risk_factors": ["economic_volatility", "industry_risk", "credit_history"],
                    "ml_enhanced": True
                },
                "description": "Demonstrates ML-enhanced credit risk assessment"
            },
            {
                "name": "Fraud Detection with Neural Networks",
                "operation_type": "fraud_detection",
                "context": {
                    "transaction_data": {
                        "amount": 15000,
                        "merchant_category": "electronics",
                        "location": "online",
                        "time_of_day": "02:30",
                        "frequency": "unusual"
                    },
                    "customer_behavior": {
                        "typical_amount": 500,
                        "typical_merchant": "retail",
                        "transaction_pattern": "normal"
                    },
                    "ml_models": ["neural_network", "lstm", "anomaly_detection"]
                },
                "description": "Shows neural network-based fraud detection"
            },
            {
                "name": "Regulatory Compliance with ML",
                "operation_type": "compliance_management",
                "context": {
                    "regulation": "Basel III",
                    "banking_activities": {
                        "trading_volume": 1000000,
                        "capital_ratio": 0.12,
                        "risk_weighted_assets": 8000000
                    },
                    "compliance_requirements": ["capital_adequacy", "liquidity_coverage", "leverage_ratio"],
                    "ml_analysis": True
                },
                "description": "Demonstrates ML-enhanced regulatory compliance"
            },
            {
                "name": "Investment Decision with Deep Learning",
                "operation_type": "investment_analysis",
                "context": {
                    "portfolio_data": {
                        "total_value": 5000000,
                        "risk_tolerance": "moderate",
                        "investment_horizon": 10
                    },
                    "market_data": {
                        "volatility": 0.18,
                        "interest_rates": 0.025,
                        "economic_indicators": ["gdp_growth", "inflation", "unemployment"]
                    },
                    "ml_models": ["lstm_prediction", "risk_neural_network", "portfolio_optimizer"]
                },
                "description": "Shows deep learning for investment decisions"
            },
            {
                "name": "Continuous Learning and Improvement",
                "operation_type": "continuous_improvement",
                "context": {
                    "learning_data": {
                        "historical_operations": 1000,
                        "success_rate": 0.85,
                        "performance_metrics": {
                            "accuracy": 0.92,
                            "confidence": 0.88,
                            "explainability": 0.90
                        }
                    },
                    "improvement_targets": {
                        "accuracy": 0.95,
                        "confidence": 0.92,
                        "efficiency": 0.90
                    },
                    "ml_optimization": True
                },
                "description": "Demonstrates continuous learning and ML optimization"
            }
        ]
    
    async def run_comprehensive_demo(self):
        """Run comprehensive demo of ML-enhanced capabilities"""
        logger.info("Starting BFSI ML Enhanced Demo")
        
        print("=" * 80)
        print("🚀 BFSI AGENT - MACHINE LEARNING ENHANCED CAPABILITIES DEMO")
        print("=" * 80)
        
        # Display enhanced capabilities
        await self._display_enhanced_capabilities()
        
        # Run ML training demo
        await self._run_ml_training_demo()
        
        # Run scenario demonstrations
        await self._run_scenario_demos()
        
        # Run continuous improvement demo
        await self._run_continuous_improvement_demo()
        
        # Display comprehensive analytics
        await self._display_comprehensive_analytics()
        
        # Display ML recommendations
        await self._display_ml_recommendations()
        
        print("\n" + "=" * 80)
        print("✅ BFSI ML Enhanced Demo completed successfully!")
        print("=" * 80)
    
    async def _display_enhanced_capabilities(self):
        """Display enhanced capabilities including ML features"""
        print("\n📊 ENHANCED CAPABILITIES:")
        print("-" * 50)
        
        for capability in self.agent.enhanced_capabilities:
            capability_name = capability.value.replace("_", " ").title()
            print(f"✅ {capability_name}")
        
        print(f"\n🔧 ML Integration Mode: {self.agent.ml_integration.integration_mode.value}")
        print(f"🧠 Neural Networks: {'Available' if self.agent.advanced_ml_system.pytorch_available else 'Fallback to sklearn'}")
        print(f"📈 Deep Learning: {'Enabled' if self.agent.advanced_ml_system.pytorch_available else 'Limited'}")
    
    async def _run_ml_training_demo(self):
        """Demonstrate ML model training"""
        print("\n🤖 MACHINE LEARNING TRAINING DEMO:")
        print("-" * 50)
        
        # Create sample training data
        training_data = [
            {
                "features": {
                    "credit_score": 750,
                    "income": 120000,
                    "debt_ratio": 0.35,
                    "employment_years": 5
                },
                "outcome": {"success": True, "confidence": 0.9}
            },
            {
                "features": {
                    "credit_score": 650,
                    "income": 80000,
                    "debt_ratio": 0.45,
                    "employment_years": 3
                },
                "outcome": {"success": False, "confidence": 0.7}
            },
            {
                "features": {
                    "credit_score": 800,
                    "income": 150000,
                    "debt_ratio": 0.25,
                    "employment_years": 8
                },
                "outcome": {"success": True, "confidence": 0.95}
            }
        ]
        
        print("📚 Training ML models with sample data...")
        
        # Train ML models
        training_results = await self.agent.train_ml_models(training_data)
        
        print("🎯 Training Results:")
        for model_type, result in training_results.items():
            if "error" not in result:
                print(f"  ✅ {model_type}: Model ID {result['model_id']}, Accuracy: {result.get('accuracy', 'N/A')}")
            else:
                print(f"  ❌ {model_type}: {result['error']}")
    
    async def _run_scenario_demos(self):
        """Run scenario demonstrations"""
        print("\n🎭 SCENARIO DEMONSTRATIONS:")
        print("-" * 50)
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n📋 Scenario {i}: {scenario['name']}")
            print(f"   {scenario['description']}")
            
            # Perform enhanced operation
            operation = await self.agent.perform_enhanced_operation(
                scenario["operation_type"],
                scenario["context"]
            )
            
            # Display results
            print(f"   🔍 Operation ID: {operation.operation_id}")
            print(f"   ⚡ Duration: {operation.duration:.2f} seconds")
            print(f"   📊 Overall Confidence: {operation.overall_confidence:.2f}")
            print(f"   🧠 Explainability Score: {operation.explainability_score:.2f}")
            
            # Display ML prediction results
            if operation.ml_prediction:
                print(f"   🤖 ML Prediction: {operation.ml_prediction.prediction}")
                print(f"   📈 ML Confidence: {operation.ml_prediction.confidence:.2f}")
                print(f"   💡 ML Recommendation: {operation.ml_prediction.recommendation}")
            
            # Display continuous improvement results
            if operation.continuous_improvement:
                print(f"   📈 Performance Gains: {operation.continuous_improvement.performance_gains}")
                print(f"   🎯 Recommendations: {len(operation.continuous_improvement.recommendations)} generated")
            
            # Display key recommendations
            if operation.recommendations:
                print(f"   💡 Key Recommendations:")
                for rec in operation.recommendations[:3]:  # Show first 3
                    print(f"      • {rec}")
    
    async def _run_continuous_improvement_demo(self):
        """Demonstrate continuous improvement capabilities"""
        print("\n🔄 CONTINUOUS IMPROVEMENT DEMO:")
        print("-" * 50)
        
        # Perform continuous improvement session
        improvement_data = {
            "reasoning_session": {
                "session_id": "demo_session",
                "mode": "analytical",
                "confidence_score": 0.85
            },
            "operation_type": "continuous_improvement",
            "context": {
                "learning_effectiveness": 0.82,
                "ml_confidence": 0.88,
                "overall_performance": 0.85
            }
        }
        
        print("🚀 Performing continuous improvement session...")
        
        improvement_session = await self.agent.ml_integration.perform_continuous_improvement(improvement_data)
        
        print(f"📊 Improvement Session ID: {improvement_session.session_id}")
        print(f"⏱️  Duration: {improvement_session.duration:.2f} seconds")
        print(f"📈 Performance Gains:")
        
        for metric, gain in improvement_session.performance_gains.items():
            print(f"   • {metric}: {gain:+.3f}")
        
        print(f"🎯 Improvement Targets:")
        for target, value in improvement_session.improvement_targets.items():
            print(f"   • {target}: {value:.2f}")
        
        print(f"💡 Recommendations ({len(improvement_session.recommendations)}):")
        for rec in improvement_session.recommendations[:5]:  # Show first 5
            print(f"   • {rec}")
    
    async def _display_comprehensive_analytics(self):
        """Display comprehensive ML analytics"""
        print("\n📊 COMPREHENSIVE ML ANALYTICS:")
        print("-" * 50)
        
        # Get ML analytics
        analytics = await self.agent.get_ml_analytics()
        
        # ML Integration Statistics
        integration_stats = analytics["ml_integration_stats"]
        print(f"🔗 ML Integration Mode: {integration_stats['integration_mode']}")
        print(f"📈 Total Integrated Results: {integration_stats['total_integrated_results']}")
        print(f"🔄 Total Improvement Sessions: {integration_stats['total_improvement_sessions']}")
        
        if "average_integrated_confidence" in integration_stats:
            print(f"📊 Average Integrated Confidence: {integration_stats['average_integrated_confidence']:.3f}")
        
        # Advanced ML Statistics
        ml_stats = analytics["advanced_ml_stats"]
        print(f"\n🤖 Advanced ML Statistics:")
        print(f"   • Total Models: {ml_stats['total_models']}")
        print(f"   • Average Confidence: {ml_stats['average_confidence']:.3f}")
        print(f"   • PyTorch Available: {ml_stats['pytorch_available']}")
        print(f"   • Training Data Size: {ml_stats['training_data_size']}")
        
        # Model Performance
        model_performance = analytics["model_performance"]
        if model_performance:
            print(f"\n🎯 Model Performance:")
            for model_id, performance in model_performance.items():
                print(f"   • {model_id}:")
                print(f"     - Algorithm: {performance['algorithm']}")
                print(f"     - Architecture: {performance['architecture']}")
                print(f"     - Training Data Size: {performance['training_data_size']}")
                if performance['performance_metrics']:
                    for metric, value in performance['performance_metrics'].items():
                        print(f"     - {metric}: {value:.3f}")
        
        # Learning System Statistics
        learning_stats = analytics["learning_system_stats"]
        print(f"\n📚 Learning System Statistics:")
        print(f"   • Learning Effectiveness: {learning_stats.get('learning_effectiveness', 0):.3f}")
        print(f"   • Total Learning Sessions: {learning_stats.get('total_learning_sessions', 0)}")
        print(f"   • Average Performance Improvement: {learning_stats.get('average_performance_improvement', 0):.3f}")
    
    async def _display_ml_recommendations(self):
        """Display ML-specific recommendations"""
        print("\n💡 ML ENHANCEMENT RECOMMENDATIONS:")
        print("-" * 50)
        
        # Get integration report
        integration_report = await self.agent.ml_integration.export_integration_report()
        
        recommendations = integration_report.get("recommendations", [])
        
        if recommendations:
            print("🎯 System Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("✅ No specific recommendations at this time")
        
        # Get ML system recommendations
        try:
            ml_report = await self.agent.advanced_ml_system.export_ml_report()
            ml_recommendations = ml_report.get("recommendations", [])
            
            if ml_recommendations:
                print(f"\n🤖 ML System Recommendations:")
                for i, rec in enumerate(ml_recommendations, 1):
                    print(f"   {i}. {rec}")
        except Exception as e:
            logger.error(f"Error getting ML recommendations: {e}")
        
        # Performance optimization recommendations
        print(f"\n🚀 Performance Optimization:")
        print("   • Continue regular continuous improvement sessions")
        print("   • Monitor ML model performance and retrain as needed")
        print("   • Expand training data for better model accuracy")
        print("   • Consider ensemble methods for improved predictions")
        print("   • Implement automated hyperparameter optimization")
    
    async def run_ml_optimization_demo(self):
        """Demonstrate ML system optimization"""
        print("\n⚙️ ML SYSTEM OPTIMIZATION DEMO:")
        print("-" * 50)
        
        print("🔧 Optimizing ML system...")
        
        optimization_results = await self.agent.optimize_ml_system()
        
        if optimization_results.get("status") == "completed":
            print("✅ ML System Optimization Completed")
            
            # Display integration optimization results
            integration_opt = optimization_results.get("integration_optimization", {})
            if integration_opt:
                print(f"📊 Integration Optimization:")
                print(f"   • Overall Improvement: {integration_opt.get('overall_improvement', 0):.3f}")
                
                ml_optimizations = integration_opt.get("ml_optimizations", {})
                if ml_optimizations:
                    print(f"   • ML Models Optimized: {len(ml_optimizations)}")
                    for model_id, opt_result in ml_optimizations.items():
                        print(f"     - {model_id}: {opt_result.get('best_score', 0):.3f}")
            
            # Display model optimizations
            model_optimizations = optimization_results.get("model_optimizations", {})
            if model_optimizations:
                print(f"🎯 Model Optimizations:")
                for model_id, opt_result in model_optimizations.items():
                    best_params = opt_result.get("best_params", {})
                    best_score = opt_result.get("best_score", 0)
                    print(f"   • {model_id}: Score {best_score:.3f}")
                    if best_params:
                        print(f"     Best Parameters: {best_params}")
        else:
            print(f"❌ Optimization Failed: {optimization_results.get('error', 'Unknown error')}")

async def main():
    """Main demo function"""
    demo = BFSIMLEnhancedDemo()
    
    print("🚀 Starting BFSI ML Enhanced Demo...")
    
    try:
        # Run comprehensive demo
        await demo.run_comprehensive_demo()
        
        # Run ML optimization demo
        await demo.run_ml_optimization_demo()
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
