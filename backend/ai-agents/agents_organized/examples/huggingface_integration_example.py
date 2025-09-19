"""
Hugging Face Integration Example for GRC Platform
Shows how to integrate HF models with existing AIAgentsManagement
"""

import asyncio
import logging
from typing import Dict, Any, List
from shared_components.huggingface_enhanced_agents import (
    HuggingFaceAgentFactory,
    HuggingFaceIntegrationManager,
    HuggingFaceModelManager
)

logger = logging.getLogger(__name__)

class HuggingFaceGRCService:
    """Service class for integrating Hugging Face with GRC platform"""
    
    def __init__(self):
        self.integration_manager = HuggingFaceIntegrationManager()
        self.model_manager = HuggingFaceModelManager()
        self.available_models = self._get_available_models()
    
    def _get_available_models(self) -> Dict[str, List[str]]:
        """Get available Hugging Face models"""
        return {
            "document_classification": [
                "distilbert-base-uncased",
                "roberta-base",
                "ProsusAI/finbert",
                "dmis-lab/biobert-base-cased-v1.1"
            ],
            "question_answering": [
                "distilbert-base-uncased-distilled-squad"
            ],
            "named_entity_recognition": [
                "dbmdz/bert-large-cased-finetuned-conll03-english"
            ],
            "summarization": [
                "facebook/bart-large-cnn"
            ],
            "conversational": [
                "microsoft/DialoGPT-medium"
            ]
        }
    
    async def analyze_risk_with_hf(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk using Hugging Face models"""
        try:
            # Create risk agent
            risk_agent = HuggingFaceAgentFactory.create_agent("risk")
            
            # Analyze risk
            result = await risk_agent.assess_risk(risk_data)
            
            return {
                "status": "success",
                "analysis": result,
                "model_used": "huggingface_transformers",
                "timestamp": result.get("timestamp")
            }
            
        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "model_used": "huggingface_transformers"
            }
    
    async def analyze_compliance_with_hf(self, document: str, industry: str) -> Dict[str, Any]:
        """Analyze compliance using Hugging Face models"""
        try:
            # Create compliance agent
            compliance_agent = HuggingFaceAgentFactory.create_agent("compliance")
            
            # Analyze compliance
            result = await compliance_agent.analyze_compliance_document(document, industry)
            
            return {
                "status": "success",
                "analysis": result,
                "model_used": "huggingface_transformers",
                "timestamp": result.get("timestamp")
            }
            
        except Exception as e:
            logger.error(f"Compliance analysis failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "model_used": "huggingface_transformers"
            }
    
    async def process_document_with_hf(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Process document using Hugging Face models"""
        try:
            # Create document agent
            doc_agent = HuggingFaceAgentFactory.create_agent("document")
            
            # Process document
            result = await doc_agent.process_document(document)
            
            return {
                "status": "success",
                "analysis": result,
                "model_used": "huggingface_transformers",
                "timestamp": result.get("timestamp")
            }
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "model_used": "huggingface_transformers"
            }
    
    async def generate_response_with_hf(self, query: str, context: str = "") -> Dict[str, Any]:
        """Generate response using Hugging Face models"""
        try:
            # Create communication agent
            comm_agent = HuggingFaceAgentFactory.create_agent("communication")
            
            # Generate response
            result = await comm_agent.generate_response(query, context)
            
            return {
                "status": "success",
                "response": result,
                "model_used": "huggingface_transformers",
                "timestamp": result.get("timestamp")
            }
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "model_used": "huggingface_transformers"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available models"""
        return {
            "available_models": self.available_models,
            "model_manager_status": "initialized" if self.model_manager else "not_initialized",
            "integration_status": "ready"
        }

# Example usage for AIAgentsManagement integration
class HuggingFaceAIAgentsService:
    """Service class for integrating HF with AIAgentsManagement component"""
    
    def __init__(self):
        self.hf_service = HuggingFaceGRCService()
    
    async def assess_risk(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk using Hugging Face models"""
        return await self.hf_service.analyze_risk_with_hf(risk_assessment)
    
    async def analyze_compliance(self, compliance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compliance using Hugging Face models"""
        document = compliance_data.get("document", "")
        industry = compliance_data.get("industry", "default")
        return await self.hf_service.analyze_compliance_with_hf(document, industry)
    
    async def process_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process document using Hugging Face models"""
        return await self.hf_service.process_document_with_hf(document_data)
    
    async def generate_insights(self, query: str, context: str = "") -> Dict[str, Any]:
        """Generate insights using Hugging Face models"""
        return await self.hf_service.generate_response_with_hf(query, context)
    
    def get_available_industries(self) -> List[Dict[str, str]]:
        """Get available industries for HF analysis"""
        return [
            {"value": "bfsi", "label": "Banking, Financial Services & Insurance"},
            {"value": "healthcare", "label": "Healthcare & Life Sciences"},
            {"value": "manufacturing", "label": "Manufacturing"},
            {"value": "telecom", "label": "Telecommunications"},
            {"value": "default", "label": "General"}
        ]
    
    def get_model_capabilities(self) -> Dict[str, Any]:
        """Get information about model capabilities"""
        return {
            "document_analysis": {
                "classification": True,
                "summarization": True,
                "entity_extraction": True,
                "sentiment_analysis": True
            },
            "compliance_analysis": {
                "gap_analysis": True,
                "regulatory_mapping": True,
                "risk_assessment": True,
                "policy_review": True
            },
            "risk_management": {
                "risk_classification": True,
                "risk_scoring": True,
                "trend_analysis": True,
                "similarity_matching": True
            },
            "communication": {
                "q_and_a": True,
                "conversational_ai": True,
                "contextual_responses": True,
                "multi_language": False  # Can be added with multilingual models
            }
        }

# Example integration with existing AIAgentsManagement
async def example_integration():
    """Example of how to integrate HF with existing AIAgentsManagement"""
    
    # Initialize HF service
    hf_agents_service = HuggingFaceAIAgentsService()
    
    # Example 1: Risk Assessment
    risk_data = {
        "description": "High risk of data breach due to outdated security protocols in financial systems",
        "context": "BFSI company with customer financial data",
        "industry": "bfsi"
    }
    
    risk_result = await hf_agents_service.assess_risk(risk_data)
    print("Risk Assessment Result:", risk_result)
    
    # Example 2: Compliance Analysis
    compliance_data = {
        "document": "Our organization must comply with SOX regulations for financial reporting and internal controls...",
        "industry": "bfsi"
    }
    
    compliance_result = await hf_agents_service.analyze_compliance(compliance_data)
    print("Compliance Analysis Result:", compliance_result)
    
    # Example 3: Document Processing
    document_data = {
        "content": "HIPAA compliance requires encryption of patient data and secure access controls...",
        "type": "policy",
        "industry": "healthcare"
    }
    
    doc_result = await hf_agents_service.process_document(document_data)
    print("Document Processing Result:", doc_result)
    
    # Example 4: Generate Insights
    query = "What are the key compliance requirements for financial institutions?"
    context = "SOX, Basel III, and PCI DSS regulations"
    
    insights_result = await hf_agents_service.generate_insights(query, context)
    print("Insights Generation Result:", insights_result)
    
    # Get model information
    model_info = hf_agents_service.get_model_capabilities()
    print("Model Capabilities:", model_info)

# Example of how to modify AIAgentsManagement.jsx to use HF
def get_jsx_integration_example():
    """Example of how to modify AIAgentsManagement.jsx"""
    return """
// Add to AIAgentsManagement.jsx

import { huggingFaceService } from '../services/huggingFaceService';

// Add new state for HF models
const [useHuggingFace, setUseHuggingFace] = useState(false);
const [hfModelInfo, setHfModelInfo] = useState(null);

// Add HF toggle in the UI
<FormControlLabel
  control={
    <Switch
      checked={useHuggingFace}
      onChange={(e) => setUseHuggingFace(e.target.checked)}
      color="primary"
    />
  }
  label="Use Hugging Face Models"
/>

// Modify handleRiskAssessment to use HF
const handleRiskAssessment = async () => {
  try {
    setLoading(true);
    
    let result;
    if (useHuggingFace) {
      // Use Hugging Face models
      result = await huggingFaceService.assessRisk(riskAssessment);
    } else {
      // Use existing AI agents
      result = await aiAgentsService.assessRisk(riskAssessment);
    }
    
    setResults(prev => ({ ...prev, riskAssessment: result }));
    setError(null);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

// Add HF model info display
{hfModelInfo && (
  <Card sx={{ mt: 2 }}>
    <CardHeader>
      <Typography variant="h6">Hugging Face Models</Typography>
    </CardHeader>
    <CardContent>
      <Typography variant="body2">
        Available Models: {hfModelInfo.available_models?.length || 0}
      </Typography>
      <Typography variant="body2">
        Status: {hfModelInfo.integration_status}
      </Typography>
    </CardContent>
  </Card>
)}
"""

if __name__ == "__main__":
    # Run example
    asyncio.run(example_integration())


