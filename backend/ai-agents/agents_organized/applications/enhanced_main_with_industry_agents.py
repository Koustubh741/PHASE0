"""
Enhanced Main Application with Industry-Specific Multi-Agent Strategy
Integrates Ollama and Chroma with industry-specific agents
"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn
from datetime import datetime

# Import our enhanced components
from industry_orchestrator_manager import IndustryOrchestratorManager
from multi_agent_integration import IntegratedGRCPlatform
from advanced_mcp_protocol import AdvancedMCPBroker

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced GRC Platform with Industry Multi-Agent Strategy",
    description="Advanced GRC Platform with Ollama, Chroma, and Industry-Specific Multi-Agent Orchestration",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
industry_manager = IndustryOrchestratorManager()
integrated_platform = IntegratedGRCPlatform()
mcp_broker = AdvancedMCPBroker()

# Pydantic models for API
class IndustryAnalysisRequest(BaseModel):
    industry: str
    organization_id: str
    analysis_type: str = "comprehensive"
    include_cross_industry: bool = False

class CrossIndustryAnalysisRequest(BaseModel):
    organization_id: str
    industries: Optional[List[str]] = None
    analysis_type: str = "comprehensive"

class IndustryComparisonRequest(BaseModel):
    organization_id: str
    industries: List[str]
    comparison_type: str = "compliance"

class ComprehensiveReportRequest(BaseModel):
    organization_id: str
    include_all_industries: bool = True

@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup"""
    try:
        logger.info("Starting Enhanced GRC Platform with Industry Multi-Agent Strategy...")
        
        # Initialize MCP broker
        await mcp_broker.initialize()
        logger.info("MCP Broker initialized")
        
        # Initialize integrated platform
        await integrated_platform.initialize()
        logger.info("Integrated GRC Platform initialized")
        
        # Initialize industry manager
        await industry_manager.initialize()
        logger.info("Industry Orchestrator Manager initialized")
        
        logger.info("Enhanced GRC Platform started successfully!")
        
    except Exception as e:
        logger.error(f"Failed to start Enhanced GRC Platform: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        logger.info("Shutting down Enhanced GRC Platform...")
        
        await industry_manager.cleanup()
        await integrated_platform.cleanup()
        await mcp_broker.cleanup()
        
        logger.info("Enhanced GRC Platform shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Enhanced GRC Platform with Industry Multi-Agent Strategy",
        "version": "2.0.0",
        "features": [
            "Industry-Specific Multi-Agent Orchestration",
            "Ollama LLM Integration",
            "Chroma Vector Database",
            "Advanced MCP Protocol",
            "Cross-Industry Analysis",
            "Real-Time Collaboration",
            "Predictive Analytics"
        ],
        "supported_industries": ["bfsi", "telecom", "manufacturing", "healthcare"],
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "industry_manager": "running" if industry_manager.is_running else "stopped",
            "integrated_platform": "running" if integrated_platform.is_running else "stopped",
            "mcp_broker": "running" if mcp_broker.is_running else "stopped"
        }
    }

# Industry-specific analysis endpoints
@app.post("/api/industry/analysis")
async def execute_industry_analysis(request: IndustryAnalysisRequest):
    """Execute analysis for specific industry"""
    try:
        result = await industry_manager.execute_industry_analysis(
            industry=request.industry,
            organization_id=request.organization_id,
            analysis_type=request.analysis_type
        )
        
        return {
            "success": True,
            "industry": request.industry,
            "organization_id": request.organization_id,
            "analysis_type": request.analysis_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Industry analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/industry/cross-industry-analysis")
async def execute_cross_industry_analysis(request: CrossIndustryAnalysisRequest):
    """Execute cross-industry analysis"""
    try:
        result = await industry_manager.execute_cross_industry_analysis(
            organization_id=request.organization_id,
            industries=request.industries,
            analysis_type=request.analysis_type
        )
        
        return {
            "success": True,
            "organization_id": request.organization_id,
            "industries": request.industries or ["bfsi", "telecom", "manufacturing", "healthcare"],
            "analysis_type": request.analysis_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cross-industry analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/industry/comparison")
async def execute_industry_comparison(request: IndustryComparisonRequest):
    """Execute industry comparison analysis"""
    try:
        result = await industry_manager.execute_industry_comparison(
            organization_id=request.organization_id,
            industries=request.industries,
            comparison_type=request.comparison_type
        )
        
        return {
            "success": True,
            "organization_id": request.organization_id,
            "industries": request.industries,
            "comparison_type": request.comparison_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Industry comparison failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/industry/comprehensive-report")
async def get_comprehensive_industry_report(request: ComprehensiveReportRequest):
    """Get comprehensive report across all industries"""
    try:
        result = await industry_manager.get_comprehensive_industry_report(
            organization_id=request.organization_id
        )
        
        return {
            "success": True,
            "organization_id": request.organization_id,
            "report": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Comprehensive report generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Industry status endpoints
@app.get("/api/industry/status")
async def get_industry_status(industry: Optional[str] = None):
    """Get status of industry orchestrator(s)"""
    try:
        result = await industry_manager.get_industry_status(industry)
        
        return {
            "success": True,
            "industry": industry,
            "status": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get industry status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/industry/supported")
async def get_supported_industries():
    """Get list of supported industries"""
    return {
        "success": True,
        "supported_industries": industry_manager.supported_industries,
        "total_industries": len(industry_manager.supported_industries),
        "timestamp": datetime.now().isoformat()
    }

# Enhanced platform endpoints (from integrated platform)
@app.post("/api/platform/archer-superior-analysis")
async def execute_archer_superior_analysis(request: Dict[str, Any]):
    """Execute Archer-superior analysis using integrated platform"""
    try:
        organization_id = request.get("organization_id")
        analysis_type = request.get("analysis_type", "comprehensive")
        
        result = await integrated_platform.execute_archer_superior_analysis(
            organization_id=organization_id,
            analysis_type=analysis_type
        )
        
        return {
            "success": True,
            "organization_id": organization_id,
            "analysis_type": analysis_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Archer-superior analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/platform/real-time-collaboration")
async def demonstrate_real_time_collaboration(request: Dict[str, Any]):
    """Demonstrate real-time agent collaboration"""
    try:
        organization_id = request.get("organization_id")
        scenario = request.get("scenario", "compliance_incident")
        
        result = await integrated_platform.demonstrate_real_time_collaboration(
            organization_id=organization_id,
            scenario=scenario
        )
        
        return {
            "success": True,
            "organization_id": organization_id,
            "scenario": scenario,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Real-time collaboration demonstration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/platform/predictive-analytics")
async def showcase_predictive_analytics(request: Dict[str, Any]):
    """Showcase predictive analytics capabilities"""
    try:
        organization_id = request.get("organization_id")
        prediction_horizon = request.get("prediction_horizon", "6_months")
        
        result = await integrated_platform.showcase_predictive_analytics(
            organization_id=organization_id,
            prediction_horizon=prediction_horizon
        )
        
        return {
            "success": True,
            "organization_id": organization_id,
            "prediction_horizon": prediction_horizon,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Predictive analytics showcase failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/platform/comprehensive-demonstration")
async def get_comprehensive_demonstration(request: Dict[str, Any]):
    """Get comprehensive demonstration of all capabilities"""
    try:
        organization_id = request.get("organization_id")
        
        result = await integrated_platform.get_comprehensive_demonstration(
            organization_id=organization_id
        )
        
        return {
            "success": True,
            "organization_id": organization_id,
            "demonstration": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Comprehensive demonstration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP broker endpoints
@app.get("/api/mcp/status")
async def get_mcp_status():
    """Get MCP broker status"""
    try:
        analytics = await mcp_broker.get_system_analytics()
        
        return {
            "success": True,
            "mcp_status": analytics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get MCP status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Demo endpoints for testing
@app.post("/api/demo/bfsi-analysis")
async def demo_bfsi_analysis():
    """Demo BFSI industry analysis"""
    try:
        result = await industry_manager.execute_industry_analysis(
            industry="bfsi",
            organization_id="demo-bfsi-org",
            analysis_type="comprehensive"
        )
        
        return {
            "success": True,
            "demo_type": "bfsi_analysis",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"BFSI demo failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/demo/telecom-analysis")
async def demo_telecom_analysis():
    """Demo Telecom industry analysis"""
    try:
        result = await industry_manager.execute_industry_analysis(
            industry="telecom",
            organization_id="demo-telecom-org",
            analysis_type="comprehensive"
        )
        
        return {
            "success": True,
            "demo_type": "telecom_analysis",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Telecom demo failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/demo/manufacturing-analysis")
async def demo_manufacturing_analysis():
    """Demo Manufacturing industry analysis"""
    try:
        result = await industry_manager.execute_industry_analysis(
            industry="manufacturing",
            organization_id="demo-manufacturing-org",
            analysis_type="comprehensive"
        )
        
        return {
            "success": True,
            "demo_type": "manufacturing_analysis",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Manufacturing demo failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/demo/healthcare-analysis")
async def demo_healthcare_analysis():
    """Demo Healthcare industry analysis"""
    try:
        result = await industry_manager.execute_industry_analysis(
            industry="healthcare",
            organization_id="demo-healthcare-org",
            analysis_type="comprehensive"
        )
        
        return {
            "success": True,
            "demo_type": "healthcare_analysis",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Healthcare demo failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/demo/cross-industry-analysis")
async def demo_cross_industry_analysis():
    """Demo cross-industry analysis"""
    try:
        result = await industry_manager.execute_cross_industry_analysis(
            organization_id="demo-cross-industry-org",
            industries=["bfsi", "telecom", "manufacturing", "healthcare"],
            analysis_type="comprehensive"
        )
        
        return {
            "success": True,
            "demo_type": "cross_industry_analysis",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cross-industry demo failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the application
    uvicorn.run(
        "enhanced_main_with_industry_agents:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="info"
    )
