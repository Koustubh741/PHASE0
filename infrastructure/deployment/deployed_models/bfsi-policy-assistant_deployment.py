#!/usr/bin/env python3
"""
Ollama Model Deployment Wrapper for bfsi-policy-assistant
Production-ready wrapper for BFSI model deployment
"""

import requests
import json
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BFSIModelAPI:
    """BFSI Model API wrapper for bfsi-policy-assistant"""
    
    def __init__(self, 
                 model_name: str = None, 
                 endpoint: str = None, 
                 validation_score: float = None):
        """
        Initialize BFSI Model API wrapper
        
        Args:
            model_name: Name of the model (defaults to env var or "bfsi-policy-assistant")
            endpoint: API endpoint URL (defaults to env var or localhost:11434)
            validation_score: Model validation score from testing (defaults to env var or 7.06)
        """
        # Use environment variables or parameters, with fallback defaults
        self.model_name = model_name or os.getenv("BFSI_MODEL_NAME", "bfsi-policy-assistant")
        self.endpoint = endpoint or os.getenv("BFSI_MODEL_ENDPOINT", "http://localhost:11434/api/generate")
        
        # Parse validation score from environment or use parameter
        if validation_score is None:
            validation_score = float(os.getenv("BFSI_VALIDATION_SCORE", "7.06"))
        
        # Generate deployment timestamp dynamically
        deployment_timestamp = datetime.now().isoformat()
        
        # Define configuration once to eliminate duplication
        self.config = {
            "model_name": self.model_name,  # Reuse instance variable
            "model_type": "ollama",
            "deployment_method": "ollama_api",
            "endpoint": self.endpoint,  # Reuse instance variable
            "model_parameters": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 512
            },
            "bfsi_config": {
                "supported_tasks": [
                    "policy_analysis",
                    "risk_assessment",
                    "compliance_guidance",
                    "implementation_advice",
                    "regulatory_framework_analysis"
                ],
                "specializations": [
                    "BFSI",
                    "compliance",
                    "risk_management"
                ],
                "max_context_length": 4096
            },
            "deployment_timestamp": deployment_timestamp,  # Dynamic timestamp
            "validation_score": validation_score  # Parameterized validation score
        }
        
        # Log initialization with dynamic values
        logger.info(f"BFSI Model API initialized: {self.model_name} at {self.endpoint}")
        logger.info(f"Deployment timestamp: {deployment_timestamp}")
        logger.info(f"Validation score: {validation_score} (from model testing/validation phase)")
    
    @classmethod
    def create_with_config(cls, model_name: str, endpoint: str, validation_score: float = None):
        """
        Create BFSI Model API instance with custom configuration
        
        Args:
            model_name: Name of the model
            endpoint: API endpoint URL
            validation_score: Model validation score (0-10 scale, from testing phase)
            
        Returns:
            BFSIModelAPI instance with custom configuration
        """
        return cls(model_name=model_name, endpoint=endpoint, validation_score=validation_score)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information including validation details
        
        Returns:
            Dictionary containing model metadata and validation information
        """
        return {
            "model_name": self.model_name,
            "endpoint": self.endpoint,
            "deployment_timestamp": self.config["deployment_timestamp"],
            "validation_score": self.config["validation_score"],
            "validation_notes": "Score represents model performance on BFSI domain tasks (0-10 scale)",
            "validation_origin": "Generated during model testing/validation phase",
            "config": self.config
        }
        
    def analyze_policy(self, policy_text: str, policy_type: str = "compliance") -> Dict[str, Any]:
        """Analyze BFSI policy"""
        prompt = f"""Analyze this {policy_type} policy and provide detailed insights:

Policy Text: {policy_text}

Please provide:
1. Key compliance requirements
2. Risk assessment
3. Implementation recommendations
4. Regulatory framework alignment
"""
        
        return self._query_model(prompt)
    
    def assess_risk(self, risk_description: str) -> Dict[str, Any]:
        """Assess BFSI risks"""
        prompt = f"""Assess the following BFSI risk scenario:

Risk Description: {risk_description}

Please provide:
1. Risk level assessment
2. Potential impact analysis
3. Mitigation strategies
4. Monitoring recommendations
"""
        
        return self._query_model(prompt)
    
    def compliance_guidance(self, compliance_question: str) -> Dict[str, Any]:
        """Provide compliance guidance"""
        prompt = f"""Provide compliance guidance for this BFSI question:

Question: {compliance_question}

Please provide:
1. Regulatory requirements
2. Compliance procedures
3. Best practices
4. Implementation steps
"""
        
        return self._query_model(prompt)
    
    def _query_model(self, prompt: str) -> Dict[str, Any]:
        """Query the deployed model"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": self.config["model_parameters"]
            }
            
            response = requests.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "success": True,
                "response": result.get("response", ""),
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error querying model: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }

# Global instance - can be configured via environment variables
# BFSI_MODEL_NAME, BFSI_MODEL_ENDPOINT, BFSI_VALIDATION_SCORE
bfsi_model = BFSIModelAPI()

# Convenience functions
def analyze_policy(policy_text: str, policy_type: str = "compliance") -> Dict[str, Any]:
    return bfsi_model.analyze_policy(policy_text, policy_type)

def assess_risk(risk_description: str) -> Dict[str, Any]:
    return bfsi_model.assess_risk(risk_description)

def get_compliance_guidance(question: str) -> Dict[str, Any]:
    return bfsi_model.compliance_guidance(question)

if __name__ == "__main__":
    # Test the deployed model
    test_policy = "This policy outlines data protection requirements for financial institutions under GDPR framework."
    
    print("Testing deployed BFSI model...")
    
    # Display model information
    model_info = bfsi_model.get_model_info()
    print(f"Model: {model_info['model_name']}")
    print(f"Endpoint: {model_info['endpoint']}")
    print(f"Deployment: {model_info['deployment_timestamp']}")
    print(f"Validation Score: {model_info['validation_score']} - {model_info['validation_notes']}")
    print(f"Validation Origin: {model_info['validation_origin']}")
    print()
    
    # Test model functionality
    result = analyze_policy(test_policy)
    
    if result["success"]:
        print("✅ Model is working correctly")
        print(f"Response: {result['response'][:200]}...")
    else:
        print(f"❌ Model error: {result['error']}")
    
    # Example of creating custom instance
    print("\nExample of custom configuration:")
    custom_model = BFSIModelAPI.create_with_config(
        model_name="custom-bfsi-model",
        endpoint="http://custom-server:11434/api/generate",
        validation_score=8.5
    )
    print(f"Custom model info: {custom_model.get_model_info()['model_name']}")
