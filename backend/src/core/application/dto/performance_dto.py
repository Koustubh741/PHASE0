"""
Performance Optimization Data Transfer Objects
DTOs for performance optimization operations
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class OptimizationType(str, Enum):
    """Optimization type enumeration"""
    DATABASE_QUERY = "database_query"
    API_RESPONSE = "api_response"
    CACHE_OPTIMIZATION = "cache_optimization"
    MEMORY_OPTIMIZATION = "memory_optimization"
    CPU_OPTIMIZATION = "cpu_optimization"
    NETWORK_OPTIMIZATION = "network_optimization"
    CONCURRENCY_OPTIMIZATION = "concurrency_optimization"


class PerformanceLevel(str, Enum):
    """Performance level enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    OPTIMAL = "optimal"


class PerformanceMetricResponse(BaseModel):
    """Performance metric response"""
    metric_id: str = Field(..., description="Metric ID")
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    unit: str = Field(..., description="Metric unit")
    timestamp: datetime = Field(..., description="Metric timestamp")
    optimization_type: str = Field(..., description="Optimization type")
    performance_level: str = Field(..., description="Performance level")
    threshold: float = Field(..., description="Performance threshold")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "metric_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "cpu_usage",
                "value": 45.2,
                "unit": "percentage",
                "timestamp": "2024-01-15T10:30:00Z",
                "optimization_type": "cpu_optimization",
                "performance_level": "low",
                "threshold": 80.0,
                "metadata": {"cores": 8}
            }
        }


class QueryOptimizationRequest(BaseModel):
    """Request to optimize database query"""
    query: str = Field(..., description="SQL query to optimize")
    execution_time: float = Field(..., description="Current execution time in seconds")
    context: Dict[str, Any] = Field(default_factory=dict, description="Query context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "SELECT * FROM users WHERE status = 'active' ORDER BY created_at DESC",
                "execution_time": 2.5,
                "context": {
                    "table_size": 100000,
                    "indexes": ["status", "created_at"],
                    "query_frequency": "high"
                }
            }
        }


class QueryOptimizationResponse(BaseModel):
    """Database query optimization response"""
    query_id: str = Field(..., description="Query optimization ID")
    original_query: str = Field(..., description="Original SQL query")
    optimized_query: str = Field(..., description="Optimized SQL query")
    execution_time_before: float = Field(..., description="Execution time before optimization")
    execution_time_after: float = Field(..., description="Execution time after optimization")
    improvement_percentage: float = Field(..., description="Improvement percentage")
    optimization_suggestions: List[str] = Field(..., description="Optimization suggestions")
    indexes_used: List[str] = Field(..., description="Indexes used")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "456e7890-e89b-12d3-a456-426614174000",
                "original_query": "SELECT * FROM users WHERE status = 'active'",
                "optimized_query": "SELECT id, name, email FROM users WHERE status = 'active'",
                "execution_time_before": 2.5,
                "execution_time_after": 1.2,
                "improvement_percentage": 52.0,
                "optimization_suggestions": [
                    "Avoid SELECT * - specify only needed columns",
                    "Ensure WHERE clauses use indexed columns"
                ],
                "indexes_used": ["status_index"],
                "metadata": {}
            }
        }


class APIOptimizationRequest(BaseModel):
    """Request to optimize API endpoint"""
    endpoint: str = Field(..., description="API endpoint path")
    method: str = Field(..., description="HTTP method")
    response_time: float = Field(..., description="Current response time in seconds")
    context: Dict[str, Any] = Field(default_factory=dict, description="Endpoint context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "endpoint": "/api/v1/users",
                "method": "GET",
                "response_time": 1.8,
                "context": {
                    "request_count": 1000,
                    "cache_enabled": False,
                    "database_queries": 5
                }
            }
        }


class APIOptimizationResponse(BaseModel):
    """API optimization response"""
    endpoint: str = Field(..., description="API endpoint")
    method: str = Field(..., description="HTTP method")
    response_time_before: float = Field(..., description="Response time before optimization")
    response_time_after: float = Field(..., description="Response time after optimization")
    improvement_percentage: float = Field(..., description="Improvement percentage")
    optimization_techniques: List[str] = Field(..., description="Optimization techniques")
    cache_hit_rate: float = Field(..., description="Cache hit rate")
    concurrent_requests: int = Field(..., description="Concurrent requests")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "endpoint": "/api/v1/users",
                "method": "GET",
                "response_time_before": 1.8,
                "response_time_after": 0.9,
                "improvement_percentage": 50.0,
                "optimization_techniques": [
                    "Implement response caching",
                    "Optimize database queries",
                    "Use connection pooling"
                ],
                "cache_hit_rate": 85.5,
                "concurrent_requests": 25,
                "metadata": {}
            }
        }


class SystemResourceResponse(BaseModel):
    """System resource response"""
    resource_type: str = Field(..., description="Resource type")
    current_usage: float = Field(..., description="Current usage")
    max_capacity: float = Field(..., description="Maximum capacity")
    utilization_percentage: float = Field(..., description="Utilization percentage")
    status: str = Field(..., description="Resource status")
    recommendations: List[str] = Field(..., description="Optimization recommendations")
    timestamp: datetime = Field(..., description="Timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resource_type": "CPU",
                "current_usage": 45.2,
                "max_capacity": 100.0,
                "utilization_percentage": 45.2,
                "status": "healthy",
                "recommendations": [
                    "Monitor CPU usage - consider optimization",
                    "Implement async processing where possible"
                ],
                "timestamp": "2024-01-15T10:30:00Z",
                "metadata": {"cores": 8}
            }
        }


class PerformanceSummaryResponse(BaseModel):
    """Performance summary response"""
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    performance_stats: Dict[str, Any] = Field(..., description="Performance statistics")
    thresholds: Dict[str, float] = Field(..., description="Performance thresholds")
    total_metrics: int = Field(..., description="Total metrics")
    query_optimizations: int = Field(..., description="Query optimizations count")
    api_optimizations: int = Field(..., description="API optimizations count")
    system_health_score: float = Field(..., description="System health score")
    last_updated: str = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "service": "performance-optimization-service",
                "version": "2.0.0",
                "performance_stats": {
                    "total_optimizations": 25,
                    "query_optimizations": 15,
                    "api_optimizations": 10,
                    "average_improvement": 35.5,
                    "cache_hit_rate": 85.0,
                    "system_health_score": 78.5
                },
                "thresholds": {
                    "database_query_time": 1.0,
                    "api_response_time": 0.5,
                    "memory_usage": 80.0,
                    "cpu_usage": 80.0,
                    "cache_hit_rate": 90.0
                },
                "total_metrics": 150,
                "query_optimizations": 15,
                "api_optimizations": 10,
                "system_health_score": 78.5,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }
