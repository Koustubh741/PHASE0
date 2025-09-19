"""
Industry Orchestrator Manager
Manages multiple industry-specific multi-agent orchestrators
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from industry_multi_agent_strategy import IndustryMultiAgentOrchestrator

logger = logging.getLogger(__name__)

class IndustryOrchestratorManager:
    """
    Manager for all industry-specific multi-agent orchestrators
    Provides unified interface for cross-industry operations
    """
    
    def __init__(self):
        self.industry_orchestrators = {}
        # Only BFSI industry supported - other industries commented out
        self.supported_industries = ["bfsi"]  # "telecom", "manufacturing", "healthcare"]
        self.is_running = False
        
    async def initialize(self):
        """Initialize all industry orchestrators"""
        try:
            logger.info("Initializing Industry Orchestrator Manager...")
            
            # Initialize each industry orchestrator
            for industry in self.supported_industries:
                logger.info(f"Initializing {industry} orchestrator...")
                orchestrator = IndustryMultiAgentOrchestrator(industry)
                await orchestrator.initialize()
                self.industry_orchestrators[industry] = orchestrator
                logger.info(f"{industry} orchestrator initialized successfully")
            
            self.is_running = True
            logger.info("All industry orchestrators initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize industry orchestrators: {e}")
            raise
    
    async def execute_industry_analysis(self, 
                                      industry: str,
                                      organization_id: str,
                                      analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Execute analysis for specific industry"""
        try:
            if industry not in self.industry_orchestrators:
                raise ValueError(f"Unsupported industry: {industry}")
            
            orchestrator = self.industry_orchestrators[industry]
            return await orchestrator.execute_industry_analysis(organization_id, analysis_type)
            
        except Exception as e:
            logger.error(f"Failed to execute {industry} analysis: {e}")
            raise
    
    async def execute_cross_industry_analysis(self, 
                                            organization_id: str,
                                            industries: List[str] = None,
                                            analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Execute BFSI analysis only - other industries disabled"""
        try:
            if industries is None:
                industries = self.supported_industries  # Only BFSI
            
            logger.info(f"Starting BFSI analysis (cross-industry disabled)")
            
            # Execute analysis for each industry in parallel
            tasks = []
            for industry in industries:
                if industry in self.industry_orchestrators:
                    task = asyncio.create_task(
                        self.execute_industry_analysis(industry, organization_id, analysis_type)
                    )
                    tasks.append((industry, task))
            
            # Wait for all analyses to complete
            results = {}
            for industry, task in tasks:
                try:
                    result = await task
                    results[industry] = result
                    logger.info(f"{industry} analysis completed successfully")
                except Exception as e:
                    logger.error(f"{industry} analysis failed: {e}")
                    results[industry] = {"error": str(e)}
            
            # Synthesize cross-industry results
            cross_industry_synthesis = await self._synthesize_cross_industry_results(results)
            
            return {
                "cross_industry_analysis": cross_industry_synthesis,
                "industry_results": results,
                "industries_analyzed": industries,
                "organization_id": organization_id,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to execute cross-industry analysis: {e}")
            raise
    
    async def _synthesize_cross_industry_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from multiple industries"""
        try:
            # Collect key metrics from each industry
            industry_metrics = {}
            overall_compliance_scores = []
            overall_risk_scores = []
            critical_issues = []
            recommendations = []
            
            for industry, result in results.items():
                if "error" not in result:
                    analysis_results = result.get("analysis_results", {})
                    
                    # Extract compliance status
                    compliance_status = analysis_results.get("compliance_status", "unknown")
                    if compliance_status == "compliant":
                        overall_compliance_scores.append(1.0)
                    elif compliance_status == "partially-compliant":
                        overall_compliance_scores.append(0.5)
                    else:
                        overall_compliance_scores.append(0.0)
                    
                    # Extract risk level
                    risk_level = analysis_results.get("risk_level", "medium")
                    risk_scores = {"low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0}
                    overall_risk_scores.append(risk_scores.get(risk_level, 0.5))
                    
                    # Collect critical issues
                    issues = analysis_results.get("critical_issues", [])
                    for issue in issues:
                        critical_issues.append(f"{industry}: {issue}")
                    
                    # Collect recommendations
                    recs = analysis_results.get("recommendations", [])
                    for rec in recs:
                        recommendations.append(f"{industry}: {rec}")
                    
                    industry_metrics[industry] = {
                        "compliance_status": compliance_status,
                        "risk_level": risk_level,
                        "confidence_score": analysis_results.get("confidence_score", 0.0),
                        "issues_count": len(issues),
                        "recommendations_count": len(recs)
                    }
            
            # Calculate overall scores
            overall_compliance_score = sum(overall_compliance_scores) / len(overall_compliance_scores) if overall_compliance_scores else 0.0
            overall_risk_score = sum(overall_risk_scores) / len(overall_risk_scores) if overall_risk_scores else 0.5
            
            # Determine overall status
            if overall_compliance_score >= 0.8:
                overall_status = "excellent"
            elif overall_compliance_score >= 0.6:
                overall_status = "good"
            elif overall_compliance_score >= 0.4:
                overall_status = "fair"
            else:
                overall_status = "poor"
            
            return {
                "overall_status": overall_status,
                "overall_compliance_score": overall_compliance_score,
                "overall_risk_score": overall_risk_score,
                "industry_metrics": industry_metrics,
                "critical_issues": critical_issues[:10],  # Top 10 issues
                "prioritized_recommendations": recommendations[:15],  # Top 15 recommendations
                "analysis_summary": {
                    "total_industries": len(results),
                    "successful_analyses": len([r for r in results.values() if "error" not in r]),
                    "failed_analyses": len([r for r in results.values() if "error" in r]),
                    "total_issues": len(critical_issues),
                    "total_recommendations": len(recommendations)
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to synthesize cross-industry results: {e}")
            return {
                "overall_status": "error",
                "overall_compliance_score": 0.0,
                "overall_risk_score": 1.0,
                "industry_metrics": {},
                "critical_issues": [f"Synthesis failed: {str(e)}"],
                "prioritized_recommendations": ["Manual review required"],
                "analysis_summary": {
                    "total_industries": len(results),
                    "successful_analyses": 0,
                    "failed_analyses": len(results),
                    "total_issues": 0,
                    "total_recommendations": 0
                }
            }
    
    async def get_industry_status(self, industry: str = None) -> Dict[str, Any]:
        """Get status of industry orchestrator(s)"""
        try:
            if industry:
                if industry not in self.industry_orchestrators:
                    return {"error": f"Industry {industry} not found"}
                
                orchestrator = self.industry_orchestrators[industry]
                return {
                    "industry": industry,
                    "status": "running" if orchestrator.is_running else "stopped",
                    "agents_count": len(orchestrator.agents),
                    "capabilities_count": len(orchestrator.agent_capabilities),
                    "ollama_model": orchestrator.industry_specific_models,
                    "chroma_collections": orchestrator.chroma_collections
                }
            else:
                # Return status for all industries
                status = {}
                for industry_name, orchestrator in self.industry_orchestrators.items():
                    status[industry_name] = {
                        "status": "running" if orchestrator.is_running else "stopped",
                        "agents_count": len(orchestrator.agents),
                        "capabilities_count": len(orchestrator.agent_capabilities),
                        "ollama_model": orchestrator.industry_specific_models,
                        "chroma_collections": orchestrator.chroma_collections
                    }
                
                return {
                    "all_industries": status,
                    "total_industries": len(self.industry_orchestrators),
                    "supported_industries": self.supported_industries
                }
                
        except Exception as e:
            logger.error(f"Failed to get industry status: {e}")
            return {"error": str(e)}
    
    async def execute_industry_comparison(self, 
                                        organization_id: str,
                                        industries: List[str],
                                        comparison_type: str = "compliance") -> Dict[str, Any]:
        """Execute BFSI analysis only - industry comparison disabled"""
        try:
            logger.info(f"Starting BFSI analysis (industry comparison disabled)")
            
            # Only execute BFSI analysis - other industries disabled
            industry_results = {}
            for industry in industries:
                if industry in self.industry_orchestrators and industry == "bfsi":
                    result = await self.execute_industry_analysis(industry, organization_id)
                    industry_results[industry] = result
            
            # Perform comparison analysis
            comparison_results = await self._perform_industry_comparison(
                industry_results, comparison_type
            )
            
            return {
                "comparison_type": comparison_type,
                "industries_compared": industries,
                "comparison_results": comparison_results,
                "industry_results": industry_results,
                "organization_id": organization_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to execute industry comparison: {e}")
            raise
    
    async def _perform_industry_comparison(self, 
                                         industry_results: Dict[str, Any], 
                                         comparison_type: str) -> Dict[str, Any]:
        """Perform detailed comparison analysis"""
        try:
            comparison_data = {}
            
            if comparison_type == "compliance":
                # Compare compliance scores
                compliance_scores = {}
                for industry, result in industry_results.items():
                    if "error" not in result:
                        analysis = result.get("analysis_results", {})
                        compliance_status = analysis.get("compliance_status", "unknown")
                        compliance_scores[industry] = compliance_status
                
                comparison_data = {
                    "compliance_comparison": compliance_scores,
                    "best_performing_industry": max(compliance_scores.keys(), 
                                                  key=lambda k: compliance_scores[k]) if compliance_scores else None,
                    "worst_performing_industry": min(compliance_scores.keys(), 
                                                   key=lambda k: compliance_scores[k]) if compliance_scores else None
                }
            
            elif comparison_type == "risk":
                # Compare risk levels
                risk_levels = {}
                for industry, result in industry_results.items():
                    if "error" not in result:
                        analysis = result.get("analysis_results", {})
                        risk_level = analysis.get("risk_level", "medium")
                        risk_levels[industry] = risk_level
                
                comparison_data = {
                    "risk_comparison": risk_levels,
                    "highest_risk_industry": max(risk_levels.keys(), 
                                               key=lambda k: risk_levels[k]) if risk_levels else None,
                    "lowest_risk_industry": min(risk_levels.keys(), 
                                              key=lambda k: risk_levels[k]) if risk_levels else None
                }
            
            elif comparison_type == "performance":
                # Compare performance metrics
                performance_metrics = {}
                for industry, result in industry_results.items():
                    if "error" not in result:
                        metrics = result.get("performance_metrics", {})
                        performance_metrics[industry] = {
                            "execution_time": metrics.get("execution_time", 0),
                            "agents_used": metrics.get("agents_used", 0),
                            "tasks_completed": metrics.get("tasks_completed", 0)
                        }
                
                comparison_data = {
                    "performance_comparison": performance_metrics,
                    "fastest_industry": min(performance_metrics.keys(), 
                                          key=lambda k: performance_metrics[k]["execution_time"]) if performance_metrics else None,
                    "most_comprehensive_industry": max(performance_metrics.keys(), 
                                                     key=lambda k: performance_metrics[k]["tasks_completed"]) if performance_metrics else None
                }
            
            return comparison_data
            
        except Exception as e:
            logger.error(f"Failed to perform industry comparison: {e}")
            return {"error": str(e)}
    
    async def get_comprehensive_industry_report(self, organization_id: str) -> Dict[str, Any]:
        """Get comprehensive BFSI report only - other industries disabled"""
        try:
            logger.info("Generating comprehensive BFSI report")
            
            # Execute BFSI analysis only
            cross_industry_results = await self.execute_cross_industry_analysis(organization_id)
            
            # Get BFSI status only
            industry_status = await self.get_industry_status()
            
            # Execute BFSI performance analysis only
            performance_comparison = await self.execute_industry_comparison(
                organization_id, 
                self.supported_industries,  # Only BFSI
                "performance"
            )
            
            return {
                "organization_id": organization_id,
                "report_type": "comprehensive_industry_report",
                "cross_industry_analysis": cross_industry_results,
                "industry_status": industry_status,
                "performance_comparison": performance_comparison,
                "report_summary": {
                    "total_industries_analyzed": len(self.supported_industries),  # Only BFSI
                    "analysis_timestamp": datetime.now().isoformat(),
                    "report_generated_by": "Industry Orchestrator Manager (BFSI Only)",
                    "technologies_used": ["Ollama LLM", "Chroma Vector DB", "Multi-Agent Strategy", "MCP Protocol", "BFSI GRC Framework"]
                },
                "recommendations": {
                    "priority_actions": cross_industry_results.get("cross_industry_analysis", {}).get("prioritized_recommendations", [])[:5],
                    "industry_focus": self._get_industry_focus_recommendations(cross_industry_results)
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate comprehensive industry report: {e}")
            raise
    
    def _get_industry_focus_recommendations(self, cross_industry_results: Dict[str, Any]) -> List[str]:
        """Get industry-specific focus recommendations"""
        try:
            industry_metrics = cross_industry_results.get("cross_industry_analysis", {}).get("industry_metrics", {})
            recommendations = []
            
            for industry, metrics in industry_metrics.items():
                compliance_status = metrics.get("compliance_status", "unknown")
                risk_level = metrics.get("risk_level", "medium")
                issues_count = metrics.get("issues_count", 0)
                
                if compliance_status in ["non-compliant", "partially-compliant"]:
                    recommendations.append(f"Focus on {industry} compliance improvement")
                
                if risk_level in ["high", "critical"]:
                    recommendations.append(f"Prioritize {industry} risk mitigation")
                
                if issues_count > 5:
                    recommendations.append(f"Address multiple issues in {industry} sector")
            
            return recommendations[:5]  # Top 5 recommendations
            
        except Exception as e:
            logger.error(f"Failed to get industry focus recommendations: {e}")
            return ["Manual review recommended for all industries"]
    
    async def cleanup(self):
        """Cleanup all industry orchestrators"""
        try:
            logger.info("Cleaning up industry orchestrators...")
            
            for industry, orchestrator in self.industry_orchestrators.items():
                try:
                    await orchestrator.cleanup()
                    logger.info(f"{industry} orchestrator cleaned up")
                except Exception as e:
                    logger.error(f"Failed to cleanup {industry} orchestrator: {e}")
            
            self.is_running = False
            logger.info("All industry orchestrators cleaned up")
            
        except Exception as e:
            logger.error(f"Failed to cleanup industry orchestrators: {e}")

# Global instance for easy access
industry_manager = IndustryOrchestratorManager()
