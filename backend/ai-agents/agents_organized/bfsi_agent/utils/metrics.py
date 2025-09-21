"""
BFSI Agent Metrics and Analytics Utilities
==========================================

This module provides performance metrics and analytics utilities for the BFSI agent system.
"""

import time
import statistics
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class OperationMetrics:
    """Metrics for a single operation."""
    operation_id: str
    operation_type: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    memory_usage: float
    cpu_usage: float
    error_count: int = 0
    retry_count: int = 0

class MetricsCollector:
    """Collects and manages performance metrics."""
    
    def __init__(self):
        self.metrics: List[OperationMetrics] = []
        self.start_time = time.time()
    
    def add_metrics(self, metrics: OperationMetrics) -> None:
        """Add metrics to the collection."""
        self.metrics.append(metrics)
        logger.debug(f"Added metrics for operation {metrics.operation_id}")
    
    def get_metrics_by_type(self, operation_type: str) -> List[OperationMetrics]:
        """Get metrics filtered by operation type."""
        return [m for m in self.metrics if m.operation_type == operation_type]
    
    def get_metrics_by_timeframe(self, start_time: float, end_time: float) -> List[OperationMetrics]:
        """Get metrics within a specific timeframe."""
        return [m for m in self.metrics if start_time <= m.start_time <= end_time]

def calculate_performance_metrics(metrics_list: List[OperationMetrics]) -> Dict[str, Any]:
    """
    Calculate performance metrics from a list of operation metrics.
    
    Args:
        metrics_list: List of operation metrics
        
    Returns:
        Dict: Calculated performance metrics
    """
    if not metrics_list:
        return {"error": "No metrics available"}
    
    successful_ops = [m for m in metrics_list if m.success]
    failed_ops = [m for m in metrics_list if not m.success]
    
    durations = [m.duration for m in successful_ops]
    memory_usage = [m.memory_usage for m in successful_ops]
    cpu_usage = [m.cpu_usage for m in successful_ops]
    
    return {
        "total_operations": len(metrics_list),
        "successful_operations": len(successful_ops),
        "failed_operations": len(failed_ops),
        "success_rate": len(successful_ops) / len(metrics_list) if metrics_list else 0,
        "average_duration": statistics.mean(durations) if durations else 0,
        "median_duration": statistics.median(durations) if durations else 0,
        "min_duration": min(durations) if durations else 0,
        "max_duration": max(durations) if durations else 0,
        "average_memory_usage": statistics.mean(memory_usage) if memory_usage else 0,
        "average_cpu_usage": statistics.mean(cpu_usage) if cpu_usage else 0,
        "total_errors": sum(m.error_count for m in metrics_list),
        "total_retries": sum(m.retry_count for m in metrics_list)
    }

def generate_analytics_report(metrics_list: List[OperationMetrics], 
                           report_type: str = "comprehensive") -> Dict[str, Any]:
    """
    Generate analytics report from metrics.
    
    Args:
        metrics_list: List of operation metrics
        report_type: Type of report ('comprehensive', 'summary', 'performance')
        
    Returns:
        Dict: Analytics report
    """
    if not metrics_list:
        return {"error": "No metrics available for report generation"}
    
    base_metrics = calculate_performance_metrics(metrics_list)
    
    if report_type == "summary":
        return {
            "report_type": "summary",
            "generated_at": datetime.now().isoformat(),
            "total_operations": base_metrics["total_operations"],
            "success_rate": base_metrics["success_rate"],
            "average_duration": base_metrics["average_duration"]
        }
    
    elif report_type == "performance":
        return {
            "report_type": "performance",
            "generated_at": datetime.now().isoformat(),
            **base_metrics,
            "performance_grade": _calculate_performance_grade(base_metrics["success_rate"])
        }
    
    else:  # comprehensive
        # Group by operation type
        operation_types = {}
        for metrics in metrics_list:
            op_type = metrics.operation_type
            if op_type not in operation_types:
                operation_types[op_type] = []
            operation_types[op_type].append(metrics)
        
        type_metrics = {}
        for op_type, type_metrics_list in operation_types.items():
            type_metrics[op_type] = calculate_performance_metrics(type_metrics_list)
        
        return {
            "report_type": "comprehensive",
            "generated_at": datetime.now().isoformat(),
            "overall_metrics": base_metrics,
            "metrics_by_operation_type": type_metrics,
            "performance_grade": _calculate_performance_grade(base_metrics["success_rate"]),
            "recommendations": _generate_recommendations(base_metrics)
        }

def track_operation_metrics(operation_id: str, 
                          operation_type: str,
                          start_time: float,
                          end_time: float,
                          success: bool,
                          memory_usage: float = 0.0,
                          cpu_usage: float = 0.0,
                          error_count: int = 0,
                          retry_count: int = 0) -> OperationMetrics:
    """
    Track metrics for a single operation.
    
    Args:
        operation_id: Unique operation identifier
        operation_type: Type of operation
        start_time: Operation start time
        end_time: Operation end time
        success: Whether operation was successful
        memory_usage: Memory usage in MB
        cpu_usage: CPU usage percentage
        error_count: Number of errors encountered
        retry_count: Number of retries performed
        
    Returns:
        OperationMetrics: Created metrics object
    """
    metrics = OperationMetrics(
        operation_id=operation_id,
        operation_type=operation_type,
        start_time=start_time,
        end_time=end_time,
        duration=end_time - start_time,
        success=success,
        memory_usage=memory_usage,
        cpu_usage=cpu_usage,
        error_count=error_count,
        retry_count=retry_count
    )
    
    logger.debug(f"Tracked metrics for operation {operation_id}")
    return metrics

def calculate_efficiency_score(metrics_list: List[OperationMetrics]) -> float:
    """
    Calculate efficiency score based on metrics.
    
    Args:
        metrics_list: List of operation metrics
        
    Returns:
        float: Efficiency score (0-100)
    """
    if not metrics_list:
        return 0.0
    
    base_metrics = calculate_performance_metrics(metrics_list)
    
    # Weight factors for efficiency calculation
    success_weight = 0.4
    speed_weight = 0.3
    resource_weight = 0.3
    
    # Success rate component (0-100)
    success_score = base_metrics["success_rate"] * 100
    
    # Speed component (inverse of average duration, normalized)
    avg_duration = base_metrics["average_duration"]
    speed_score = max(0, 100 - (avg_duration * 10))  # Penalty for longer operations
    
    # Resource efficiency component (lower memory/CPU usage is better)
    avg_memory = base_metrics["average_memory_usage"]
    avg_cpu = base_metrics["average_cpu_usage"]
    resource_score = max(0, 100 - (avg_memory + avg_cpu) * 2)
    
    efficiency_score = (
        success_score * success_weight +
        speed_score * speed_weight +
        resource_score * resource_weight
    )
    
    return min(100, max(0, efficiency_score))

def _calculate_performance_grade(success_rate: float) -> str:
    """Calculate performance grade based on success rate."""
    if success_rate >= 0.95:
        return "A"
    elif success_rate >= 0.90:
        return "B"
    elif success_rate >= 0.80:
        return "C"
    elif success_rate >= 0.70:
        return "D"
    else:
        return "F"

def _generate_recommendations(metrics: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on metrics."""
    recommendations = []
    
    if metrics["success_rate"] < 0.9:
        recommendations.append("Improve error handling and retry mechanisms")
    
    if metrics["average_duration"] > 5.0:
        recommendations.append("Optimize operation performance and reduce processing time")
    
    if metrics["average_memory_usage"] > 100:
        recommendations.append("Implement memory optimization strategies")
    
    if metrics["total_errors"] > 0:
        recommendations.append("Review and fix error-prone operations")
    
    if metrics["total_retries"] > metrics["total_operations"] * 0.1:
        recommendations.append("Improve initial operation success rate to reduce retries")
    
    if not recommendations:
        recommendations.append("Performance is within acceptable parameters")
    
    return recommendations
