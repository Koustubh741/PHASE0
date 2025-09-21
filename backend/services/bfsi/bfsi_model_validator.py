#!/usr/bin/env python3
"""
BFSI Model Validator
Comprehensive testing and validation system for trained BFSI models
"""

import json
import sqlite3
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BFSIModelValidator:
    """Validator for BFSI trained models"""
    
    def __init__(self, db_path: str = "bfsi_policies.db"):
        self.db_path = db_path
        self.results_dir = Path("validation_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Test cases for validation
        self.test_cases = self._load_test_cases()
        
        logger.info("BFSI Model Validator initialized")
    
    def _load_test_cases(self) -> List[Dict[str, Any]]:
        """Load test cases for model validation"""
        return [
            {
                "id": "policy_analysis",
                "category": "Policy Analysis",
                "prompt": "Analyze this BFSI compliance policy and identify key requirements:",
                "context": "Our organization needs to implement a comprehensive data protection policy under GDPR framework for financial services.",
                "expected_keywords": ["GDPR", "data protection", "compliance", "financial services", "privacy"],
                "difficulty": "medium"
            },
            {
                "id": "risk_assessment",
                "category": "Risk Assessment",
                "prompt": "What are the main risks associated with this BFSI policy?",
                "context": "A new operational risk management policy for banking operations.",
                "expected_keywords": ["operational risk", "banking", "mitigation", "controls", "assessment"],
                "difficulty": "high"
            },
            {
                "id": "compliance_guidance",
                "category": "Compliance Guidance",
                "prompt": "How should this policy ensure SOX compliance?",
                "context": "Internal controls policy for financial reporting.",
                "expected_keywords": ["SOX", "internal controls", "financial reporting", "audit", "compliance"],
                "difficulty": "high"
            },
            {
                "id": "implementation_advice",
                "category": "Implementation",
                "prompt": "Provide implementation guidance for this BFSI policy:",
                "context": "Anti-money laundering (AML) policy for financial institutions.",
                "expected_keywords": ["AML", "implementation", "training", "monitoring", "procedures"],
                "difficulty": "medium"
            },
            {
                "id": "regulatory_framework",
                "category": "Regulatory Framework",
                "prompt": "Which regulatory frameworks apply to this policy?",
                "context": "Customer due diligence policy for banks.",
                "expected_keywords": ["regulatory", "framework", "due diligence", "banks", "compliance"],
                "difficulty": "medium"
            }
        ]
    
    def test_ollama_model(self, model_name: str) -> Dict[str, Any]:
        """Test Ollama model with validation cases"""
        logger.info(f"Testing Ollama model: {model_name}")
        
        try:
            # Check if model exists
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if model_name not in result.stdout:
                return {"error": f"Model {model_name} not found", "status": "failed"}
            
            test_results = []
            total_score = 0
            
            for test_case in self.test_cases:
                logger.info(f"Running test: {test_case['id']}")
                
                # Prepare test prompt
                full_prompt = f"{test_case['prompt']}\n\nContext: {test_case['context']}"
                
                # Run test
                start_time = time.time()
                result = self._run_ollama_test(model_name, full_prompt)
                response_time = time.time() - start_time
                
                # Evaluate response
                score = self._evaluate_response(result, test_case)
                
                test_result = {
                    "test_id": test_case['id'],
                    "category": test_case['category'],
                    "difficulty": test_case['difficulty'],
                    "prompt": full_prompt,
                    "response": result,
                    "score": score,
                    "response_time": response_time,
                    "keywords_found": self._find_keywords(result, test_case['expected_keywords']),
                    "timestamp": datetime.now().isoformat()
                }
                
                test_results.append(test_result)
                total_score += score
                
                logger.info(f"Test {test_case['id']} completed - Score: {score}/10")
            
            # Calculate overall metrics
            avg_score = total_score / len(self.test_cases)
            avg_response_time = sum(t['response_time'] for t in test_results) / len(test_results)
            
            validation_result = {
                "model_name": model_name,
                "model_type": "ollama",
                "total_tests": len(self.test_cases),
                "total_score": total_score,
                "average_score": avg_score,
                "average_response_time": avg_response_time,
                "test_results": test_results,
                "overall_rating": self._get_rating(avg_score),
                "validation_timestamp": datetime.now().isoformat()
            }
            
            # Save results
            self._save_validation_results(validation_result)
            
            logger.info(f"Ollama model validation completed - Average Score: {avg_score:.2f}/10")
            return validation_result
            
        except Exception as e:
            logger.error(f"Error testing Ollama model: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _run_ollama_test(self, model_name: str, prompt: str) -> str:
        """Run a test with Ollama model"""
        try:
            cmd = ['ollama', 'run', model_name, prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"
        
        except subprocess.TimeoutExpired:
            return "Error: Test timed out"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_huggingface_model(self, model_path: str) -> Dict[str, Any]:
        """Test Hugging Face model with validation cases"""
        logger.info(f"Testing Hugging Face model: {model_path}")
        
        try:
            # Check if transformers is available
            try:
                from transformers import pipeline, AutoTokenizer
                import torch
            except ImportError:
                return {"error": "transformers library not available", "status": "failed"}
            
            # Load model
            try:
                generator = pipeline("text-generation", 
                                   model=model_path,
                                   device=0 if torch.cuda.is_available() else -1)
            except (OSError, FileNotFoundError, ValueError, RuntimeError) as e:
                # Specific exceptions for model loading failures
                error_msg = f"Failed to load custom model '{model_path}': {str(e)}"
                logger.error(error_msg)
                return {"error": error_msg, "status": "failed"}
            except Exception as e:
                # Catch any other unexpected errors
                error_msg = f"Unexpected error loading model '{model_path}': {str(e)}"
                logger.error(error_msg)
                return {"error": error_msg, "status": "failed"}
            
            test_results = []
            total_score = 0
            
            for test_case in self.test_cases:
                logger.info(f"Running test: {test_case['id']}")
                
                # Prepare test prompt
                full_prompt = f"{test_case['prompt']}\n\nContext: {test_case['context']}\n\nResponse:"
                
                # Run test
                start_time = time.time()
                result = generator(full_prompt, max_length=200, num_return_sequences=1, 
                                 temperature=0.7, do_sample=True)
                response_time = time.time() - start_time
                
                # Extract response
                response = result[0]["generated_text"][len(full_prompt):].strip()
                
                # Evaluate response
                score = self._evaluate_response(response, test_case)
                
                test_result = {
                    "test_id": test_case['id'],
                    "category": test_case['category'],
                    "difficulty": test_case['difficulty'],
                    "prompt": full_prompt,
                    "response": response,
                    "score": score,
                    "response_time": response_time,
                    "keywords_found": self._find_keywords(response, test_case['expected_keywords']),
                    "timestamp": datetime.now().isoformat()
                }
                
                test_results.append(test_result)
                total_score += score
                
                logger.info(f"Test {test_case['id']} completed - Score: {score}/10")
            
            # Calculate overall metrics
            avg_score = total_score / len(self.test_cases)
            avg_response_time = sum(t['response_time'] for t in test_results) / len(test_results)
            
            validation_result = {
                "model_name": model_path,
                "model_type": "huggingface",
                "total_tests": len(self.test_cases),
                "total_score": total_score,
                "average_score": avg_score,
                "average_response_time": avg_response_time,
                "test_results": test_results,
                "overall_rating": self._get_rating(avg_score),
                "validation_timestamp": datetime.now().isoformat()
            }
            
            # Save results
            self._save_validation_results(validation_result)
            
            logger.info(f"Hugging Face model validation completed - Average Score: {avg_score:.2f}/10")
            return validation_result
            
        except Exception as e:
            logger.error(f"Error testing Hugging Face model: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _evaluate_response(self, response: str, test_case: Dict[str, Any]) -> float:
        """Evaluate model response quality"""
        if not response or response.startswith("Error:"):
            return 0.0
        
        score = 0.0
        
        # Check for expected keywords (4 points)
        keywords_found = self._find_keywords(response, test_case['expected_keywords'])
        keyword_score = (len(keywords_found) / len(test_case['expected_keywords'])) * 4
        score += keyword_score
        
        # Check response length (2 points)
        if len(response) > 100:
            score += 2
        elif len(response) > 50:
            score += 1
        
        # Check for BFSI-specific terms (2 points)
        bfsi_terms = ["policy", "compliance", "risk", "regulation", "financial", "banking", "security"]
        bfsi_found = self._find_keywords(response, bfsi_terms)
        bfsi_score = (len(bfsi_found) / len(bfsi_terms)) * 2
        score += bfsi_score
        
        # Check for structured response (2 points)
        if any(indicator in response.lower() for indicator in ["1.", "2.", "•", "-", "key", "important"]):
            score += 2
        elif any(indicator in response.lower() for indicator in ["first", "second", "next", "then"]):
            score += 1
        
        return min(score, 10.0)  # Cap at 10
    
    def _find_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """Find keywords in text (case-insensitive)"""
        text_lower = text.lower()
        found = []
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                found.append(keyword)
        
        return found
    
    def _get_rating(self, score: float) -> str:
        """Get rating based on score"""
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        elif score >= 4:
            return "Fair"
        elif score >= 2:
            return "Poor"
        else:
            return "Very Poor"
    
    def _save_validation_results(self, results: Dict[str, Any]):
        """Save validation results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validation_{results['model_name'].replace('/', '_')}_{timestamp}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Validation results saved: {filepath}")
    
    def compare_models(self, model_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple model validation results"""
        if len(model_results) < 2:
            return {"error": "Need at least 2 models to compare"}
        
        comparison = {
            "comparison_timestamp": datetime.now().isoformat(),
            "models_compared": len(model_results),
            "models": [],
            "rankings": {},
            "summary": {}
        }
        
        # Extract metrics for each model
        for result in model_results:
            model_info = {
                "name": result["model_name"],
                "type": result["model_type"],
                "average_score": result["average_score"],
                "average_response_time": result["average_response_time"],
                "overall_rating": result["overall_rating"]
            }
            comparison["models"].append(model_info)
        
        # Sort by average score
        sorted_models = sorted(comparison["models"], key=lambda x: x["average_score"], reverse=True)
        
        # Create rankings
        comparison["rankings"]["by_score"] = [
            {"rank": i+1, "model": model["name"], "score": model["average_score"]}
            for i, model in enumerate(sorted_models)
        ]
        
        # Sort by response time (fastest first)
        sorted_by_time = sorted(comparison["models"], key=lambda x: x["average_response_time"])
        comparison["rankings"]["by_speed"] = [
            {"rank": i+1, "model": model["name"], "time": model["average_response_time"]}
            for i, model in enumerate(sorted_by_time)
        ]
        
        # Summary statistics
        scores = [model["average_score"] for model in comparison["models"]]
        times = [model["average_response_time"] for model in comparison["models"]]
        
        comparison["summary"] = {
            "best_score": max(scores),
            "worst_score": min(scores),
            "average_score": sum(scores) / len(scores),
            "fastest_time": min(times),
            "slowest_time": max(times),
            "average_time": sum(times) / len(times),
            "best_overall_model": sorted_models[0]["name"] if sorted_models else None
        }
        
        # Save comparison
        self._save_validation_results(comparison)
        
        return comparison
    
    def get_validation_history(self) -> List[Dict[str, Any]]:
        """Get validation history"""
        history = []
        
        for result_file in self.results_dir.glob("validation_*.json"):
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract summary info
                summary = {
                    "model_name": data.get("model_name", "unknown"),
                    "model_type": data.get("model_type", "unknown"),
                    "average_score": data.get("average_score", 0),
                    "overall_rating": data.get("overall_rating", "unknown"),
                    "validation_timestamp": data.get("validation_timestamp", "unknown"),
                    "file": str(result_file)
                }
                
                history.append(summary)
            
            except Exception as e:
                logger.warning(f"Error reading validation file {result_file}: {e}")
        
        return sorted(history, key=lambda x: x["validation_timestamp"], reverse=True)

def main():
    """Main function"""
    print("🧪 BFSI Model Validator")
    print("=" * 40)
    
    validator = BFSIModelValidator()
    
    try:
        # Test Ollama model if available
        print("\n🤖 Testing Ollama models...")
        ollama_result = validator.test_ollama_model("bfsi-policy-assistant")
        
        if "error" not in ollama_result:
            print(f"✅ Ollama model validation completed")
            print(f"   Model: {ollama_result['model_name']}")
            print(f"   Average Score: {ollama_result['average_score']:.2f}/10")
            print(f"   Rating: {ollama_result['overall_rating']}")
            print(f"   Response Time: {ollama_result['average_response_time']:.2f}s")
        else:
            print(f"⚠️ Ollama validation: {ollama_result['error']}")
        
        # Test Hugging Face models
        print("\n🤖 Testing Hugging Face models...")
        hf_models = ["bfsi-transformers-model", "bfsi-quick-transformers"]
        
        hf_results = []
        for model_name in hf_models:
            model_path = f"trained_models/{model_name}"
            if Path(model_path).exists():
                result = validator.test_huggingface_model(model_path)
                if "error" not in result:
                    hf_results.append(result)
                    print(f"✅ {model_name} validation completed - Score: {result['average_score']:.2f}/10")
                else:
                    print(f"⚠️ {model_name} validation: {result['error']}")
        
        # Compare models if we have multiple results
        all_results = []
        if "error" not in ollama_result:
            all_results.append(ollama_result)
        all_results.extend(hf_results)
        
        if len(all_results) > 1:
            print("\n📊 Comparing models...")
            comparison = validator.compare_models(all_results)
            print(f"Best overall model: {comparison['summary']['best_overall_model']}")
            print(f"Best score: {comparison['summary']['best_score']:.2f}/10")
            print(f"Fastest model: {comparison['rankings']['by_speed'][0]['model']}")
        
        # Show validation history
        print("\n📈 Validation History:")
        history = validator.get_validation_history()
        for entry in history[:5]:  # Show last 5 validations
            print(f"  {entry['model_name']} ({entry['model_type']}) - {entry['average_score']:.2f}/10 - {entry['overall_rating']}")
        
        print("\n✅ Model validation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
