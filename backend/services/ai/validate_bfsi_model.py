#!/usr/bin/env python3
"""
BFSI Model Validation Script
Validates the quality and accuracy of the retrained BFSI model
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BFSIModelValidator:
    """Validates BFSI model quality and accuracy"""
    
    def __init__(self):
        self.models_dir = Path("trained_models")
        
        # Quality criteria
        self.quality_criteria = {
            "completeness": {
                "min_length": 100,
                "required_elements": ["specific requirements", "implementation details", "regulatory context"]
            },
            "specificity": {
                "avoid_generic": ["compliance program", "regulatory requirements", "policy framework"],
                "require_specific": ["specific percentages", "timeframes", "regulatory names", "technical details"]
            },
            "accuracy": {
                "regulatory_frameworks": ["SOX", "Basel III", "PCI DSS", "GDPR", "IFRS", "FATCA"],
                "key_concepts": ["capital ratios", "internal controls", "data protection", "risk management"]
            },
            "diversity": {
                "avoid_repetition": True,
                "require_variation": True
            }
        }
    
    def validate_model(self, model_name: str = "bfsi-transformers-model") -> Dict[str, Any]:
        """Validate a specific BFSI model"""
        logger.info(f"Validating model: {model_name}")
        
        # Load model info
        model_path = self.models_dir / f"{model_name}_info.json"
        if not model_path.exists():
            return {"error": f"Model file not found: {model_path}"}
        
        with open(model_path, 'r') as f:
            model_info = json.load(f)
        
        # Extract test output
        test_output = model_info.get('test_output', '')
        
        # Validate quality
        validation_results = {
            "model_name": model_name,
            "overall_score": 0.0,
            "quality_metrics": {},
            "issues": [],
            "recommendations": []
        }
        
        # Test completeness
        completeness_score = self._test_completeness(test_output)
        validation_results["quality_metrics"]["completeness"] = completeness_score
        
        # Test specificity
        specificity_score = self._test_specificity(test_output)
        validation_results["quality_metrics"]["specificity"] = specificity_score
        
        # Test accuracy
        accuracy_score = self._test_accuracy(test_output)
        validation_results["quality_metrics"]["accuracy"] = accuracy_score
        
        # Test diversity
        diversity_score = self._test_diversity(test_output)
        validation_results["quality_metrics"]["diversity"] = diversity_score
        
        # Calculate overall score
        validation_results["overall_score"] = (
            completeness_score + specificity_score + accuracy_score + diversity_score
        ) / 4
        
        # Generate recommendations
        validation_results["recommendations"] = self._generate_recommendations(validation_results)
        
        return validation_results
    
    def _test_completeness(self, text: str) -> float:
        """Test if responses are complete and detailed"""
        score = 0.0
        
        # Check minimum length
        if len(text) > 500:
            score += 0.3
        
        # Check for specific elements
        required_elements = self.quality_criteria["completeness"]["required_elements"]
        for element in required_elements:
            if element.lower() in text.lower():
                score += 0.2
        
        # Check for structured responses (numbered lists, bullet points)
        if re.search(r'\d+\)', text) or re.search(r'•', text):
            score += 0.2
        
        # Check for multiple questions answered
        if text.count('Q:') > 1:
            score += 0.1
        
        return min(score, 1.0)
    
    def _test_specificity(self, text: str) -> float:
        """Test if responses are specific rather than generic"""
        score = 0.0
        
        # Check for specific regulatory frameworks
        frameworks = self.quality_criteria["accuracy"]["regulatory_frameworks"]
        framework_count = sum(1 for framework in frameworks if framework in text)
        score += min(framework_count * 0.15, 0.6)
        
        # Check for specific numbers/percentages
        if re.search(r'\d+%', text) or re.search(r'\d+\.\d+', text):
            score += 0.2
        
        # Check for specific timeframes
        if re.search(r'\d+\s*(days?|months?|years?)', text):
            score += 0.1
        
        # Check for technical details
        technical_terms = ["capital ratios", "liquidity coverage", "internal controls", "data encryption"]
        technical_count = sum(1 for term in technical_terms if term.lower() in text.lower())
        score += min(technical_count * 0.05, 0.1)
        
        return min(score, 1.0)
    
    def _test_accuracy(self, text: str) -> float:
        """Test if responses contain accurate regulatory information"""
        score = 0.0
        
        # Check for accurate regulatory framework names
        accurate_frameworks = ["SOX", "Basel III", "PCI DSS", "GDPR"]
        for framework in accurate_frameworks:
            if framework in text:
                score += 0.2
        
        # Check for accurate key concepts
        key_concepts = ["capital adequacy", "internal controls", "data protection", "risk management"]
        concept_count = sum(1 for concept in key_concepts if concept.lower() in text.lower())
        score += min(concept_count * 0.1, 0.2)
        
        return min(score, 1.0)
    
    def _test_diversity(self, text: str) -> float:
        """Test if responses show diversity and avoid repetition"""
        score = 0.0
        
        # Check for repetition of phrases
        words = text.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 5:  # Only check longer words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Calculate repetition score
        total_words = len([w for w in words if len(w) > 5])
        repeated_words = sum(1 for count in word_freq.values() if count > 1)
        
        if total_words > 0:
            repetition_ratio = repeated_words / total_words
            score += (1 - repetition_ratio) * 0.5
        
        # Check for varied sentence structures
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) > 5:
            score += 0.3
        
        # Check for different question types
        question_patterns = [r'What is', r'How does', r'What are', r'How should']
        pattern_count = sum(1 for pattern in question_patterns if re.search(pattern, text))
        score += min(pattern_count * 0.05, 0.2)
        
        return min(score, 1.0)
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        metrics = results["quality_metrics"]
        
        if metrics["completeness"] < 0.7:
            recommendations.append("Increase response length and detail with more specific examples")
        
        if metrics["specificity"] < 0.7:
            recommendations.append("Add more specific regulatory details, percentages, and timeframes")
        
        if metrics["accuracy"] < 0.7:
            recommendations.append("Include more accurate regulatory framework information")
        
        if metrics["diversity"] < 0.7:
            recommendations.append("Reduce repetitive phrases and increase response variety")
        
        if results["overall_score"] < 0.8:
            recommendations.append("Consider retraining with more diverse and specific training data")
        
        return recommendations
    
    def compare_models(self, model1: str, model2: str) -> Dict[str, Any]:
        """Compare two models"""
        logger.info(f"Comparing models: {model1} vs {model2}")
        
        results1 = self.validate_model(model1)
        results2 = self.validate_model(model2)
        
        comparison = {
            "model1": results1,
            "model2": results2,
            "improvement": {},
            "winner": ""
        }
        
        # Calculate improvements
        for metric in ["completeness", "specificity", "accuracy", "diversity", "overall_score"]:
            if metric in results1["quality_metrics"] and metric in results2["quality_metrics"]:
                improvement = results2["quality_metrics"][metric] - results1["quality_metrics"][metric]
                comparison["improvement"][metric] = improvement
        
        # Determine winner
        if results2["overall_score"] > results1["overall_score"]:
            comparison["winner"] = model2
        else:
            comparison["winner"] = model1
        
        return comparison

def main():
    """Main function"""
    print("🔍 BFSI Model Validation System")
    print("=" * 50)
    
    validator = BFSIModelValidator()
    
    try:
        # Validate the enhanced model
        print("📊 Validating enhanced BFSI model...")
        results = validator.validate_model("enhanced-bfsi-model")
        
        if "error" in results:
            print(f"❌ Validation failed: {results['error']}")
        else:
            print(f"✅ Model validation completed!")
            print(f"   Overall Score: {results['overall_score']:.2f}")
            print(f"   Completeness: {results['quality_metrics']['completeness']:.2f}")
            print(f"   Specificity: {results['quality_metrics']['specificity']:.2f}")
            print(f"   Accuracy: {results['quality_metrics']['accuracy']:.2f}")
            print(f"   Diversity: {results['quality_metrics']['diversity']:.2f}")
            
            if results['recommendations']:
                print(f"\n💡 Recommendations:")
                for rec in results['recommendations']:
                    print(f"   • {rec}")
        
        # Compare with original model if it exists
        original_path = Path("trained_models/bfsi-transformers-model_info.json")
        if original_path.exists():
            print(f"\n🔄 Comparing with original model...")
            comparison = validator.compare_models("bfsi-transformers-model", "enhanced-bfsi-model")
            
            print(f"   Winner: {comparison['winner']}")
            print(f"   Improvements:")
            for metric, improvement in comparison['improvement'].items():
                if improvement > 0:
                    print(f"     {metric}: +{improvement:.2f}")
                elif improvement < 0:
                    print(f"     {metric}: {improvement:.2f}")
        
        print("\n✅ Model validation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()
