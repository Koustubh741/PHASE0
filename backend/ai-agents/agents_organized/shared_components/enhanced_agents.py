"""
Enhanced AI Agents with Vector Database Integration
Archer-style GRC Platform AI Agents
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
import uvicorn

# Import simple vector store
from ..utilities.simple_vector_store import SimpleVectorStore

# Mock vector service for compatibility
class MockVectorService:
    def __init__(self):
        self.store = SimpleVectorStore("compliance-policies")
    
    def search_similar_documents(self, query, collection_type="compliance", n_results=5, organization_id=None, filters=None):
        """Mock search that returns empty results for now"""
        return {
            'documents': [],
            'similarities': [],
            'metadata': []
        }
    
    def get_all_collections_stats(self):
        """Mock stats"""
        return {
            'total_documents': 0,
            'collections': {}
        }

# Global mock service
vector_service = MockVectorService()

# Import existing agent classes using relative imports
from ...src.agents.compliance_agent import ComplianceAgent

# Mock classes for missing agents
class RiskAgent:
    def __init__(self):
        self.agent_id = "mock_risk"
        self.name = "Mock Risk Agent"
    
    def analyze_risk(self, *args, **kwargs):
        return {"risk_level": "medium", "recommendations": []}

class DocumentAgent:
    def __init__(self):
        self.agent_id = "mock_document"
        self.name = "Mock Document Agent"
    
    def classify_document(self, *args, **kwargs):
        return {"classification": "policy", "confidence": 0.8}

class CommunicationAgent:
    def __init__(self):
        self.agent_id = "mock_communication"
        self.name = "Mock Communication Agent"
    
    def send_notification(self, *args, **kwargs):
        return {"status": "sent", "message_id": "mock_123"}

logger = logging.getLogger(__name__)

class EnhancedComplianceAgent(ComplianceAgent):
    """
    Enhanced Compliance Agent with Vector Database Integration
    """
    
    def __init__(self):
        super().__init__()
        self.vector_service = vector_service
        self.agent_type = "enhanced_compliance"
        
    async def analyze_compliance_gaps(self, 
                                    organization_id: str,
                                    framework: str = None) -> Dict[str, Any]:
        """
        Analyze compliance gaps using vector database search
        """
        try:
            # Search for compliance-related documents
            search_query = f"compliance requirements {framework or 'general'}"
            
            results = self.vector_service.search_similar_documents(
                query=search_query,
                collection_type="compliance",
                n_results=20,
                organization_id=organization_id,
                filters={"framework": framework} if framework else None
            )
            
            # Analyze results for gaps with proper validation
            gaps = []
            for result in results:
                try:
                    # Validate result structure
                    if not isinstance(result, dict):
                        continue
                    
                    metadata = result.get("metadata")
                    if not isinstance(metadata, dict):
                        continue
                    
                    # Check if status indicates non-compliance
                    if metadata.get("status") != "NON_COMPLIANT":
                        continue
                    
                    # Safely extract content
                    content = result.get("content", "")
                    if not isinstance(content, str):
                        content = str(content) if content is not None else ""
                    
                    # Safely extract distance
                    distance = result.get("distance", 0)
                    if not isinstance(distance, (int, float)) or distance is None:
                        distance = 0
                    
                    # Build gap entry with safe defaults
                    gap = {
                        "requirement": metadata.get("title", "Unknown Requirement"),
                        "description": content[:200] + "..." if len(content) > 200 else content,
                        "severity": "HIGH" if metadata.get("priority") == "HIGH" else "MEDIUM",
                        "similarity_score": max(0, 1 - distance) if distance is not None else 0
                    }
                    gaps.append(gap)
                    
                except (KeyError, TypeError, AttributeError) as e:
                    # Log and skip malformed entries
                    logging.warning(f"Skipping malformed result in compliance analysis: {e}")
                    continue
            
            return {
                "organization_id": organization_id,
                "framework": framework,
                "total_gaps": len(gaps),
                "gaps": gaps,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing compliance gaps: {e}")
            raise
    
    async def recommend_compliance_actions(self,
                                         organization_id: str,
                                         risk_level: str = "MEDIUM") -> List[Dict[str, Any]]:
        """
        Recommend compliance actions based on vector database analysis
        """
        try:
            # Search for similar compliance issues
            search_query = f"compliance remediation actions {risk_level} risk"
            
            results = self.vector_service.search_similar_documents(
                query=search_query,
                collection_type="compliance",
                n_results=10,
                organization_id=organization_id
            )
            
            recommendations = []
            for result in results:
                recommendations.append({
                    "action": result["metadata"].get("title", "Compliance Action"),
                    "description": result["content"][:300] + "...",
                    "priority": result["metadata"].get("priority", "MEDIUM"),
                    "estimated_effort": result["metadata"].get("effort", "MEDIUM"),
                    "similarity_score": 1 - result["distance"] if result["distance"] else 0
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating compliance recommendations: {e}")
            raise

class EnhancedRiskAgent(RiskAgent):
    """
    Enhanced Risk Agent with Vector Database Integration
    """
    
    def __init__(self):
        super().__init__()
        self.vector_service = vector_service
        self.agent_type = "enhanced_risk"
    
    async def identify_similar_risks(self,
                                   organization_id: str,
                                   risk_description: str) -> List[Dict[str, Any]]:
        """
        Identify similar risks using vector database search
        """
        try:
            # Search for similar risks
            results = self.vector_service.search_similar_documents(
                query=risk_description,
                collection_type="risks",
                n_results=10,
                organization_id=organization_id
            )
            
            similar_risks = []
            for result in results:
                similar_risks.append({
                    "risk_id": result["metadata"].get("risk_id"),
                    "title": result["metadata"].get("title"),
                    "description": result["content"][:200] + "...",
                    "risk_type": result["metadata"].get("risk_type"),
                    "impact_score": result["metadata"].get("impact_score"),
                    "probability_score": result["metadata"].get("probability_score"),
                    "similarity_score": 1 - result["distance"] if result["distance"] else 0
                })
            
            return similar_risks
            
        except Exception as e:
            logger.error(f"Error identifying similar risks: {e}")
            raise
    
    async def predict_risk_trends(self,
                                organization_id: str,
                                time_period: str = "6_months") -> Dict[str, Any]:
        """
        Predict risk trends based on historical data in vector database
        """
        try:
            # Search for risk-related documents
            search_query = f"risk trends analysis {time_period}"
            
            results = self.vector_service.search_similar_documents(
                query=search_query,
                collection_type="risks",
                n_results=15,
                organization_id=organization_id
            )
            
            # Analyze trends
            risk_types = {}
            for result in results:
                risk_type = result["metadata"].get("risk_type", "UNKNOWN")
                if risk_type not in risk_types:
                    risk_types[risk_type] = {
                        "count": 0,
                        "avg_impact": 0,
                        "avg_probability": 0
                    }
                
                risk_types[risk_type]["count"] += 1
                risk_types[risk_type]["avg_impact"] += result["metadata"].get("impact_score", 0)
                risk_types[risk_type]["avg_probability"] += result["metadata"].get("probability_score", 0)
            
            # Calculate averages
            for risk_type in risk_types:
                count = risk_types[risk_type]["count"]
                risk_types[risk_type]["avg_impact"] /= count
                risk_types[risk_type]["avg_probability"] /= count
            
            return {
                "organization_id": organization_id,
                "time_period": time_period,
                "risk_trends": risk_types,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting risk trends: {e}")
            raise

class EnhancedDocumentAgent(DocumentAgent):
    """
    Enhanced Document Agent with Vector Database Integration
    """
    
    def __init__(self):
        super().__init__()
        self.vector_service = vector_service
        self.agent_type = "enhanced_document"
    
    async def classify_document(self,
                              document_content: str,
                              organization_id: str) -> Dict[str, Any]:
        """
        Classify document using vector database similarity
        """
        try:
            # Search for similar documents to determine classification
            results = self.vector_service.search_similar_documents(
                query=document_content[:500],  # Use first 500 chars for search
                collection_type="documents",
                n_results=5,
                organization_id=organization_id
            )
            
            # Determine classification based on similar documents
            classifications = {}
            for result in results:
                doc_type = result["metadata"].get("type", "unknown")
                if doc_type not in classifications:
                    classifications[doc_type] = 0
                classifications[doc_type] += 1 - result["distance"] if result["distance"] else 0
            
            # Get the most likely classification
            best_classification = max(classifications.items(), key=lambda x: x[1]) if classifications else ("unknown", 0)
            
            return {
                "document_type": best_classification[0],
                "confidence": best_classification[1],
                "all_classifications": classifications,
                "similar_documents": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error classifying document: {e}")
            raise
    
    async def extract_key_information(self,
                                    document_content: str,
                                    organization_id: str) -> Dict[str, Any]:
        """
        Extract key information from document using vector database context
        """
        try:
            # Search for similar documents to understand context
            results = self.vector_service.search_similar_documents(
                query=document_content[:300],
                collection_type="documents",
                n_results=10,
                organization_id=organization_id
            )
            
            # Extract common patterns from similar documents
            key_terms = set()
            for result in results:
                # Simple keyword extraction (in production, use NLP)
                words = result["content"].lower().split()
                key_terms.update([word for word in words if len(word) > 4])
            
            # Get metadata patterns
            metadata_patterns = {}
            for result in results:
                for key, value in result["metadata"].items():
                    if key not in metadata_patterns:
                        metadata_patterns[key] = set()
                    if isinstance(value, str):
                        metadata_patterns[key].add(value)
            
            return {
                "key_terms": list(key_terms)[:20],  # Top 20 terms
                "metadata_patterns": {k: list(v) for k, v in metadata_patterns.items()},
                "similar_documents_count": len(results),
                "extraction_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting key information: {e}")
            raise

class EnhancedCommunicationAgent(CommunicationAgent):
    """
    Enhanced Communication Agent with Vector Database Integration
    """
    
    def __init__(self):
        super().__init__()
        self.vector_service = vector_service
        self.agent_type = "enhanced_communication"
    
    async def generate_contextual_responses(self,
                                          query: str,
                                          organization_id: str,
                                          context_type: str = "general") -> Dict[str, Any]:
        """
        Generate contextual responses using vector database knowledge
        """
        try:
            # Search for relevant context
            search_results = {}
            for collection_type in ["policies", "risks", "compliance", "documents"]:
                results = self.vector_service.search_similar_documents(
                    query=query,
                    collection_type=collection_type,
                    n_results=3,
                    organization_id=organization_id
                )
                search_results[collection_type] = results
            
            # Generate response based on context
            response_context = {
                "query": query,
                "organization_id": organization_id,
                "context_type": context_type,
                "relevant_policies": len(search_results.get("policies", [])),
                "relevant_risks": len(search_results.get("risks", [])),
                "relevant_compliance": len(search_results.get("compliance", [])),
                "relevant_documents": len(search_results.get("documents", [])),
                "timestamp": datetime.now().isoformat()
            }
            
            # Add top relevant content
            all_results = []
            for collection_type, results in search_results.items():
                for result in results:
                    all_results.append({
                        "type": collection_type,
                        "title": result["metadata"].get("title", "Unknown"),
                        "content": result["content"][:200] + "...",
                        "similarity": 1 - result["distance"] if result["distance"] else 0
                    })
            
            # Sort by similarity
            all_results.sort(key=lambda x: x["similarity"], reverse=True)
            response_context["top_relevant_content"] = all_results[:5]
            
            return response_context
            
        except Exception as e:
            logger.error(f"Error generating contextual response: {e}")
            raise

class GRCPlatformOrchestrator:
    """
    Enhanced GRC Platform Orchestrator with Vector Database Integration
    """
    
    def __init__(self):
        self.vector_service = vector_service
        self.agents = {
            "compliance": EnhancedComplianceAgent(),
            "risk": EnhancedRiskAgent(),
            "document": EnhancedDocumentAgent(),
            "communication": EnhancedCommunicationAgent()
        }
        self.agent_status = {agent_id: "active" for agent_id in self.agents.keys()}
        
    async def perform_cross_domain_analysis(self,
                                          organization_id: str,
                                          analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Perform cross-domain analysis using all agents and vector database
        """
        try:
            analysis_results = {
                "organization_id": organization_id,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "results": {}
            }
            
            # Compliance analysis
            compliance_agent = self.agents["compliance"]
            compliance_gaps = await compliance_agent.analyze_compliance_gaps(organization_id)
            analysis_results["results"]["compliance"] = compliance_gaps
            
            # Risk analysis
            risk_agent = self.agents["risk"]
            risk_trends = await risk_agent.predict_risk_trends(organization_id)
            analysis_results["results"]["risk"] = risk_trends
            
            # Document analysis
            document_agent = self.agents["document"]
            # Get sample document for analysis
            sample_docs = self.vector_service.search_similar_documents(
                query="sample document",
                collection_type="documents",
                n_results=1,
                organization_id=organization_id
            )
            
            if sample_docs:
                doc_classification = await document_agent.classify_document(
                    sample_docs[0]["content"],
                    organization_id
                )
                analysis_results["results"]["document"] = doc_classification
            
            # Generate overall insights
            analysis_results["insights"] = await self._generate_insights(analysis_results["results"])
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error performing cross-domain analysis: {e}")
            raise
    
    async def _generate_insights(self, results: Dict[str, Any]) -> List[str]:
        """
        Generate insights from analysis results
        """
        insights = []
        
        # Compliance insights
        if "compliance" in results:
            compliance_data = results["compliance"]
            if compliance_data.get("total_gaps", 0) > 0:
                insights.append(f"Found {compliance_data['total_gaps']} compliance gaps requiring attention")
        
        # Risk insights
        if "risk" in results:
            risk_data = results["risk"]
            if "risk_trends" in risk_data:
                high_risk_types = [rt for rt, data in risk_data["risk_trends"].items() 
                                 if data.get("avg_impact", 0) > 3 or data.get("avg_probability", 0) > 3]
                if high_risk_types:
                    insights.append(f"High-risk areas identified: {', '.join(high_risk_types)}")
        
        # Document insights
        if "document" in results:
            doc_data = results["document"]
            if doc_data.get("confidence", 0) > 0.8:
                insights.append(f"Document classification confidence: {doc_data['confidence']:.2f}")
        
        return insights
    
    async def get_platform_status(self) -> Dict[str, Any]:
        """
        Get overall platform status including vector database stats
        """
        try:
            # Get vector database statistics
            vector_stats = self.vector_service.get_all_collections_stats()
            
            # Get agent status
            agent_status = {}
            for agent_id, agent in self.agents.items():
                agent_status[agent_id] = {
                    "status": self.agent_status.get(agent_id, "unknown"),
                    "type": getattr(agent, 'agent_type', 'unknown'),
                    "last_activity": datetime.now().isoformat()
                }
            
            return {
                "platform_status": "operational",
                "timestamp": datetime.now().isoformat(),
                "agents": agent_status,
                "vector_database": vector_stats,
                "total_documents": sum(stats["document_count"] for stats in vector_stats.values())
            }
            
        except Exception as e:
            logger.error(f"Error getting platform status: {e}")
            raise

# FastAPI App for Enhanced Agents
app = FastAPI(
    title="Enhanced GRC AI Agents",
    description="AI agents with vector database integration for GRC Platform",
    version="2.0.0"
)

# Global orchestrator instance
grc_orchestrator = GRCPlatformOrchestrator()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "enhanced-ai-agents"}

@app.get("/status")
async def get_platform_status():
    """Get platform status"""
    try:
        status = await grc_orchestrator.get_platform_status()
        return status
    except Exception as e:
        logger.error(f"Error getting platform status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get platform status")

@app.post("/analysis/cross-domain")
async def perform_cross_domain_analysis(request: Dict[str, Any]):
    """Perform cross-domain analysis"""
    try:
        organization_id = request.get("organization_id", "org-123")
        analysis_type = request.get("analysis_type", "comprehensive")
        
        results = await grc_orchestrator.perform_cross_domain_analysis(
            organization_id, analysis_type
        )
        
        return results
        
    except Exception as e:
        logger.error(f"Error performing cross-domain analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform analysis")

@app.post("/compliance/analyze-gaps")
async def analyze_compliance_gaps(request: Dict[str, Any]):
    """Analyze compliance gaps"""
    try:
        organization_id = request.get("organization_id", "org-123")
        framework = request.get("framework")
        
        compliance_agent = grc_orchestrator.agents["compliance"]
        results = await compliance_agent.analyze_compliance_gaps(organization_id, framework)
        
        return results
        
    except Exception as e:
        logger.error(f"Error analyzing compliance gaps: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze compliance gaps")

@app.post("/risk/identify-similar")
async def identify_similar_risks(request: Dict[str, Any]):
    """Identify similar risks"""
    try:
        organization_id = request.get("organization_id", "org-123")
        risk_description = request.get("risk_description", "")
        
        risk_agent = grc_orchestrator.agents["risk"]
        results = await risk_agent.identify_similar_risks(organization_id, risk_description)
        
        return results
        
    except Exception as e:
        logger.error(f"Error identifying similar risks: {e}")
        raise HTTPException(status_code=500, detail="Failed to identify similar risks")

@app.post("/document/classify")
async def classify_document(request: Dict[str, Any]):
    """Classify document"""
    try:
        organization_id = request.get("organization_id", "org-123")
        document_content = request.get("document_content", "")
        
        document_agent = grc_orchestrator.agents["document"]
        results = await document_agent.classify_document(document_content, organization_id)
        
        return results
        
    except Exception as e:
        logger.error(f"Error classifying document: {e}")
        raise HTTPException(status_code=500, detail="Failed to classify document")

@app.get("/vector-db/stats")
async def get_vector_database_stats():
    """Get vector database statistics"""
    try:
        stats = vector_service.get_all_collections_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting vector database stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get vector database stats")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
