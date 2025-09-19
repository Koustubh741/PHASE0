"""
Hugging Face Enhanced Agents for GRC Platform
Integrates Hugging Face Transformers with existing agent architecture
"""

import logging
from typing import Dict, List, Any, Optional
from transformers import (
    pipeline, 
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    AutoModelForQuestionAnswering,
    AutoModelForTokenClassification,
    AutoModelForCausalLM
)
import torch
import numpy as np
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class HuggingFaceModelManager:
    """Manages Hugging Face models for different GRC tasks"""
    
    def __init__(self):
        self.models = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all required models"""
        try:
            # Document Classification Models
            self.models["document_classifier"] = pipeline(
                "text-classification",
                model="distilbert-base-uncased",
                device=0 if self.device == "cuda" else -1
            )
            
            # Question Answering for Compliance
            self.models["qa_model"] = pipeline(
                "question-answering",
                model="distilbert-base-uncased-distilled-squad",
                device=0 if self.device == "cuda" else -1
            )
            
            # Named Entity Recognition for Regulations
            self.models["ner_model"] = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                device=0 if self.device == "cuda" else -1
            )
            
            # Text Summarization for Risk Reports
            self.models["summarizer"] = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=0 if self.device == "cuda" else -1
            )
            
            # Financial Sentiment Analysis (BFSI)
            self.models["finbert"] = pipeline(
                "text-classification",
                model="ProsusAI/finbert",
                device=0 if self.device == "cuda" else -1
            )
            
            # Conversational AI for Compliance Q&A
            self.models["dialog_model"] = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("All Hugging Face models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Hugging Face models: {e}")
            raise

class HuggingFaceEnhancedComplianceAgent:
    """Enhanced Compliance Agent with Hugging Face models"""
    
    def __init__(self):
        self.model_manager = HuggingFaceModelManager()
        self.industry_models = {
            "bfsi": "ProsusAI/finbert",
            "healthcare": "dmis-lab/biobert-base-cased-v1.1",
            "manufacturing": "microsoft/codebert-base",
            "telecom": "distilbert-base-uncased"
        }
    
    async def analyze_compliance_document(self, document: str, industry: str) -> Dict[str, Any]:
        """Analyze compliance document using industry-specific models"""
        try:
            results = {}
            
            # Document Classification
            classification = self.model_manager.models["document_classifier"](document)
            results["classification"] = classification
            
            # Named Entity Recognition for regulations
            entities = self.model_manager.models["ner_model"](document)
            results["entities"] = entities
            
            # Industry-specific analysis
            if industry in self.industry_models:
                industry_model = self.industry_models[industry]
                # Load industry-specific model
                industry_pipeline = pipeline(
                    "text-classification",
                    model=industry_model,
                    device=0 if torch.cuda.is_available() else -1
                )
                industry_analysis = industry_pipeline(document)
                results["industry_analysis"] = industry_analysis
            
            # Compliance gap analysis
            compliance_qa = self._analyze_compliance_gaps(document)
            results["compliance_gaps"] = compliance_qa
            
            return {
                "status": "success",
                "analysis": results,
                "timestamp": datetime.now().isoformat(),
                "model_used": "huggingface_transformers"
            }
            
        except Exception as e:
            logger.error(f"Compliance analysis failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_compliance_gaps(self, document: str) -> Dict[str, Any]:
        """Analyze compliance gaps using Q&A model"""
        compliance_questions = [
            "What are the key compliance requirements mentioned?",
            "Are there any regulatory references?",
            "What are the risk factors identified?",
            "Are there any control measures mentioned?"
        ]
        
        gaps = []
        for question in compliance_questions:
            try:
                answer = self.model_manager.models["qa_model"]({
                    "question": question,
                    "context": document
                })
                gaps.append({
                    "question": question,
                    "answer": answer["answer"],
                    "confidence": answer["score"]
                })
            except Exception as e:
                logger.warning(f"Failed to answer question '{question}': {e}")
        
        return {"gaps": gaps}

class HuggingFaceEnhancedRiskAgent:
    """Enhanced Risk Agent with Hugging Face models"""
    
    def __init__(self):
        self.model_manager = HuggingFaceModelManager()
    
    async def assess_risk(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk using Hugging Face models"""
        try:
            risk_description = risk_data.get("description", "")
            risk_context = risk_data.get("context", "")
            
            # Risk classification
            risk_classification = self.model_manager.models["document_classifier"](risk_description)
            
            # Risk summarization
            if len(risk_description) > 100:
                summary = self.model_manager.models["summarizer"](
                    risk_description,
                    max_length=100,
                    min_length=30,
                    do_sample=False
                )
            else:
                summary = [{"summary_text": risk_description}]
            
            # Risk scoring based on classification confidence
            risk_score = self._calculate_risk_score(risk_classification, risk_context)
            
            return {
                "status": "success",
                "risk_assessment": {
                    "classification": risk_classification,
                    "summary": summary[0]["summary_text"],
                    "risk_score": risk_score,
                    "confidence": max([item["score"] for item in risk_classification])
                },
                "timestamp": datetime.now().isoformat(),
                "model_used": "huggingface_transformers"
            }
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _calculate_risk_score(self, classification: List[Dict], context: str) -> float:
        """Calculate risk score based on classification results"""
        # Simple risk scoring based on classification confidence and labels
        high_risk_labels = ["NEGATIVE", "RISK", "HIGH_RISK", "CRITICAL"]
        
        for item in classification:
            if item["label"] in high_risk_labels:
                return min(1.0, item["score"] * 1.5)  # Boost high-risk scores
        
        return max([item["score"] for item in classification])

class HuggingFaceEnhancedDocumentAgent:
    """Enhanced Document Agent with Hugging Face models"""
    
    def __init__(self):
        self.model_manager = HuggingFaceModelManager()
    
    async def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Process document using Hugging Face models"""
        try:
            content = document.get("content", "")
            doc_type = document.get("type", "unknown")
            
            # Document classification
            classification = self.model_manager.models["document_classifier"](content)
            
            # Named entity recognition
            entities = self.model_manager.models["ner_model"](content)
            
            # Document summarization
            if len(content) > 200:
                summary = self.model_manager.models["summarizer"](
                    content,
                    max_length=150,
                    min_length=50,
                    do_sample=False
                )
            else:
                summary = [{"summary_text": content}]
            
            # Extract key information
            key_info = self._extract_key_information(content, entities)
            
            return {
                "status": "success",
                "document_analysis": {
                    "classification": classification,
                    "entities": entities,
                    "summary": summary[0]["summary_text"],
                    "key_information": key_info,
                    "document_type": doc_type
                },
                "timestamp": datetime.now().isoformat(),
                "model_used": "huggingface_transformers"
            }
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_key_information(self, content: str, entities: List[Dict]) -> Dict[str, Any]:
        """Extract key information from document"""
        key_info = {
            "organizations": [],
            "regulations": [],
            "dates": [],
            "risks": []
        }
        
        for entity in entities:
            entity_type = entity["entity"]
            entity_text = entity["word"]
            
            if entity_type == "ORG":
                key_info["organizations"].append(entity_text)
            elif entity_type == "MISC" and any(reg in entity_text.upper() for reg in ["SOX", "HIPAA", "GDPR", "PCI"]):
                key_info["regulations"].append(entity_text)
            elif entity_type == "DATE":
                key_info["dates"].append(entity_text)
        
        return key_info

class HuggingFaceEnhancedCommunicationAgent:
    """Enhanced Communication Agent with Hugging Face models"""
    
    def __init__(self):
        self.model_manager = HuggingFaceModelManager()
    
    async def generate_response(self, query: str, context: str = "") -> Dict[str, Any]:
        """Generate contextual response using Hugging Face models"""
        try:
            # Use conversational model for responses
            response = self.model_manager.models["dialog_model"](
                query,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            
            # If context is provided, use Q&A model for more accurate responses
            if context:
                qa_response = self.model_manager.models["qa_model"]({
                    "question": query,
                    "context": context
                })
                
                return {
                    "status": "success",
                    "response": {
                        "conversational": response[0]["generated_text"],
                        "contextual": qa_response["answer"],
                        "confidence": qa_response["score"]
                    },
                    "timestamp": datetime.now().isoformat(),
                    "model_used": "huggingface_transformers"
                }
            
            return {
                "status": "success",
                "response": {
                    "conversational": response[0]["generated_text"],
                    "confidence": 0.8
                },
                "timestamp": datetime.now().isoformat(),
                "model_used": "huggingface_transformers"
            }
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Factory class for creating Hugging Face enhanced agents
class HuggingFaceAgentFactory:
    """Factory for creating Hugging Face enhanced agents"""
    
    @staticmethod
    def create_agent(agent_type: str):
        """Create Hugging Face enhanced agent by type"""
        agents = {
            "compliance": HuggingFaceEnhancedComplianceAgent,
            "risk": HuggingFaceEnhancedRiskAgent,
            "document": HuggingFaceEnhancedDocumentAgent,
            "communication": HuggingFaceEnhancedCommunicationAgent
        }
        
        if agent_type not in agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agents[agent_type]()

# Integration with existing agent system
class HuggingFaceIntegrationManager:
    """Manages integration of Hugging Face models with existing agents"""
    
    def __init__(self):
        self.enhanced_agents = {}
        self.model_manager = HuggingFaceModelManager()
    
    async def enhance_existing_agent(self, agent_type: str, original_agent):
        """Enhance existing agent with Hugging Face capabilities"""
        try:
            enhanced_agent = HuggingFaceAgentFactory.create_agent(agent_type)
            self.enhanced_agents[agent_type] = enhanced_agent
            
            # Add Hugging Face methods to original agent
            if hasattr(enhanced_agent, 'analyze_compliance_document'):
                original_agent.analyze_compliance_document_hf = enhanced_agent.analyze_compliance_document
            
            if hasattr(enhanced_agent, 'assess_risk'):
                original_agent.assess_risk_hf = enhanced_agent.assess_risk
            
            if hasattr(enhanced_agent, 'process_document'):
                original_agent.process_document_hf = enhanced_agent.process_document
            
            if hasattr(enhanced_agent, 'generate_response'):
                original_agent.generate_response_hf = enhanced_agent.generate_response
            
            logger.info(f"Successfully enhanced {agent_type} agent with Hugging Face models")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enhance {agent_type} agent: {e}")
            return False
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available Hugging Face models"""
        return {
            "document_classification": ["distilbert-base-uncased", "roberta-base"],
            "question_answering": ["distilbert-base-uncased-distilled-squad"],
            "named_entity_recognition": ["dbmdz/bert-large-cased-finetuned-conll03-english"],
            "summarization": ["facebook/bart-large-cnn"],
            "financial_analysis": ["ProsusAI/finbert"],
            "conversational": ["microsoft/DialoGPT-medium"],
            "biomedical": ["dmis-lab/biobert-base-cased-v1.1"],
            "code_analysis": ["microsoft/codebert-base"]
        }


