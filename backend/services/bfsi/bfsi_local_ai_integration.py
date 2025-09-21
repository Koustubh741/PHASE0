#!/usr/bin/env python3
"""
BFSI Agent Integration with Local AI Services
Enhanced BFSI GRC Agent that uses local Ollama and Hugging Face services
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from local_ai_client import ai_client, ChatResponse, EmbeddingResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BFSITask:
    """BFSI task data structure"""
    task_id: str
    task_type: str
    priority: str
    data: Dict[str, Any]
    timestamp: datetime
    status: str = "pending"

@dataclass
class BFSIAnalysis:
    """BFSI analysis result"""
    analysis_id: str
    task_id: str
    task_type: str
    findings: List[str]
    risk_score: float
    compliance_score: float
    recommendations: List[str]
    ai_insights: str
    timestamp: datetime

class BFSILocalAIAgent:
    """
    Enhanced BFSI Agent with Local AI Integration
    Uses Ollama and Hugging Face services for intelligent BFSI operations
    """
    
    def __init__(self, agent_id: str = "bfsi-local-ai-agent"):
        self.agent_id = agent_id
        self.name = "BFSI Local AI Agent"
        self.status = "active"
        
        # BFSI-specific configurations
        self.bfsi_categories = {
            "compliance": ["SOX", "PCI DSS", "Basel III", "GDPR", "CCPA"],
            "risk": ["Credit Risk", "Market Risk", "Operational Risk", "Liquidity Risk"],
            "fraud": ["AML", "KYC", "Transaction Monitoring", "Identity Verification"],
            "regulatory": ["FDIC", "OCC", "FRB", "SEC", "FINRA"]
        }
        
        # AI service configurations
        self.ai_service_preferences = {
            "compliance_check": "ollama",  # Use Ollama for complex compliance analysis
            "risk_assessment": "ollama",   # Use Ollama for detailed risk analysis
            "document_analysis": "huggingface",  # Use HF for document processing
            "fraud_detection": "ollama",   # Use Ollama for fraud analysis
            "quick_query": "huggingface"   # Use HF for simple queries
        }
        
        # Task queue and results
        self.task_queue: List[BFSITask] = []
        self.analysis_results: List[BFSIAnalysis] = []
        
        logger.info(f"Initialized {self.name} with Local AI Integration")
    
    async def process_bfsi_request(self, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process BFSI requests using local AI services"""
        logger.info(f"Processing BFSI request: {request_type}")
        
        try:
            # Create task
            task = BFSITask(
                task_id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                task_type=request_type,
                priority=data.get("priority", "medium"),
                data=data,
                timestamp=datetime.now(),
                status="processing"
            )
            
            # Route to appropriate AI service
            ai_service = self.ai_service_preferences.get(request_type, "auto")
            
            # Generate AI analysis
            analysis = await self._generate_ai_analysis(task, ai_service)
            
            # Store results
            self.analysis_results.append(analysis)
            
            return {
                "task_id": task.task_id,
                "analysis_id": analysis.analysis_id,
                "findings": analysis.findings,
                "risk_score": analysis.risk_score,
                "compliance_score": analysis.compliance_score,
                "recommendations": analysis.recommendations,
                "ai_insights": analysis.ai_insights,
                "timestamp": analysis.timestamp.isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error processing BFSI request: {e}")
            return {
                "task_id": task.task_id if 'task' in locals() else "unknown",
                "error": str(e),
                "status": "failed"
            }
    
    async def _generate_ai_analysis(self, task: BFSITask, ai_service: str) -> BFSIAnalysis:
        """Generate AI analysis for BFSI task"""
        
        # Prepare context for AI
        context = self._prepare_bfsi_context(task)
        
        # Generate AI insights
        ai_response = ai_client.chat(context, service=ai_service)
        
        # Parse AI response and extract structured information
        findings = self._extract_findings(ai_response.response, task.task_type)
        risk_score = self._calculate_risk_score(ai_response.response, task.data)
        compliance_score = self._calculate_compliance_score(ai_response.response, task.data)
        recommendations = self._extract_recommendations(ai_response.response)
        
        return BFSIAnalysis(
            analysis_id=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            task_id=task.task_id,
            task_type=task.task_type,
            findings=findings,
            risk_score=risk_score,
            compliance_score=compliance_score,
            recommendations=recommendations,
            ai_insights=ai_response.response,
            timestamp=datetime.now()
        )
    
    def _prepare_bfsi_context(self, task: BFSITask) -> str:
        """Prepare BFSI-specific context for AI analysis"""
        
        context_prompts = {
            "compliance_check": f"""
            You are a BFSI compliance expert. Analyze the following compliance data:
            
            Task: {task.task_type}
            Data: {json.dumps(task.data, indent=2)}
            
            Please provide:
            1. Compliance assessment
            2. Regulatory requirements analysis
            3. Potential violations
            4. Recommendations for compliance
            """,
            
            "risk_assessment": f"""
            You are a BFSI risk management expert. Analyze the following risk data:
            
            Task: {task.task_type}
            Data: {json.dumps(task.data, indent=2)}
            
            Please provide:
            1. Risk identification and assessment
            2. Risk impact analysis
            3. Risk mitigation strategies
            4. Risk monitoring recommendations
            """,
            
            "fraud_detection": f"""
            You are a BFSI fraud detection expert. Analyze the following transaction data:
            
            Task: {task.task_type}
            Data: {json.dumps(task.data, indent=2)}
            
            Please provide:
            1. Fraud indicators analysis
            2. Suspicious activity patterns
            3. Investigation recommendations
            4. Prevention measures
            """,
            
            "document_analysis": f"""
            You are a BFSI document analyst. Analyze the following document:
            
            Task: {task.task_type}
            Data: {json.dumps(task.data, indent=2)}
            
            Please provide:
            1. Document classification
            2. Key information extraction
            3. Compliance requirements
            4. Action items
            """
        }
        
        return context_prompts.get(task.task_type, f"""
        You are a BFSI expert. Analyze the following:
        
        Task: {task.task_type}
        Data: {json.dumps(task.data, indent=2)}
        
        Please provide comprehensive analysis and recommendations.
        """)
    
    def _extract_findings(self, ai_response: str, task_type: str) -> List[str]:
        """Extract structured findings from AI response"""
        findings = []
        
        # Simple extraction based on common patterns
        lines = ai_response.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['finding', 'issue', 'concern', 'violation', 'risk']):
                if line and not line.startswith('#') and len(line) > 10:
                    findings.append(line)
        
        # If no specific findings, create general ones
        if not findings:
            findings = [
                f"AI analysis completed for {task_type}",
                "Review AI insights for detailed findings",
                "Consider implementing recommended actions"
            ]
        
        return findings[:5]  # Limit to 5 findings
    
    def _calculate_risk_score(self, ai_response: str, data: Dict[str, Any]) -> float:
        """Calculate risk score based on AI response and data"""
        risk_indicators = [
            'high risk', 'critical', 'urgent', 'severe', 'major',
            'violation', 'non-compliance', 'fraud', 'suspicious'
        ]
        
        low_risk_indicators = [
            'low risk', 'compliant', 'normal', 'acceptable', 'minor'
        ]
        
        response_lower = ai_response.lower()
        
        # Count risk indicators
        high_risk_count = sum(1 for indicator in risk_indicators if indicator in response_lower)
        low_risk_count = sum(1 for indicator in low_risk_indicators if indicator in response_lower)
        
        # Base score
        if high_risk_count > low_risk_count:
            base_score = 70 + min(high_risk_count * 5, 30)
        elif low_risk_count > high_risk_count:
            base_score = 20 + min(low_risk_count * 5, 30)
        else:
            base_score = 50
        
        # Adjust based on data characteristics
        if data.get('amount', 0) > 100000:  # High value transactions
            base_score += 10
        if data.get('priority') == 'high':
            base_score += 15
        
        return min(max(base_score, 0), 100)  # Clamp between 0-100
    
    def _calculate_compliance_score(self, ai_response: str, data: Dict[str, Any]) -> float:
        """Calculate compliance score based on AI response and data"""
        compliance_indicators = [
            'compliant', 'meets requirements', 'in compliance', 'satisfactory',
            'follows guidelines', 'proper documentation', 'approved'
        ]
        
        non_compliance_indicators = [
            'non-compliant', 'violation', 'breach', 'deficiency', 'gap',
            'missing documentation', 'inadequate', 'failed'
        ]
        
        response_lower = ai_response.lower()
        
        # Count compliance indicators
        compliant_count = sum(1 for indicator in compliance_indicators if indicator in response_lower)
        non_compliant_count = sum(1 for indicator in non_compliance_indicators if indicator in response_lower)
        
        # Calculate score
        if compliant_count > non_compliant_count:
            score = 80 + min(compliant_count * 3, 20)
        elif non_compliant_count > compliant_count:
            score = 30 - min(non_compliant_count * 5, 30)
        else:
            score = 60
        
        return min(max(score, 0), 100)  # Clamp between 0-100
    
    def _extract_recommendations(self, ai_response: str) -> List[str]:
        """Extract recommendations from AI response"""
        recommendations = []
        
        # Look for recommendation patterns
        lines = ai_response.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should', 'must', 'action']):
                if line and not line.startswith('#') and len(line) > 15:
                    recommendations.append(line)
        
        # If no specific recommendations, create general ones
        if not recommendations:
            recommendations = [
                "Review the analysis findings thoroughly",
                "Implement appropriate controls and monitoring",
                "Schedule follow-up assessment",
                "Update policies and procedures as needed"
            ]
        
        return recommendations[:4]  # Limit to 4 recommendations
    
    async def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of all analyses"""
        if not self.analysis_results:
            return {"message": "No analyses available"}
        
        total_analyses = len(self.analysis_results)
        avg_risk_score = sum(a.risk_score for a in self.analysis_results) / total_analyses
        avg_compliance_score = sum(a.compliance_score for a in self.analysis_results) / total_analyses
        
        return {
            "total_analyses": total_analyses,
            "average_risk_score": round(avg_risk_score, 2),
            "average_compliance_score": round(avg_compliance_score, 2),
            "recent_analyses": [
                {
                    "analysis_id": a.analysis_id,
                    "task_type": a.task_type,
                    "risk_score": a.risk_score,
                    "compliance_score": a.compliance_score,
                    "timestamp": a.timestamp.isoformat()
                }
                for a in self.analysis_results[-5:]  # Last 5 analyses
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of BFSI agent and AI services"""
        # Check AI services health
        ai_health = ai_client.health_check()
        
        return {
            "bfsi_agent": {
                "status": self.status,
                "agent_id": self.agent_id,
                "name": self.name,
                "tasks_processed": len(self.analysis_results),
                "timestamp": datetime.now().isoformat()
            },
            "ai_services": ai_health,
            "overall_health": "healthy" if all(ai_health.values()) else "degraded"
        }

# Global BFSI agent instance
bfsi_agent = BFSILocalAIAgent()

# Convenience functions for easy integration
async def process_bfsi_compliance_check(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process BFSI compliance check using local AI"""
    return await bfsi_agent.process_bfsi_request("compliance_check", data)

async def process_bfsi_risk_assessment(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process BFSI risk assessment using local AI"""
    return await bfsi_agent.process_bfsi_request("risk_assessment", data)

async def process_bfsi_fraud_detection(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process BFSI fraud detection using local AI"""
    return await bfsi_agent.process_bfsi_request("fraud_detection", data)

async def process_bfsi_document_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process BFSI document analysis using local AI"""
    return await bfsi_agent.process_bfsi_request("document_analysis", data)

# Example usage and testing
if __name__ == "__main__":
    async def test_bfsi_integration():
        """Test BFSI Local AI integration"""
        print("🚀 Testing BFSI Local AI Integration")
        print("=" * 50)
        
        # Test health check
        health = await bfsi_agent.health_check()
        print(f"Health Status: {health['overall_health']}")
        print(f"AI Services: {health['ai_services']}")
        
        # Test compliance check
        compliance_data = {
            "regulation": "SOX",
            "process": "Financial Reporting",
            "controls": ["Access Control", "Data Integrity", "Audit Trail"],
            "priority": "high"
        }
        
        print("\n📋 Testing Compliance Check...")
        result = await process_bfsi_compliance_check(compliance_data)
        print(f"Task ID: {result.get('task_id')}")
        print(f"Risk Score: {result.get('risk_score')}")
        print(f"Compliance Score: {result.get('compliance_score')}")
        print(f"Findings: {result.get('findings', [])[:2]}")
        
        # Test risk assessment
        risk_data = {
            "risk_type": "Credit Risk",
            "portfolio": "Corporate Loans",
            "exposure": 10000000,
            "probability": "medium"
        }
        
        print("\n⚠️ Testing Risk Assessment...")
        result = await process_bfsi_risk_assessment(risk_data)
        print(f"Task ID: {result.get('task_id')}")
        print(f"Risk Score: {result.get('risk_score')}")
        print(f"Recommendations: {result.get('recommendations', [])[:2]}")
        
        # Get summary
        summary = await bfsi_agent.get_analysis_summary()
        print(f"\n📊 Analysis Summary:")
        print(f"Total Analyses: {summary.get('total_analyses')}")
        print(f"Average Risk Score: {summary.get('average_risk_score')}")
        print(f"Average Compliance Score: {summary.get('average_compliance_score')}")
    
    # Run the test
    asyncio.run(test_bfsi_integration())



