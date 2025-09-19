"""
Enhanced Main Application with Optimization
Complete integration of Ollama and Chroma optimization with existing agents
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import optimization components
from agent_integration_layer import integration_manager
from ollama_enhanced_agents import create_ollama_enhanced_agent
from chroma_enhanced_agents import create_chroma_enhanced_agent
from migration_strategy import migration_strategy
from backward_compatibility_layer import compatibility_layer
from performance_monitoring import performance_monitor

# Import existing components
from industry_multi_agent_strategy import IndustryMultiAgentOrchestrator
from industry_orchestrator_manager import industry_manager

logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Enhanced GRC Platform with Ollama & Chroma Optimization",
    description="Optimized GRC Platform with multi-agent strategy, Ollama LLM, and Chroma vector database",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class OptimizationRequest(BaseModel):
    agent_type: str
    optimization_type: str = "full"  # full, ollama_only, chroma_only

class MigrationRequest(BaseModel):
    agent_types: List[str]
    migration_phase: str = "preparation"

class PerformanceTestRequest(BaseModel):
    agent_type: str
    duration: int = 300  # 5 minutes
    test_cases: List[Dict[str, Any]] = []

class LegacyAPIRequest(BaseModel):
    endpoint: str
    request_data: Dict[str, Any]

# Global optimization state
optimization_state = {
    "is_initialized": False,
    "optimized_agents": {},
    "migration_status": {},
    "performance_tests": {}
}

@app.on_event("startup")
async def startup_event():
    """Initialize all optimization components"""
    try:
        logger.info("Starting Enhanced GRC Platform with Optimization...")
        
        # Initialize integration manager
        await integration_manager.initialize()
        logger.info("Integration Manager initialized")
        
        # Initialize migration strategy
        await migration_strategy.initialize()
        logger.info("Migration Strategy initialized")
        
        # Initialize backward compatibility layer
        await compatibility_layer.initialize()
        logger.info("Backward Compatibility Layer initialized")
        
        # Initialize performance monitor
        await performance_monitor.initialize()
        logger.info("Performance Monitor initialized")
        
        # Initialize industry manager
        await industry_manager.initialize()
        logger.info("Industry Manager initialized")
        
        optimization_state["is_initialized"] = True
        logger.info("Enhanced GRC Platform with Optimization started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start Enhanced GRC Platform: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup all optimization components"""
    try:
        logger.info("Shutting down Enhanced GRC Platform...")
        
        # Cleanup components
        await integration_manager.cleanup()
        await migration_strategy.cleanup()
        await compatibility_layer.cleanup()
        await performance_monitor.cleanup()
        await industry_manager.cleanup()
        
        optimization_state["is_initialized"] = False
        logger.info("Enhanced GRC Platform shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "optimization_initialized": optimization_state["is_initialized"],
        "timestamp": datetime.now().isoformat()
    }

# Optimization endpoints
@app.post("/api/optimization/optimize-agent")
async def optimize_agent(request: OptimizationRequest, background_tasks: BackgroundTasks):
    """Optimize agent with Ollama and Chroma"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Optimization system not initialized")
        
        logger.info(f"Optimizing {request.agent_type} agent with {request.optimization_type}")
        
        # Start optimization in background
        background_tasks.add_task(
            _run_optimization,
            request.agent_type,
            request.optimization_type
        )
        
        return {
            "message": f"Optimization started for {request.agent_type}",
            "optimization_type": request.optimization_type,
            "status": "started",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimization/optimize-all")
async def optimize_all_agents(background_tasks: BackgroundTasks):
    """Optimize all agents with Ollama and Chroma"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Optimization system not initialized")
        
        logger.info("Starting optimization of all agents")
        
        # Start optimization in background
        background_tasks.add_task(_run_optimize_all)
        
        return {
            "message": "Optimization started for all agents",
            "status": "started",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start optimization of all agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimization/status")
async def get_optimization_status():
    """Get optimization status"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Optimization system not initialized")
        
        # Get integration manager status
        integration_status = await integration_manager.get_migration_status()
        
        return {
            "optimization_status": integration_status,
            "optimized_agents": optimization_state["optimized_agents"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get optimization status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Migration endpoints
@app.post("/api/migration/start")
async def start_migration(request: MigrationRequest, background_tasks: BackgroundTasks):
    """Start migration process"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Migration system not initialized")
        
        logger.info(f"Starting migration for agents: {request.agent_types}")
        
        # Start migration in background
        background_tasks.add_task(
            _run_migration,
            request.agent_types
        )
        
        return {
            "message": f"Migration started for {request.agent_types}",
            "agent_types": request.agent_types,
            "status": "started",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start migration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/migration/status")
async def get_migration_status():
    """Get migration status"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Migration system not initialized")
        
        migration_status = await migration_strategy.get_migration_status()
        
        return {
            "migration_status": migration_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get migration status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/migration/rollback")
async def rollback_migration(agent_type: str, background_tasks: BackgroundTasks):
    """Rollback migration for specific agent"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Migration system not initialized")
        
        logger.info(f"Rolling back migration for {agent_type}")
        
        # Start rollback in background
        background_tasks.add_task(_run_rollback, agent_type)
        
        return {
            "message": f"Migration rollback started for {agent_type}",
            "agent_type": agent_type,
            "status": "started",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start rollback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Performance monitoring endpoints
@app.post("/api/performance/start-test")
async def start_performance_test(request: PerformanceTestRequest, background_tasks: BackgroundTasks):
    """Start performance test"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Performance monitoring not initialized")
        
        logger.info(f"Starting performance test for {request.agent_type}")
        
        # Create test configuration
        test_config = {
            "duration": request.duration,
            "test_cases": request.test_cases or _get_default_test_cases(request.agent_type)
        }
        
        # Start test in background
        test_id = await performance_monitor.start_performance_test(
            request.agent_type, test_config
        )
        
        optimization_state["performance_tests"][test_id] = {
            "agent_type": request.agent_type,
            "status": "started",
            "start_time": datetime.now()
        }
        
        return {
            "message": f"Performance test started for {request.agent_type}",
            "test_id": test_id,
            "agent_type": request.agent_type,
            "status": "started",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start performance test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/performance/test-status/{test_id}")
async def get_test_status(test_id: str):
    """Get performance test status"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Performance monitoring not initialized")
        
        status = await performance_monitor.get_test_status(test_id)
        
        return {
            "test_status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get test status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/performance/summary")
async def get_performance_summary():
    """Get performance summary"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Performance monitoring not initialized")
        
        summary = await performance_monitor.get_performance_summary()
        
        return {
            "performance_summary": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get performance summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Backward compatibility endpoints
@app.post("/api/legacy/{endpoint:path}")
async def handle_legacy_endpoint(endpoint: str, request: LegacyAPIRequest):
    """Handle legacy API endpoints with backward compatibility"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Compatibility layer not initialized")
        
        # Handle legacy request through compatibility layer
        result = await compatibility_layer.handle_legacy_request(
            f"/api/legacy/{endpoint}",
            request.request_data
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to handle legacy endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compatibility/status")
async def get_compatibility_status():
    """Get backward compatibility status"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Compatibility layer not initialized")
        
        status = await compatibility_layer.get_compatibility_status()
        
        return {
            "compatibility_status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get compatibility status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced industry analysis endpoints
@app.post("/api/industry/{industry}/analysis")
async def industry_analysis(industry: str, request: Dict[str, Any]):
    """Enhanced industry analysis with optimization"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Industry analysis not initialized")
        
        logger.info(f"Running enhanced analysis for {industry}")
        
        # Get industry orchestrator
        orchestrator = industry_manager.get_orchestrator(industry)
        if not orchestrator:
            raise HTTPException(status_code=404, detail=f"Industry {industry} not found")
        
        # Execute enhanced analysis
        result = await orchestrator.execute_industry_analysis(
            organization_id=request.get("organization_id", "default-org"),
            analysis_type=request.get("analysis_type", "comprehensive"),
            enhanced_features=request.get("enhanced_features", ["ollama", "chroma", "multi_agent"])
        )
        
        return {
            "industry": industry,
            "analysis_result": result,
            "enhanced_features_used": ["ollama", "chroma", "multi_agent"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to run industry analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/platform/archer-superior-analysis")
async def archer_superior_analysis(request: Dict[str, Any]):
    """Archer-superior analysis with full optimization"""
    try:
        if not optimization_state["is_initialized"]:
            raise HTTPException(status_code=503, detail="Platform analysis not initialized")
        
        logger.info("Running Archer-superior analysis")
        
        # Execute comprehensive platform analysis
        result = await industry_manager.get_comprehensive_demonstration(
            request.get("organization_id", "default-org")
        )
        
        return {
            "analysis_type": "archer_superior",
            "analysis_result": result,
            "enhanced_features_used": ["ollama", "chroma", "multi_agent", "advanced_mcp"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to run Archer-superior analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task functions
async def _run_optimization(agent_type: str, optimization_type: str):
    """Run agent optimization in background"""
    try:
        result = await integration_manager.optimize_agent_with_ollama_chroma(
            agent_type, optimization_type
        )
        
        optimization_state["optimized_agents"][agent_type] = {
            "optimization_type": optimization_type,
            "result": result,
            "completed_at": datetime.now()
        }
        
        logger.info(f"Optimization completed for {agent_type}")
        
    except Exception as e:
        logger.error(f"Optimization failed for {agent_type}: {e}")
        optimization_state["optimized_agents"][agent_type] = {
            "optimization_type": optimization_type,
            "error": str(e),
            "failed_at": datetime.now()
        }

async def _run_optimize_all():
    """Run optimization for all agents in background"""
    try:
        result = await integration_manager.optimize_all_agents("full")
        
        optimization_state["optimized_agents"]["all_agents"] = {
            "optimization_type": "full",
            "result": result,
            "completed_at": datetime.now()
        }
        
        logger.info("Optimization completed for all agents")
        
    except Exception as e:
        logger.error(f"Optimization failed for all agents: {e}")
        optimization_state["optimized_agents"]["all_agents"] = {
            "optimization_type": "full",
            "error": str(e),
            "failed_at": datetime.now()
        }

async def _run_migration(agent_types: List[str]):
    """Run migration in background"""
    try:
        result = await migration_strategy.execute_full_migration(agent_types)
        
        optimization_state["migration_status"] = result
        
        logger.info(f"Migration completed for {agent_types}")
        
    except Exception as e:
        logger.error(f"Migration failed for {agent_types}: {e}")
        optimization_state["migration_status"] = {
            "error": str(e),
            "failed_at": datetime.now()
        }

async def _run_rollback(agent_type: str):
    """Run rollback in background"""
    try:
        result = await migration_strategy.rollback_migration(agent_type)
        
        logger.info(f"Rollback completed for {agent_type}")
        
    except Exception as e:
        logger.error(f"Rollback failed for {agent_type}: {e}")

def _get_default_test_cases(agent_type: str) -> List[Dict[str, Any]]:
    """Get default test cases for agent type"""
    test_cases = {
        "bfsi": [
            {
                "name": "basel_compliance_test",
                "input": {"type": "compliance_check", "content": "Check Basel III compliance for capital adequacy ratio"},
                "expected_output": {"compliance_status": "compliant"}
            },
            {
                "name": "risk_assessment_test",
                "input": {"type": "risk_assessment", "content": "Assess credit risk for loan portfolio"},
                "expected_output": {"risk_level": "medium"}
            }
        ],
        "telecom": [
            {
                "name": "fcc_compliance_test",
                "input": {"type": "compliance_check", "content": "Check FCC compliance for spectrum usage"},
                "expected_output": {"compliance_status": "compliant"}
            }
        ],
        "manufacturing": [
            {
                "name": "iso_compliance_test",
                "input": {"type": "compliance_check", "content": "Check ISO 9001 quality management compliance"},
                "expected_output": {"compliance_status": "compliant"}
            }
        ],
        "healthcare": [
            {
                "name": "hipaa_compliance_test",
                "input": {"type": "compliance_check", "content": "Check HIPAA compliance for patient data"},
                "expected_output": {"compliance_status": "compliant"}
            }
        ],
        "compliance": [
            {
                "name": "general_compliance_test",
                "input": {"type": "compliance_check", "content": "General compliance assessment"},
                "expected_output": {"compliance_status": "compliant"}
            }
        ]
    }
    
    return test_cases.get(agent_type, [
        {
            "name": "general_test",
            "input": {"type": "general", "content": "General test case"},
            "expected_output": {"status": "success"}
        }
    ])

if __name__ == "__main__":
    uvicorn.run(
        "enhanced_main_with_optimization:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="info"
    )
