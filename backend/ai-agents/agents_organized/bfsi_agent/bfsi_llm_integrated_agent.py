"""
BFSI LLM Integrated Agent
========================

This module provides a BFSI agent that integrates with both Ollama and Hugging Face services
for comprehensive financial analysis, risk assessment, and compliance management.

Features:
- Integration with Ollama (llama2) for conversational AI
- Integration with Hugging Face (DialoGPT, embeddings) for advanced NLP
- Risk assessment and management
- Compliance analysis
- Portfolio analysis
- Strategic decision making
- Real-time LLM-powered insights
"""

import asyncio
import json
import logging
import httpx
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class BFSIAnalysisResult:
    """Result of BFSI analysis with LLM integration"""
    analysis_id: str
    analysis_type: str
    context: Dict[str, Any]
    llm_insights: Dict[str, Any]
    risk_score: float
    confidence_score: float
    recommendations: List[str]
    compliance_status: str
    timestamp: datetime
    duration: float

@dataclass
class LLMResponse:
    """Response from LLM services"""
    service: str  # 'ollama' or 'huggingface'
    model: str
    response: str
    confidence: float
    metadata: Dict[str, Any]

# =============================================================================
# MAIN BFSI LLM INTEGRATED AGENT CLASS
# =============================================================================

class BFSILLMIntegratedAgent:
    """
    BFSI Agent with full LLM integration
    
    This agent provides comprehensive BFSI functionality with real-time LLM integration
    for enhanced analysis, insights, and decision-making capabilities.
    """
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 huggingface_url: str = "http://localhost:8007"):
        """
        Initialize BFSI LLM Integrated Agent
        
        Args:
            ollama_url: URL for Ollama service
            huggingface_url: URL for Hugging Face service
        """
        self.agent_id = "bfsi-llm-integrated"
        self.name = "BFSI LLM Integrated Agent"
        self.ollama_url = ollama_url
        self.huggingface_url = huggingface_url
        self.analysis_history: List[BFSIAnalysisResult] = []
        
        # Initialize HTTP client
        self.client = httpx.AsyncClient(timeout=300.0)
        
        logger.info(f"🚀 Initialized {self.name}")
        logger.info(f"   Ollama URL: {ollama_url}")
        logger.info(f"   Hugging Face URL: {huggingface_url}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.client.aclose()
    
    # =============================================================================
    # LLM SERVICE INTEGRATION
    # =============================================================================
    
    async def query_ollama(self, prompt: str, model: str = "llama2") -> Optional[LLMResponse]:
        """
        Query Ollama service for LLM insights
        
        Args:
            prompt: The prompt to send to the model
            model: The model to use (default: llama2)
            
        Returns:
            LLMResponse with the model's response
        """
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            logger.info(f"🦙 Querying Ollama with model {model}")
            response = await self.client.post(
                f"{self.ollama_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return LLMResponse(
                    service="ollama",
                    model=model,
                    response=result.get("response", ""),
                    confidence=0.8,  # Ollama doesn't provide confidence scores
                    metadata={
                        "total_duration": result.get("total_duration", 0),
                        "load_duration": result.get("load_duration", 0),
                        "prompt_eval_count": result.get("prompt_eval_count", 0),
                        "eval_count": result.get("eval_count", 0)
                    }
                )
            else:
                logger.error(f"Ollama request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error querying Ollama: {e}")
            return None
    
    async def query_huggingface(self, text: str, task: str = "chat", model_id: str = None) -> Optional[LLMResponse]:
        """
        Query Hugging Face service for NLP tasks (Enhanced with multi-model support)
        
        Args:
            text: The input text
            task: The task type ('chat', 'embeddings', 'sentiment')
            model_id: Specific model to use (optional, auto-select if not provided)
            
        Returns:
            LLMResponse with the model's response
        """
        try:
            if task == "chat":
                payload = {
                    "message": text,
                    "max_length": 150,
                    "temperature": 0.7,
                    "auto_model_selection": True
                }
                
                # Use specific model if provided, otherwise auto-select
                if model_id:
                    payload["model_id"] = model_id
                    payload["auto_model_selection"] = False
                else:
                    # Try to get best model for the task
                    try:
                        rec_response = await self.client.post(
                            f"{self.huggingface_url}/models/recommend",
                            json={"task_description": text, "preferred_speed": "balanced"}
                        )
                        if rec_response.status_code == 200:
                            rec_data = rec_response.json()
                            payload["model_id"] = rec_data.get("primary_recommendation", {}).get("model_id", "tiny-llama")
                            payload["auto_model_selection"] = False
                    except:
                        pass  # Fallback to auto-selection
                        
                endpoint = "/chat"
            elif task == "embeddings":
                payload = {
                    "text": text,
                    "auto_model_selection": True
                }
                
                # Use specific model if provided
                if model_id:
                    payload["model_id"] = model_id
                    payload["auto_model_selection"] = False
                    
                endpoint = "/embeddings"
            else:
                logger.error(f"Unsupported task: {task}")
                return None
            
            logger.info(f"🤗 Querying Hugging Face for {task}")
            response = await self.client.post(
                f"{self.huggingface_url}{endpoint}",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if task == "chat":
                    return LLMResponse(
                        service="huggingface",
                        model=result.get("model_used", "unknown"),
                        response=result.get("response", ""),
                        confidence=result.get("confidence_score", 0.7),
                        metadata={
                            "processing_time": result.get("processing_time", 0),
                            "tokens_generated": result.get("tokens_generated", 0),
                            "model_info": result.get("model_info", {})
                        }
                    )
                elif task == "embeddings":
                    return LLMResponse(
                        service="huggingface",
                        model=result.get("model_used", "unknown"),
                        response=str(result.get("embedding", [])),
                        confidence=1.0,
                        metadata={
                            "embedding_dim": result.get("dimension", 0),
                            "processing_time": result.get("processing_time", 0),
                            "model_info": result.get("model_info", {})
                        }
                    )
            else:
                logger.error(f"Hugging Face request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error querying Hugging Face: {e}")
            return None
    
    # =============================================================================
    # BFSI ANALYSIS FUNCTIONS
    # =============================================================================
    
    async def analyze_risk(self, risk_context: Dict[str, Any]) -> BFSIAnalysisResult:
        """
        Perform comprehensive risk analysis with LLM insights
        
        Args:
            risk_context: Context containing risk data and parameters
            
        Returns:
            BFSIAnalysisResult with comprehensive risk analysis
        """
        start_time = datetime.now()
        analysis_id = f"risk-{int(start_time.timestamp())}"
        
        logger.info(f"🎯 Starting risk analysis: {analysis_id}")
        
        # Prepare risk analysis prompt for LLM
        risk_prompt = self._prepare_risk_prompt(risk_context)
        
        # Get insights from both LLM services
        ollama_response = await self.query_ollama(risk_prompt)
        hf_response = await self.query_huggingface(risk_prompt, "chat")
        
        # Calculate risk score based on context data
        risk_score = self._calculate_risk_score(risk_context)
        
        # Generate recommendations using LLM insights
        recommendations = await self._generate_risk_recommendations(
            risk_context, ollama_response, hf_response
        )
        
        # Compile LLM insights
        llm_insights = {
            "ollama_analysis": ollama_response.response if ollama_response else "Not available",
            "huggingface_analysis": hf_response.response if hf_response else "Not available",
            "combined_confidence": self._calculate_combined_confidence([ollama_response, hf_response])
        }
        
        # Create result
        result = BFSIAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="risk_assessment",
            context=risk_context,
            llm_insights=llm_insights,
            risk_score=risk_score,
            confidence_score=llm_insights["combined_confidence"],
            recommendations=recommendations,
            compliance_status="compliant" if risk_score < 0.7 else "needs_attention",
            timestamp=start_time,
            duration=(datetime.now() - start_time).total_seconds()
        )
        
        # Store result
        self.analysis_history.append(result)
        
        logger.info(f"✅ Risk analysis completed: {analysis_id}")
        logger.info(f"   Risk Score: {risk_score:.2f}")
        logger.info(f"   Confidence: {result.confidence_score:.2f}")
        logger.info(f"   Recommendations: {len(recommendations)}")
        
        return result
    
    async def analyze_compliance(self, compliance_context: Dict[str, Any]) -> BFSIAnalysisResult:
        """
        Perform comprehensive compliance analysis with LLM insights
        
        Args:
            compliance_context: Context containing compliance data and requirements
            
        Returns:
            BFSIAnalysisResult with comprehensive compliance analysis
        """
        start_time = datetime.now()
        analysis_id = f"compliance-{int(start_time.timestamp())}"
        
        logger.info(f"📋 Starting compliance analysis: {analysis_id}")
        
        # Prepare compliance analysis prompt for LLM
        compliance_prompt = self._prepare_compliance_prompt(compliance_context)
        
        # Get insights from both LLM services
        ollama_response = await self.query_ollama(compliance_prompt)
        hf_response = await self.query_huggingface(compliance_prompt, "chat")
        
        # Calculate compliance score based on context data
        compliance_score = self._calculate_compliance_score(compliance_context)
        
        # Generate recommendations using LLM insights
        recommendations = await self._generate_compliance_recommendations(
            compliance_context, ollama_response, hf_response
        )
        
        # Compile LLM insights
        llm_insights = {
            "ollama_analysis": ollama_response.response if ollama_response else "Not available",
            "huggingface_analysis": hf_response.response if hf_response else "Not available",
            "combined_confidence": self._calculate_combined_confidence([ollama_response, hf_response])
        }
        
        # Create result
        result = BFSIAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="compliance_assessment",
            context=compliance_context,
            llm_insights=llm_insights,
            risk_score=1.0 - compliance_score,  # Inverse relationship
            confidence_score=llm_insights["combined_confidence"],
            recommendations=recommendations,
            compliance_status="compliant" if compliance_score > 0.8 else "non_compliant",
            timestamp=start_time,
            duration=(datetime.now() - start_time).total_seconds()
        )
        
        # Store result
        self.analysis_history.append(result)
        
        logger.info(f"✅ Compliance analysis completed: {analysis_id}")
        logger.info(f"   Compliance Score: {compliance_score:.2f}")
        logger.info(f"   Status: {result.compliance_status}")
        logger.info(f"   Recommendations: {len(recommendations)}")
        
        return result
    
    async def analyze_portfolio(self, portfolio_context: Dict[str, Any]) -> BFSIAnalysisResult:
        """
        Perform comprehensive portfolio analysis with LLM insights
        
        Args:
            portfolio_context: Context containing portfolio data and parameters
            
        Returns:
            BFSIAnalysisResult with comprehensive portfolio analysis
        """
        start_time = datetime.now()
        analysis_id = f"portfolio-{int(start_time.timestamp())}"
        
        logger.info(f"📊 Starting portfolio analysis: {analysis_id}")
        
        # Prepare portfolio analysis prompt for LLM
        portfolio_prompt = self._prepare_portfolio_prompt(portfolio_context)
        
        # Get insights from both LLM services
        ollama_response = await self.query_ollama(portfolio_prompt)
        hf_response = await self.query_huggingface(portfolio_prompt, "chat")
        
        # Calculate portfolio risk score
        portfolio_risk = self._calculate_portfolio_risk(portfolio_context)
        
        # Generate recommendations using LLM insights
        recommendations = await self._generate_portfolio_recommendations(
            portfolio_context, ollama_response, hf_response
        )
        
        # Compile LLM insights
        llm_insights = {
            "ollama_analysis": ollama_response.response if ollama_response else "Not available",
            "huggingface_analysis": hf_response.response if hf_response else "Not available",
            "combined_confidence": self._calculate_combined_confidence([ollama_response, hf_response])
        }
        
        # Create result
        result = BFSIAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="portfolio_analysis",
            context=portfolio_context,
            llm_insights=llm_insights,
            risk_score=portfolio_risk,
            confidence_score=llm_insights["combined_confidence"],
            recommendations=recommendations,
            compliance_status="compliant" if portfolio_risk < 0.6 else "needs_review",
            timestamp=start_time,
            duration=(datetime.now() - start_time).total_seconds()
        )
        
        # Store result
        self.analysis_history.append(result)
        
        logger.info(f"✅ Portfolio analysis completed: {analysis_id}")
        logger.info(f"   Portfolio Risk: {portfolio_risk:.2f}")
        logger.info(f"   Confidence: {result.confidence_score:.2f}")
        logger.info(f"   Recommendations: {len(recommendations)}")
        
        return result
    
    async def strategic_decision_analysis(self, decision_context: Dict[str, Any]) -> BFSIAnalysisResult:
        """
        Perform strategic decision analysis with LLM insights
        
        Args:
            decision_context: Context containing decision alternatives and criteria
            
        Returns:
            BFSIAnalysisResult with comprehensive decision analysis
        """
        start_time = datetime.now()
        analysis_id = f"decision-{int(start_time.timestamp())}"
        
        logger.info(f"🎯 Starting strategic decision analysis: {analysis_id}")
        
        # Prepare decision analysis prompt for LLM
        decision_prompt = self._prepare_decision_prompt(decision_context)
        
        # Get insights from both LLM services
        ollama_response = await self.query_ollama(decision_prompt)
        hf_response = await self.query_huggingface(decision_prompt, "chat")
        
        # Calculate decision confidence
        decision_confidence = self._calculate_decision_confidence(decision_context)
        
        # Generate recommendations using LLM insights
        recommendations = await self._generate_decision_recommendations(
            decision_context, ollama_response, hf_response
        )
        
        # Compile LLM insights
        llm_insights = {
            "ollama_analysis": ollama_response.response if ollama_response else "Not available",
            "huggingface_analysis": hf_response.response if hf_response else "Not available",
            "combined_confidence": self._calculate_combined_confidence([ollama_response, hf_response]),
            "recommended_alternative": self._select_best_alternative(decision_context, ollama_response, hf_response)
        }
        
        # Create result
        result = BFSIAnalysisResult(
            analysis_id=analysis_id,
            analysis_type="strategic_decision",
            context=decision_context,
            llm_insights=llm_insights,
            risk_score=1.0 - decision_confidence,
            confidence_score=llm_insights["combined_confidence"],
            recommendations=recommendations,
            compliance_status="approved" if decision_confidence > 0.7 else "requires_review",
            timestamp=start_time,
            duration=(datetime.now() - start_time).total_seconds()
        )
        
        # Store result
        self.analysis_history.append(result)
        
        logger.info(f"✅ Strategic decision analysis completed: {analysis_id}")
        logger.info(f"   Decision Confidence: {decision_confidence:.2f}")
        logger.info(f"   Recommended Alternative: {llm_insights['recommended_alternative']}")
        logger.info(f"   Recommendations: {len(recommendations)}")
        
        return result
    
    # =============================================================================
    # PROMPT PREPARATION METHODS
    # =============================================================================
    
    def _prepare_risk_prompt(self, risk_context: Dict[str, Any]) -> str:
        """Prepare prompt for risk analysis"""
        return f"""
As a BFSI risk analyst, analyze the following risk scenario:

Risk Type: {risk_context.get('risk_type', 'Unknown')}
Portfolio Data: {json.dumps(risk_context.get('portfolio_data', {}), indent=2)}
Stress Scenarios: {risk_context.get('stress_scenarios', [])}

Please provide:
1. Risk assessment summary
2. Key risk factors identified
3. Potential impact analysis
4. Mitigation strategies
5. Regulatory considerations

Keep the analysis professional and focused on actionable insights.
"""
    
    def _prepare_compliance_prompt(self, compliance_context: Dict[str, Any]) -> str:
        """Prepare prompt for compliance analysis"""
        return f"""
As a BFSI compliance officer, analyze the following compliance scenario:

Framework: {compliance_context.get('framework', 'Unknown')}
Compliance Data: {json.dumps(compliance_context.get('compliance_data', {}), indent=2)}
Regulatory Changes: {compliance_context.get('regulatory_changes', [])}

Please provide:
1. Compliance status assessment
2. Gaps identified
3. Regulatory requirements analysis
4. Remediation recommendations
5. Timeline considerations

Keep the analysis focused on regulatory compliance and risk mitigation.
"""
    
    def _prepare_portfolio_prompt(self, portfolio_context: Dict[str, Any]) -> str:
        """Prepare prompt for portfolio analysis"""
        return f"""
As a BFSI portfolio manager, analyze the following portfolio:

Portfolio Data: {json.dumps(portfolio_context.get('portfolio_data', {}), indent=2)}
Risk Tolerance: {portfolio_context.get('risk_tolerance', 'Unknown')}
Investment Horizon: {portfolio_context.get('investment_horizon', 'Unknown')}

Please provide:
1. Portfolio performance assessment
2. Risk-return analysis
3. Diversification evaluation
4. Optimization recommendations
5. Market outlook considerations

Keep the analysis focused on investment strategy and risk management.
"""
    
    def _prepare_decision_prompt(self, decision_context: Dict[str, Any]) -> str:
        """Prepare prompt for decision analysis"""
        alternatives = decision_context.get('alternatives', [])
        alt_summary = "\n".join([f"- {alt.get('name', 'Unknown')}: {alt.get('description', 'No description')}" 
                                for alt in alternatives])
        
        return f"""
As a BFSI strategic advisor, analyze the following decision scenario:

Decision Type: {decision_context.get('decision_type', 'Unknown')}
Description: {decision_context.get('description', 'No description')}

Alternatives:
{alt_summary}

Constraints: {decision_context.get('constraints', [])}
Stakeholders: {decision_context.get('stakeholders', [])}

Please provide:
1. Alternative evaluation
2. Risk-benefit analysis
3. Strategic alignment assessment
4. Implementation considerations
5. Recommendation with rationale

Keep the analysis focused on strategic value and implementation feasibility.
"""
    
    # =============================================================================
    # CALCULATION METHODS
    # =============================================================================
    
    def _calculate_risk_score(self, risk_context: Dict[str, Any]) -> float:
        """Calculate risk score based on context data"""
        portfolio_data = risk_context.get('portfolio_data', {})
        
        # Basic risk calculation based on available data
        default_rate = portfolio_data.get('default_rate', 0.02)
        recovery_rate = portfolio_data.get('recovery_rate', 0.4)
        credit_score = portfolio_data.get('average_credit_score', 720)
        
        # Normalize credit score (300-850 range)
        normalized_credit = (credit_score - 300) / 550
        
        # Calculate risk score (0-1, higher is riskier)
        risk_score = (default_rate * (1 - recovery_rate)) + (1 - normalized_credit) * 0.3
        
        return min(max(risk_score, 0.0), 1.0)
    
    def _calculate_compliance_score(self, compliance_context: Dict[str, Any]) -> float:
        """Calculate compliance score based on context data"""
        compliance_data = compliance_context.get('compliance_data', {})
        
        scores = []
        
        # Basel III compliance
        basel_data = compliance_data.get('basel_capital_adequacy', {})
        if basel_data:
            tier1_ratio = basel_data.get('tier_1_ratio', 0)
            total_capital_ratio = basel_data.get('total_capital_ratio', 0)
            # Basel III minimum requirements
            scores.append(1.0 if tier1_ratio >= 8.5 else tier1_ratio / 8.5)
            scores.append(1.0 if total_capital_ratio >= 10.5 else total_capital_ratio / 10.5)
        
        # SOX compliance
        sox_data = compliance_data.get('sox_internal_controls', {})
        if sox_data:
            effectiveness = sox_data.get('effectiveness', 0.8)
            scores.append(effectiveness)
        
        # PCI compliance
        pci_data = compliance_data.get('pci_data_protection', {})
        if pci_data:
            pci_score = sum([1.0 if v else 0.0 for v in pci_data.values()]) / len(pci_data) if pci_data else 0.8
            scores.append(pci_score)
        
        # AML compliance
        aml_data = compliance_data.get('aml_transaction_monitoring', {})
        if aml_data:
            alerts_resolved = aml_data.get('alerts_resolved', 95)
            alerts_total = aml_data.get('alerts_total', 100)
            aml_score = alerts_resolved / alerts_total if alerts_total > 0 else 0.95
            scores.append(aml_score)
        
        # Return average score or default
        return sum(scores) / len(scores) if scores else 0.8
    
    def _calculate_portfolio_risk(self, portfolio_context: Dict[str, Any]) -> float:
        """Calculate portfolio risk based on context data"""
        portfolio_data = portfolio_context.get('portfolio_data', {})
        
        if not portfolio_data:
            return 0.5  # Default moderate risk
        
        # Calculate weighted risk based on portfolio composition
        total_risk = 0.0
        total_weight = 0.0
        
        for asset_class, data in portfolio_data.items():
            if isinstance(data, dict) and 'weight' in data and 'risk_score' in data:
                weight = data['weight']
                risk_score = data['risk_score']
                total_risk += weight * risk_score
                total_weight += weight
        
        # Normalize risk score
        portfolio_risk = total_risk / total_weight if total_weight > 0 else 0.5
        
        return min(max(portfolio_risk, 0.0), 1.0)
    
    def _calculate_decision_confidence(self, decision_context: Dict[str, Any]) -> float:
        """Calculate decision confidence based on alternatives"""
        alternatives = decision_context.get('alternatives', [])
        
        if not alternatives:
            return 0.5  # Default moderate confidence
        
        # Calculate average success probability
        success_probs = []
        for alt in alternatives:
            if isinstance(alt, dict) and 'success_probability' in alt:
                success_probs.append(alt['success_probability'])
        
        return sum(success_probs) / len(success_probs) if success_probs else 0.5
    
    def _calculate_combined_confidence(self, llm_responses: List[Optional[LLMResponse]]) -> float:
        """Calculate combined confidence from multiple LLM responses"""
        valid_responses = [r for r in llm_responses if r is not None]
        
        if not valid_responses:
            return 0.5  # Default confidence
        
        confidences = [r.confidence for r in valid_responses]
        return sum(confidences) / len(confidences)
    
    # =============================================================================
    # RECOMMENDATION GENERATION METHODS
    # =============================================================================
    
    async def _generate_risk_recommendations(self, risk_context: Dict[str, Any], 
                                           ollama_response: Optional[LLMResponse],
                                           hf_response: Optional[LLMResponse]) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []
        
        # Base recommendations
        risk_score = self._calculate_risk_score(risk_context)
        
        if risk_score > 0.7:
            recommendations.extend([
                "Implement immediate risk mitigation measures",
                "Review and strengthen credit policies",
                "Increase monitoring frequency for high-risk exposures"
            ])
        elif risk_score > 0.4:
            recommendations.extend([
                "Monitor risk metrics closely",
                "Consider diversification strategies",
                "Review risk appetite and limits"
            ])
        else:
            recommendations.extend([
                "Maintain current risk management practices",
                "Continue regular monitoring",
                "Consider opportunities for controlled growth"
            ])
        
        # Add LLM-derived recommendations
        if ollama_response and "recommend" in ollama_response.response.lower():
            recommendations.append("LLM Analysis: " + ollama_response.response.split("recommend")[1][:100] + "...")
        
        if hf_response and "suggest" in hf_response.response.lower():
            recommendations.append("AI Insight: " + hf_response.response.split("suggest")[1][:100] + "...")
        
        return recommendations
    
    async def _generate_compliance_recommendations(self, compliance_context: Dict[str, Any],
                                                 ollama_response: Optional[LLMResponse],
                                                 hf_response: Optional[LLMResponse]) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        # Base recommendations
        compliance_score = self._calculate_compliance_score(compliance_context)
        
        if compliance_score < 0.8:
            recommendations.extend([
                "Address compliance gaps immediately",
                "Conduct comprehensive compliance review",
                "Implement additional controls and monitoring"
            ])
        elif compliance_score < 0.9:
            recommendations.extend([
                "Strengthen compliance framework",
                "Enhance monitoring and reporting",
                "Provide additional staff training"
            ])
        else:
            recommendations.extend([
                "Maintain current compliance standards",
                "Continue regular compliance monitoring",
                "Stay updated on regulatory changes"
            ])
        
        # Add regulatory change recommendations
        reg_changes = compliance_context.get('regulatory_changes', [])
        if reg_changes:
            recommendations.append(f"Prepare for upcoming regulatory changes: {', '.join(reg_changes)}")
        
        return recommendations
    
    async def _generate_portfolio_recommendations(self, portfolio_context: Dict[str, Any],
                                                ollama_response: Optional[LLMResponse],
                                                hf_response: Optional[LLMResponse]) -> List[str]:
        """Generate portfolio optimization recommendations"""
        recommendations = []
        
        # Base recommendations
        portfolio_risk = self._calculate_portfolio_risk(portfolio_context)
        risk_tolerance = portfolio_context.get('risk_tolerance', 'moderate')
        
        if portfolio_risk > 0.7 and risk_tolerance in ['conservative', 'moderate']:
            recommendations.extend([
                "Consider reducing high-risk investments",
                "Increase allocation to fixed-income securities",
                "Implement risk management strategies"
            ])
        elif portfolio_risk < 0.3 and risk_tolerance == 'aggressive':
            recommendations.extend([
                "Consider increasing growth investments",
                "Evaluate opportunities in emerging markets",
                "Review asset allocation for optimization"
            ])
        else:
            recommendations.extend([
                "Maintain current portfolio balance",
                "Regular rebalancing as needed",
                "Monitor market conditions for opportunities"
            ])
        
        # Add diversification recommendations
        portfolio_data = portfolio_context.get('portfolio_data', {})
        if len(portfolio_data) < 4:
            recommendations.append("Consider additional diversification across asset classes")
        
        return recommendations
    
    async def _generate_decision_recommendations(self, decision_context: Dict[str, Any],
                                               ollama_response: Optional[LLMResponse],
                                               hf_response: Optional[LLMResponse]) -> List[str]:
        """Generate strategic decision recommendations"""
        recommendations = []
        
        # Base recommendations
        alternatives = decision_context.get('alternatives', [])
        constraints = decision_context.get('constraints', [])
        
        if alternatives:
            # Find best alternative based on success probability
            best_alt = max(alternatives, key=lambda x: x.get('success_probability', 0))
            recommendations.append(f"Recommended alternative: {best_alt.get('name', 'Unknown')}")
        
        if constraints:
            recommendations.append("Ensure all constraints are addressed in implementation")
        
        # Add stakeholder consideration
        stakeholders = decision_context.get('stakeholders', [])
        if stakeholders:
            recommendations.append("Engage all stakeholders in decision implementation")
        
        # General strategic recommendations
        recommendations.extend([
            "Develop detailed implementation plan",
            "Establish success metrics and monitoring",
            "Prepare contingency plans for risks"
        ])
        
        return recommendations
    
    def _select_best_alternative(self, decision_context: Dict[str, Any],
                               ollama_response: Optional[LLMResponse],
                               hf_response: Optional[LLMResponse]) -> str:
        """Select the best alternative based on analysis"""
        alternatives = decision_context.get('alternatives', [])
        
        if not alternatives:
            return "No alternatives provided"
        
        # Simple selection based on success probability and implementation feasibility
        best_alt = max(alternatives, key=lambda x: (
            x.get('success_probability', 0) * 0.6 + 
            x.get('performance_scores', {}).get('implementation_feasibility', 0) * 0.4
        ))
        
        return best_alt.get('name', 'Unknown Alternative')
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        # Test LLM service connectivity
        ollama_status = await self._test_ollama_connection()
        hf_status = await self._test_huggingface_connection()
        
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "active",
            "llm_services": {
                "ollama": {
                    "url": self.ollama_url,
                    "status": "connected" if ollama_status else "disconnected",
                    "models": ["llama2"] if ollama_status else []
                },
                "huggingface": {
                    "url": self.huggingface_url,
                    "status": "connected" if hf_status else "disconnected",
                    "models": ["tiny-llama", "phi-2", "gemma-2b", "llama2-7b", "mistral-7b", "codellama-7b", "all-minilm", "all-mpnet"] if hf_status else []
                }
            },
            "capabilities": [
                "risk_assessment",
                "compliance_analysis", 
                "portfolio_analysis",
                "strategic_decision_making",
                "llm_integration"
            ],
            "analysis_history_count": len(self.analysis_history),
            "last_analysis": self.analysis_history[-1].timestamp.isoformat() if self.analysis_history else None
        }
    
    async def _test_ollama_connection(self) -> bool:
        """Test Ollama service connection"""
        try:
            response = await self.client.get(f"{self.ollama_url}/api/tags", timeout=5.0)
            return response.status_code == 200
        except:
            return False
    
    async def _test_huggingface_connection(self) -> bool:
        """Test Hugging Face service connection"""
        try:
            response = await self.client.get(f"{self.huggingface_url}/health", timeout=5.0)
            return response.status_code == 200
        except:
            return False
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get analysis history"""
        return [asdict(analysis) for analysis in self.analysis_history]
    
    def get_latest_analysis(self) -> Optional[Dict[str, Any]]:
        """Get the latest analysis result"""
        if self.analysis_history:
            return asdict(self.analysis_history[-1])
        return None

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def create_bfsi_agent() -> BFSILLMIntegratedAgent:
    """Create and initialize BFSI LLM Integrated Agent"""
    return BFSILLMIntegratedAgent()

async def quick_risk_analysis(risk_data: Dict[str, Any]) -> Dict[str, Any]:
    """Quick risk analysis with default settings"""
    async with BFSILLMIntegratedAgent() as agent:
        result = await agent.analyze_risk(risk_data)
        return asdict(result)

async def quick_compliance_check(compliance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Quick compliance check with default settings"""
    async with BFSILLMIntegratedAgent() as agent:
        result = await agent.analyze_compliance(compliance_data)
        return asdict(result)

async def quick_portfolio_analysis(portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
    """Quick portfolio analysis with default settings"""
    async with BFSILLMIntegratedAgent() as agent:
        result = await agent.analyze_portfolio(portfolio_data)
        return asdict(result)

async def quick_decision_analysis(decision_data: Dict[str, Any]) -> Dict[str, Any]:
    """Quick decision analysis with default settings"""
    async with BFSILLMIntegratedAgent() as agent:
        result = await agent.strategic_decision_analysis(decision_data)
        return asdict(result)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    async def main():
        """Main execution for testing"""
        async with BFSILLMIntegratedAgent() as agent:
            # Test agent status
            status = await agent.get_agent_status()
            print("🚀 BFSI LLM Integrated Agent Status:")
            print(json.dumps(status, indent=2, default=str))
            
            # Test risk analysis
            risk_context = {
                "risk_type": "credit_risk",
                "portfolio_data": {
                    "total_exposure": 1000000000,
                    "number_of_borrowers": 1000,
                    "average_credit_score": 720,
                    "default_rate": 0.02,
                    "recovery_rate": 0.4
                }
            }
            
            print("\n📈 Testing Risk Analysis...")
            risk_result = await agent.analyze_risk(risk_context)
            print(f"Risk Score: {risk_result.risk_score:.2f}")
            print(f"Confidence: {risk_result.confidence_score:.2f}")
            print(f"Recommendations: {len(risk_result.recommendations)}")
    
    asyncio.run(main())
