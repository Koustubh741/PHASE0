"""
Compliance Monitoring Agent
Automated compliance checking and monitoring
"""

import os
import logging
from typing import Dict, Any, List
from datetime import datetime

# Optional imports with fallbacks
try:
    import openai
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import OpenAIEmbeddings
    HAS_AI_DEPENDENCIES = True
except ImportError as e:
    logging.warning(f"AI dependencies not available: {e}")
    HAS_AI_DEPENDENCIES = False
    # Create dummy classes for fallback
    class PyPDFLoader:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyPDFLoader not available")
    class RecursiveCharacterTextSplitter:
        def __init__(self, *args, **kwargs):
            pass
    class OpenAIEmbeddings:
        def __init__(self, *args, **kwargs):
            raise ImportError("OpenAIEmbeddings not available")

from shared_components.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ComplianceAgent(BaseAgent):
    """AI Agent for compliance monitoring and checking"""
    
    def __init__(self):
        super().__init__("compliance_001", "Compliance Monitoring Agent")
        self.openai_client = None
        self.embeddings = None
        self.vector_store = None
        self.setup_ai_services()
    
    def setup_ai_services(self):
        """Setup AI services and vector store"""
        try:
            # Initialize OpenAI client
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OpenAI API key not found")
                return
            
            self.openai_client = openai.OpenAI(api_key=api_key)
            
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            
            # Initialize Simple Vector Store
            try:
                from shared_components.simple_vector_store import SimpleVectorStore
                self.vector_store = SimpleVectorStore(
                    collection_name="compliance-policies",
                    persist_directory="./vector_store"
                )
                logger.info("Connected to Simple Vector Store")
            except Exception as e:
                logger.error(f"Failed to initialize Vector Store: {e}")
                self.vector_store = None
            
            logger.info("AI services initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup AI services: {e}")
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages"""
        try:
            message_type = message.get("type")
            
            if message_type == "compliance_check":
                return await self.check_compliance(message.get("data", {}))
            elif message_type == "policy_analysis":
                return await self.analyze_policy(message.get("data", {}))
            elif message_type == "violation_detection":
                return await self.detect_violations(message.get("data", {}))
            else:
                return {"error": f"Unknown message type: {message_type}"}
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {"error": str(e)}
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific compliance tasks"""
        task_type = task.get("type")
        
        if task_type == "batch_compliance_check":
            return await self.batch_compliance_check(task.get("data", {}))
        elif task_type == "policy_update":
            return await self.update_policy_embeddings(task.get("data", {}))
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    async def check_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance against policies"""
        try:
            document_content = data.get("content", "")
            policy_id = data.get("policy_id")
            
            if not document_content:
                return {"error": "No document content provided"}
            
            # Get relevant policy sections
            relevant_sections = await self.find_relevant_policy_sections(
                document_content, policy_id
            )
            
            # Use GPT-4 to analyze compliance
            compliance_result = await self.analyze_compliance_with_gpt(
                document_content, relevant_sections
            )
            
            return {
                "compliance_status": compliance_result.get("status"),
                "violations": compliance_result.get("violations", []),
                "recommendations": compliance_result.get("recommendations", []),
                "confidence_score": compliance_result.get("confidence", 0.0),
                "checked_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Compliance check failed: {e}")
            return {"error": str(e)}
    
    async def find_relevant_policy_sections(self, content: str, policy_id: str = None) -> List[str]:
        """Find relevant policy sections using vector similarity"""
        try:
            if not self.vector_store:
                logger.warning("Vector store not available")
                return []
            
            # Search for similar policy sections
            docs = self.vector_store.similarity_search(content, k=5)
            
            # Extract text from documents
            relevant_sections = [doc.page_content for doc in docs]
            
            return relevant_sections
            
        except Exception as e:
            logger.error(f"Failed to find relevant policy sections: {e}")
            return []
    
    async def analyze_compliance_with_gpt(self, content: str, policies: List[str]) -> Dict[str, Any]:
        """Analyze compliance using GPT-4"""
        try:
            if not self.openai_client:
                return {
                    "status": "error",
                    "violations": [],
                    "recommendations": ["AI service not available"],
                    "confidence": 0.0
                }
            
            # Prepare prompt
            policies_text = "\n\n".join(policies) if policies else "No specific policies provided"
            
            prompt = f"""
            Analyze the following content for compliance against the provided policies:
            
            Content to analyze:
            {content}
            
            Relevant policies:
            {policies_text}
            
            Please provide a JSON response with the following structure:
            {{
                "status": "compliant|non-compliant|partially-compliant",
                "violations": ["list of specific violations found"],
                "recommendations": ["list of recommendations for improvement"],
                "confidence": 0.95
            }}
            
            Be specific about violations and provide actionable recommendations.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            
            # Try to extract JSON from response
            try:
                import json
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError:
                # Fallback parsing if JSON is not properly formatted
                return {
                    "status": "partially-compliant",
                    "violations": ["Unable to parse AI response"],
                    "recommendations": ["Manual review recommended"],
                    "confidence": 0.5
                }
            
        except Exception as e:
            logger.error(f"GPT analysis failed: {e}")
            return {
                "status": "error",
                "violations": [],
                "recommendations": [f"Analysis failed: {str(e)}"],
                "confidence": 0.0
            }
    
    async def analyze_policy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze policy document"""
        try:
            policy_content = data.get("content", "")
            
            if not policy_content:
                return {"error": "No policy content provided"}
            
            # Analyze policy structure and content
            analysis = await self.analyze_policy_structure(policy_content)
            
            return {
                "policy_analysis": analysis,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Policy analysis failed: {e}")
            return {"error": str(e)}
    
    async def analyze_policy_structure(self, content: str) -> Dict[str, Any]:
        """Analyze policy structure and content"""
        # This is a simplified analysis - in production, you'd use more sophisticated NLP
        sections = content.split('\n\n')
        
        return {
            "total_sections": len(sections),
            "word_count": len(content.split()),
            "has_definitions": "definition" in content.lower(),
            "has_procedures": "procedure" in content.lower(),
            "has_penalties": "penalty" in content.lower() or "consequence" in content.lower()
        }
    
    async def detect_violations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect potential violations in documents"""
        try:
            document_content = data.get("content", "")
            
            if not document_content:
                return {"error": "No document content provided"}
            
            # Use pattern matching and AI to detect violations
            violations = await self.scan_for_violations(document_content)
            
            return {
                "violations": violations,
                "detected_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Violation detection failed: {e}")
            return {"error": str(e)}
    
    async def scan_for_violations(self, content: str) -> List[Dict[str, Any]]:
        """Scan content for potential violations"""
        violations = []
        
        # Simple pattern-based violation detection
        violation_patterns = [
            {"pattern": "password.*123", "type": "weak_password", "severity": "high"},
            {"pattern": "admin.*admin", "type": "default_credentials", "severity": "critical"},
            {"pattern": "http://", "type": "insecure_protocol", "severity": "medium"},
        ]
        
        import re
        for pattern_info in violation_patterns:
            if re.search(pattern_info["pattern"], content, re.IGNORECASE):
                violations.append({
                    "type": pattern_info["type"],
                    "severity": pattern_info["severity"],
                    "description": f"Potential {pattern_info['type']} violation detected"
                })
        
        return violations
    
    async def batch_compliance_check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform batch compliance checking on multiple documents"""
        try:
            documents = data.get("documents", [])
            policy_id = data.get("policy_id")
            
            if not documents:
                return {"error": "No documents provided"}
            
            results = []
            for doc in documents:
                result = await self.check_compliance({
                    "content": doc.get("content", ""),
                    "policy_id": policy_id
                })
                results.append({
                    "document_id": doc.get("id", "unknown"),
                    "result": result
                })
            
            return {
                "batch_results": results,
                "total_documents": len(documents),
                "processed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Batch compliance check failed: {e}")
            return {"error": str(e)}
    
    async def update_policy_embeddings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update policy embeddings in vector store"""
        try:
            policy_content = data.get("content", "")
            policy_id = data.get("policy_id", "unknown")
            
            if not policy_content or not self.vector_store:
                return {"error": "Policy content or vector store not available"}
            
            # Add policy to vector store
            self.vector_store.add_documents([{
                "content": policy_content,
                "metadata": {"policy_id": policy_id, "type": "policy"}
            }])
            
            return {
                "status": "success",
                "policy_id": policy_id,
                "updated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Policy embedding update failed: {e}")
            return {"error": str(e)}
