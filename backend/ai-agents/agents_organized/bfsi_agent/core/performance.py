"""
BFSI Performance Optimization Module
===================================

This module provides performance optimization utilities for the BFSI agent system.
"""

import time
import psutil
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""
    operation_id: str
    start_time: float
    end_time: float
    duration: float
    memory_usage: float
    cpu_usage: float
    success: bool
    operation_type: str
    error_message: Optional[str] = None

class BFSIPerformanceOptimizer:
    """
    Performance optimization utilities for BFSI operations.
    """
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.active_operations: Dict[str, Dict[str, Any]] = {}
    
    def start_operation(self, operation_id: str, operation_type: str = "general") -> None:
        """Start tracking an operation."""
        start_time = time.time()
        process = psutil.Process()
        
        # Get accurate baseline CPU usage with small interval
        start_cpu = process.cpu_percent(interval=0.1)
        
        self.active_operations[operation_id] = {
            'start_time': start_time,
            'start_memory': process.memory_info().rss / 1024 / 1024,  # MB
            'start_cpu': start_cpu,
            'operation_type': operation_type
        }
        
        logger.debug(f"Started operation {operation_id} of type {operation_type}")
    
    def end_operation(self, operation_id: str, success: bool = True, error_message: Optional[str] = None) -> Optional[PerformanceMetrics]:
        """End tracking an operation and return metrics."""
        if operation_id not in self.active_operations:
            logger.warning(f"Operation {operation_id} not found in active operations")
            return None
        
        operation_data = self.active_operations.pop(operation_id)
        end_time = time.time()
        process = psutil.Process()
        
        # Calculate accurate CPU usage with interval
        end_cpu = process.cpu_percent(interval=0.1)
        cpu_usage = max(0, end_cpu - operation_data['start_cpu'])
        
        # Calculate memory usage difference, ensuring non-negative
        end_memory = process.memory_info().rss / 1024 / 1024
        memory_usage = max(0, end_memory - operation_data['start_memory'])
        
        metrics = PerformanceMetrics(
            operation_id=operation_id,
            start_time=operation_data['start_time'],
            end_time=end_time,
            duration=end_time - operation_data['start_time'],
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            success=success,
            operation_type=operation_data['operation_type'],
            error_message=error_message
        )
        
        self.metrics_history.append(metrics)
        logger.debug(f"Completed operation {operation_id} in {metrics.duration:.2f}s")
        
        return metrics
    
    def get_performance_summary(self, operation_type: Optional[str] = None) -> Dict[str, Any]:
        """Get performance summary for operations."""
        if operation_type:
            filtered_metrics = [m for m in self.metrics_history 
                              if m.operation_type == operation_type]
        else:
            filtered_metrics = self.metrics_history
        
        if not filtered_metrics:
            return {"message": "No metrics available"}
        
        successful_ops = [m for m in filtered_metrics if m.success]
        failed_ops = [m for m in filtered_metrics if not m.success]
        
        return {
            "total_operations": len(filtered_metrics),
            "successful_operations": len(successful_ops),
            "failed_operations": len(failed_ops),
            "success_rate": len(successful_ops) / len(filtered_metrics) if filtered_metrics else 0,
            "average_duration": sum(m.duration for m in successful_ops) / len(successful_ops) if successful_ops else 0,
            "average_memory_usage": sum(m.memory_usage for m in successful_ops) / len(successful_ops) if successful_ops else 0,
            "average_cpu_usage": sum(m.cpu_usage for m in successful_ops) / len(successful_ops) if successful_ops else 0
        }
    
    def optimize_memory_usage(self) -> Dict[str, Any]:
        """Analyze and suggest memory optimization."""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "current_memory_mb": memory_info.rss / 1024 / 1024,
            "memory_percent": process.memory_percent(),
            "suggestions": [
                "Consider implementing lazy loading for large datasets",
                "Use generators instead of lists for large data processing",
                "Clear unused variables and objects",
                "Implement caching strategies for frequently accessed data"
            ]
        }
    
    def clear_metrics_history(self) -> None:
        """Clear performance metrics history."""
        self.metrics_history.clear()
        logger.info("Performance metrics history cleared")
