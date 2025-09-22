"""
Performance Optimization API Endpoints
RESTful API endpoints for performance optimization and monitoring
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from ...core.application.services.performance_optimization_service import (
    PerformanceOptimizationService,
    OptimizationType,
    PerformanceLevel
)
from ...core.application.dto.performance_dto import (
    PerformanceMetricResponse,
    QueryOptimizationRequest,
    QueryOptimizationResponse,
    APIOptimizationRequest,
    APIOptimizationResponse,
    SystemResourceResponse,
    PerformanceSummaryResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/performance", tags=["Performance Optimization"])

# Global service instance
performance_service = PerformanceOptimizationService()

@router.get("/metrics", response_model=List[PerformanceMetricResponse])
async def get_performance_metrics():
    """Get all performance metrics"""
    try:
        metrics = performance_service.get_performance_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/{metric_name}", response_model=List[PerformanceMetricResponse])
async def get_metric_by_name(metric_name: str):
    """Get performance metrics by name"""
    try:
        all_metrics = performance_service.get_performance_metrics()
        metrics = [m for m in all_metrics if m["name"] == metric_name]
        return metrics
    except Exception as e:
        logger.error(f"Error getting metric by name: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize/query", response_model=QueryOptimizationResponse)
async def optimize_database_query(request: QueryOptimizationRequest):
    """Optimize database query performance"""
    try:
        optimization = await performance_service.optimize_database_query(
            query=request.query,
            execution_time=request.execution_time,
            context=request.context
        )
        
        return QueryOptimizationResponse(
            query_id=optimization.query_id,
            original_query=optimization.original_query,
            optimized_query=optimization.optimized_query,
            execution_time_before=optimization.execution_time_before,
            execution_time_after=optimization.execution_time_after,
            improvement_percentage=optimization.improvement_percentage,
            optimization_suggestions=optimization.optimization_suggestions,
            indexes_used=optimization.indexes_used,
            metadata=optimization.metadata
        )
    except Exception as e:
        logger.error(f"Error optimizing database query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/optimize/query", response_model=List[QueryOptimizationResponse])
async def get_query_optimizations():
    """Get all query optimizations"""
    try:
        optimizations = performance_service.get_query_optimizations()
        return optimizations
    except Exception as e:
        logger.error(f"Error getting query optimizations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize/api", response_model=APIOptimizationResponse)
async def optimize_api_endpoint(request: APIOptimizationRequest):
    """Optimize API endpoint performance"""
    try:
        optimization = await performance_service.optimize_api_endpoint(
            endpoint=request.endpoint,
            method=request.method,
            response_time=request.response_time,
            context=request.context
        )
        
        return APIOptimizationResponse(
            endpoint=optimization.endpoint,
            method=optimization.method,
            response_time_before=optimization.response_time_before,
            response_time_after=optimization.response_time_after,
            improvement_percentage=optimization.improvement_percentage,
            optimization_techniques=optimization.optimization_techniques,
            cache_hit_rate=optimization.cache_hit_rate,
            concurrent_requests=optimization.concurrent_requests,
            metadata=optimization.metadata
        )
    except Exception as e:
        logger.error(f"Error optimizing API endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/optimize/api", response_model=List[APIOptimizationResponse])
async def get_api_optimizations():
    """Get all API optimizations"""
    try:
        optimizations = performance_service.get_api_optimizations()
        return optimizations
    except Exception as e:
        logger.error(f"Error getting API optimizations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resources", response_model=List[SystemResourceResponse])
async def get_system_resources():
    """Get system resource information"""
    try:
        resources = performance_service.get_system_resources()
        return resources
    except Exception as e:
        logger.error(f"Error getting system resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resources/{resource_type}", response_model=SystemResourceResponse)
async def get_system_resource(resource_type: str):
    """Get specific system resource information"""
    try:
        resources = performance_service.get_system_resources()
        resource = next((r for r in resources if r["resource_type"].lower() == resource_type.lower()), None)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Resource type not found")
        
        return resource
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting system resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary", response_model=PerformanceSummaryResponse)
async def get_performance_summary():
    """Get performance optimization summary"""
    try:
        summary = performance_service.get_performance_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting performance summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize/memory")
async def optimize_memory_usage():
    """Optimize memory usage"""
    try:
        optimization_result = performance_service.optimize_memory_usage()
        return optimization_result
    except Exception as e:
        logger.error(f"Error optimizing memory usage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cache/statistics")
async def get_cache_statistics():
    """Get cache statistics"""
    try:
        stats = performance_service.get_cache_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting cache statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cache/clear")
async def clear_cache():
    """Clear all caches"""
    try:
        # Clear all caches
        performance_service.query_cache.clear()
        performance_service.response_cache.clear()
        performance_service.optimization_cache.clear()
        
        return {
            "message": "All caches cleared successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        summary = performance_service.get_performance_summary()
        return {
            "status": "healthy",
            "service": "performance-optimization",
            "version": "2.0.0",
            "system_health_score": summary["system_health_score"],
            "total_optimizations": summary["performance_stats"]["total_optimizations"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "performance-optimization",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@router.get("/recommendations")
async def get_optimization_recommendations():
    """Get performance optimization recommendations"""
    try:
        # Get current system resources
        resources = performance_service.get_system_resources()
        
        recommendations = []
        
        for resource in resources:
            if resource["status"] != "healthy":
                recommendations.extend(resource["recommendations"])
        
        # Add general recommendations
        recommendations.extend([
            "Implement database query optimization",
            "Use connection pooling for database connections",
            "Implement response caching for frequently accessed data",
            "Consider horizontal scaling for high-traffic endpoints",
            "Monitor and optimize memory usage regularly"
        ])
        
        return {
            "recommendations": list(set(recommendations)),  # Remove duplicates
            "total_recommendations": len(set(recommendations)),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting optimization recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
