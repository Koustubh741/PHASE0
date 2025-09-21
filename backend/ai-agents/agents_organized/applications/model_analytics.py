#!/usr/bin/env python3
"""
Model Analytics and Performance Tracking
Provides detailed analytics and insights for model usage
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict
import statistics

@dataclass
class ModelUsageRecord:
    """Individual model usage record"""
    timestamp: float
    model_id: str
    task_type: str
    processing_time: float
    input_length: int
    output_length: int
    tokens_generated: int
    success: bool
    error_message: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

@dataclass
class ModelPerformanceMetrics:
    """Aggregated performance metrics for a model"""
    model_id: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_processing_time: float
    median_processing_time: float
    min_processing_time: float
    max_processing_time: float
    average_tokens_per_second: float
    average_input_length: float
    average_output_length: float
    success_rate: float
    total_processing_time: float
    usage_by_task_type: Dict[str, int]
    peak_usage_hour: int
    most_common_task: str

class ModelAnalytics:
    """Analytics engine for model usage tracking"""
    
    def __init__(self, max_records: int = 10000):
        self.max_records = max_records
        self.usage_records: List[ModelUsageRecord] = []
        self.model_metrics_cache: Dict[str, ModelPerformanceMetrics] = {}
        self.cache_timestamp: Dict[str, float] = {}
        self.cache_ttl = 300  # 5 minutes cache TTL
    
    def record_usage(self, record: ModelUsageRecord):
        """Record a model usage event"""
        self.usage_records.append(record)
        
        # Maintain max records limit
        if len(self.usage_records) > self.max_records:
            self.usage_records = self.usage_records[-self.max_records:]
        
        # Invalidate cache for this model
        if record.model_id in self.cache_timestamp:
            del self.cache_timestamp[record.model_id]
    
    def get_model_metrics(self, model_id: str, time_window_hours: Optional[int] = None) -> ModelPerformanceMetrics:
        """Get performance metrics for a specific model"""
        # Check cache
        cache_key = f"{model_id}_{time_window_hours}"
        if (cache_key in self.cache_timestamp and 
            time.time() - self.cache_timestamp[cache_key] < self.cache_ttl and
            cache_key in self.model_metrics_cache):
            return self.model_metrics_cache[cache_key]
        
        # Filter records by time window if specified
        cutoff_time = None
        if time_window_hours:
            cutoff_time = time.time() - (time_window_hours * 3600)
        
        model_records = [
            record for record in self.usage_records
            if record.model_id == model_id and (cutoff_time is None or record.timestamp >= cutoff_time)
        ]
        
        if not model_records:
            # Return empty metrics
            return ModelPerformanceMetrics(
                model_id=model_id,
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                average_processing_time=0.0,
                median_processing_time=0.0,
                min_processing_time=0.0,
                max_processing_time=0.0,
                average_tokens_per_second=0.0,
                average_input_length=0.0,
                average_output_length=0.0,
                success_rate=0.0,
                total_processing_time=0.0,
                usage_by_task_type={},
                peak_usage_hour=0,
                most_common_task=""
            )
        
        # Calculate metrics
        total_requests = len(model_records)
        successful_requests = sum(1 for r in model_records if r.success)
        failed_requests = total_requests - successful_requests
        
        processing_times = [r.processing_time for r in model_records]
        average_processing_time = statistics.mean(processing_times) if processing_times else 0.0
        median_processing_time = statistics.median(processing_times) if processing_times else 0.0
        min_processing_time = min(processing_times) if processing_times else 0.0
        max_processing_time = max(processing_times) if processing_times else 0.0
        
        # Calculate tokens per second
        tokens_per_second = [
            r.tokens_generated / r.processing_time if r.processing_time > 0 else 0
            for r in model_records if r.success
        ]
        average_tokens_per_second = statistics.mean(tokens_per_second) if tokens_per_second else 0.0
        
        # Input/output lengths
        input_lengths = [r.input_length for r in model_records]
        output_lengths = [r.output_length for r in model_records]
        average_input_length = statistics.mean(input_lengths) if input_lengths else 0.0
        average_output_length = statistics.mean(output_lengths) if output_lengths else 0.0
        
        success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0.0
        total_processing_time = sum(processing_times)
        
        # Usage by task type
        usage_by_task_type = defaultdict(int)
        for record in model_records:
            usage_by_task_type[record.task_type] += 1
        
        # Peak usage hour
        hour_usage = defaultdict(int)
        for record in model_records:
            hour = datetime.fromtimestamp(record.timestamp).hour
            hour_usage[hour] += 1
        peak_usage_hour = max(hour_usage.items(), key=lambda x: x[1])[0] if hour_usage else 0
        
        # Most common task
        most_common_task = max(usage_by_task_type.items(), key=lambda x: x[1])[0] if usage_by_task_type else ""
        
        metrics = ModelPerformanceMetrics(
            model_id=model_id,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            average_processing_time=average_processing_time,
            median_processing_time=median_processing_time,
            min_processing_time=min_processing_time,
            max_processing_time=max_processing_time,
            average_tokens_per_second=average_tokens_per_second,
            average_input_length=average_input_length,
            average_output_length=average_output_length,
            success_rate=success_rate,
            total_processing_time=total_processing_time,
            usage_by_task_type=dict(usage_by_task_type),
            peak_usage_hour=peak_usage_hour,
            most_common_task=most_common_task
        )
        
        # Cache the result
        self.model_metrics_cache[cache_key] = metrics
        self.cache_timestamp[cache_key] = time.time()
        
        return metrics
    
    def get_comparative_analysis(self, model_ids: List[str], time_window_hours: Optional[int] = None) -> Dict[str, Any]:
        """Compare performance across multiple models"""
        if len(model_ids) < 2:
            raise ValueError("At least 2 models required for comparison")
        
        metrics = {}
        for model_id in model_ids:
            metrics[model_id] = self.get_model_metrics(model_id, time_window_hours)
        
        # Find best performing model in each category
        best_speed = max(metrics.items(), key=lambda x: x[1].average_tokens_per_second)
        best_success_rate = max(metrics.items(), key=lambda x: x[1].success_rate)
        most_used = max(metrics.items(), key=lambda x: x[1].total_requests)
        
        # Calculate relative performance
        relative_performance = {}
        for model_id, metric in metrics.items():
            relative_performance[model_id] = {
                "speed_rank": sorted(metrics.keys(), key=lambda x: metrics[x].average_tokens_per_second, reverse=True).index(model_id) + 1,
                "success_rank": sorted(metrics.keys(), key=lambda x: metrics[x].success_rate, reverse=True).index(model_id) + 1,
                "usage_rank": sorted(metrics.keys(), key=lambda x: metrics[x].total_requests, reverse=True).index(model_id) + 1
            }
        
        return {
            "comparison_period": f"Last {time_window_hours} hours" if time_window_hours else "All time",
            "models_compared": model_ids,
            "metrics": {k: asdict(v) for k, v in metrics.items()},
            "best_performers": {
                "speed": {"model": best_speed[0], "tokens_per_second": best_speed[1].average_tokens_per_second},
                "success_rate": {"model": best_success_rate[0], "success_rate": best_success_rate[1].success_rate},
                "most_used": {"model": most_used[0], "total_requests": most_used[1].total_requests}
            },
            "relative_performance": relative_performance,
            "recommendations": self._generate_recommendations(metrics)
        }
    
    def _generate_recommendations(self, metrics: Dict[str, ModelPerformanceMetrics]) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        # Find models with low success rates
        low_success_models = [mid for mid, m in metrics.items() if m.success_rate < 90 and m.total_requests > 10]
        if low_success_models:
            recommendations.append(f"Models with low success rates (<90%): {', '.join(low_success_models)}. Consider investigating error patterns.")
        
        # Find slow models
        slow_models = [mid for mid, m in metrics.items() if m.average_processing_time > 5.0 and m.total_requests > 10]
        if slow_models:
            recommendations.append(f"Slow models (>5s avg): {', '.join(slow_models)}. Consider optimization or replacement.")
        
        # Find unused models
        unused_models = [mid for mid, m in metrics.items() if m.total_requests < 5]
        if unused_models:
            recommendations.append(f"Rarely used models: {', '.join(unused_models)}. Consider removing to free resources.")
        
        # Find overused models
        total_requests = sum(m.total_requests for m in metrics.values())
        overused_models = [mid for mid, m in metrics.items() if m.total_requests > total_requests * 0.7]
        if overused_models:
            recommendations.append(f"Heavily used models: {', '.join(overused_models)}. Consider load balancing or adding more instances.")
        
        return recommendations
    
    def get_usage_trends(self, model_id: str, days: int = 7) -> Dict[str, Any]:
        """Get usage trends over time for a model"""
        cutoff_time = time.time() - (days * 24 * 3600)
        model_records = [
            record for record in self.usage_records
            if record.model_id == model_id and record.timestamp >= cutoff_time
        ]
        
        if not model_records:
            return {"error": f"No usage data found for model {model_id} in the last {days} days"}
        
        # Group by day
        daily_usage = defaultdict(lambda: {"requests": 0, "successful": 0, "total_time": 0.0})
        
        for record in model_records:
            day = datetime.fromtimestamp(record.timestamp).strftime("%Y-%m-%d")
            daily_usage[day]["requests"] += 1
            if record.success:
                daily_usage[day]["successful"] += 1
            daily_usage[day]["total_time"] += record.processing_time
        
        # Convert to sorted list
        trends = []
        for day in sorted(daily_usage.keys()):
            data = daily_usage[day]
            trends.append({
                "date": day,
                "total_requests": data["requests"],
                "successful_requests": data["successful"],
                "success_rate": (data["successful"] / data["requests"]) * 100 if data["requests"] > 0 else 0,
                "average_processing_time": data["total_time"] / data["requests"] if data["requests"] > 0 else 0
            })
        
        return {
            "model_id": model_id,
            "period_days": days,
            "daily_trends": trends,
            "summary": {
                "total_requests": len(model_records),
                "average_daily_requests": len(model_records) / days,
                "overall_success_rate": (sum(1 for r in model_records if r.success) / len(model_records)) * 100
            }
        }
    
    def export_data(self, format: str = "json") -> str:
        """Export analytics data in specified format"""
        if format == "json":
            data = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "total_records": len(self.usage_records),
                "usage_records": [asdict(record) for record in self.usage_records[-1000:]]  # Last 1000 records
            }
            return json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def get_system_health_score(self) -> Dict[str, Any]:
        """Calculate overall system health score"""
        if not self.usage_records:
            return {"health_score": 0, "status": "No data", "recommendations": ["Start using models to generate health metrics"]}
        
        # Calculate health metrics
        total_requests = len(self.usage_records)
        successful_requests = sum(1 for r in self.usage_records if r.success)
        overall_success_rate = (successful_requests / total_requests) * 100
        
        # Average processing time
        avg_processing_time = statistics.mean([r.processing_time for r in self.usage_records])
        
        # Model diversity (how many different models are being used)
        unique_models = len(set(r.model_id for r in self.usage_records))
        
        # Calculate health score (0-100)
        success_score = min(overall_success_rate, 100)
        speed_score = max(0, 100 - (avg_processing_time * 10))  # Penalty for slow responses
        diversity_score = min(unique_models * 10, 100)  # Reward for using multiple models
        
        health_score = (success_score * 0.5 + speed_score * 0.3 + diversity_score * 0.2)
        
        status = "Excellent" if health_score >= 90 else "Good" if health_score >= 70 else "Fair" if health_score >= 50 else "Poor"
        
        recommendations = []
        if overall_success_rate < 95:
            recommendations.append("Improve error handling and model reliability")
        if avg_processing_time > 3.0:
            recommendations.append("Optimize model performance or consider faster alternatives")
        if unique_models < 2:
            recommendations.append("Consider using multiple models for better load distribution")
        
        return {
            "health_score": round(health_score, 2),
            "status": status,
            "metrics": {
                "overall_success_rate": round(overall_success_rate, 2),
                "average_processing_time": round(avg_processing_time, 2),
                "unique_models_used": unique_models,
                "total_requests": total_requests
            },
            "recommendations": recommendations
        }

# Global analytics instance
analytics = ModelAnalytics()
